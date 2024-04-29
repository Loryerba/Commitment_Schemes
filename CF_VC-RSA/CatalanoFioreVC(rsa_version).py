import math
from Crypto.Util import number
import copy
import random
import time 

#verify fun
def verify(C:int, message:int, i:int, open:int, S:list, ei_list:list, n:int) -> bool:

    #evaluate proof^ei-th % n
    proofToEi =pow(open, ei_list[i], n)
    #evaluate si-th^message * (proofToEi)
    newC = proofToEi*pow(S[i], message, n)%n

    #returns 1 if two commitment are equals, else 0
    if(C == newC):
        return 1
    else:
        return 0

#opening fun
def open(messages:list, ei_list:list, a:int, n:int, i:int) -> int:

    #creating deepcopied list of ei_list primes
    newlist = copy.deepcopy(ei_list)
    #remove ei-th primes from list
    newlist.remove(ei_list[i])
    #recalculation of Si elements without ei-th prime number
    newsi_list = evaluate_Si( newlist, a, n)
    #set prod to neutral element 1
    prod = 1

    counter = 0
    for j in range(len(newsi_list)): 
        #if ei-th random primes is at index i, skip (one S value is gone)
        if(counter == i):
            counter += 1
        #evaluate opening value
        prod = (prod*pow(newsi_list[j], messages[counter], n))%n
        #next message pointer
        counter += 1

    return prod

#commit fun
def commit(messages:list, S:list, n:int) -> int:
    #set neutral element c = 1
    c = 1
    for i in range(len(messages)):
        #set c = s1^m1*...*sq^mq
        c = (c*pow(S[i], messages[i], n))%n
    return c


#divide et impera method
def evaluate_Si(primes:list, a:int, n:int) -> list: 
    num = len(primes)
    if num == 1:
        return [a]

    a1 = []
    a2 = []

    partial_a1 = a
    partial_a2 = a

    #for each primes number append a^primes[i] mod n
    for i in range(math.floor(len(primes)/2)):
        partial_a2 = pow(partial_a2, primes[i], n)
        a1.append(primes[i])
    #for each primes number append a^primes[i] mod n
    for i in range(math.floor(len(primes)/2), len(primes)):
        partial_a1 = pow(partial_a1, primes[i], n)
        a2.append(primes[i])

    #recursive call to self fun
    l1 = evaluate_Si(a1, partial_a1, n)
    l2 = evaluate_Si(a2, partial_a2, n)

    si_list = []
    for element in l1:
        si_list.append(element)
    for element in l2:
        si_list.append(element)

    return si_list

def keyGen(k:int,qlen:int, l:int) -> tuple:
    #generation of two k/2-bit primes p and q
    p =number.getPrime(math.floor(k/2))
    q = number.getPrime(math.floor(k/2))
    #set n = p*q (rsa)
    n = p*q
    #fix a=5 random value
    a = 5


    
    #list of l+1-bit q random primes
    random_primes = []
    while True:
        #temporary prime
        tmp = number.getPrime(l + 1)
        #boolean variable to check if prime number is already used
        alreadyUsed = False
        #foreach to check duplicate
        for num in random_primes:
            if tmp == num:
                alreadyUsed = True
        if alreadyUsed:
            continue
        #add prime number if is not duplicated
        random_primes.append(tmp)
        #check if are generated q primes 
        if len(random_primes) == qlen:
            break
    
    #call fun to evaluate Si element
    si_list = evaluate_Si(random_primes, a, n)
    return n, random_primes, a, si_list


#comute commitment update
def update(C: int, m:int, new_m:int,i:int,si_list:list,n:int) -> int:
    new_c = 1
    b = pow(si_list[i],(new_m-m),n)
    new_c = (C * b) % n
    return new_c


def updateProof(oldProof: int, e:list, oldm: int, newm: int, a:int, i:int, j:int, n:int) -> int:
    alt = a
    for k in range(len(e)):
        if(k == i or k == j):
            continue
        alt = pow(alt, e[k], n)

    rootS = alt
    right = pow(rootS, newm - oldm, n)
    full = (oldProof*right)%n
    return full
     
        
  

    


def main():

    dim = 100
    messages = [random.randint(0,100) for i in range(0,dim)]

    
    start_time = time.time()
    n, ei_list, a, si_list = keyGen(k=1024,qlen= len(messages),l=25)
    print("Generation messages required: " + str(time.time()-start_time) + " seconds")

    start_time = time.time()
    c = commit(messages, si_list, n)
    print("Commitment required:" + str(time.time()-start_time)  + " seconds")

    start_time = time.time()
    proof = open(messages, ei_list, a, n, 0)
    print("Generation proof required: " + str(time.time()-start_time) + " seconds")
    #later use (opening at pos 1)
    oldProof = open(messages, ei_list, a, n, 1) 
    

    start_time = time.time()
    verified = verify(c, messages[0], 0, proof, si_list, ei_list, n)
    print("Verify proof required: " + str(time.time()-start_time) + " seconds")
    if(verified):
        print("Verifying worked")
    else:
        print("Verifying not worked")


    newmessage = random.randint(1,12234567) #random new message, update position 0
    start_time = time.time()
    newC = update(c,messages[0],newmessage,0,si_list,n)
    print("Update commitment required: " + str(time.time()-start_time) + " seconds")


    verified2 = verify(newC, newmessage, 0, proof, si_list, ei_list, n)
    if(verified2):
       print("Verifying update worked")
    else:
      print("Verifying update not worked")


    start_time = time.time()
    #update proof at pos j (newC is the updated commitment)
    newProof = updateProof(oldProof, ei_list, messages[0], newmessage, a, 0, 1, n)
    print("Update proof required: " + str(time.time()-start_time) + " seconds")
    verified3 = verify(newC, messages[1], 1, newProof, si_list, ei_list, n)
    if(verified3):
        print("Verifying update proof worked")
    else:
        print("Verifying update proof not worked")

    #sanity check for previous proof

    verified4 = verify(newC,messages[1],1,oldProof,si_list,ei_list,n)

    if(verified4):
        print("Old proof still works")
    else:
        print("Old proof no longer works")

main()