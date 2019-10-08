# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 23:16:53 2017

@author: pstmr
"""

from fonctions_image import convert_tuple_to_list, convert_list_to_tuple
from conversion_binaire import to_binary, to_decimale
from LSB import put_LSB, get_LSB
from PIL import Image

def convert_255_to_7(number):#Pour faire changer d'échelle un canal de couleur de 255 à 8
    val = number * 7 / 255
    reste = val%1#Récupère les décimales pour arrondir
    if reste > 0.5:#Arrondi au dessus
        reste = 1
    else:#Arrondi au dessous
        reste = 0
    new_number = int(val) + reste
        
    return new_number
    
def convert_7_to_255(canal):
    new_canal = list()
    for i in canal:
        new_canal.append(i * 255 / 7)
        if new_canal[i] > 255:
            new_canal[i] = 255
        
    return new_canal
    
def steganographie(cover_im, secret_im):
    """Les images doivent être toutes les deux de la même taille
    et en RGB"""
    
    if (cover_im.size != secret_im.size) or (cover_im.mode != secret_im.mode):
        print("Error, images do not have the same size or are not in 'RGB' mode")
        return None
    
    #grey_im = convert_grey(secret_im, save = True)#Change l'image en gris
    #data = convert_255_to_7(grey_im.getdata())#Réduit la qualité de l'image 
    data = secret_im.getdata()

    data_cover = cover_im.getdata()
    print("Passage des tuples en liste pour le traitement...")
    data_cover = convert_tuple_to_list(data_cover)#Enlève les tuples pour traiter les pixels
    
    print("Traitement des data et insertion dans la data_cover...")
    for i in range(len(data_cover)):
        grey_data = (data[i][0] + data[i][1] + data[i][2]) / 3#Conversion en gris
        grey_data = convert_255_to_7(grey_data)#Passage à une échelle plus petite (perte d'information)
        grey_data = to_binary(grey_data, 3)#Passage en bits
        for j in range(3):
            data_cover[i][j] = to_binary(data_cover[i][j], 8)#Passage en bits
            data_cover[i][j] = data_cover[i][j][:-1] + grey_data[j]#Remplacement du dernier bit par la valeur du bit de data
            data_cover[i][j] = to_decimale(data_cover[i][j])#Repasse en décimale

    print("Repassage en tuple pour la sauvegarde de l'image...")
    data_cover = convert_list_to_tuple(data_cover)#Remets les tuples pour la création de la nouvelle image
    
    print("Sauvegarde de la nouvelle image...")
    cover_im = Image.new("RGB", cover_im.size)
    cover_im.putdata(data_cover)
    cover_im.save("stegano_image" + ".bmp")
    print("Fini !")
    
def desteganographie(cover_im):
    """Il faut une image RGB"""
    if cover_im.mode != "RGB":
        print("Error, the image is not in an RGB mode")
        return None
    
    print("Récupération de la data de l'image...")
    data = cover_im.getdata()
    print("Enlèvement des tuples de la data...")
    data = convert_tuple_to_list(data)
    grey_data = list()
    
    print("Récuperation de la data dans l'image...")
    for i in range(len(data)):#Récupère tout les pixels de l'image et les changes en bits
        for j in range(3):
            data[i][j] = to_binary(data[i][j], 8)#Passage en bits
        grey_data.append("" + data[i][0][7] + data[i][1][7] + data[i][2][7])#Récupère les LSB de l'image cover
        grey_data[i] = to_decimale(grey_data[i])#Retour en décimale
        grey_data[i] *= 255 / 7#Retour à une bonne échelle de gris
    
    print("Sauvegarde de la nouvelle image...")
    grey_image = Image.new("L", cover_im.size)#Nouveau mode : mode greyscale
    grey_image.putdata(grey_data)
    grey_image.save("secret_image.bmp")
    print("Fini !")

def recup_data(data):
    """Retourne un tableau avec uniquement les bits utiles"""
    new_data = list()
    temp = 0
    for i in range(len(data)):
        temp = (data[i][0] + data[i][1] + data[i][2]) / 3#Passage en gris
        temp = convert_255_to_7(temp)#Changement d'échelle et réduction de la qualité
        temp = to_binary(temp, 3)#Changement en binaire
        
        for j in range(3):
            new_data.append(temp[j])#Ajout dans le noveau tableau
            
    return new_data


    
def steganographieV2(image_cover, secret_image):
    """Permet de cacher une image de type 'RGB' dans une autre image 'RGB' en la passant auparavant
    en gris et en réduisant la qualité.
    Il faut que la taille de l'image a caché soit inferieur à celle de l'image à cacher.
    Pour être plus précis, il faut que : longueur_s * largeur_s * 3 + 22 < longueur_c * largeur_c * 3"""
    if image_cover.mode != 'RGB' or secret_image.mode != 'RGB':
        print("Images are not in 'RGB' mode")
        return None
    
    longueur, largeur = secret_image.size
    L, l = image_cover.size
    taille_information_s = largeur * longueur * 3 + 22
    taille_information_c = l*L*3
    if taille_information_s > taille_information_c:
        print("L'image a caché est trop grosse par rapport à l'image_cover.")
        return None
        
    data = secret_image.getdata()
    data_cover = image_cover.getdata()
    
    print("Conversion des tuples en listes...")
    data_cover = convert_tuple_to_list(data_cover)
    
    print("Passage en bits de l'image_cover...")
    for i in range(taille_information_s):
        for j in range(3):
            data_cover[i][j] = to_binary(data_cover[i][j], 8)
    
    print("Insertion de la taille de l'image (", longueur, "x", largeur,")...", sep = "")
    longueur = to_binary(longueur, 11)
    largeur = to_binary(largeur, 11)
    data_cover = put_LSB(data_cover, longueur + largeur, bit_start = 0)
    
    print("Conversion en gris et récupération des bits...")
    data = recup_data(data)
    
    print("Insertion des bits dans les LSB...")
    data_cover = put_LSB(data_cover, data, bit_start = 22)
    
    print("Repassage en décimal...")
    for i in range(taille_information_s):
        for j in range(3):
            data_cover[i][j] = to_decimale(data_cover[i][j])
    
    print("Repassage en tuple...")
    data_cover = convert_list_to_tuple(data_cover)
    
    print("Sauvegarde de l'image...")
    image_cover = Image.new("RGB", image_cover.size)
    image_cover.putdata(data_cover)
    image_cover.save("stegano_image.bmp")
    print("Fini !")
    
def desteganographieV2(secret_image):
    """A besoin d'une image RGB pour que la fonction marche"""
    if secret_image.mode != 'RGB':
        print("Image not in 'RGB' mode")
        return None
        
    data = secret_image.getdata()
    
    print("Conversion des tuples en listes...")
    data = convert_tuple_to_list(data)
    
    for i in range(22):
        pixel = int(i/3)
        canal = i%3
        data[pixel][canal] = to_binary(data[pixel][canal], 8)
    
    print("Récupération de la taille de l'image...")
    size = get_LSB(data, nbr_bits = 22, bit_start = 0)
    longueur = ""
    largeur = ""

    longueur = to_decimale(size[:11])
    largeur = to_decimale(size[11:])
    secret_data = list()
    
    print("La longueur de l'image est :", longueur)
    print("La largeur de l'image est :", largeur)
    
    print("Récupération des LSB...")
    for i in range(22, longueur * largeur * 3 + 22):#Converti uniquement les pixels interessants en bits
        pixel = int(i/3)
        canal = i%3
        data[pixel][canal] = to_binary(data[pixel][canal], 8)
    
    temp = get_LSB(data, longueur * largeur * 3, 22)
    print("Taille de l'information en bits : ", len(temp))
        
    j = 0
    i = 0
    while i < len(temp)/3:#Divise le tableau en un tableau groupé par 3 bits (3bits = 1 pixel gris)
        secret_data.append(temp[j] + temp[j + 1] + temp[j + 2])
        secret_data[i] = to_decimale(secret_data[i])
        secret_data[i] *= 255 / 7#Passage du pixel gris à une echelle sur 255
        i += 1
        j = i*3
    
    print("Sauvegarde de l'image...")
    secret_image = Image.new("L", (longueur, largeur))
    secret_image.putdata(secret_data)
    secret_image.save("secret_image.bmp")
    print("Fini !")