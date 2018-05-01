######################################
####     Scientfic Calculator     ####
####     Written by Zijian Yao    ####
####  Lexer: fomula tokenization  ####
######################################

from decimal import Decimal
import ply.lex as lex

# List of token names
tokens = (
	    'INT','FLOAT', 'FUN', 'INTFUN', 'TRIGFUN',
	    'PLUS','MINUS','TIMES','DIVIDE','DEGREE',
	    'LPAREN','RPAREN','COMMA','EXL', 'EXP', 
	    'FRAC', 'COMPLEX', 'X', 'D', 'I', 'S',
	    'LBRACK', 'RBRACK', 'IP', 'LS'
	    )

def CalcLexer():
	
	# Regular expression rules for simple tokens
	t_PLUS    = r'\+'
	t_MINUS   = r'-'
	t_TIMES   = r'\*'
	t_DIVIDE  = r'/'
	t_LPAREN  = r'\('
	t_RPAREN  = r'\)'
	t_LBRACK = r'\['
	t_RBRACK = r'\]'
	t_COMMA  = r','
	t_EXL = r'!'
	t_EXP = r'E'
	t_X = r'x'
	t_D = r'dx'
	t_S = r'sum'
	t_I = r'intg'
	t_IP = r'intp'
	t_LS = r'lstsq'
	t_DEGREE = r'°'
	t_FRAC = r'frac'
	t_FUN = r'sqrt|pow|recip|sqr|ln|log10|abs|log'
	t_INTFUN = r'chs|gcd|lcm'
	t_TRIGFUN = r'sin|cos|tan'
	
	# Ignoring characters
	t_ignore  = ' '
	
	# Regular expression rules with some action code

	def t_COMPLEX(t):
		r'\d+j|\d*\.\d+j'
		t.value = complex(t.value)
		return t

	# Parsing float
	def t_FLOAT(t):
		r'\d*\.\d+'
		t.value = Decimal(t.value) # convert to decimal representation to avoid inaccuracy 
		return t
	
	# Parsing int
	def t_INT(t):
		r'\d+'
		t.value = int(t.value)
		return t

	# Raise syntax error when token not recognized
	def t_error(t):
		raise SyntaxError("Illegal Character '%s'" % t.value[0])
	
	return lex.lex()

lexer = CalcLexer()