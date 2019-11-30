from modular import zint
from matrix import matrix 

z5 = zint(5) # dynamic class creation
A = matrix( ((z5(3),z5(4)),(z5(1),z5(3))) )
E = matrix( ((z5(1),z5(0)),(z5(0),z5(1))) )

print(A**0)
print()
print(A@E)
print()
print(E@A)
print()
print(E@E)
print()
print(A**(2**12))
print()



