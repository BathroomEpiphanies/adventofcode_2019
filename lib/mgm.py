import sys
from math import gcd

def mgm(list_):
    mgm = list_[0]
    for i in range(1,len(list_)):
        mgm = mgm*list_[i]//gcd(mgm,list_[i])
    return mgm

if __name__ == '__main__':
    #list_ = [int(x) for x in sys.argv[1].split(',')]
    list_ = [121,11,55,67]
    print(mgm(list_))
