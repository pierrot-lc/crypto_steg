# -*- coding: utf-8 -*-
"""
Created on Mon May 15 22:41:25 2017

@author: pstmr
This module allows the user to get a list of prime numbers.
Note that they are saved on a file (prime.txt).
"""

import os
from math import log, sqrt
from secrets import randbits

list_prime = []

def next_prime(num):
    """Check the next 'num' numbers, and add all the primes to the array."""
    cur = list_prime[-1]
    for i in range(cur + 1, cur + num + 1):
        divisor = False
        max_divisor = sqrt(i)#Numbers above it can't be prime factors
        for j in list_prime:
            if i%j == 0:
                divisor = True
                break
            if j > max_divisor:
                break
                
        if not divisor:
            list_prime.append(i)
            
def len_primes(len_list):
    """Check the next primes until the list is at the len given."""
    a = len(list_prime)
    cur = list_prime[-1] + 1
    print(a)
    while a < len_list:
        divisor = False
        max_divisor = sqrt(cur)#Numbers above it can't be prime factors
        for j in list_prime:
            if cur%j == 0:
                divisor = True
                break
            if j > max_divisor:
                break
                
        if not divisor:
            list_prime.append(cur)
            a += 1
        cur += 1
        
def save_prime(last_number):
    """Add to the "prime.txt" all the primes after the last_number in the array of primes."""
    index = 0
    for i in range(len(list_prime)):#Check where is the prime in the array
        if list_prime[i] == last_number:
            index = i
    
    with open("prime.txt", 'a') as file:#Append mode
        for i in range(index + 1, len(list_prime)):#Write all primes at the end of the file
            file.write(" {}".format(list_prime[i]))
            
def read_prime():
    """Read the "prime.txt" file and save all the primes in the array 'list_prime'."""
    with open("prime.txt", 'r') as file:
        content = file.read()
        content = content.split(" ")
        
        for num in content:
            list_prime.append(int(num))
            
def found_prime(how_much):
    """Return an array full of randomly taken primes. The length of the array
    is given by the parameter 'how_much'."""
    read_prime()#To make sure the array is up-to-date
    len_prime = len(list_prime)
    len_bits = int(log(len_prime, 2)) + 1#Represent the number of bits needed to write len_prime
    
    primes = []

    for i in range(how_much):    
        place = len_prime
        while place >= len_prime:
            place = randbits(len_bits)#Return a random number writen with 'len_bits' bits
            
        primes.append(list_prime[place])
        
    return primes


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    read_prime()
    last_number = list_prime[-1]
    print("How many numbers do you want to test ? (current max prime is {})".format(last_number), end='')
    num = int(input("> "))
    next_prime(num)
    save_prime(last_number)