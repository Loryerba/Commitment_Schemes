import ecpy
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

def castMessage(message:str):
    return int.from_bytes(message.encode(),sys.byteorder)

def mul_to_pow(g: ecpy.elliptic_curve.EllipticCurve, scalar: int):
    while(scalar > 0):
        g = g.__add__(g)
        scalar-=1
    return g

def div_between_point(g: ecpy.elliptic_curve.EllipticCurve, g2: ecpy.elliptic_curve.EllipticCurve):
    return g.__sub__(g2)

def mul_between_point(g:ecpy.elliptic_curve.EllipticCurve,g2: ecpy.elliptic_curve.EllipticCurve):
    return g.__add__(g2)

def keyGen(q):  
    
    #F = Based Field object of E
    #E = Elliptic Curve corresponding to 'name'
    #g = Base point, generator
    #p = order of g
    field ,ec,generator,prime_order = EllipticCurveRepository('secp256k1')
    #modular class from 0 to p-1
    Zp = prime_order
    zilist = list ()
    hilist = list ()
    himatrix = list ()
    #choose randomly z1,...,zq
    #set hi = g ** zi
    for i in range(0,q):
        zilist.append(random.randrange(1,10))
        hilist.append(mul_to_pow(generator,zilist[i]))
    
    #initialize qxq matrix to -1
    himatrix = [[-1 for _ in range(q)] for _ in range(q)]
    
    #print(hi_matrix)

    #for all i,j = 1...q, i!=q set hij = g ** (zi*zj)
    for i in range(0,q):
        for j in range(0,q):
            if(i!=j):
                himatrix[i][j] = mul_to_pow(generator, (zilist[i]*zilist[j]))

    return(field,ec,generator,prime_order,zilist,hilist,himatrix)

    
def Com(q:int,message:list):
    C = mul_to_pow(hi_list[0],castMessage(message[0]))
    for i in range(1,q):
        C = mul_between_point(C,mul_to_pow(g=hi_list[i],scalar=castMessage(message[i])))
    return C


def Open(q:int,message:str, i:int):
    check = True
    for j in range(0,q):
        if(j!=i and check):
            proof = mul_to_pow(hi_matrix[i][j],castMessage(message[j]))
            check = False
        elif (j!=i):
            proof = mul_between_point(proof,mul_to_pow(hi_matrix[i][j],castMessage(message[j])))
    
    return proof


def Vrfy(C,proof,i:int,message:list):
    hi= mul_to_pow(hi_list[i],castMessage(message[i]))
    return tate_pairing(E,div_between_point(C,hi),hi_list[i],p) == tate_pairing(E,proof,g,p)


(F,E,g,p,zi_list,hi_list,hi_matrix) = keyGen(q=3)
message = list(("1","2","3"))
print(g.__add__(g))
C = Com(q=3,message=message)
proof = Open(q=3,message=message,i=0)
print(Vrfy(C,proof,i=0,message=message))

print("Ordine del gruppo: " + str(p))
print("Generatore del gruppo: " + g.__str__())


