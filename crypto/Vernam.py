# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 20:23:42 2017

@author: pstmr
"""

from secrets import randbits
from crypt import XOR, create_file, read_file, save_key, convert_bits_to_bytes, convert_bytes_to_bits
from conversion_binaire import to_binary

def Vernam(bits, key=-1):
    """Permet de crypter des bits grâce à une clef et un XOR appliqué aux bits.

    key est un paramètre optionnel, si une clef est donnée en paramètre alors le programme va décrypter les données
    sinon il crypte les données et renvois les données cryptées ainsi que la clef

    """
    if key == -1:
        key = randbits(len(bits))
        key = to_binary(key, len(bits))
        return XOR(bits, key), key
    else:
        return XOR(bits, key)

def crypt(chemin, key=-1):
    """Crypte les données du chemin en utilisant en appliquant un XOR sur les données.

    Les données sont cryptées dans le fichier d'origine et la clef est enregistrée dans un fichier txt.
    Si une clef est donnée en paramètre alors c'est l'action inverse qui se produit et le fichier est décrypté.

    """
    data, name = read_file(chemin)
    data = convert_bytes_to_bits(data)

    if key == -1:
        data, key = Vernam(data)
        save_key(key)
    else:
        key = str(key)
        data = Vernam(data, key)

    data = convert_bits_to_bytes(data)

    create_file(data, name)
