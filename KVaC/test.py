from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, pair
from binascii import hexlify
import random
#define pairing group over SS512 ec
group1 = PairingGroup("SS512")
import time

def KeyGen() -> tuple:
    #get random generator of ZR
    #order of Zr is group1.order()
    g = group1.random(ZR)
    return (1,g)

start = time.time()
C = KeyGen()
end = time.time()

print("Key gen required: " + str((end-start)*1000) + " ms")
g= C[1]

#hash function which takes an element of ZR and return a digest which fits in ZR group
def hash2Zr(g) ->ZR:
    return group1.hash(group1.serialize(g).decode('ascii'))

#encode of a string into ZR element
def string2zr(s: str) -> ZR:
    s_int = int(hexlify(s.encode()), 16)
    return group1.init(ZR, s_int)


def Insert(C:tuple,k:int,v:int,g:ZR) -> tuple:
    #parse C as C1,C2
    c1,c2= C
    #parse Ak as ((C1,C2),(g,1,1),0)
    Ak = ((c1,c2),(g,1,1),0)
    #z<-$ H(k)
    z = hash2Zr(string2zr(str(k)))
    #first operand (C1^{z})
    first = c1**z
    #second operand (C2^{v})
    second = c2**v
    #C as (C1^{z} * C2^{v},C2^{z})
    C = (first*second,c2**z)
    return (C,Ak)

key_value = dict()

commit = list()
dim=1000
for i in range(1,dim+1):
    key_value.update({str(i):random.randint(0,100)})

start= time.time()
c3,A3 = Insert(C,k=3,v=3,g=g)

commit.append((c3,A3))
for i in range(1,dim):
    commit.append(Insert(commit[i-1][0],k=i,v=key_value.get(str(i)),g=g))
end = time.time()
print("Insert required: " + str((end-start)*1000) + " ms")

def Verifiy(C:tuple,k:int,v:int,Ak:tuple) -> tuple:
    #parse C as C1,C2
    c1,c2 = C
    #parse ak1 as first element of the first couple in AK
    ak1 = Ak[0][0]
    #parse ak2 as second element of the first couple in AK
    ak2 = Ak[0][1]
    #z<-$ H(k)
    z = hash2Zr(string2zr(str(k)))
    #first condition, assert ak2^{z} = c2
    firstcond = (ak2**z == c2)
    #second condition, assert ak1^{z} * ak2^{v} = c1
    secondcond = ((ak1**z) * (ak2**v) == c1)
    #return true if first and second condition are both true
    return (firstcond == True and secondcond == True)

start = time.time()
if Verifiy(c3,k=3,v=3,Ak=A3):
    print("Verify Worked")
else:
    print("Verify not Worked")

end = time.time()

print("Verify required: " + str((end-start)*1000) + " ms")

def ProofUpdate(k:int,Ak:tuple) -> tuple:
    #z<-$ H(k)
    z = hash2Zr(string2zr(str(k)))
    #set Ak as ((Ak1,Ak2^{z}),(Ak2,Ak3,Ak4),uk+1)
    Ak = ((Ak[0][0],(Ak[0][1]**z)),(Ak[1][0],Ak[1][1],Ak[1][2]),Ak[2]+1)
    return Ak

start = time.time()
A3 = ProofUpdate(3,A3)
end = time.time()

print("Proof update required: " + str((end-start)*1000) + " ms")

def Update(C:tuple,k:int,v:int) -> tuple:
    #parse C as C1,C2
    c1,c2= C
    #z<-$ H(k)
    z = hash2Zr(string2zr(str(k)))
    #first operand C1^{z}.
    first = c1**z
    #second operand C2^{v}
    second = c2**v
    #C as (C1^{z} * C2^{v},C2^{z})
    C = (first*second,c2**z)
    return C

start = time.time()
c3 = Update(c3,k=3,v=8)
end = time.time()

print("Update required: " + str((end-start)*1000) + " ms")

def VerifiyUpdate(C:tuple,k:int,v:int,Ak:tuple):
    #parse C as C1,C2
    c1,c2 = C
    #parse ak1 as first element of the first couple in AK
    ak1 = Ak[0][0]
    #parse ak2 as second element of the first couple in AK
    ak2 = Ak[0][1]
    #parse ak3 as first element of the second couple in AK
    ak3 = Ak[1][0]
    #parse ak4 as second element of the second couple in AK
    ak4 = Ak[1][1]
    #parse ak5 as third element of the second couple in AK
    ak5 = Ak[1][2]
    #z<-$ H(k)
    z = hash2Zr(string2zr(str(k)))
    #parse uk as first element of the third couple in AK
    uk = Ak[2]
    #first condition assert ak2^{z} = c2
    firstcond = (ak2**z == c2)
    #set temp as ak1^{z}
    temp = (ak1**z)

    #perform exponentiations as described in the paper, avoiding "double" exponent
    for i in range(1,uk+1):
        temp = temp**z  
    #first condition assert ak1^{z^(uk+1)} * ak2^{v} = c1
    secondcond = ((temp) * (ak2**v) == c1)
    #set temp as ak3^{z}
    temp = (ak3**z)
    #perform exponentiations as described in the paper, avoiding "double" exponent
    for i in range(1,uk+1):
        temp = temp**z
    #third condition assert ak3^{z^(uk+1)}    
    thirdcond = ((temp) == c2)
    #fourth condition assert ak3^{z} * ak3^{ak5} = g
    fourthcond = ((ak4**z)*(ak3**ak5) == g) 
    #return true if first, second, third and fourth condition are all true
    return (firstcond == True and secondcond == True
            and thirdcond == True and fourthcond == True)

start = time.time()
if VerifiyUpdate(c3,k=3,v=11,Ak=A3):
    print("Update Worked")
else:
    print("Update not Worked")

end = time.time()

print("Verifiy update required: " + str((end-start)*1000) + " ms")