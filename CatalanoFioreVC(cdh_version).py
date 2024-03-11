from ecpy import EllipticCurve, FiniteField, gcd, modinv, tate_pairing
from ecpy import EllipticCurveRepository
from Crypto.Util import number
from Crypto.Random import random
from numpy import matrix
import sys

#print(G)
#newg = G.__mul__(5)

#print(number.isPrime(n))
#print (tate_pairing(E,G,newg,n))

#public info about curve
F,E,g,p
zi_list : list
hi_list: list
hi_matrix : list
def keyGen(q):
    #refers to global variables
    global F,E,g,p,zi_list,hi_list,hi_matrix
    
    #F = Based Field object of E
    #E = Elliptic Curve corresponding to 'name'
    #g = Base point, generator
    #p = order of g
    F, E, g, p = EllipticCurveRepository('secp256k1')
    #modular class from 0 to p-1
    Zp = p
    #choose randomly z1,...,zq
    #set hi = g ** zi
    for i in range(0,q):
        zi_list[i] = random.randrange(start=1,stop=Zp-1)
        hi_list[i] = g**zi_list[i]
    
    #initialize qxq matrix to -1
    hi_matrix = [[-1 for _ in range(q)] for _ in range(q)]
    
    #print(hi_matrix)

    #for all i,j = 1...q, i!=q set hij = g ** (zi*zj)
    for i in range(0,q):
        for j in range(0,q):
            if(i!=j):
                hi_matrix[i][j] = g ** (zi_list[i]*zi_list[j])

    
def Com(q:int,message:list)
    C : int
    for i in range(0,q):
        C = C * (hi_list[i]**int.from_bytes(message[i].encode(),sys.byteorder))
    return C


