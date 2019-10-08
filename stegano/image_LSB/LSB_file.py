# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 20:14:40 2017

@author: pstmr

Module qui permet de cacher/récupérer des fichiers dans des images en utilisant la technique du LSB.
"""

from PIL import Image

from conversion_binaire import to_binary, to_decimale
from LSB import get_LSB, put_LSB
from fonctions_image import convert_tuple_to_list, convert_list_to_tuple, convert_bits_to_bytes, convert_bytes_to_bits, read_file, create_file


'''Constantes pour le programme. Elles permettent de définir le nombre de bits alloués
au nom du fichier et a la taille du fichier en bits.'''
taille_nbr_bits = 22
taille_name = 80

def steganographie(chemin_f, chemin_i, chemin_dossier=''):
    """Cache un fichier dans une image grâce aux LSB.
    
    chemin_f est le chemin du fichier à cacher.
    chemin_i est le chemin de l'image dans laquelle est caché le fichier.
    
    """
    taille_tot = taille_nbr_bits + taille_name
    image = Image.open(chemin_i)
    di = image.getdata()
    
    print("Récupération de la data du fichier...")
    df, name_f = read_file(chemin_f)
    
    print("Passage de la data en bits...")
    df = convert_bytes_to_bits(df)
    n = ""#Nom du fichier codé en bits
    for i in name_f:#Ajoute le nom changé en bits dans n
        temp = ord(i)
        temp = to_binary(temp, 8)
        n += temp
    
    if len(n) > taille_name:#Vérifie si le nom n'est pas trop long
        print("Taille du nom du fichier supérieur à {} bits !".format(taille_name))
        return None
        
    name_f = n
    for i in range(len(name_f), taille_name):#Ajuste pour avoir 80 bits de data
        name_f = '0' + name_f
    
    nbr_bits = len(df)
    taille_tot += nbr_bits
    print("Nombre de bits :", nbr_bits)
    
    capacite_i = len(di) * 3#Multiplie par trois car chaque pixels peuvent contenir 3 bits
    print("Capacité de l'image :", capacite_i, "bits.")
    
    if capacite_i < taille_tot:
        print("L'image est trop petite pour le fichier (taille des infos :", taille_tot, "bits).")
        return None
    
    print("Converti les tuples de l'image en listes...")
    di = convert_tuple_to_list(di)
    
    print("Passage en bits des pixels de l'image...")
    for i in range(0, taille_tot, 3):
        pixel = int(i/3)
        for j in range(3):
            di[pixel][j] = to_binary(di[pixel][j], 8)
            
    print("Ajout de la data du fichier dans l'image...")
    di = put_LSB(di, to_binary(nbr_bits, taille_nbr_bits), 0)#Commmence à écrire à 0
    di = put_LSB(di, name_f, taille_nbr_bits)#Commence à écrire après le nombre de bits
    di = put_LSB(di, df, taille_name + taille_nbr_bits)#Commence à écrire après les deux premières opérations
    
    print("Retour en décimal des pixels de l'image...")
    for i in range(0, taille_tot, 3):
        pixel = int(i/3)
        for j in range(3):
            di[pixel][j] = to_decimale(di[pixel][j])
            
    print("Retour en tuples...")
    di = convert_list_to_tuple(di)
    
    print("Sauvegarde de l'image (stegano_image.bmp)...")
    image = Image.new("RGB", image.size)
    image.putdata(di)
    image.save(chemin_dossier + "stegano_image" + ".bmp")
    print("Fini !")
    
def desteganographie(chemin_i, chemin_dossier=''):    
    """Récupère un fichier caché dans une image à partir des LSB.
    
    chemin_i représente l'image dans laquelle chercher le fichier.
    
    """
    taille_tot = taille_nbr_bits + taille_name
    image = Image.open(chemin_i)
    di = image.getdata()
    
    print("Passage des tuples de l'image en listes...")
    di = convert_tuple_to_list(di)
    
    print("Passage en bits et récupération des infos du fichier caché...")
    for i in range(taille_nbr_bits + taille_name):
        pixel = int(i/3)
        canal = i%3
        di[pixel][canal] = to_binary(di[pixel][canal], 8)
    
    df = get_LSB(di, taille_nbr_bits)
    nbr_bits_f = ""
    for i in df:
        nbr_bits_f += i
    nbr_bits_f = to_decimale(nbr_bits_f)
    taille_tot += nbr_bits_f
    print("Nombre de bits du fichier :", nbr_bits_f)
    
    for i in range(taille_name + taille_nbr_bits, nbr_bits_f + taille_name + taille_nbr_bits):#Convertion du bon nombre de bits
        pixel = int(i/3)
        canal = i%3
        di[pixel][canal] = to_binary(di[pixel][canal], 8)
    
    print("Récupération des LSB dans l'image...")
    name_f = get_LSB(di, nbr_bits = taille_name, bit_start = taille_nbr_bits)
    df = get_LSB(di, nbr_bits = nbr_bits_f, bit_start = taille_name + taille_nbr_bits)
    
    print("Conversion du nom du fichier en caractères...")
    name_f = convert_bits_to_bytes(name_f)#Renvoi les valeurs décimales des paquets de 8 bits
    n = ""
    for i in name_f:
        n += chr(i)#Converti les valeurs décimales en caractères (ASCII)
    name_f = str(n)
    
    n = ""
    for i in name_f:
        if i != '\x00':#Caractère vide qui a pu être créée lors du codage dans l'image du nom (lors de l'ajustement de la taille du nom)
            n += i
    print("Nom du fichier :", n)
    
    print("Création du fichier...")
    df = convert_bits_to_bytes(df)
    create_file(df, chemin_dossier + n)
    
    print("Fini !")