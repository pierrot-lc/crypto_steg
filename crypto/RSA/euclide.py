# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 13:16:46 2017

@author: pstmr

Module that can calcul the gcd of 2 numbers and use the Extended Euclidean algorithm
"""

def gcd(a, b):
    """Return the gcd of (a, b)"""
    if b > a:#The program consider that a > b
        b, a = a, b
    
    r = a%b
    if r == 0:
        return b
    else:
        return gcd(b, r)
        
def extended_euclidean(a, b, rsa=False):
    """Found a couple (u, v) so that a*u + v*b = gcd(a, b)."""
    reverse = False
    if b > a:
        b, a = a, b
        reverse = True
        
    r0, r1, u0, u1, v0, v1 = a, b, 1, 0, 0, 1
    while r1 != 0:
        r = int(r0/r1)
        r0, r1 = r1, r0 - r*r1
        u0, u1 = u1, u0 - r*u1
        v0, v1 = v1, v0 - r*v1
        
    if reverse:
        u0, v0 = v0, u0
        a, b = b, a
        
    if rsa:
        i = 1
        while u0 < 2:
            u0 += i*b
            v0 -= i*a
            
        while u0 > b:
            u0 -= i*b
            v0 -= i*a
        
    return r0, u0, v0