# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 22:14:57 2017

@author: pstmr

Module qui permet d'appliquer le Data Encryption Standart sur n'importe quel fichier (en cryptage ou en décryptage).

"""

from secrets import randbits

from crypt import *
from conversion_binaire import to_decimale, to_binary

def DES(chemin, key=-1, encrypt=True):
    """Applique l'algorithme Data Encryption Standart pour chaque blocs de 64 bits du fichier demandé.
    
    La clef doit faire 64 bits (donnée en string).
    Paramètres optionnels:
    key=-1 -- Si une clef est donnée, alors l'algorithme va utiliser cette clef pour le DES. De plus, la clef
    sera sauvegarder dans un fichier 'key.txt'.
    encrypt=True -- Indique si l'algo doit encrypter (True) ou décrypter (False).
    
    """
    data, f_name = read_file(chemin)#Récupère la data en bytes (numérique)
    data = convert_bytes_to_bits(data)#Passage en une liste de bits
    data, reste = convert_bits_to_bloc(data, 64)#Récupère les blocs de 64 bits
    
    if key == -1:#Lorsque la clef n'a pas changé de valeur, c'est que l'utilisateur n'a pas donné de clef.
        key = create_key()
        save_key("Clef : " + key)#Sauvegarde la clef
        
    K = div_key(key)#Diversification de la clef
    if not encrypt:#Renversement des clefs si on est en mode décryptage
        K = K[::-1]
        
    cr_data = ""
    cnt = 0
    temp = 0
    for i in data:
        cr_data += crypt_bloc(i, K, encrypt)#Applique l'algorithme sur chacuns des blocs
        cnt += 1
        val = int(cnt/len(data) * 100)#Pourcentage d'avancement de l'algo
        if val != temp:#Si le pourcentage actuel est différent de l'ancien pourcentage affiché.
            print(val, "%")
            temp = val#Sauvegarde la dernière valeur affichée pour ne pas la réafficher par la suite.
    cr_data += reste#Ajoute le reste qui n'a pas été crypté/décrypté
    
    cr_data = convert_bits_to_bytes(cr_data)#Repassage en bytes (pour l'écriture dans un fichier)
    create_file(cr_data, f_name)#Création du nouveau fichier
    
def create_key():
    """Créé une clef de 64 bits dont les bits 8-16-24...64 sont des bits de parité,
    de sorte que les bytes aient un nombre impaire de 1."""
    key = randbits(56)#Nombre aléatoire de 56 bits
    key = to_binary(key, 56)
    cnt = 0
    sous_key = []
    for i in range(8):
        sous_key.append(key[i * 7 : (i+1) * 7])#Sépare en 8 sous tableaux de 7 bits (8*7 = 56)
    
    for i in range(len(sous_key)):#Parcourt les sous-tableaux
        for j in range(len(sous_key[i])):
            if sous_key[i][j] == '1':
                cnt += 1#Compteur pour la parité
                
        sous_key[i] += str( (cnt+1)%2 )#On ajoute un dans le cas où notre nombre est pair, sinon 0 si le nombre est impair
        cnt = 0
    
    key = ""
    for i in range(len(sous_key)):
        for j in range(len(sous_key[i])):
            key += sous_key[i][j]#Ajoute enfin toutes les sous-clefs en une seule clef

    return key
    
def perm_circ(tab, pas):
    """Décale tout les élément d'un tableau par le pas demandé."""
    n_tab = list(tab)#Copie le tableau (pour avoir un tableau de la même taille)
    
    for i in range(len(tab)):
        try:
            n_tab[i + pas] = tab[i]
        except IndexError:
            n_tab[(i + pas)%len(n_tab)] = tab[i]#Cas de dépassement de l'index, on prends que ce qui dépasse grâce au modulo
    return n_tab

def permutation(bits, P):
    """Utilise la P-box pour faire une permutation sur les bits envoyés en paramètre."""
    n_tab = ""
    for i in range(len(P)):
        n_tab += bits[P[i] - 1]#Diminution de 1 car P ne prends pas en compte que les bits commences à l'indice 0
    return n_tab
        
    
def div_key(key):
    """Diversifie la clef de 64 bits envoyée en 16 sous_clefs de 48 bits."""
    K = []

    PC = permutation(key, PC1)#Permute une première fois la clef avec une sortie de 56 bits
    C, D = list(PC[:28]), list(PC[28:])#C et D ont respectivement les 28 premiers et derniers bits de la permutation
    del PC
    
    pos = {1, 2, 9, 16}

    for i in range(17):
        if i in pos:#Si i est égal à 1, 2, 9 ou 16
            C = perm_circ(C, -1)#Permutation circulaire que d'un cran vers la gauche
            D = perm_circ(D, -1)
        else:
            C = perm_circ(C, -2)#Deux crans vers la gauche sinon
            D = perm_circ(D, -2)
        if i != 0:
            K.append(permutation(C+D, PC2))#On ajoute la clé numéro i dans le tableau des clés
    
    return K

