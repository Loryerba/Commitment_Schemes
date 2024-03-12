from ecpy import ExtendedFiniteField,EllipticCurve, FiniteField, gcd, modinv, tate_pairing
from ecpy import EllipticCurveRepository
from Crypto.Util import number
from Crypto.Random import random
import sys
#print(G)
#newg = G.__mul__(5)

#print(number.isPrime(n))
#print (tate_pairing(E,G,newg,n))

#public info about curve
F: FiniteField
E: EllipticCurve
g: EllipticCurve
p: int
zi_list : list
hi_list: list
hi_matrix : list
def keyGen(q):  
    
    #F = Based Field object of E
    #E = Elliptic Curve corresponding to 'name'
    #g = Base point, generator
    #p = order of g
    field ,ec,generator,prime_order = EllipticCurveRepository('secp256k1')
    #modular class from 0 to p-1
    Zp = prime_order
    print(generator*4)
    zilist = list ()
    hilist = list ()
    himatrix = list ()
    #choose randomly z1,...,zq
    #set hi = g ** zi
    for i in range(0,q):
        zilist.append(random.randrange(1,Zp-1))
        hilist.append(generator**zilist[i])
    
    #initialize qxq matrix to -1
    himatrix = [[-1 for _ in range(q)] for _ in range(q)]
    
    #print(hi_matrix)

    #for all i,j = 1...q, i!=q set hij = g ** (zi*zj)
    for i in range(0,q):
        for j in range(0,q):
            if(i!=j):
                himatrix[i][j] = generator ** (zilist[i]*zilist[j])

    return(field,ec,generator,prime_order,zilist,hilist,himatrix)

    
def Com(q:int,message:list):
    C : int
    for i in range(0,q):
        C = C * (hi_list[i]**int.from_bytes(message[i].encode(),sys.byteorder))
    return C



(F,E,g,p,zi_list,hi_list,hi_matrix) = keyGen(q=5)


print("Ordine del gruppo: " + p)

