from ecpy import ExtendedFiniteField,EllipticCurve, FiniteField, gcd, modinv, tate_pairing
from ecpy import EllipticCurveRepository
import random

field ,ec,generator,prime_order = EllipticCurveRepository('secp256k1')


def keygen(g, q):
    z=[]
    for i in range(q):
       z.append(random.randint(0,50))
    h1 = []
    for i in range(len(z)):
        h1.append(generator.__mul__(z[i]))
    h2 = []
    for i in range(len(z)):
        h2.append([])
        for j in range(len(z)):
            if(i == j):
                h2[i].append(0)
                continue
            h2[i].append(generator.__mul__(z[i]*z[j]))
    return h1, h2, z

def commit(messages, h1):
    C = h1[0].__mul__(0)
    for i in range(len(messages)):
        C = C.__add__(h1[i].__mul__(messages[i]))
    return C

def open(message, i, messages, h2, g):
    #print(g)
    A = generator.__mul__(0)
    for j in range(len(messages)):
        if(i==j):
            continue
        A = A.__add__(h2[i][j].__mul__(messages[j]))
    return A

def open2(messages,i,h1,z):
    A = generator.__mul__(0)
    for j in range(len(messages)):
        if(i==j):
            continue
        A = A.__add__(h1[i].__mul__(messages[j]*z[j]))
    
    return A

def verify(C, message, i, A, g, h1):
    
    denominatore = h1[i].__mul__(message)
    #calcolo di C/denom come C + -denom
    C = C.__sub__(denominatore)
    
    t1 = tate_pairing(ec,C,h1[i],prime_order)
    t2 = tate_pairing(ec,A,g,prime_order)
    print(t1)
    print(t2)
    return t1 == t2


def main():
    h1,h2,z = keygen(generator,q=3)
    messages = [1,2,3]
    C = commit(messages,h1)    
    A = open(messages[0],0,messages,h2,generator)
    A2 = open2(messages,0,h1,z)

    print(A == A2)
    
    """comm = h1[1].__mul__(0)
    for i in range(1,len(messages)):
        comm = comm.__add__(h1[i].__mul__(messages[i]))
    
    C = C.__sub__(h1[0].__mul__(messages[0]))

    print(comm == C)"""
    if(verify(C, messages[0], 0, A, generator, h1)):
        print("verified")
    else:
       print("not verified")
   
main()