def subs(B, i):
    """Applique la S-box numéro i sur les 6-bits B."""
    colonne = to_decimale(B[1:5])#4 bits centraux
    ligne = to_decimale(B[0] + B[-1])#2 bits extrêmes
    
    B = to_binary(S[i][ligne][colonne], 4)#4 bits de sortie
    return B
    
def func_conf(D, K):
    """Effectue la fonction de confusion avec D les 32 bits de droite et K la clef de 48 bits."""
    D = permutation(D, E)
    A = XOR(D, K)
    B = []
    sortie = ""

    for i in range(8):
        B.append(A[i*6 : (i+1)*6])#Divise le tableau A en 8 sous tableaux Bi de 6 bits
        sortie += subs(B[i], i)#Applique la S-box i sur le sous tableau Bi
        
    sortie = permutation(sortie, PF)#Permutation finale des 32 bits
    return sortie
    
def Feistel(G,D,K):
    """Effectue un tour de boucle du schéma de Feistel, retourne le nouveau G et D"""
    temp = func_conf(D, K)
    temp = XOR(G, temp)
    
    return D, temp#Retourne le nouveau G(=D) et le nouveau D(=temp)

def crypt_bloc(bloc, K, encrypt):
    """Crypte un bloc de 64 bits en lui appliquant l'algorithme du DES.
    
    Cette fonction prends en paramètres :
    - le bloc de bits qui doit faire 64 caractères
    - les 16 sous-clefs K qui doivent déjà être dans le bon ordre
    - un booléen encrypt qui indique le programme doit encrypter ou décrypter le bloc
    
    """
    
    c_bloc = permutation(bloc, P)#Permutation initiale
    G,D = str(c_bloc[:32]), str(c_bloc[32:])#G0,D0

    for i in range(16):#Calcul G16,D16 en faisant 16 tours de Feistel
        if encrypt:#Effectue l'algorithme en mode normal (cryptage)
            G, D = Feistel(G, D, K[i])            
        else:#Sens inverse de l'algorithme pour le décryptage
            D, G = Feistel(D, G, K[i])
    
    
    c_bloc = permutation(G+D, PI)#Permutation finale
    return c_bloc

"""Tous les tableaux ici sont des matrices de permutation, de substitution ou d'expansion.
Elles sont utilisés dans l'algorithme DES en tant que constantes."""

PC1 = [57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,43,35,27,19,11,3,60,52,44,36,63,55,47,39,31,
       23,15,7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,28,20,12,4]
PC2 = [14,17,11,24,1,5,3,28,15,6,21,10,23,19,12,4,26,8,16,7,27,20,13,2,41,52,31,37,47,55,
       30,40,51,45,33,48,44,49,39,56,34,53,46,42,50,36,29,32]
       
P = [58,50,42,34,26,18,10,2,
     60,52,44,36,28,20,12,4,
     62,54,46,38,30,22,14,6,
     64,56,48,40,32,24,16,8,
     57,49,41,33,25,17,9,1,
     59,51,43,35,27,19,11,3,
     61,53,45,37,29,21,13,5,
     63,55,47,39,31,23,15,7]
     
PI = [40,8,48,16,56,24,64,32,
      39,7,47,15,55,23,63,31,
      38,6,46,14,54,22,62,30,
      37,5,45,13,53,21,61,29,
      36,4,44,12,52,20,60,28,
      35,3,43,11,51,19,59,27,
      34,2,42,10,50,18,58,26,
      33,1,41,9,49,17,57,25]
      
E = [32,1,2,3,4,5,
     4,5,6,7,8,9,
     8,9,10,11,12,13,
     12,13,14,15,16,17,
     16,17,18,19,20,21,
     20,21,22,23,24,25,
     24,25,26,27,28,29,
     28,29,30,31,32,1]
     
PF = [16,7,20,21,29,12,28,17,1,15,23,26,5,18,31,10,2,8,24,14,32,27,3,9,19,13,30,6,22,11,4,25]
      
S = [
     [[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],#S-box 1
      [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
      [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
      [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]],
     [[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],#S-box 2
      [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
      [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
      [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]],
     [[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],#S-box 3
      [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
      [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
      [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]],
     [[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],#S-box 4
      [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
      [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
      [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]],
     [[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],#S-box 5
      [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
      [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
      [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]],
     [[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],#S-box 6
      [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
      [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
      [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]],
     [[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],#S-box 7
      [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
      [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
      [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]],
     [[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],#S-box 8
      [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
      [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
      [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]
      ]
