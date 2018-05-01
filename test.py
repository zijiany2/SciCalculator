import unittest, math
from parser import acc
from decimal import Decimal
from fractions import Fraction

class MyTest(unittest.TestCase):

    def test_int_plus_minus(self):
        s = '3+5-7'
        self.assertEquals(acc.parse(s), 1)

    def test_int_mult_divide(self):
        s = '2*9/6'
        self.assertEquals(acc.parse(s), 3)

    def test_int_precedence(self):
        s = '2*9+12/6-10'
        self.assertEquals(acc.parse(s), 10)

    def test_float_plus_minus(self):
        s = '0.3+0.5-0.7'
        self.assertEquals(acc.parse(s), Fraction(1,10))

    def test_float_mult_divide(self):
        s = '0.2*9/0.6'
        self.assertEquals(acc.parse(s), 3.0)

    def test_float_precedence(self):
        s = '0.2*9+1.2/6-1'
        self.assertEquals(acc.parse(s), 1.0)

    def test_negative_num(self):
        s = '-0.2+-0.8*-2.0'
        self.assertEquals(acc.parse(s), Fraction(7,5))

    def test_parenthesis(self):
        s = '(-0.2+-0.8)*-2.0'
        self.assertEquals(acc.parse(s), 2.0)

    def test_valid_factorial(self):
        s = '6!'
        self.assertEquals(acc.parse(s), 720)

    def test_zero_factorial(self):
        s = '0!'
        self.assertEquals(acc.parse(s), 1)

    def test_invalid_factorial(self):
        s = '3.5!'
        with self.assertRaises(SyntaxError) as se:
        	acc.parse(s)

    def test_positive_exp(self):
        s = '3E5'
        self.assertEquals(acc.parse(s), 300000)

    def test_negative_exp(self):
        s = '3E-5'
        self.assertEquals(acc.parse(s), Fraction(3, 100000))

    def test_n_choose_k(self):
        s = 'chs(4,2)'
        self.assertEquals(acc.parse(s), 6)

    def test_n_choose_0(self):
        s = 'chs(4,0)'
        self.assertEquals(acc.parse(s), 1)

    def test_n_choose_nplus1(self):
        s = 'chs(4,5)'
        self.assertEquals(acc.parse(s), 0)

    def test_invalid_n_choose_k(self):
        s = 'chs(4.5,2)'
        with self.assertRaises(SyntaxError) as se:
        	acc.parse(s)

    def test_gcd(self):
    	s = 'gcd(50,75)'
    	self.assertEquals(acc.parse(s), 25)

    def test_gcd2(self):
    	s = 'gcd(27,64)'
    	self.assertEquals(acc.parse(s), 1)

    def test_lcm(self):
    	s = 'lcm(50,75)'
    	self.assertEquals(acc.parse(s), 150)

    def test_invalid_lcm(self):
        s = 'lcm(1.2,3.7)'
        with self.assertRaises(SyntaxError) as se:
        	acc.parse(s)

    def test_log(self):
    	s='log(5,25)'
    	self.assertEquals(acc.parse(s), 2.0)

    def test_ln(self):
    	s='ln(8)'
    	self.assertEquals(acc.parse(s), math.log(8))

    def test_pow(self):
    	s='pow(2,10)'
    	self.assertEquals(acc.parse(s), 1024)

    def test_sqrt(self):
    	s='sqrt(100)'
    	self.assertEquals(acc.parse(s), 10.0)

    def test_sqr(self):
    	s='sqr(10)'
    	self.assertEquals(acc.parse(s), 100)

    def test_trig(self):
    	s='cos(1)'
    	self.assertEquals(acc.parse(s), math.cos(1))

    def test_trig_degree(self):
    	s='sin(90°)'
    	self.assertEquals(acc.parse(s), 1.0)

    def test_frac(self):
        s='frac(2,-6)'
        self.assertEquals(str(acc.parse(s)), '-1/3')

    def test_frac_add(self):
        s='1/2+1/3'
        self.assertEquals(str(acc.parse(s)), '5/6')

    def test_frac_mul(self):
        s='1/2*2/3'
        self.assertEquals(str(acc.parse(s)), '1/3')

    def test_complex(self):
        s='1+2j+4+3j'
        self.assertEquals(str(acc.parse(s)), '(5+5j)')

    def test_polynomial_add(self):
        s='1x2+2x1+2x2'
        self.assertEquals(str(acc.parse(s)), '(3x2+2x1)')

    def test_polynomial_sub(self):
        s='1x2+2x1-2x2'
        self.assertEquals(str(acc.parse(s)), '(-1x2+2x1)') 

    def test_polynomial_mul(self):
        s='(1x2+2x1)*(3x0+2x1)'
        self.assertEquals(str(acc.parse(s)), '(2x3+7x2+6x1)')

    def test_polynomial_deri(self):
        s='dx(1x2+2x1)'
        self.assertEquals(str(acc.parse(s)), '(2x1+2x0)')

    def test_polynomial_intg(self):
        s='intg(2x1+2x0)'
        self.assertEquals(str(acc.parse(s)), '(1x2+2x1)') 

    def test_polynomial_eval(self):
        s='(1x2+2x1)1'
        self.assertEquals(acc.parse(s), 3)

    def test_polynomial_definte_intg(self):
        s='(2x1+2x0)intg(1,2)'
        self.assertEquals(acc.parse(s), 5) 

    def test_polynomial_rangesum(self):
        s='(1x2+2x1)sum(1,2)'
        self.assertEquals(acc.parse(s), 11) 

    def test_vector_sum(self):
        s='[1,2,3]+[4,5,6]'
        self.assertEquals(list(acc.parse(s)), [5,7,9])

    def test_vector_times_num(self):
        s='[1,2,3]*2'
        self.assertEquals(list(acc.parse(s)), [2,4,6])

    def test_vector_inner(self):
        s='[1,2,3][4,5,6]'
        self.assertEquals(acc.parse(s), 32)

    def test_vector_cross(self):
        s='[1,2,3]*[1,2,3]'
        self.assertEquals(list(acc.parse(s)), [0,0,0])

    def test_interpolation(self):
        s='intp[(1,2),(3,4)]'
        self.assertEquals(str(acc.parse(s)), '(1.0x1+1.0x0)') 

    def test_least_square(self):
        s='lstsq[(1,2),(3,4),(4,5.2)]'
        self.assertEquals(str(acc.parse(s)), '(1.0571x1+0.9143x0)') 
    	
if __name__ == '__main__':
    unittest.main()
