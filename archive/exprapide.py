#exponentiation rapide
	
import random
import sys
sys.setrecursionlimit(10000)

def exprap(x,n,p): # (x**n)%p
    if n == 0:
        return 1
    k = exprap(x, n//2,p)
    if n % 2 == 0:
        return (k*k)%p
    else:
        return (x * k * k)%p

