# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 16:43:41 2018

@author: pstmr
"""

import read_wave_file as r
import conversion_binaire as c

def LSB_encrypt(data_bits, data_octet):
    """Les bits représentent la donnée à cacher dans les octets.
    Tout ceci en utilisant la technique des LSB."""
    
    if len(data_bits) > len(data_octet):
        print("Erreur, la taille de data_octet est trop petite.")
        return False
        
    data_LSB = []
    for i in range(len(data_bits)):
        o = data_octet[i]
        b = data_bits[i]

        if o%2 == 1:
            o -= 1#Enlève le LSB de l'octet (le fixe à 0)
        
        data_LSB.append(o+b)#Ajoute le LSB en fonction de la valeur du bit
    
    for i in range(len(data_bits), len(data_octet)):
        data_LSB.append(data_octet[i])#Complète les octets restants par leurs valeurs exacte

    return data_LSB
    
    
def LSB_decrypt(data_LSB, nbr_mots=-1):
    """Récupère les LSB contenus dans la data_LSB. Possibilité de demandé un certain nombre d'octets."""
    bits = []
    for i in data_LSB:
        bits.append(i%2)#Récupère le LSB
        if len(bits) >= nbr_mots * 8 and nbr_mots != -1:
            return bits
        
    return bits
    
def from_oct_to_bit(octets):
    bits = []
    for i in octets:
        word = c.to_binary(i, 8)
        for b in word:
            bits.append(int(b))
            
    return bits
    
def from_bit_to_oct(bits):
    octets = []
    for i in range(len(bits)//8):
        word = ""
        for j in bits[i*8 : (i+1)*8]:
            word += str(j)
            
        octets.append(c.to_decimale(word))
        
    return octets
    
def encrypt(wav_file, data_file, name):
    """Créé un nouveau fichier WAVE avec la data_file dans les LSB."""
    print("Lecture du fichier son...")
    wave_data, name_file = r.read_file(wav_file)
    sound_data = r.get_data(wave_data)
    print("Lecture du fichier de données...")
    file_data, n = r.read_file(data_file)
    file_data = from_oct_to_bit(file_data)
    
    print("Application de la méthode des LSB...")
    sound_data = LSB_encrypt(file_data, sound_data)
    print("Création du fichier {}...".format(name))
    r.create_wave_file(wave_data, sound_data, name)
    
def decrypt(wav_file, name, nbr_caract=-1):
    print("Lecture du fichier son...")
    wave_data, name_file = r.read_file(wav_file)
    sound_data = r.get_data(wave_data)
    print("Récupèration des LSB...")
    file_data = LSB_decrypt(sound_data, nbr_caract)
    file_data = from_bit_to_oct(file_data)
    
    print("Création du fichier {}...".format(name))
    r.create_file(file_data, name)