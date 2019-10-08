# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 19:44:57 2017

@author: pstmr

Module permettant de convertir des nombres binaires en décimale et inversement.

"""

def to_decimale(nbr_initial):
    """Renvoi le nombre donné en paramètre dans sa base 10 en integer.
    
    Le nombre doit être initialement en base 2 et en string.
    L'algorithme multiplie ensuite chaques unités du nombre par la base à la puissance du rang de l'unité,
    puis ajoute chaques résultats dans un résultat final qui est celui renvoyé.
    
    """
    nbr_final = 0
    expo_max = len(nbr_initial) - 1#Exposant maximal lors du décodage du nombre
    b = 2#la base de conversion
    
    for case, valeur in enumerate(nbr_initial):
        valeur = int(valeur)
        nbr_final += valeur * b**(expo_max-case)#Ajout fait du plus grand exposant au plus petit

    return nbr_final
    
def to_binary(nbr_initial, nbr_bits=0):
    """Converti un nombre en base 10 en sa version en base 2.
    
    Le nombre donné doit être un integer.
    Renvoi le nombre en base 2 sous forme de string.
    
    Paramètre nommé :
    nbr_bits -- nombre de bits du nombre de sortie, si le nombre donné
    fais plus de bits que demandé alors ce paramètre n'a aucun effet.
    
    """
    nbr_final = ""
    b = 2#la base de conversion
    
    reste = 0
    while nbr_initial >= b:
        reste = nbr_initial%b
        nbr_initial = nbr_initial//b
        nbr_final += str(reste)
    
    nbr_final += str(nbr_initial)#On oubli pas le dernier reste
    
    liste = list(nbr_final)#Passage en liste pour la fonction reverse
    liste.reverse()
    nbr_final = ""#Nouvelle chaîne vide
    for i in liste:#Transformation de la liste en string
        nbr_final += str(i)
    
    if len(nbr_final) < nbr_bits:#Regarde si la taille du nombre ne correspond pas au nombre de bits demandés.
        for i in range(nbr_bits - len(nbr_final)):#Ajuste le nombre pour avoir le bon nombre de bits
            nbr_final = "0" + nbr_final
    
    return nbr_final