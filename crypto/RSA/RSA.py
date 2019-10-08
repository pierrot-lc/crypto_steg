# -*- coding: utf-8 -*-
"""
Created on Sun May 14 17:30:51 2017

@author: pstmr
The RSA algorithm, used to encryp and decrypt with a private and a public key.
"""

from secrets import randbits

from euclide import gcd, extended_euclidean
import prime_numbers

def create_keys():
    """Create the keys used by the RSA model. Public key is given first, and
    the private key is given in second.
    
    Note that :
     - the private key is the tuple (U, N)
     - public key is the tuple (N, C)
    
    """
    P = prime_numbers.found_prime(2)
    P, Q = P[0], P[1]

    N = P * Q
    M = (P - 1)*(Q - 1)
    
    C = randbits(8)
    while gcd(M, C) != 1:
        C = randbits(8)
        
    R, U, V = extended_euclidean(C, M, rsa=True)
    
    return ((N, C), (U, N))
    
def encrypt(msg, public_key):
    """Encrypt the message using the RSA algorithm.
    
    msg must be a string or an array full of characters.
    public_key must be the couple (N, C).
    """
    crypted_msg = []
    N, C = public_key[0], public_key[1]

    for char in msg:
        char = ord(char)
        char = char**C
        char = char%N
        crypted_msg.append(char)
        
    return crypted_msg

def decrypt(crypted_msg, private_key):
    """Decrypt the message using the RSA algorithm.
    
    crypted_msg must be an array full of integers.
    private_key must be the couple (U, N).
    """
    msg = ""
    U, N = private_key[0], private_key[1]
    
    for num in crypted_msg:
        num = num**U
        num = num%N
        msg += chr(num)
        
    return msg