###################################
####    Scientfic Calculator   ####
####    Written by Zijian Yao  ####
###################################

from CalcLex import lexer, tokens
from function import funs, factorial
from decimal import Decimal
from fractions import Fraction
from polynomial import Polynomial,interp,lstsq
import math
import numpy as np
import ply.yacc as yacc

start = 'exp' # CFG start token

# uppermost level
def p_exp(p):
    '''
       exp : frac_exp 
           | float_exp
           | poly_exp
           | vector_exp
           | interp_exp
           | lstsq_exp
           | poly_atom frac_atom
           | poly_atom S LPAREN INT COMMA INT RPAREN
           | poly_atom I LPAREN INT COMMA INT RPAREN
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1](p[2])
    else:
        if p[2] =='sum':
            p[0] = p[1].rangeSum(p[4],p[6])
        else:
            intg = p[1].integral()
            p[0] = intg(p[6]) - intg(p[4])

# handle interpolation
def p_interp_exp(p):
  '''
     interp_exp : IP point_list
                | IP INT point_list
  '''
  if len(p) == 3:
    p[0] = interp(p[2])
  else:
    p[0] = interp(p[3], k=p[2]+1)

# handle linear least sqaure
def p_lstsq_exp(p):
  '''
     lstsq_exp : LS point_list
               | LS MINUS point_list
  '''
  if len(p) == 3:
    p[0] = lstsq(p[2])
  else:
     p[0] = lstsq(p[3], remove=True)

# handle plus and minus for fractions
# left associative
def p_frac_exp(p):
    '''
       frac_exp : frac_exp PLUS frac_term
           | frac_exp MINUS frac_term
           | frac_term
    '''
    if len(p) == 2:
    	p[0] = p[1]
    elif p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]


# handle times and divide for fractions
# left associative
def p_frac_term(p):
    '''
       frac_term : frac_term TIMES frac_atom
            | frac_term DIVIDE frac_atom
            | frac_atom
    '''
    if len(p) == 2:
    	p[0] = p[1]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = Fraction(p[1]) / p[3] 

# atomic expression for fractions
# functions, numbers, parentheses
def p_frac_atom(p):
	'''
	   frac_atom : int_function
	        | num
	        | LPAREN frac_exp RPAREN
	'''
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = p[2]

# uppermost level for polynomial
# handle plus and minus: left associative
# handle derivative and indefinite integral
def p_poly_exp(p):
    '''
       poly_exp : poly_exp PLUS poly_term
                | poly_exp MINUS poly_term
                | poly_term
                | D poly_atom
                | I poly_atom
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        if p[1] == 'dx':
            p[0]=p[2].derivative()
        else:
            p[0]=p[2].integral()
    elif p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]

# handle times for polynomial
def p_poly_term(p):
    '''
       poly_term : poly_term TIMES poly_atom
                 | poly_atom
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] * p[3]

# atomtic expression for polynomial
def p_poly_atom(p):
    '''
       poly_atom : num X INT 
                 | LPAREN poly_exp RPAREN
    '''
    if p[1] == '(':
        p[0] = p[2] 
    elif p[2] == 'x':
        p[0] = Polynomial({p[3]:p[1]}) #num TIMES FUN LPAREN X COMMA INT RPAREN p[7]
    else:
        raise SyntaxError('Invalid Syntax')

# handle plus and minus for float
# left associative
def p_float_exp(p):
    '''
       float_exp : frac_exp PLUS float_term
                  | frac_exp MINUS float_term
                  | float_exp PLUS frac_term
                  | float_exp MINUS frac_term
                  | float_exp PLUS float_term
                  | float_exp MINUS float_term
                  | float_term
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]


# handle times and divide for float
# left associative
def p_float_term(p):
    '''
       float_term : frac_term TIMES float_atom
                  | frac_term DIVIDE float_atom
                  | float_term TIMES frac_atom
                  | float_term DIVIDE frac_atom
                  | float_term TIMES float_atom
                  | float_term DIVIDE float_atom
                  | float_atom
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3] 

# atmoatic expression for float/complex
def p_float_atom(p):
    '''
       float_atom : unary_function
                  | binary_function
                  | trig_function
                  | LPAREN float_exp RPAREN
                  | COMPLEX
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

