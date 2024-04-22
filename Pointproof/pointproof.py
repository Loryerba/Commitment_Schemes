from charm.toolbox.pairinggroup import PairingGroup, G1,G2,GT,pair
import random
from operator import add
from functools import reduce
import time
group = PairingGroup("MNT159")
g1 = group.random(G1)
g2 = group.random(G2)
alpha = random.randint(1,group.order())

def KeyGen(N:int):

    lg1 = [g1**(alpha*i) for i in range(1,N+1)]
    lg1N = [g1**(alpha*(N+i)) for i in range(1,N+1)]
    lg2 = [g2**(alpha*i) for i in range(1,N+1)]

    #gt^{alpha*(N+1)} equals pair(g1^{alpha},g2^{N+1})
    gt = pair(g1**alpha,g2**(alpha**N))
    return lg1,lg1N,lg2,gt


def Commit(messages:list,lg1):
    #default value
    C = lg1[0] ** 0
    for i in range(len(messages)):
        #calculate C as g^{m1*alpha^1 + .... + mn*alpha^n}
        #equals to g^{{alpha^1}^message1} + .. + g^{{alpha^n}^messagen}
        C+=lg1[i]**messages[i]
    return C


def Proof(messages:list, i:int, N:int, C):

    #calculate inner exponent as mi*alpha^{i}
    innerexp = messages[i] * (alpha**i)
    #calcualte proof as (C/g1^{inner exponent} )^{alpha^{N+1-i}}
    proof = (C/(g1**innerexp))**(alpha**(N+1-i))

    return proof

def Proof2(messages:list, i:int, N:int, C):

    innerexp = 0
    for j in range(len(messages)):
        if(j == i):
            continue
        innerexp = innerexp + messages[j] * (alpha ** (N+1-i+j))
    return g1**innerexp

def Verify(C,N:int,proof,messages:list,i:int,gt):
    
    #calculate first pairing value as e(C,g2^{alpha^{N+1-i}})
    pair1 = pair(C,g2**(alpha**(N+1-i)))
    #calculate second pairing value as e(pi,g2) * gt^{alpha^{N+1}*mi}
    pair2 = pair(proof,g2) * (gt**messages[i])  


    return(pair1 == pair2)


def main():

    messages = [random.randint(0,100) for i in range(0,100000)]
    start = time.time()
    lg1,lg1N,lg2,gt = KeyGen(len(messages))
    print("required: " + str((time.time()-start)*1000) + " ms")

    start = time.time()
    C = Commit(messages,lg1)
    end = time.time()

    print("Commitment required: " + str((end-start)*1000) + " ms")

    start = time.time()
    A = Proof(messages,0,len(messages),C)
    end = time.time()

    print("Opening required: " + str((end-start)*1000) + " ms")

    start = time.time()
    print("Verifiy Output: " + str(Verify(C,len(messages),A,messages,0,gt)))
    end = time.time()
    print("Verifiy required: " + str((end-start)*1000) + " ms")

main()
