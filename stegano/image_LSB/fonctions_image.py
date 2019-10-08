# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 23:07:28 2017

@author: pstmr

Module contentant des fonctions utiles pour traiter des images.
"""

from PIL import Image

from conversion_binaire import to_binary, to_decimale

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

def get_dir(full_path):
    """Renvoie le chemin du dossier où est situé l'image."""
    i = len(full_path) - 1
    while full_path[i] != '\\':
        i -= 1
        
    return full_path[:i+1]

def get_image(chemin):
    """Récupère l'image du chemin donné."""
    im = Image.open(chemin)
    
    return im
    
def convert_grey(image):
    """Permet de convertir une image en couleur en gris.
    
    Le gris taux de gris est obtenu en faisant la moyenne des intensités des trois couleurs du pixel.
    
    """
    longueur, largeur = image.size
    pixels = list(image.getdata())
    grey_pixels = list()

    for i in range(len(pixels)):
        grey_pixels.append((pixels[i][0] + pixels[i][1] + pixels[i][2]) / 3)#moyenne des trois pixels
    
    grey_image = Image.new("L", image.size)#Nouveau mode : mode greyscale
    grey_image.putdata(grey_pixels)
    
    return grey_image
    
def convert_tuple_to_list(data):
    """Change une tableau de tuple en un tableau de list."""
    new_data = list()
    for i in range(len(data)):
        new_data.append(list())
        for j in range(len(data[i])):
            new_data[i].append(data[i][j])
    return new_data
    
def convert_list_to_tuple(data):
    """Change un tableau de list en un tableau de tuple."""
    new_data = list()
    for i in range(len(data)):
        new_data.append( (data[i][0], data[i][1], data[i][2]) )
        
    return new_data
    
def convert_bytes_to_bits(data):
    """Converti des données numériques en paquet d'octets en bits.
    
    Ce qui est retourné est une string contenant toute la data en bits.
    
    """
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