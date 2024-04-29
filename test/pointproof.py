from charm.toolbox.pairinggroup import PairingGroup, G1,G2,GT,pair
import random
import sys
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


def Commit(lg1:list,messages:list):
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

def Verify(C,N:int,proof,gt,messages:list,i:int):
    
    #calculate first pairing value as e(C,g2^{alpha^{N+1-i}})
    pair1 = pair(C,g2**(alpha**(N+1-i)))
    #calculate second pairing value as e(pi,g2) * gt^{alpha^{N+1}*mi}
    pair2 = pair(proof,g2) * (gt**messages[i])  

    return(pair1 == pair2)

def Aggregate(proofs:list,scalars:list):
    #default value
    Ai = g1**0
    for i in range(len(proofs)):
        #calculate aggregation of i proofs as pi_1^{t1} + .. + pi_i^{ti}
        Ai= Ai + (proofs[i]**scalars[i])
    return Ai

def VerifiyAggregate(C,N,Ai,messages,number,scalars,gt):
    #exponent of first pairing
    innterexp = 0
    for i in range(number):
       #calculate the exponent for i proofs as alpha^{N+1-1}*t1 + .. + alpha^{N+1-i}*ti
       innterexp= innterexp + ((alpha**(N+1-i)) * scalars[i])
    
    #calculate the first pairing as e(C,g2^{innterexp})
    pair1 = pair(C,g2**innterexp)
    
    #exponent of second pairing
    exp = 0

    #calculate mi*ti
    for i in range(number):
        exp = exp + (messages[i]*scalars[i])
    
    #calculate second pairing as e(pi_aggregate,g2) * gt^{exp}
    pair2 = pair(Ai,g2) * (gt**exp)
    return pair1 == pair2

def UpdateCommit(C,i,oldm,newm,lg1):
    #calculate new commitment C' as C*g1^{mi'-m*alpha^{i}}
    C = C + (g1**((newm-oldm)*(alpha**i)))

    return C

def main():
    dim = int(sys.argv[1])
    messages = [random.randint(0,100) for i in range(0,dim)]

        
    start = time.time()
    lg1,lg2,lg1N,gt = KeyGen(len(messages))
    end = time.time()
    print("Key gen required: " + str((end-start)*1000) + " ms")



    start = time.time()
    C = Commit(lg1,messages)
    end = time.time()
    print("Commitment required: " + str((end-start)*1000) + " ms")
    print(C)

    start = time.time()
    A = Proof(messages,0,len(messages),C)
    end = time.time()

    print("Opening required: " + str((end-start)*1000) + " ms")
    A1= Proof(messages,1,len(messages),C)
    print(A)
    print(A1)

    start = time.time()
    print("Verifiy Output: " + str(Verify(C,len(messages),A,gt,messages,0)))
    end = time.time()
    print("Verifiy required: " + str((end-start)*1000) + " ms")


    proofs = [A,A1]
    scalars = [1202039,1292330]
    start = time.time()
    Ai = Aggregate(proofs,scalars)
    end = time.time()
    print("Aggregation required: " + str((end-start)*1000) + " ms")
    print(Ai)


    start = time.time()
    print("Verify Aggregate output: " + str(VerifiyAggregate(C,len(messages),Ai,messages,len(scalars),scalars,gt)))
    end = time.time()
    print("Verify aggregation required: " + str((end-start)*1000) + " ms")


    newvalue = random.randint(100,110)
    start = time.time()
    newC = UpdateCommit(C,0,messages[0],newvalue,lg1)
    end = time.time()

    print("Update commitment required: " + str((end-start)*1000) + " ms")
    #new vector generated at pos 0 new message equals 10
    messages[0] = newvalue
    print("Verifiy update commit output: " + str(Verify(newC,len(messages),A,gt,messages,0)))

main()
