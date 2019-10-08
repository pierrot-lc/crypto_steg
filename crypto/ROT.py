# -*- coding: utf-8 -*-
"""
Created on Fri May 11 10:16:50 2018

@author: pstmr
"""

def ROT(message, nbr):
    """Rotation des lettres du nombre donné."""
    nbr %= 26
    message = message.lower()

    msg_rot = ""
    for c in message:
        c = ord(c)
        if c < 97 or c > 123:#ord('a') = 97 et ord('z') = 97+26
            msg_rot += chr(c)#Ce caractère n'est pas une lettre
            continue

        c = chr((c%97 + nbr)%26 + 97)#Se ramène à la ieme lettre, ajoute le nombre modulo 26, puis revient à la 97ieme lettre
        msg_rot += c

    return msg_rot
