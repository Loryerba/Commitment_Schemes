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
    return t1 == t2

def update(C, oldmessage, newmessage, i,h1):
    newc = C+h1[i]**(newmessage-oldmessage)
    return newc

def updateProof(A,newmessage,oldmessage,i,j,h2):
    newproof = A+(h2[j][i]**(newmessage - oldmessage))
    return newproof


def main():

    dim = 1000

    group = PairingGroup('SS1024')
    g = group.random(G1)

    start_time = time.time()
    h1,h2,z = keygen(g, q = dim)
    print("KeyGen required:" + str(time.time()-start_time) + " seconds")
    messages = []


    for i in range(0,dim):
        messages.append(random.randint(0,1000000))

    start_time = time.time()
    C = commit(messages,h1)
    print("Commit required:" + str(time.time()-start_time) + " seconds")

    start_time = time.time()
    A = open(0,messages,h2,g)
    print("Opening required:" + str(time.time()-start_time) + " seconds")

    #A2 = open2(messages,0,h1,z,g)

    start_time = time.time()
    print("Verify output:" + str(verify(C,messages[0],0,A,g,h1)))
    print("Verify required:" + str(time.time()-start_time) + " seconds")

    start_time = time.time()
    #perform new commitment at pos 0 for newmessage == 10 
    newc = update(C,messages[0],10000002,0,h1)
    print("Update commitment required:" + str(time.time()-start_time) + " seconds")
    verified2 = verify(newc,10000002,0,A,g,h1)
    if(verified2):
       print("Verifying update worked")
    else:
      print("Verifying update not worked")

    #perform another opening at pos 1
    oldproof = open(1,messages,h2,g)
    start_time = time.time()
    #peform an update of olderproof, to a new proof from pos 0 to 1, from old message at pos [0] to newmessage
    newproof = updateProof(oldproof,10000002,messages[0],0,1,h2)
    print("Update proof required:" + str(time.time()-start_time) + " seconds")

    verified3 = verify(newc,messages[1],1,newproof,g,h1)

    if(verified3):
        print("Verifying update proof worked")
    else:
        print("Verifying update proof not worked")




main()