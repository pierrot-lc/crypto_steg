# -*- coding: utf-8 -*-
"""
Created on Wed May 17 22:19:17 2017

@author: pstmr
"""

import os

import RSA

def main_RSA():
    while True:
        choice = main_menu()
        if choice == 4:#Quit
            return None
        elif choice == 1:
            public, private = RSA.create_keys()
            data = "Public key : {}, {}\nPrivate key : {}, {}".format(public[0], public[1], private[0], private[1])
            save_into_file("keys.txt", data)
        elif choice == 2:#Encrypt
            path = ask_file()
            data = read_file(path)
            public_k = ask_key(private=False)
            data = RSA.encrypt(data, public_k)
            data = list_to_string(data)
            save_into_file(path, data)
        elif choice == 3:#Decrypt
            path = ask_file()
            data = read_file(path)
            data = string_to_list(data)
            private_k = ask_key(private=True)
            data = RSA.decrypt(data, private_k)
            save_into_file(path, data)
            
def main_menu():
    menu = "----Main menu----\n"
    menu += "1. Make new keys\n"
    menu += "2. Encrypt a file\n"
    menu += "3. Decrypt a file\n"
    menu += "4. Quit\n"

    choice = -1
    while choice < 1 or choice > 4:
        os.system("cls")
        print(menu, end = '')
        try:
            choice = int(input("> "))
        except ValueError:
            print("Wrong entry! Give a number ...")
    return choice
    
def ask_file():
    menu = "----File path----\n"
    menu += "Enter the path of the file to use :"
    
    os.system("cls")
    print(menu, end = '')
    path = input("> ")
    
    return path

def read_file(path):
    with open(path, 'r') as file:
        data = file.read()
    return data
    
def ask_key(private):
    if private:
        key_type = "private"
    else:
        key_type = "public"
        
    tab = ["first", "second"]
    keys = []

    os.system("cls")
    print("----Keys----")
    for i in range(2):
        print("Enter the {} number of the {} key :".format(tab[i], key_type), end='')
        keys.append(int(input("> ")))
        
    return keys
    
def list_to_string(data):
    data_str = ""
    for d in data:
        data_str += str(d) + " "
    return data_str[:-1]#Without the last element because it is an useless space
    
def string_to_list(data):
    data_list = []
    data = data.split(" ")
    for d in data:
        data_list.append(int(d))
    return data_list
    
def save_into_file(file_name, data):
    with open(file_name, 'w') as file:
        file.write(data)
    
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    main_RSA()