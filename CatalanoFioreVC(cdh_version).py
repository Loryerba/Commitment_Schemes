from ecpy import ExtendedFiniteField,EllipticCurve, FiniteField, gcd, modinv, tate_pairing
from ecpy import EllipticCurveRepository
import random

#Generazione della curva ellittica secp256k1
#field == Campo finito su cui è definita la curva
#ec == Curva ellittica corrispondente a secp256k1
#generator == Generatore della curva
#prime_order == ordine primo del gruppo G
field ,ec,generator,prime_order = EllipticCurveRepository('secp256k1')


#keyGen (q=>quantità di numeri da generare randomicamente da Zp, corrisponde al numero di elementi nel vector) 
#=> restituisce in output h1 (insieme di g^zi), h2 (matrice di g^zi*zj), z (insieme di numeri) generati da [0,Zp]
def keygen(q):
    z=[]
    #generazione di q elementi estratti casualmente da Zp
    for i in range(q):
       z.append(random.randint(0,50))
    h1 = []
    #generazione di tutti gli elementi basati su g^zi
    for i in range(len(z)):
        h1.append(generator.__mul__(z[i]))
    h2 = []
    #generazione della matrice hij, dove per ogni cella ij con i!=j calcola g^(zi*zj)
    for i in range(len(z)):
        h2.append([])
        for j in range(len(z)):
            if(i == j):
                h2[i].append(0)
                continue
            h2[i].append(generator.__mul__(z[i]*z[j]))
    return h1, h2, z

#commit (messages=> lista dei messaggi di cui fare il commit, h1=>(insieme di g^zi))
#=>restituisce in output il commitment calcolato
def commit(messages, h1):
    #commitment value vuoto (0:1:0)
    C = h1[0].__mul__(0)
    #per ogni elemento presente nel messaggio
    for i in range(len(messages)):
        #calcolo di h1^m1 * .... *hq^mq
        #in EC il * si traduce in +, e ** si traduce in *
        C = C.__add__(h1[i].__mul__(messages[i]))
    return C

#open (message=> messaggio di cui fare l'opening, i => posizione nel vector, h2 => matrice hij, g => generatore)
#=> restituisce in output l'opening alla posizione i
def open(message, i, messages, h2, g):
    #opening vuoto (0:1:0)
    A = generator.__mul__(0)
    #per ogni elemento nel messaggio
    for j in range(len(messages)):
        if(i==j):
            continue
        #opening calcolato come hij^mj in produttoria da j=1 a j=q
        A = A.__add__(h2[i][j].__mul__(messages[j]))
    return A

#opening equivalente a open (sopra)
def open2(messages,i,h1,z):
    A = generator.__mul__(0)
    for j in range(len(messages)):
        if(i==j):
            continue
        A = A.__add__(h1[i].__mul__(messages[j]*z[j]))
    
    return A

#verify della opening A su commit C alla posizione i del messaggio message.
#(C=> commitment value, message=>messaggio su cui fare la verifica, i=>posizione su cui fare la verifica, A=>opening value, g=>generatore, h1=>lista di g^zi)
#restituisce true se entrambi i pairing restituiscono lo stesso valore, false altrimenti
def verify(C, message, i, A, g, h1):
    
    denominatore = h1[i].__mul__(message)
    #calcolo di C/denom come C-denom
    C = C.__sub__(denominatore)
    
    t1 = tate_pairing(ec,C,h1[i],prime_order)
    t2 = tate_pairing(ec,A,g,prime_order)
    print(t1)
    print(t2)
    return t1 == t2


def main():
    h1,h2,z = keygen(q=3)
    messages = [1,2,3]
    C = commit(messages,h1)    
    A = open(messages[0],0,messages,h2,generator)
    A2 = open2(messages,0,h1,z)

    #controllo se le due opening sono effettivamente equivalenti
    print(A == A2)
    
    #metodo nel main grezzo per controllare se il metodo __sub__ effettua correttamente la sottrazione (FUNZIONA)
    """comm = h1[1].__mul__(0)
    for i in range(1,len(messages)):
        comm = comm.__add__(h1[i].__mul__(messages[i]))
    
    C = C.__sub__(h1[0].__mul__(messages[0]))

    print(comm == C)"""

    
    if(verify(C, messages[0], 0, A, generator, h1)):
        print("verified")
    else:
       print("not verified")
   
main()


