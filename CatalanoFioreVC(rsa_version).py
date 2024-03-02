from Crypto.Util import number
from Crypto.Random import random
import time
from functools import reduce
import operator
import sys
from sympy.ntheory import totient
from sympy.polys.polytools import gcd
from egcd import egcd


sys.set_int_max_str_digits(0)
start_time = time.time()

#global public parameters
N: int
g: int
si: list
ei : list 


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
    ei_primes_list = list ()
    
    N_totient = totient(N)
    while(0 <= len(ei_primes_list) < q):
        #we can use := inside larger expression like if statement since Python 3.8
        if(N_totient % (ei := number.getPrime(l+1))  != 0):
            ei_primes_list.append(ei)
    
    si_list = list()
    
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
        ei_primes_list_copy = list(ei_primes_list)
        ei_primes_list_copy.pop(i)
        si_list.append(g**reduce(operator.mul,ei_primes_list_copy))
        
           
        
    
    return N,g,si_list,ei_primes_list


#committing procedure. Return the commitment value C and aux information (message:list)

def com(message : list):

    C : int = 1
    for i in range(0,len(si)):
        C = C * (si[i]**int.from_bytes(message[i].encode(),sys.byteorder))
    return C


#opening procedure
def open(m:str,i:int,aux:list):

    
    #evaluate moduler ethroot of message
    def __ethRoot(e: int, message: int, m: int):
        m_totient = totient(m)
        if(gcd(e,m_totient) == 1 and gcd(message,m) ==1):
            (gcd_,t,s) = egcd(e,m_totient)
            power = message ** t
            remainder = power % m
            if((remainder**e)%m == (message%m)):
                return remainder
            else:
                return -1

        else:
            return -1


    
    prod = 1
    #evaluating product of series
    for j in range(0,len(si)):
        if(j != i):
            prod *= (si[j]**int.from_bytes(aux[j].encode(),sys.byteorder))
    #evaluating product's root

    if((remainder:= __ethRoot(ei[i],prod,N)) == -1):
        print("Error while evaluating eth root")
    else:
        return remainder


#verify procedu1re
def vrfy(C: int, m: str, i: int, proof):
    #evaluate si^m
    firstvalue = ((si[i]**int.from_bytes(m.encode(),sys.byteorder))) 

    #evaluate si^m * proof^ei
    productvalue = firstvalue * (proof**ei[i])

    #evalue product mod N
    modulevalue = productvalue%(N)
    #check if commitmentvalue == commitment_evaluated
    if (C == modulevalue):
        return True
    else:
        return False



#message space is {0,1}^l, e.g if l = 1024 bit or 1 KByte and a string is made of 1 byte for 1 character, we can store onlye 128 character
#getting pubblic parameter pp such as (N,g,si_list,ei_set)
(N,g,si,ei) = keyGen(k=6,l=8,q=2)
commitment_value = com(message=["1","2","3"])
print("Commitment value: " + str(commitment_value))
proof = open("1",1,aux = ["1","2","3"])
print("Proof value: " + str(proof))
print("Verfying output: " + str(vrfy(commitment_value,"1",1,proof)))
out = "Terminated in {} ms"
print(out.format(time.time() - start_time))

