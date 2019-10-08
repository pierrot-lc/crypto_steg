# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 16:56:50 2018

@author: pstmr
"""

import conversion_binaire as c

def read_file(chemin):
    """Lit le fichier en mode binaire et renvois la data ainsi que le nom du fichier."""
    with open(chemin, 'rb') as fichier:
        data = fichier.read()
        
    return data, fichier.name
    
def create_file(data, name):
    """Créé le fichier demandé à partir d'une data binaire.
    
    La data doit être en numérique (valeur décimale d'un octet).
    Le fichier est créé dans le répertoire courant.
    
    """
    data = bytes(data)#Convertissement des données numériques en bytes
    
    with open(name, 'wb') as fichier:
        fichier.write(data)
        
def create_wave_file(data_wave, data_sound, name):
    data = []
    for i in range(44):
        data.append(data_wave[i])
        
    for i in data_sound:
        data.append(i)
        
    
    data = bytes(data)
    
    with open(name, 'wb') as fichier:
        fichier.write(data)
        
def get_info(wave_data):
    """Retourne quelques valeurs utiles contenues dans l'encodage
    du fichier WAVE.
    Dans l'ordre :
        - nbr de canaux
        - frequence d'échantionnage
        - nbr de bits par échantillon
        
    NB : Dans un fichier WAV, les 44 premiers octets sont des bits qui donnent les paramètres du
    fichier.
    """
    val = ""
    for i in wave_data[22:24]:#Nombre de canaux
        val = c.to_binary(i, 8) + val
    nbr_canaux = c.to_decimale(val)
    
    val = ""
    for i in wave_data[24:28]:#Frequence d'échantillonage
        val = c.to_binary(i, 8) + val
    freq_ech = c.to_decimale(val)
    
    val = ""
    for i in wave_data[34:36]:#Bits par échantillonage
        val = c.to_binary(i, 8) + val
    bits_ech = c.to_decimale(val)
    
    print("Nombre de canaux :", nbr_canaux)
    print("Frequence d'échantillonnage : {} Hz".format(freq_ech))
    print("Nombre de bits par échantillon :", bits_ech)
    
    return nbr_canaux, freq_ech, bits_ech
    
def get_data(wave_data):
    """Retourne la data utile, celle qui contient les données sonores. Elles commencent à partir
    de l'octet 45."""
    return wave_data[44::]