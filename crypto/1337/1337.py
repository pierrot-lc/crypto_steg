# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 23:23:47 2017

@author: pstmr
"""
from random import randint

def create_dic():
    tab = {}
    chemin = '1337.txt'
    
    with open(chemin, 'r') as fichier:
        for ligne in fichier:
            ligne = ligne.split('\t')
            ligne[1] = ligne[1][:-1]
            tab[ligne[0]] = ligne[1].split(' or ')
            
    return tab
    
def random_case(tab):
    return tab[randint(0, len(tab)-1)]
    
def t0_1337(string, random=True):
    value = ""
    for char in string:
        try:
            if random:
                value += random_case(dic[char.upper()])
            else:
                value += dic[char.upper()][0]
        except KeyError:
            value += char
    return value
    
def to_ascii(string):
    value = ""
    for char in string:
        cle = find_cle(char)
        if cle != None:
            value += cle
        else:
            value += char
    return value
        
def find_cle(item):
    tab = []
    for cle in dic:
        if item in dic[cle]:
            tab.append(cle)
    if tab == []:
        return None
    return tab[randint(0, len(tab)-1)]
    
dic = create_dic()