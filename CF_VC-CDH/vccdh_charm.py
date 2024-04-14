from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, pair
import random
from Crypto.Random import random
import time
#mul == g**scalar
#sum = g + g2
#div = g/g2 = g-g2

"""
KeyGen requires:
    g : generator of group
    q: length of message list
"""
def keygen(g:G1,q:int) -> tuple:

    #list comprehension version
    """
     #calculate zi element <-$ Zp
    z=[random.randint(0,q) for i in range(0,q)]

    #calculate hi as g^{zi}
    hi = [g**z[i] for i in range(len(z))]
    
    #calculate hij as g^{zi*zj}
    h_ij = [[g**(z[i]*z[j]) if i!=j else 0 for j in range(len(z))] for i in range(len(z))]
    
    return hi, h_ij, z"""
    z=[]
    #calculate zi element <-$ Zp
    for i in range(q):
       z.append(random.randint(0,q))
    hi = []
    #calculate hi as g^{zi}
    for i in range(len(z)):
        hi.append(g**z[i])
    h_ij = []
    #calculate hij as g^{zi*zj}
    for i in range(len(z)):
        h_ij.append([])
        for j in range(len(z)):
            if(i == j):
                h_ij[i].append(0)
                continue
            h_ij[i].append(g**(z[i]*z[j]))
    return hi, h_ij, z

"""
Commit requires:
    messages: list of messages to commit
    hi: public parameter as g^{zi} for 1<=i<=q
"""
def commit(messages:list, hi:list) -> G1:
    #default value
    C = hi[0]**(0)
    for i in range(len(messages)):
        #calculate C as hi^{mi} * .. * hn^{mn}
        C = C+(hi[i]**(messages[i]))
    return C

"""
Open requires:
    i : index of message to open
    messages: list of messages
    h_ij: public parameter as g^{zi*zj}
    g: generator of group

"""
def open(i:int, messages:list, h_ij:list, g:G1) -> G1:
    #default value
    A = g**(0)
    for j in range(len(messages)):
        #skip i == j
        if(i==j):
            continue
        #calculate A as hij^{mij} * ... * hij^{mij}
        A = A+(h_ij[i][j]**(messages[j]))
    return A

"""
Open2 is an alternative opening method which requires:
    messages: list of messages
    i : index of message to open
    hi: public parameter as g^{zi}
    z: public parameter as z1,...zq <-$ Zp
    g: generator of group
"""
def open2(messages:list,i:int,hi:list,z:list,g:G1) -> G1:
    #default value
    A = g**(0)
    for j in range(len(messages)):
        #skip i == j
        if(i==j):
            continue
        #calculate A as hi^{mj*zj}
        A = A+(hi[j]**(messages[j]*z[j]))
    return A


"""
Verify requires:
    C: commitment value
    message: message to verify
    i: index of message in messages list
    A: proof of message at pos i
    g: generator of group
    hi: public parameter as g^{zi}
"""
def verify(C: G1, message:int, i:int, A:G1, g:G1, hi:list) -> bool:
    
    #calculate external divisor as hi^{mi}
    externsub = hi[i]**(message)
    #calculate first member of the first pairing as C/hi^{mi}
    C = C/(externsub)
    
    #calculate first pairing as e(C/hi^{mi},hi)
    t1 = pair(C,hi[i])
    #calculate second pairing as e(Ai,g)
    t2 = pair(A,g)
    return t1 == t2

"""
Update commitment requires:
    C: commitment value
    oldmessage: the old message 
    newmessage: the new message to commit
    i: index of previous and new message
    hi: public parameter as g^{zi}
"""
def update(C:G1, oldmessage:int, newmessage:int,i:int,hi:list)-> G1:
    #calculate the new commitment C' as C*hi^{m'-m}
    newc = C+hi[i]**(newmessage-oldmessage)
    return newc

"""
Update proof requires:
    A: old proof
    newmessage: new message to commit
    oldmessage: old message
    i: index of old message
    j: index of new message
    h_ij: public parameter as g^{zi*zj}
"""
def updateProof(A:G1,newmessage:int,oldmessage:int,i:int,j:int,h_ij:list) -> G1:
    #calculate newproof Aj' as Aj*(hij^{m'-m})
    newproof = A+(h_ij[j][i]**(newmessage - oldmessage))
    return newproof


def main():

    dim = 1000

    group = PairingGroup('SS1024')
    g = group.random(G1)

    
    messages = []

    start_time = time.time()
    for i in range(0,dim):
        messages.append(random.randint(0,1000000))
    print("Message gen required:" + str(time.time()-start_time) + " seconds")

    start_time = time.time()
    hi,h_ij,z = keygen(g, q = dim)
    print("KeyGen required:" + str(time.time()-start_time) + " seconds")

    start_time = time.time()
    C = commit(messages,hi)
    print("Commit required:" + str(time.time()-start_time) + " seconds")

    start_time = time.time()
    A = open(0,messages,h_ij,g)
    print("Opening required:" + str(time.time()-start_time) + " seconds")

  

    start_time = time.time()
    print("Verify output:" + str(verify(C,messages[0],0,A,g,hi)))
    print("Verify required:" + str(time.time()-start_time) + " seconds")

    start_time = time.time()
    #perform new commitment at pos 0 for newmessage == 10 
    newc = update(C,messages[0],10000002,0,hi)
    print("Update commitment required:" + str(time.time()-start_time) + " seconds")
    verified2 = verify(newc,10000002,0,A,g,hi)
    if(verified2):
       print("Verifying update worked")
    else:
      print("Verifying update not worked")

    #perform another opening at pos 1
    oldproof = open(1,messages,h_ij,g)
    start_time = time.time()
    #peform an update of olderproof, to a new proof from pos 0 to 1, from old message at pos [0] to newmessage
    newproof = updateProof(oldproof,10000002,messages[0],0,1,h_ij)
    print("Update proof required:" + str(time.time()-start_time) + " seconds")

    verified3 = verify(newc,messages[1],1,newproof,g,hi)

    if(verified3):
        print("Verifying update proof worked")
    else:
        print("Verifying update proof not worked")




main()