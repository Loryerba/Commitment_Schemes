from charm.toolbox.pairinggroup import PairingGroup, G1,G2,GT,pair
import random
from operator import add
from functools import reduce
group = PairingGroup("MNT159")
g1 = group.random(G1)
g2 = group.random(G2)
alpha = random.randint(1,group.order())

def KeyGen(N:int):

    lg1 = []
    #genearete pp g1^{alpha*i} where 1<= i <= N
    for i in range (1,N+1):
        lg1.append(g1**(alpha*i))

    #generate pp g1^{alpha*(N+i)} where 2<=i<=N
    lg1N = []
    for i in range(2,N+1):
        lg1N.append(g1**(alpha*(N+i)))

    lg2 = []
    #genereatre pp g2^{alpha*i} where 1<= i <=N
    for i in range (1,N+1):
        lg2.append(g1**(alpha*i))

    #gt^{alpha*(N+1)} equals pair(g1^{alpha},g2^{N+1})
    gt = pair(g1**alpha,g2**(N+1))
    return lg1,lg1N,lg2,gt


def Commit(messages:list):
    innersum = 0
    for i in range(len(messages)):
        innersum = innersum + (messages[i] * (alpha**i))

    C = g1**(innersum)
    return C


def Proof(messages:list, i:int, N:int, C):

    innerexp = messages[i] * (alpha**i)
    proof = (C/(g1**innerexp))**(alpha**(N+1-i))

    return proof

def Verify(C,N:int,proof,gt,messages:list,i:int):
    
    pair1 = pair(C,g2**(alpha**(N+1-i)))
    pair2 = pair(proof,g2) * (gt**messages[i])  

    return(pair1 == pair2)


def main():

    messages = [2,3,4]
    lg1,lg1N,lg2,gt = KeyGen(len(messages))

    C = Commit(messages)

    A = Proof(messages,0,len(messages),C)

    print(Verify(C,len(messages),A,gt,messages,0))

main()
