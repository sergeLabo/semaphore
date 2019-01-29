#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

########################################################################
# This file is part of Semaphore.
#
# Semaphore is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Semaphore is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
########################################################################

"""
Lance en terminal les différentes étapes

menu avec choix
    1 - Lance blender pour créer les images NB 320x320


    
"""


import os, sys
import subprocess
from time import sleep

# Mon module perso: voir le readme pour install
import pymultilame

from semaphore_ia.ia import SemaphoreIA, ShotsCompression
from resize_blur.resize_blur import ResizeBlur


menu_1 = """\n\n    Menu principal
        Choisir 1 pour créer les images NB 320x320
        Choisir 2 pour retailler les images du 1
        Choisir 3 pour créer le fichier compressé des images
        Choisir 4 pour excécuter l'apprentissage de l'IA
        Choisir 5 pour tester l'IA
        Choisir 6 pour modifier la configuration
        Choisir 0 pour quitter
        """
        
menu_2 = """\n\nConfiguration
        Choisir 1 pour 
        Choisir 2 pour 
        Choisir 0 pour retour au menu principal
        """

def clear(): 
    """Efface le terminal"""
    
    # Windows 
    if os.name == 'nt': 
        os.system('cls') 
  
    # Mac and Linux (os.name is 'posix') 
    else: 
        os.system('clear') 


class Menu:
    """Menu de tout le projet semaphore"""
    global menu_1
    
    def __init__(self):
        self.root = pymultilame.MyTools().get_absolute_path(__file__)[:-12]
        print('Dossier de ce script:', self.root)
                    
    def menu(self):
        global menu_1
        
        choice ='0'
        while choice == '0':
            print(menu_1)

            choice = input("Votre choix: ")

            if choice == "1":
                print("Création des images 320x320 en NB")
                blend = self.root + '/game_NB/semaphore_NB.blend'
                pop = ['xterm', '-e', 'blenderplayer', blend]
                # shell=True ok pour linux seul
                p = subprocess.Popen(pop, shell=False)
                
            elif choice == "2":
                print("Resize en 40x40 et blur des images du 1")
                SIZE, BLUR = 40, 2
                rb = ResizeBlur(SIZE, BLUR)
                rb.batch()
                rb.compression()
                clear()
                self.menu()
                
            elif choice == "3":
                print("\nCompression des images de shots")
                sc = ShotsCompression()
                sc.create_semaphore_npz()
                clear()
                self.menu()
                            
            elif choice == "4":
                print("\nApprentissage")
                sia = SemaphoreIA()
                sia.ia_training()
                clear()
                self.menu()
                            
            elif choice == "5":
                print("\nTest de l'IA")
                sia = SemaphoreIA()
                sia.ia_testing()
                sleep(10)
                clear()
                self.menu()
                                    
            elif choice == "6":
                print("Modification de la configuration")
                self.config_menu()
                
            else:
                break
                
        print("\n\nLe chemin est long du projet à la chose. Molière")
        os._exit(0)
        
    def config_menu(self):
        global menu_2
        
        choice ='0'
        print(menu_2)
        
        while choice == '0':
            choice = input("Votre choix: ")

            if choice == "1":
                print("choix 1")
                clear()
                self.config_menu()
                
            elif choice == "2":
                print("Do Something 2")
                clear()
                self.config_menu()
                
            else:
                clear()
                self.menu()  


if __name__ == "__main__":
    m = Menu()
    m.menu()
