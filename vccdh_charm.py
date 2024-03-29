from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, pair
import random
from Crypto.Random import random
import time
#mul == g**scalar
#sum = g + g2
#div = g/g2 = g-g2

def keygen(g,q):
    z=[]
    #generazione di q elementi estratti casualmente da Zp
    for i in range(q):
       z.append(random.randint(0,q))
    h1 = []
    #generazione di tutti gli elementi basati su g^zi
    for i in range(len(z)):
        h1.append(g**z[i])
    h2 = []
    #generazione della matrice hij, dove per ogni cella ij con i!=j calcola g^(zi*zj)
    for i in range(len(z)):
        h2.append([])
        for j in range(len(z)):
            if(i == j):
                h2[i].append(0)
                continue
            h2[i].append(g**(z[i]*z[j]))
    return h1, h2, z

def commit(messages, h1):
    #commitment value vuoto (0:1:0)
    C = h1[0]**(0)
    #per ogni elemento presente nel messaggio
    for i in range(len(messages)):
        #calcolo di h1^m1 * .... *hq^mq
        #in EC il * si traduce in +, e ** si traduce in *
        C = C+(h1[i]**(messages[i]))
    return C

def open(i, messages, h2, g):
    #opening vuoto (0:1:0)
    A = g**(0)
    #per ogni elemento nel messaggio
    for j in range(len(messages)):
        if(i==j):
            continue
        #opening calcolato come hij^mj in produttoria da j=1 a j=q
        A = A+(h2[i][j]**(messages[j]))
    return A

def open2(messages,i,h1,z,g):
    A = g**(0)
    for j in range(len(messages)):
        if(i==j):
            continue
        A = A+(h1[i]**(messages[j]*z[j]))
    
    return A

def verify(C, message, i, A, g, h1):
    
    denominatore = h1[i]**(message)
    #calcolo di C/denom come C-denom
    C = C/(denominatore)
    
    t1 = pair(C,h1[i])
    t2 = pair(A,g)
    print(t1)
    print(t2)
    return t1 == t2


def main():
    group = PairingGroup('SS512')
    g = group.random(G1)
    start_time = time.time()
    h1,h2,z = keygen(g, q = 1000)
    print(time.time()-start_time)
    """messages = [1,2,3]
    C = commit(messages,h1)
    A = open(0,messages,h2,g)
    #A2 = open2(messages,0,h1,z,g)
    print(verify(C,messages[0],0,A,g,h1))"""

main()