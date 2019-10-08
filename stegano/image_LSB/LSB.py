# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 20:11:43 2017

@author: pstmr

Module ayant les fonctions qui sont utiles pour utiliser la technique du LSB sur une image.
"""

def put_LSB(data_cover, data_in, bit_start=0):
    """Ajoute dans data_cover la data_in
    
    Le data_cover doit être donner en 'RGB' et converti en bits.
    Le data_in doit être uniquement un tableau de bits à rentrer dans le data_cover.
    Paramètre optionnel:
    -bit_start=0 -- Permet de définir un bit sur lequel commencer à placer la data_in dans data_cover
    
    """
    for i in range(bit_start, len(data_in) + bit_start):
        pixel = int(i/3)
        canal = i%3
        data_cover[pixel][canal] = data_cover[pixel][canal][:-1] + data_in[i - bit_start]
    return data_cover

def get_LSB(data_cover, nbr_bits=-1, bit_start=0):
    """ Récupère la data caché dans les LSB du data_cover.
    
    La data_cover doit être un tableau de pixels 'RGB' déjà converti en bits
    Paramètres optionnels :
    -nbr_bits=-1 -- Permet d'indiquer combien de bits doit récupérer le programme. Si il n'a pas été changé,
    alors le programme lit tout le tableau data_cover.
    -bit_start=0 -- Permet de donner un bit sur lequel commencer à récupérer la data.
    
    """
    data = list()
    
    if nbr_bits == -1:
        nbr_bits = len(data_cover) * 3#Si le nbr_bits n'as pas été changé alors on prends par défaut tout le tableau data_cover

    for i in range(bit_start, nbr_bits + bit_start):
        pixel = int(i/3)
        canal = i%3
        data.append(data_cover[pixel][canal][7])#Récupère le LSB
    return data