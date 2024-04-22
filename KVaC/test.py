"""from charm.toolbox.integergroup import IntegerGroup
from hashlib import sha256
group1 = IntegerGroup()
group1.paramgen(1024)
g = group1.randomGen()
x = 10232343
hash = int.from_bytes(sha256(str(x).encode('utf-8')).digest(), 'big')
print(hash)
print(g)

C = (12,24)

c1,c2 = C
print(c1)
print(c2)"""


from charm.toolbox.integergroup import IntegerGroup
from Crypto.Random import random

def KeyGen():
    group1 = IntegerGroup()
    group1.paramgen(10)
    g = group1.randomGen()
    return (1,g)

C = KeyGen()
g = C[1]





from hashlib import sha256
def Insert(C:tuple,k:int,v:int,g:int):
    c1,c2= C
    Ak = ((c1,c2),(g,1,1),0)
    z = int.from_bytes(sha256(str(k).encode('utf-8')).digest(), 'big')
    first = c1**z
    second = c2**v
    C = (first*int(second),int(c2**z))
    return (C,Ak)


c3,A3= Insert(C,k=3,v=5,g=g)

#c4,A4 = Insert(c3,k=4,v=6,g=g)

def Verifiy(C:tuple,k:int,v:int,Ak:tuple):
    c1,c2 = C
    z = int.from_bytes(sha256(str(k).encode('utf-8')).digest(), 'big')
    ak1 = Ak[0][0]
    ak2 = Ak[0][1]
    uk = Ak[2]
    firstcond = (ak2**z == c2)
    secondcond = (((ak1**z)**(uk+1)) * int((ak2**v)) == c1)
    return firstcond == secondcond


if Verifiy(c3,k=3,v=5,Ak=A3):
    print("Verify Worked")
else:
    print("Verify not Worked")