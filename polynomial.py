from function import gcd
from decimal import Decimal
import numpy as np
import numpy.linalg as la

class Polynomial:

	def __init__(self, coef):
		'''
		   constructor. 
		   @para coef: coefficent dict with key=exponent and value=coefficient
		'''
		self.coef = coef

	def __add__(self, other):
		'''
			overloading +
			return the sum polynomial
		'''
		new = {}
		for k in self.coef.keys()|other.coef.keys():
			sum = self.coef.get(k,0) + other.coef.get(k,0)
			if sum!=0:
				new[k] = sum
		return Polynomial(new)

	def __sub__(self, other):
		'''
			overloading -
			return the difference polynomial
		'''
		new = {}
		for k in self.coef.keys()|other.coef.keys():
			diff = self.coef.get(k,0) - other.coef.get(k,0)
			if diff!=0:
				new[k] = diff
		return Polynomial(new)

	def __mul__(self, other):
		'''
			overloading *
			return the product polynomial
		'''
		new = {}
		for a in self.coef:
			for b in other.coef:
				new[a+b] = new.get(a+b, 0) + self.coef[a] * other.coef[b]
		return Polynomial(new)

	def __repr__(self):
		'''
			ocverloading print()
			speicify the representation of polynomial
			e.g. x^2+2x represented as 1x2+2x1
			return the representation
		'''
		s = ''
		for k in sorted(list(self.coef.keys()), reverse=True):
			sign = ''
			coef = self.coef[k]
			if coef > 0:
				sign = '+'
			s += sign + str(self.coef[k]) + 'x' + str(k)
		if s[0]=='+':
			s =  s[1:]
		return '(' + s + ')'

	def __str__(self):
		'''
			overloading str() 
			return the representatio
		'''
		return self.__repr__()

	def __call__(self,x):
		'''
			call a polynomial with input x
			evaluate the polynomial at x
			return the result
		'''
		r = 0
		for k in self.coef:
			r+= self.coef[k]*x**k
		return r

	def derivative(self):
		'''
			return the derivative polynomial
		'''
		new = {}
		for k in self.coef:
			if k!= 0:
				new[k-1] = k * self.coef[k]
		return Polynomial(new)

	def integral(self):
		'''
			return the indefinite integral (without constant term)
		'''
		from fractions import Fraction
		new = {}
		for k in self.coef:
			new[k+1] = Fraction(self.coef[k],k+1)
		return Polynomial(new)

	def rangeSum(self, lo, hi):
		'''
			sum the polynomial over range [lo, hi]
		'''
		from math import floor, ceil
		r = 0
		for i in range(ceil(lo),floor(hi)+1):
			r+=self(i)
		return r

def interp(points, k=None):
	'''
		polynomial interpolation of points
		when k is smaller than number of points, return the best fit by least square
		return a polynomial object
	'''
	n = len(points)
	if not k:
		k = n
	else:
		k = min(n,k)
	A = np.array([[points[i][0]**j for j in range(k)] for i in range(n)])
	b = np.array([points[i][1] for i in range(n)])
	x = la.solve(A,b) if k==n else np.linalg.lstsq(A, b)[0]
	return Polynomial(dict(zip(range(k),x)))

def lstsq(points, remove=False):
	'''
		linear least square 
		when remove=True, refine the fitting by remove one element with biggest error
		return a linear function
	'''
	x,y = zip(*points)
	A = np.vstack([x, np.ones(len(x))]).T
	m, c = np.linalg.lstsq(A, y)[0]
	if remove:
		err = []
		for xp, yp in points:
			err.append((m*xp+c-yp)**2)
		del points[np.argmax(err)]
		x,y = zip(*points)
		A = np.vstack([x, np.ones(len(x))]).T
		m, c = np.linalg.lstsq(A, y)[0]
	m = np.around(m,decimals=4)
	c = np.around(c,decimals=4)
	return Polynomial({0:c,1:m})
