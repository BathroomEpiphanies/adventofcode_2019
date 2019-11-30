from copy import copy,deepcopy
from numbers import Number


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m



def zint(modulus):
    return type(f'z{modulus}',(_zint,),{'modulus':modulus})

class _zint(Number):

    def __init__(self,number):
        self.value = int(number)%self.modulus

    #def __repr__(self):
    #    return f'{type(self)}({self.value})'
    def __str__(self):
        return f'{self.value}\{self.modulus}' 
    __repr__ = __str__
       
    def __eq__(self,other):
        return int(self) == int(other)%self.modulus
    def __ne__(self,other):
        return int(self) != int(other)%self.modulus
    def __lt__(self,other):
        return int(self) <  int(other)%self.modulus
    def __le__(self,other):
        return int(self) <= int(other)%self.modulus
    def __gt__(self,other):
        return int(self) >  int(other)%self.modulus
    def __ge__(self,other):
        return int(self) >= int(other)%self.modulus

    def __abs__(self,other):
        return type(self)(  int(self) )
    def __neg__(self):
        return type(self)( -int(self) )

    def __add__(self,other):
        return type(self)( int(self)+int(other) )
    __radd__ = __add__

    def __mul__(self,other):
        return type(self)( int(self)*int(other) )
    __rmul__ = __mul__

    def __truediv__(self,other):
        return self*pow(type(self)(other),-1)
    __floordiv__ = __truediv__
    
    def __rtruediv__(self,other):
        return type(self)(other)*pow(self,-1)
    __rfloordiv__ = __rtruediv__

    def __sub__(self,other):
        return type(self)( int(self)-int(other) )
    def __rsub__(self,other):
        return type(self)( int(other)-int(self) )

    def __hash__(self):
        return hash((self.value,self.modulus))
    
    def __bool__(self):
        return bool(self.value)
    def __int__(self):
        return self.value
    
    def __copy__(self):
        return type(self)( self )
    
    def __pow__(self,other):
        if int(other) > 0:
            return type(self)( pow(int(self),int(other),self.modulus) )
        else:
            inverse = modinv(self.value,self.modulus)
            return type(self)( pow(inverse,-int(other),self.modulus) )


if __name__ == '__main__':

    z5 = zint(5)
    print(z5)
    
    a = z5(3)
    b = z5(2)
    c = z5(a)
    d = z5(0)
    #print(d)
    #print( "hej" if not a else "hopp")
    #print( "hej" if d else "hopp")
    ##c = z5(None)

    s = set()
    s.add(a)
    s.add(b)
    s.add(c)
    s.add(a)

    print(f'{str(s)}')
    
    #print( 6>a )
    #print( a<6 )
    #print( a>6 )
    print(c)
    print()
    print( f'{a}' )
    print()
    print( b )
    print()
    print( str(a+b) )
    print()
    print( str(9+b) )
    print()
    print( str(b+9) )
    print()
    print( str(a-b) )
    print()
    print( str(3-b) )
    print()
    print( str(b-3) )
    print()
    print( str(a*b) )
    print()
    print( str(9*b) )
    print()
    print( str(b*9) )
    print()
    print( str(a**b) )
    print()
    print( str(b**-1) )
    print()
    print( str(a/b) )
    print()
    
    
#    a = modint( 3,5 )
#    b = modint( 2,5 )
#    
#    print( int(a) )
#    print()
#    print( b )
#    print()
#    print( a+b )
#    print()
#    print( a-b )
#    print()
#    print( a*b )
#    print()
#    print( a**b )
#    print()
