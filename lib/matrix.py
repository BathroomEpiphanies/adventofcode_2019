from copy import copy,deepcopy
from numbers import Number


def unit(M):
    return [[1 if c==r else 0 for c,_ in enumerate(row)] for r,row in enumerate(M)]

def invert(M):
    E = unit(M)
    M = [[c for c in row] for row in M]
    # gauss-jordan elimination per row
    for i in range(len(M)):
        # swap remaining row with largest value in current column to current row
        k = i
        for j in range(i+1,len(M)):
            if M[j][i] > M[k][i]:
                k = j
        M[i],M[k] = M[k],M[i]
        E[i],E[k] = E[k],E[i]

        # reduce current row to have 1 in current column
        a = M[i][i]
        for k in range(len(M)):
            E[i][k] /= a
            M[i][k] /= a
        
        # subtract current row from others
        for j in range(len(M)):
            if i==j:
                continue
            b = M[j][i]
            for k in range(len(M)):
                E[j][k] -= b*E[i][k]
                M[j][k] -= b*M[i][k]
    return E

    
    

class matrix(Number):
    
    def __init__(self,matrix):
        self.matrix = matrix
        return
    
    def __repr__(self):
        return   "\n".join(['|'+' '.join([str(c) for c in r])+'|' for r in self.matrix])
    
    def __matmul__(self,other):
        R = len(self.matrix)
        C = len(other.matrix[0])
        out = [[0 for _ in range(C)] for _ in range(R)]
        for r in range(R):
            for c in range(C):
                out[r][c] = sum(self.matrix[r][i] * other.matrix[i][c] for i in range(R))
        return matrix(out)
    
    def __add__(self,other):
        return matrix( tuple(tuple(c1+c2 for c1,c2 in zip(r1,r2)) for r1,r2 in zip(self.matrix,other.matrix)) )
    
    def __sub__(self,other):
        return matrix( tuple(tuple(c1-c2 for c1,c2 in zip(r1,r2)) for r1,r2 in zip(self.matrix,other.matrix)) )
    
    def __mul__(self,other):
        return matrix( tuple(tuple(c*other for c in r) for r in self.matrix) )
    
    def __rmul__(self,other):
        return matrix( tuple(tuple(c*other for c in r) for r in self.matrix) )

    def __truediv__(self,other):
        return matrix( tuple(tuple(c/other for c in r) for r in self.matrix) )

    def __floordiv__(self,other):
        return matrix( tuple(tuple(c//other for c in r) for r in self.matrix) )

    def __mod__(self,other):
        return matrix( tuple(tuple(c%other for c in r) for r in self.matrix) )
    
    def __copy__(self):
        return matrix(deepcopy(self.matrix))
    
    def __pow__(self,other):
        if other < 0:
            inverse = type(self)(invert(self.matrix))
            return pow(inverse,-other)
        if other == 0:
            return type(self)(unit(self.matrix))
        if other == 1:
            return copy(self)
        half = self**(other//2)
        if other%2==0:
            return half@half
        else:
            return self@half@half

    
if __name__ == '__main__':
    A = matrix( ((2,0),(0,2)) )
    B = matrix( ((0,3),(3,0)) )
    E = matrix( ((1,0),(0,1)) )
    F = matrix( ((0,1),(1,0)) )
    T = matrix( ((0,6),(9,1)) )

    #print(unit(A.matrix))

    a = A**-3
    
    print(a)
    print()
    
    print(A)
    print()
    
    print( T )
    print()

    print( 51*T**-1 )
    print()

    print( T@T**-1 )
    print()

    print( T**-1@T )
    print()

    exit()
    print( B )
    print()
    print( A+B )
    print()
    print( A-B )
    print()
    print( A@B )
    print()
    print( 3*B )
    print()
    print( E*3 )
    print()
    print( A**0 )
    print()
    print( A**1 )
    print()
    print( A**2 )
    print()
    print( A**3 )
    print()
    print( T )
    print()
    
