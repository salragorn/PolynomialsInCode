import re
def isPositive(num):
    return num > 0
class monomial:
    exponent = 0
    coefficient = 1
    def __init__(self, *args):
        if len(args) == 1:
            monomialString = args[0]
            if monomialString.find("X") == -1:
                self.coefficient = float(monomialString)
            else:
                Xidx = monomialString.find("X")
                if Xidx > 1:
                    self.coefficient = float(monomialString[:Xidx])
                elif Xidx == 1 and monomialString[0] not in ['+', '-']:
                    self.coefficient = float(monomialString[:Xidx])
                else:
                    self.coefficient = float(monomialString[:Xidx] + '1')

                self.exponent = float(monomialString[Xidx + 2:])
        elif len(args) == 2:
            self.coefficient, self.exponent = args
    def __str__(self):
        return str(self.coefficient) + "X^" + str(self.exponent)

    def evaluatePoint(self, point):
        value = self.coefficient * pow(point, self.exponent)
        return value
    def derivative(self):
        if self.exponent != 0:
            return monomial(self.coefficient * self.exponent, self.exponent - 1)
    def integral(self):
        return monomial(self.coefficient / (self.exponent + 1), self.exponent + 1)
    
class polynomial:
    monomialList = []
    def __init__(self, monomialList, diff=True, integrable=True):
        self.monomialList = monomialList
        if diff:
            self.derivated = polynomial([i.derivative() for i in monomialList if i.exponent != 0], False, False)
        if integrable:
            self.integrated = polynomial([i.integral() for i in monomialList], False, False)
    def evaluatePoint(self, point):
        value = 0
        for i in self.monomialList:
            value += i.evaluatePoint(point)
        return value
    def derivativePoint(self, point):
        return self.derivated.evaluatePoint(point)
    
    def definiteIntegral(self, left, right):
        return self.integrated.evaluatePoint(right) - self.integrated.evaluatePoint(left)
    def __str__(self):
        polyString = ''
        for i in self.monomialList:
            polyString += str(i) + ' '
        polyString = polyString[:-1]
        return polyString
    def newtonsMethod(self, start):
        for _ in range(1, 1000):
            start -= (self.evaluatePoint(start) / self.derivated.evaluatePoint(start))
        return start
    def bisectionMethod(self, start, end):
        epsilon = 10e-20
        for _ in range(1, 1000):
            if abs(self.evaluatePoint((end + start) / 2)) < epsilon:
                return (end + start) / 2
            if isPositive(self.evaluatePoint(start)) == isPositive(self.evaluatePoint((end + start) / 2)):
                start = (end + start) / 2
            else:
                end = (end + start) / 2
        return (end + start) / 2



        

        
print("Welcome to the my Polynomial solver, please input your polynomial")
print("f(X)=", end=' ')
polyString = input()
monomialsString = polyString.split()
poly = polynomial([monomial(i) for i in monomialsString])
print("f'(X): " + str(poly.derivated))
print("F(x): " + str(poly.integrated))
print("At what point would you like the function evaluated?, enter end to stop the program")
pointer = input()
while pointer != "end":
    if pointer != "solve":
        print("f(" + pointer + ")= " + str(poly.evaluatePoint(float(pointer))))
        print("f'(" + pointer + ")= " + str(poly.derivativePoint(float(pointer))))   
        print("F(" + pointer + ")= " + str(poly.integrated.evaluatePoint(float(pointer))))
    else:
        print("Which solving algorithm would you like to use? enter newton for newton's method and bisection for bisection method.")
        method = input()
        if method == 'newton':
            print("please enter starting point")
            start = float(input())
            while poly.derivated.evaluatePoint(start) == 0:
                print("Please enter a point with a non zero derivative")
                start = float(input())
            print("A root is at: " + str(poly.newtonsMethod(start)))
        elif method == 'bisection':
            start = end = -1
            while isPositive(start) == isPositive(end):
                print('please enter start and end searching points, which have opposite signs to find a root')
                start, end = list(map(float, input().split()))
            print("A root is at: " + str(poly.bisectionMethod(start, end)))
    print("At what point would you like the function evaluated?, enter solve for root-finding algorithms, enter end to stop the program")
    pointer = input()




