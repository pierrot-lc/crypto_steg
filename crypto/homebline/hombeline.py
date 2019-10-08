# -*- coding: utf-8 -*-
"""
Created on Sat May 12 17:01:26 2018

@author: pstmr

Chiffre en utilisant un jeu de lettres. Ce jeu de lettres represente la clef
de chiffrement et de dechiffrement. On encode le texte a chiffrer en mettant
le numero de chaque lettre du texte dans le jeu de lettres (la clef).

Chaque lettre est definie par rapport au numero precedent. Ainsi '_23_1_'
veut dire : 'lire la 23eme lettre de la clef, puis 1ere lettre apres la 23eme'.
"""

from crypto import Cryptographie

list_of_letters = [chr(i) for i in range(97, 97+26)]
sep = '_'

class Hombeline(Cryptographie):
    def __init__(self):
        self.param = {"sep" : '_', "key_file" : "", "file_input" : "", "file_output" : ""}

    def encrypt(self):
        msg, letters = self.init_crypto()
        encrypted_msg = ""

        i = 0 # indice de decalage par rapport au dernier caractere trouve
        j = 0 # indice dernier caractere trouve
        deb = True
        for c in msg:
            if not (c in list_of_letters):#Ne crypte pas les caractères spéciaux
                encrypted_msg += c#passe le caractère
                deb = True
                continue

            while i+j < len(letters) and letters[j+i] != c:#Trouve le caractère dans les lettres suivantes
                i += 1

            if i+j >= len(letters):
                return ""#Le jeu de lettres ne permet pas de crypter le message (il manque des lettres)

            if deb:
                encrypted_msg += sep#Démarre avec un sep pour séparer les caractères normaux des spéciaux
                deb = False
            encrypted_msg += str(i+1) + sep#Décalage des indices dû aux listes
            j += i+1
            i = 0

        if encrypted_msg[-1] != sep:#Si le msg se finit par un caractère spécial, il faut finir la marche (le sep n'a pas été mis).
            encrypted_msg += sep

        if self.params["file_output"] != "":
            with open(self.param["file_output"], 'w') as file:
                file.write(encrypted_msg)

        return encrypted_msg

    def init_crypto(self):
        with open(self.param["key_file"], 'r') as file:
            letters = file.read()
        letters = init_letters(letters)

        with open(self.param["file_intput"], 'r') as file:
            msg = file.read()
        msg = msg.lower()

        return msg, letters

def encrypt(msg, letters):
    msg = msg.lower()
    encrypted_msg = ""
    letters = init_letters(letters)

    i = 0
    j = 0
    deb = True
    for c in msg:
        if not (c in list_of_letters):#Ne crypte pas les caractères spéciaux
            encrypted_msg += c#passe le caractère
            deb = True
            continue

        while i+j < len(letters) and letters[j+i] != c:#Trouve le caractère dans les lettres suivantes
            i += 1

        if i+j >= len(letters):
            return ""#Le jeu de lettres ne permet pas de crypter le message (il manque des lettres)

        if deb:
            encrypted_msg += sep#Démarre avec un sep pour séparer les caractères normaux des spéciaux
            deb = False
        encrypted_msg += str(i+1) + sep#Décalage des indices dû aux listes
        j += i+1
        i = 0

    if encrypted_msg[-1] != sep:#Si le msg se finit par un caractère spécial, il faut finir la marche (le sep n'a pas été mis).
        encrypted_msg += sep

    return encrypted_msg

def decrypt(msg, letters):
    msg = group_numbers(msg)
    decrypted_msg = ""
    letters = init_letters(letters)

    i, j = 0, 0
    for c in msg:
        try:
            i = int(c) - 1

            if i+j >= len(letters):
                return ""
            decrypted_msg += letters[j+i]
            j += i+1
        except ValueError:#Cas du caractère spécial
            decrypted_msg += c

    return decrypted_msg

def group_numbers(msg):
    tab = []
    temp = ""

    for c in msg:
        if c == sep:
            tab.append(temp)
            temp = ""
        else:
            temp += c

    return tab

def init_letters(letters):
    letters = letters.lower()
    clean_letters = ""
    for c in letters:
        if c in list_of_letters:
            clean_letters += c

    return clean_letters

def Hombe(msg, file_name, encr):
    with open(file_name, 'r') as file:
        letters = file.read()

    if encr == True:
        msg = encrypt(msg, letters)
    else:
        msg = decrypt(msg, letters)

    if msg == "":#Le fichier et le message donné ne peuvent pas se crypter ensemble (fichier trop court, msg trop long ....)
        return None

    return msg

if __name__ == "__main__":
    msg = "Gros bisous partout"
    msg_e = Hombe(msg, "lettres.txt", encr=True)
    msg_d = Hombe(msg_e, "lettres.txt", False)

    print("Message initial :", msg)
    print("Message crypté :", msg_e)
    print("Message décrypté :", msg_d)
