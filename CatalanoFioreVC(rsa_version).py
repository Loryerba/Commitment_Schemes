import math
from Crypto.Util import number
import copy

#verify fun
def verify(C, message, i, open, S, ei_list, n):

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
def open(messages, ei_list, a, n, i):

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
def commit(messages, S, n):
    #set neutral element c = 1
    c = 1
    for i in range(len(messages)):
        #set c = s1^m1*...*sq^mq
        c = (c*pow(S[i], messages[i], n))%n
    return c


#divide et impera method
def evaluate_Si(primes, a, n): 
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

def keyGen(k,qlen, l):
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


def main():
    messages = [1234, 5678, 9101112] 

    n, ei_list, a, si_list = keyGen(k=2048,qlen= len(messages),l=25)

    c = commit(messages, si_list, n)

    proof = open(messages, ei_list, a, n, 0)
    verified = verify(c, messages[0], 0, proof, si_list, ei_list, n)
    if(verified):
        print("Verifying worked")
    else:
        print("Verifying not worked")




main()