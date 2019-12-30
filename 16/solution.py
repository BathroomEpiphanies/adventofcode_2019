#!/usr/bin/python3

import sys
import numpy as np
import math







#line = sys.stdin.readline().strip()
line="12345678"
#line="80871224585914546619083218645595"
#line="19617804207202209144916044189917"
#line="69317163492948606335995924319873"


#line = f"{'0'}{line}{'0'*(len(line)-1)}"
print(len(line))
print(line)




l = 12
patterns=[]
for i in range(1,l+1):
    k = math.ceil((l+1)/i/4)
    #print(i,k)
    r = []
    r.extend([ 0 for j in range(i)])
    r.extend([ 1 for j in range(i)])
    r.extend([ 0 for j in range(i)])
    r.extend([-1 for j in range(i)])
    q = []
    for j in range(k):
        q.extend(r)
    patterns.append(q[1:l+1])


for row in patterns:
    for n in row:
        print(f"{n:3d}",end='')
    print()



















exit()



















nums = [int(x) for x in line]
#fft = np.fft.fft(nums,len(nums))
#fft = np.fft.fft(nums,4)
#fft = np.fft.fft(nums)
#print(len(fft))
#for i,c in enumerate(list(fft)):
#    print(i,c)
#print([np.real(x) for x in fft])


#line = f"{line}{'0'*(len(line)-1)}"
for k in range(1,len(line)+1):
    print()
    print(k)
    summa = 0
    for m in range(k):
        fft = np.fft.fft(nums[k-1+m::k],len(line))
        for i,c in enumerate(list(fft)):
            print(i,c)
        summa += fft[3]
    print(f"sum: {summa}")

exit()


# X0,...,N−1 ← ditfft2(x, N, s):             DFT of (x0, xs, x2s, ..., x(N-1)s):
#     if N = 1 then
#         X0 ← x0                                      trivial size-1 DFT base case
#     else
#         X0,...,N/2−1 ← ditfft2(x, N/2, 2s)             DFT of (x0, x2s, x4s, ...)
#         XN/2,...,N−1 ← ditfft2(x+s, N/2, 2s)           DFT of (xs, xs+2s, xs+4s, ...)
#         for k = 0 to N/2−1                           combine DFTs of two halves into full DFT:
#             t ← Xk
#             Xk ← t + exp(−2πi k/N) Xk+N/2
#             Xk+N/2 ← t − exp(−2πi k/N) Xk+N/2
#         endfor
#     endif


#def ditfft2(x,N,s):
#    if N == 1:
#        return x[0]
#    else:
#        l1 = ditfft2(x  ,N/2,2s)
#        l2 = ditfft2(x+s,N/2,2s)
#        for k in range(0,N/2):
#            t = x[k]
#            X[k]     = t
#            X[k+N/2] = t
#


fft = ditfft2([int(x) for x in line],len(line),1)
print(fft)

exit()
a = [0,1,0,-1,0]
def mp(r,c):
    return a[((c+1)//(r+1))%4]

for r in range(len(line)):
    for c in range(len(line)):
        print(f"{mp(r,c): 2d}",end='')
    print()


off = int(line[0:7])

print(off)
off = off%len(line)
print(f"{line}{line}"[off:off+8])

line = f"{line}{line}"
for c in range(off,off+24):
    for r in range(off,off+24):
        m = mp(r,c)
        mes = int(line[c])
        for i in range(100):
            mes = mes*m
            if mes < 0 and mes%10 != 0:
                mes = 10 - mes%10
            else:
                mes = mes%10
        print(f"{mes: 2d}",end='')
            

        
#patterns=[]
#for i in range(1,1+len(line)):
#    k = math.ceil((len(line)+1)/i/4)
#    #print(i,k)
#    r = []
#    r.extend([ 0 for j in range(i)])
#    r.extend([ 1 for j in range(i)])
#    r.extend([ 0 for j in range(i)])
#    r.extend([-1 for j in range(i)])
#    q = []
#    for j in range(k):
#        q.extend(r)
#    patterns.append(q[1:len(line)+1])
#
##for row in patterns:
##    print(row)
#
#
#def mod(l):
#    for i in range(len(l)):
#        if l[i] < 0 and l[i]%10 != 0:
#            l[i] = 10 - l[i]%10
#        else:
#            l[i] = l[i]%10
#            
#mes = np.array([int(x) for x in line])
#mat = np.array(patterns)
#print(mes)
#print(mat)
#
#
#for i in range(103):
#    #print(i,''.join(mes.list()))
#    print(i,mes)
#    mes = np.matmul(mat,mes)
#    mod(mes)
#
