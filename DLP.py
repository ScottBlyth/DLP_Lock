
import gmpy2
import math
import random
import time
from nprime import miller_rabin

# altered baby step giant step DLP where every kth a^{i*k} is computed, to reduce memory usage
# can hasten unlock time by using faster language/algorithm 
def dlp(a,b,n, k): 
    m = math.ceil(n**(1/2))
    a_inv = gmpy2.invert(a, n)   
    a_m_inv = gmpy2.powmod(a_inv, m, n)

    pow_mod_a_m_i = [None]*k
    a_m_inv_r = 1
    for i in range(k):
        pow_mod_a_m_i[i] = a_m_inv_r
        a_m_inv_r = (a_m_inv*a_m_inv_r)%n
        
    values = {}
    current = 1 
    values[1] = 0 # a^0
    a_m_k = gmpy2.powmod(a,m*k,n)
    for i in range(1,m//k+k):
        current = (a_m_k*current)%n # a^(i*k*m)
        values[current] = i*k
    current = 1
    for j in range(m+2):
        right = (b*current)%n
        for r in range(k):
            val = (right*pow_mod_a_m_i[r])%n
            if val in values:
                i = values[val]+r
                return i*m+j
        current = (a_inv * current)%n
    raise Exception("logarithm does not exist")

def generate_prime_candidate(lower, upper): 
    # primes greater than 3 are 
    # in the form 6*k-1 or 6*k+1 
    # so no need to generate primes in other forms
    
    # generate prime of from 6k+1 
    if random.randint(0,1) == 0: 
        # l <= 6k+1 <= u
        # -> (l-1)/6 <= k <= (u-1)/6
        # -> floor((l-1)/6) <= k <= ceil((u-1)/6)
        l = (lower-1)//6
        u = (upper-1)//6 + 1 
        return 6*random.randint(l, u)+1
    # l <= 6k-1 <= u
    # -> (l+1)/6 <= k <= (u+1)/6
    # -> floor((l+1)/6) <= k <= ceil((u+1)/6)
    l = (lower+1)//6
    u = (upper+1)//6 + 1
    return 6*random.randint(l, u) - 1



def is_sophie_germain(n):
    return miller_rabin(n) and miller_rabin(2*n+1)
    
def generate_sophie_prime(n):
    random.seed(time.time())
    lower,upper = 1<<n, (1<<(n+1))-1
    current = 6*random.randint(lower,upper)+1
    while not is_sophie_germain(current):
        current =generate_prime_candidate(lower,upper)
    return 2*current+1

def is_generator(g, sophie_prime):
    # factors are 2, (sophie_prime-1)/2 
    # psi(sophie_prime) = sophie_prime-1
    if (g*g)%sophie_prime == 1:
        return False
    return gmpy2.powmod(g, (sophie_prime-1)//2, sophie_prime) != 1
    
    
def generate_pk_key(n):
    prime = generate_sophie_prime(n)
    # find generator
    g = 2
    while not is_generator(g, prime):
        g = random.randint(2, n-1) 
    return (g,prime)

def hide_combination(combination, n, g): 
    prime = generate_sophie_prime(n)
    seed_l = prime.bit_length()-combination.bit_length()-5
    seed = random.randint(1<<(seed_l-1), 1<<seed_l)
    d = len(str(seed))
    number = int(str(combination)+str(seed))
    return int(gmpy2.powmod(g, number, prime)), g, prime,d
