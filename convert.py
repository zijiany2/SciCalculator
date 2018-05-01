from CalcLex import lexer, tokens
from decimal import Decimal
from fractions import Fraction
from cmath import polar, rect
import ply.yacc as yacc
from numpy import around

start = 'conv' # CFG start token

# uppermost level
# convert fraction, decimal, complex
def p_conv(p):
    '''
       conv : int DIVIDE INT
           | LPAREN conv RPAREN
           | float COMMA float
           | float
           | INT
           | complex


    '''
    if len(p) == 4:
      if p[2] == '/':
        p[0] = around(p[1] / p[3],decimals=16)
      elif p[1] == '(':
        p[0] = p[2]
      else:
        p[0] = rect(p[1], p[3])
    else:
        if type(p[1]) is int:
          p[0] = p[1]
        elif type(p[1]) is complex: 
          p[0] = polar(p[1])
        else:
          p[0] = Fraction(p[1])

# parse complex number 
def p_complex(p):
  '''
     complex : int PLUS COMPLEX
             | int MINUS COMPLEX
             | float PLUS COMPLEX
             | float MINUS COMPLEX
  '''
  if p[2] == '+':
    p[0] = p[1] + p[3]
  else:
    p[0] = p[1] - p[3]

# parse int
def p_int(p):
  '''
     int : INT
         | MINUS INT
  '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    p[0] = -p[2]

# parse float
def p_float(p):
  '''
     float : FLOAT
           | MINUS FLOAT
  '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    p[0] = -p[2]

# parse error
def p_error(p):
  if p:
    raise SyntaxError('Unsupported Type')

converter = yacc.yacc()