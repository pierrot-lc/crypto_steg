# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 18:15:38 2018

@author: pstmr
"""

import os
import sys

import LSB_wave as LSB

def main():
    """Boucle qui affiche le menu principal et qui agit en fonction de ce que veux l'utilisateur."""
    while True:
        choix = main_menu()
        if choix == 3:#Quitter
            return None
            
        path_wave = choix_fichier("chemin du fichier .wav")
        if choix == 1:
            path_file = choix_fichier("chemin du fichier de données")
            LSB.encrypt(path_wave, path_file, "encrypted_file.wav")
        elif choix == 2:
            nbr_caract = int(choix_fichier("nombre de caractères à prendre (-1 pour tout prendre)"))
            LSB.decrypt(path_wave, "decrypted_file.txt", nbr_caract)

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
    """Demande à l'utilisateur une information."""
    menu = "---Demande d'information---\n"
    menu += "Entrez le {} :\n".format(string)
    
    os.system("cls")
    print(menu, end = '')
    chemin = input("> ")
    
    return chemin

if __name__ == "__main__":
    if 'python.exe' in sys.executable:#Si le programme est lancé par python (donc c'est le fichier.py que l'on lance)
        os.chdir(os.path.dirname(os.path.realpath(__file__)))#Change le working directory sinon il ne trouvera pas les fichiers cartes
    else:#Sinon c'est le fichier en .exe que l'on a lancé
        os.chdir(os.path.dirname(sys.executable))#Change le dossier lorsque ce programme est en .exe
    main()