# unary function
def p_unary_function_expr(p):
    '''
       unary_function : FUN LPAREN exp RPAREN
    '''
    p[0] = funs[p[1]](p[3])

# binary function
def p_binary_function_expr(p):
    '''
       binary_function : FUN LPAREN exp COMMA exp RPAREN
    '''
    p[0] = funs[p[1]](p[3], p[5])

# binary functions only taking integer inputs
def p_int_function_expr(p):
    '''
       int_function : INTFUN LPAREN INT COMMA INT RPAREN
    '''
    p[0] = funs[p[1]](p[3], p[5])

# fraction expression: only take int as numerator and denominator
def p_fraction_expr(p):
    '''
       fraction_expr : FRAC LPAREN frac_exp COMMA frac_exp RPAREN
    '''
    p[0] = Fraction(p[3], p[5])

# trig function: take radian (by default) or degree 
def p_trig_function_expr(p):
    '''
       trig_function : TRIGFUN LPAREN exp RPAREN
                     | TRIGFUN LPAREN deg RPAREN
    '''
    p[0] = funs[p[1]](p[3])

# vector uppermost level - handle plus minus
def p_vector_exp(p):
  '''
     vector_exp : vector_exp PLUS vector_cross
                | vector_exp MINUS vector_cross
                | vector_cross
  '''
  if len(p) == 2:
    p[0] = p[1]
  elif p[2] == '+':
    p[0] = p[1] + p[3]
  else:
    p[0] = p[1] - p[3]

# handle vector cross product/ linear product
def p_vector_cross(p):
  '''
      vector_cross : vector_cross TIMES vector
                   | vector_cross TIMES num
                   | vector
                   
  '''
  if len(p) > 2:
    if type(p[1]) is np.ndarray and type(p[3]) is np.ndarray:
      p[0] = np.cross(p[1], p[3])
    else:
      p[0] = p[1] * p[3]
  else:
    p[0] = p[1]

# atomic vector
def p_vector(p):
  '''
     vector : vector_builder RBRACK
  '''
  p[0] = np.array(p[1])

# vector builder
def p_vector_builder(p):
  '''
    vector_builder : vector_builder COMMA num
                   | LBRACK num
  '''
  if len(p) == 3:
    p[0] = [p[2]]
  else: 
    p[1].append(p[3])
    p[0] = p[1]

# list of points, as argument of interpolation/least square
def p_point_list(p):
  '''
     point_list : point_list_builder RBRACK
  '''
  p[0] = p[1]

# list builder
def p_point_list_builder(p):
  '''
     point_list_builder : point_list_builder COMMA LPAREN num COMMA num RPAREN
                        | LBRACK LPAREN num COMMA num RPAREN                        
  '''
  if len(p) == 7:
    p[0] = [(p[3], p[5])]
  else:
    p[1].append((p[4], p[6]))
    p[0] = p[1]


# atomic numbers
# int, float, -int, -float, int!, E(to the power of 10)
# handle vector dot product
def p_num(p):
    '''
	   num : INT
	       | FLOAT
         | fraction_expr
	       | MINUS INT
	       | MINUS FLOAT
         | MINUS fraction_expr
	       | INT EXL
	       | num EXP INT
	       | num EXP MINUS INT
         | vector vector
	'''
    if len(p) == 2:
        if type(p[1]) is Decimal:
            p[0] = Fraction(p[1])
        else:
            p[0] = p[1]
    elif type(p[1]) is np.ndarray and type(p[2]) is np.ndarray:
      p[0] = np.dot(p[1], p[2])
    elif p[1] == '-':
        p[0] = -p[2]
    elif p[2] == '!':
        p[0] = factorial(p[1])
    elif p[2] == 'E':
        if len(p) == 4:
            p[0] = p[1]*10**p[3]
        else:
            p[0] = p[1]/Fraction(10**(p[4]))
      
# degrees, only as input of trig functions
def p_deg(p):
	'''
	   deg : INT DEGREE
	       | FLOAT DEGREE
	'''
	p[0] = math.radians(p[1])

# error_handler
def p_error(p):
	if p:
		raise SyntaxError('Invalid Syntax')

# parser
acc = yacc.yacc()

