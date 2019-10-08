# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 17:19:24 2017

@author: pstmr

Module qui met en place une interface pour utiliser le DES
"""

import os
import re

from DES import DES, create_key
from crypt import save_key

def main_DES():
    """Menu principal du programme, réagit en fonction de la demande de l'utilisateur."""
    while True:
        choix = main_menu()
        if choix == 5:#Quitter
            return None
        
        chemin = choix_fichier()
        
        if choix == 1:
            DES(chemin, encrypt=True)
        elif choix == 2:
            clef = recup_clef()
            DES(chemin, key=clef, encrypt=False)
        elif choix == 3:
            clef = []
            for i in range(3):
                clef.append(create_key())#Créé trois clefs différentes
                
                if i%2 == 0:#Crypte lorsque i est pair
                    b = True
                else:
                    b = False
                
                DES(chemin, key=clef[i], encrypt=b)#Crypte le fichier avec la clef fraîchement créée
            save_key("Clef 1 : {}\nClef 2 : {}\nClef 3 : {}".format(clef[0], clef[1], clef[2]))#Sauvegarde les trois clefs dans le fichier
        elif choix == 4:
            clef = []
            for i in range(3):
                clef.append(recup_clef(i+1))
                
            for i in range(3):
                if i%2 == 0:#Décrypte lorsque i est pair
                    b = False
                else:
                    b = True
                DES(chemin, key=clef[2-i], encrypt=b)#Utilise l'algorithme avec les clefs pris dans l'autre sens que celui utilisé pour le cryptage
                
def main_menu():
    """Affiche le menu principal et renvois ce qu'à choisi l'utilisateur."""
    menu = "---Menu Principal---\n"
    menu += "1 - Crypter un fichier\n"
    menu += "2 - Décrypter un fichier\n"
    menu += "3 - Crypter un fichier (triple DES)\n"
    menu += "4 - Décrypter un fichier (triple DES)\n"
    menu += "5 - Quitter\n"
    
    choix = -1
    while choix < 1 or choix > 5:
        os.system("cls")
        print(menu, end = '')
        try:
            choix = int(input("> "))
        except ValueError:
            print("Mauvaise entrée ! Entrez un nombre svp ...")
    return choix
    
def choix_fichier():
    """Demande à l'utilisateur un chemin de fichier."""
    menu = "---Choix du fichier---\n"
    menu += "Entrez le chemin du fichier à utiliser :\n"
    
    os.system("cls")
    print(menu, end = '')
    chemin = input("> ")
    
    return chemin
    
def recup_clef(triple_key=0):
    """Demande une clef à l'utilisateur.
    
    Il est possible de préciser un numéro de clef (triple_key=0) ce
    qui permet de préciser à l'utilisateur le numéro de clef demandé.
    
    """
    menu = "---Récupération de clef---\n"
    menu += "La clef doit être une suite de 64 bits (0 ou 1).\n"
    if triple_key == 0:
        menu += "Entrez la clef de décryptage :\n"
    else:
        menu += "Entrez la clef numéro {} :\n".format(triple_key)
    
    expression = r'^[01]{64}$'#Regex qui dit que la clef doit être une suite de 64 0 ou 1
        
    key = ""
    while not re.match(expression, key):#Tant que le regex ne match pas on demande à l'utilisateur de réentrer la clef
        os.system("cls")
        print(menu, end = '')
        key = input("> ")
    return key
    
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))#Change le working directory sinon il ne trouvera pas les fichiers cartes
    main_DES()