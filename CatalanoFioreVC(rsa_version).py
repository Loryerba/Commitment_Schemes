from Crypto.Util import number
from Crypto.Random import random
import time
from functools import reduce
import operator
import sys
start_time = time.time()

#global public parameters
N: int
g: int
si_set : set
ei_prime_set : set


def keyGen(k : int,l : int, q : int):
    """k correspond to security parameter, must larger than 1
        l correspond to length of q (l+1)-bit random primes and q is the number of primes e1,...,eq"""
    #first prime number
    p1 = 0
    #second prime number
    p2 = 0
    #generating two distinct  k/2-bit primes number
    while(p1 == p2):
        p1 = number.getPrime(int(k/2))
        p2 = number.getPrime(int(k/2))
    #evaluate N = p1*p2
    N: int = 0
    N = p1*p2
    
    #set of q l(+1)-bit primes since e1,....,eq do not divide for N
    ei_primes_set = set()

    while(0 <= len(ei_primes_set) < q):
        #we can use := inside larger expression like if statement since Python 3.8
        if((ei := number.getPrime(l+1)) % N != 0):
            ei_primes_set.add(ei)
    

    
    si_set = set()
    
    #private function for calcutating generator of cyclic group Zn which has N-order 
    def __get_generator(order: int):
        s = set(range(1,order))
        for g_element in s:
            element_generated = set()
            for i in s:
                element_generated.add((g_element**i)%order)
            if element_generated == s:
                return g_element

        
    #get first generator of Zn
    #g: int = __get_generator(N)
    g: int = random.randrange(1,N)
    #evaluate Si value 
    for i in range(0,q):
        ei_primes_list = list(ei_primes_set)
        ei_primes_list.pop(i)
        si_set.add(g**reduce(operator.mul,ei_primes_list))
        
           
        
    
    return N,g,si_set,ei_primes_set


#committing procedure. Return the commitment value C and aux information (message:list)

def com(message : list):

    C = 1
    for i in si_set:
        C *= si_set[i]**int.from_bytes(message[i].encode(),sys.byteorder)
    return C


#opening procedure
def open(m:str,i:int,aux:list):
    
    prod = 1
    #evaluating product of series
    for j in len(si_set):
        if(j != i):
            prod *= (si_set[j]**int.from_bytes(aux[j].encode(),sys.byteorder)) % N
    #evaluating proof 
    return prod**(1/ei_prime_set[i])



#verify procedure
def vrfy(C: int, m: str, i: int, proof):
    if (C == ((si_set[i]**int.from_bytes(m.encode(),sys.byteorder))*(proof**ei_prime_set[i]) % N)):
        return True
    else:
        return False




#getting pubblic parameter pp such as (N,g,si_set,ei_set)
(N,g,si_set,ei_prime_set) = keyGen(k=12,l=8,q=2)

#message space is {0,1}^l, e.g if l = 1024 bit or 1 KByte and a string is made of 1 byte for 1 character, we can store onlye 128 character


out = "Terminated in {} ms"
print(out.format(time.time() - start_time))


