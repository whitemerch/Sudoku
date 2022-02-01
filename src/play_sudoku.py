#!/usr/bin/python3
#-*-coding: utf8-*-

from grid import *
def debut():
    t = True
    while t:
        choisir = input("Voulez vous utiliser votre propre jeu(o) ou non(n)? : ")
        if choisir == "o":
            filename = input("Saisir le nom de votre fichier: ")
            ligne = input("Saisir le numéro de votre ligne: ")
            jeu=SudokuGrid.from_file(filename, int(ligne))
            t = False
        elif choisir == "n":
            jeu = SudokuGrid.from_stdin()
            t = False
        else:
            print("Votre saisie est incorrecte")
    return jeu

def jouer(jeu):
    entree = jeu
    while len(entree.get_empty_pos()) != 0:
        print("Voici les cases vide dans le sudoku", entree.get_empty_pos())
        x = int(input("Veuillez entrer la ligne sur laquelle se situe la case à modifier (de haut en bas, de 0 à 8) : "))
        y = int(input("Veuillez entrer la colonne sur laquelle se situe la case à modifier (de gauche à droite, de 0 à 8) : "))
        z = int(input("Veuillez entrer la valeur à mettre dans cette case (de 1 à 9) : "))
        if (x,y) in entree.get_empty_pos():
            entree.write(x, y, z)
        else:
            test = input("La case n'est pas vide, voulez vous modifier la valeur ? Si oui tapez (o)")
            if test == "o":
                entree.write(x, y, z)
            else:
                print("Aucune modification n'a été faite !")
        entree = entree.copy()
        print(entree)
    return entree

jouer(debut())

