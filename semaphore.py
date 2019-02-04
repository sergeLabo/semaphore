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
from pymultilame import MyTools, MyConfig

from semaphore_ia.train_semaphore import int_art
from semaphore_ia.shot_compression import ShotsCompression
from resize_blur.resize_blur import ResizeBlur


menu_1 = """\n\n    Menu principal
        Choisir 1 pour créer les images NB 320x320
        Choisir 2 pour retailler les images
        Choisir 3 pour créer le fichier compressé des images
        Choisir 4 pour excécuter et tester l'apprentissage de l'IA
        Choisir 5 pour rien
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


class SemaphoreConfig(MyConfig):
    """# self.conf.save_config(section, key, value)"""

    def __init__(self):
        self.root = MyTools().get_absolute_path(__file__)[:-12]
        print('Dossier de ce script:', self.root)
        super().__init__(self.root + "semaphore.ini")


class Menu(SemaphoreConfig):
    """Menu de tout le projet semaphore"""
    global menu_1, menu_2

    def __init__(self):
        super().__init__()

    def menu(self):
        global menu_1

        choice ='0'
        while choice == '0':
            print(menu_1)

            choice = input("Votre choix: ")

            if choice == "1":  # Blender
                print("Création des images 320x320 en NB")
                blend = self.root + 'get_training_shot/get_training_shot.blend'
                pop = ['xterm', '-e', 'blenderplayer', blend]
                # shell=True ok pour linux seul
                p = subprocess.Popen(pop, shell=False)

            elif choice == "2":  # resize
                print("Resize en 40x40 et blur des images du 1")
                SIZE, BLUR = 40, 2
                rb = ResizeBlur(self.root, SIZE, BLUR)
                rb.batch()
                clear()
                self.menu()

            elif choice == "3":  # Compression
                print("\nCompression des images de shots")
                train, test, size, gray = 60000, 10000, 40, 0
                sc = ShotsCompression(self.root, train, test, size, gray)
                sc.create_semaphore_npz()
                clear()
                self.menu()

            elif choice == "4":  # IA training
                print("\nApprentissage et test de l'IA")
                learning_rate = 0.05
                res = int_art(self.root, learning_rate)
                sleep(10)
                clear()
                self.menu()

            elif choice == "5":  # IA testing
                print("\nrien")
                clear()
                self.menu()

            elif choice == "6":  # config
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
