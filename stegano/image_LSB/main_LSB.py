# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 22:44:43 2017

@author: pstmr

Module qui permet de créer une interface pour utiliser la stéganographie LSB.
"""

import os
import sys

from LSB_file import steganographie, desteganographie
from fonctions_image import get_dir

def main_LSB():
    """Boucle qui affiche le menu principal et qui agit en fonction de ce que veux l'utilisateur."""
    while True:
        choix = main_menu()
        if choix == 3:#Quitter
            return None
            
        path_image = choix_fichier("de l'image")
        if choix == 1:
            path_file = choix_fichier("du fichier")
            steganographie(path_file, path_image)
        elif choix == 2:
            desteganographie(path_image)

def main_menu():
    """Affiche le menu principal et renvois ce qu'à choisi l'utilisateur."""
    menu = "---Menu Principal---\n"
    menu += "1 - Cacher un fichier\n"
    menu += "2 - Récupérer un fichier\n"
    menu += "3 - Quitter\n"
    
    choix = -1
    while choix < 1 or choix > 3:
        os.system("cls")
        print(menu, end = '')
        try:
            choix = int(input("> "))
        except ValueError:
            print("Mauvaise entrée ! Entrez un nombre svp ...")
    return choix

def choix_fichier(string=""):
    """Demande à l'utilisateur un chemin de fichier."""
    menu = "---Choix du fichier---\n"
    menu += "Entrez le chemin {} :\n".format(string)
    
    os.system("cls")
    print(menu, end = '')
    chemin = input("> ")
    
    return chemin

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file = sys.argv[1]
        path_dir = get_dir(file)
        desteganographie(file, chemin_dossier=path_dir)
    else:
        if 'python.exe' in sys.executable:#Si le programme est lancé par python (donc c'est le fichier.py que l'on lance)
            os.chdir(os.path.dirname(os.path.realpath(__file__)))#Change le working directory sinon il ne trouvera pas les fichiers cartes
        else:#Sinon c'est le fichier en .exe que l'on a lancé
            os.chdir(os.path.dirname(sys.executable))#Change le dossier lorsque ce programme est en .exe
        main_LSB()