from Crypto.Util import number
import time
from functools import reduce
import operator
start_time = time.time()

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
    g: int = __get_generator(N)
    #evaluate Si value 
    for i in range(0,q):
        ei_primes_list = list(ei_primes_set)
        si_set.add(g**reduce(operator.mul,ei_primes_list.pop(i)))
        
           
        
    
    return p1,p2 #return a tuple


(p1,p2) = keyGen(k=1028,l=1023,q=10)
output_primes = "First prime: {} and second prime: {}. Terminated in {} ms"
print(output_primes.format(p1,p2,time.time() - start_time))


