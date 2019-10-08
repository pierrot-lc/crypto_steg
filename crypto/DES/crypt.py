# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 20:18:47 2017

@author: pstmr

Module qui possède des fonctions utiles pour du cryptage.

"""

from conversion_binaire import to_binary, to_decimale

def XOR(b1, b2):
    """Renvoi b1 XOR b2.
    
    b1 et b2 doivent être des strings de bits.
    
    """
    result = ""
    
    for i in range(len(b1)):
        if (b1[i] == '1' and b2[i] == '0') or (b1[i] == '0' and b2[i] == '1'):#Si une des deux cases seulement vaut 1 alors on ajoute 1
            result += '1'
        else:
            result += '0'
            
    return result
    
def read_file(chemin):
    """Lit un fichier en byte. Renvoi la data et le nom du fichier."""
    with open(chemin, 'rb') as fichier:
        data = fichier.read()
    
    return data, fichier.name
    
def create_file(data, name):
    """Créé le fichier à partir d'une data sous forme de données numériques (8bits en base 10)."""
    data = bytes(data)#Convertissement des données numériques en bytes
    
    with open(name, 'wb') as fichier:
        fichier.write(data)
        
def save_key(key):
    """Sauvegarde la clef donnée dans un fichier nommé 'key.txt'."""
    with open("key.txt", 'w') as fichier:
        fichier.write(str(key))
        
def convert_bytes_to_bits(data):
    """Renvoi une liste de bits réunis dans une seule string."""
    n_data = ""
    for i in range(len(data)):
        n_data += to_binary(data[i], 8)
        
    return n_data
        
def convert_bits_to_bytes(data):
    """Regroupe les bits en paquet de bytes (8-bits) et donne l'équivalent en décimal."""
    n_data = list()
    byte = ""
    for i in range(len(data)):
        byte += data[i]
        if len(byte) == 8:
            n_data.append(to_decimale(byte))
            byte = ""
    
    return n_data
        
def convert_bits_to_bloc(bits, taille):
    """Renvois une tableau de blocs de la taille demandée, ainsi que le reste si len(bits)%taille != 0.
    
    Si le reste est nul, alors la deuxième valeur renvoyée vaut "".
    
    """
    bloc = ""
    n_data = []

    for i in range(len(bits)):
        bloc += bits[i]
        if len(bloc) == taille:
            n_data.append(bloc)
            bloc = ""
    return n_data, bloc#Retourne les blocs + le reste (si la taille%len(bits) != 0)
    
def convert_key_to_ASCII(key):
    key = convert_bits_to_bytes(key)
    n_key = ""
    for i in key:
        n_key += chr(i)
        
    return n_key
    
def convert_ASCII_to_key(key):
    n_key = ""
    for i in key:
        n_key += to_binary(ord(i), 8)
        
    return n_key