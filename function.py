######################################
####     Scientfic Calculator     ####
####     Written by Zijian Yao    ####
####      Built-in Functions      ####
######################################
import math

def sqrt(x):
	return math.sqrt(x)

def recip(x):
	return 1/x

def sqr(x):
	return x*x

def ln(x):
	return math.log(x)

def log(a,b):
	''' log of b to the base of a  '''
	return math.log(b,a)

def log10(x):
	return math.log(x,10)

def sin(x):
	return math.sin(x)

def cos(x):
	return math.cos(x)

def tan(x):
	return math.tan(x)

def factorial(x):
	''' compute x!, where x is assumed to be non-negative integer  '''
	f = 1
	for i in range(2, x+1):
		f *= i
	return f

def choose(n,k):
	''' n choose k, n and k are non-negative integers '''
	return factorial(n)//(factorial(k) * factorial(n-k))

def gcd(a,b):
	'''greatest common divisor of two integers a, b'''
	def rec_gcd(a,b):
		'''
		   Assume a, b are positive and a<b
		'''
		if a == 0:
			return b
		elif a == 1:
			return 1
		return rec_gcd(b%a, a)

	a, b = abs(a), abs(b)
	if a > b:
		a, b = b, a
	return rec_gcd(a,b)

def lcm(a,b):
	'''least common multiple of two integers a, b'''
	return abs(a*b)//gcd(a,b)

# mapping from function names to callables
funs = {'sqrt':sqrt, 
        'pow':pow, 
        'recip':recip, 
        'sqr':sqr, 
        'ln':ln, 
        'log':log,
        'log10':log10,
        'sin':sin, 
        'cos':cos, 
        'tan':tan,
        'chs':choose,
        'abs':abs,
        'gcd':gcd,
        'lcm':lcm
        }