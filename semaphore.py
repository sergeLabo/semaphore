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

Result: 92.94   4 fev 16:19


"""


import os, sys
import subprocess
from time import sleep

# Mon module perso: voir le readme pour install
from pymultilame import MyTools, MyConfig

from resize_blur.resize_blur import ResizeBlur
from semaphore_ia.shot_compression import ShotsCompression
from semaphore_ia.semaphore_ia import SemaphoreIA


menu_1 = """\n\n    Menu principal
        Choisir 1 pour créer les images NB 320x320
        Choisir 2 pour retailler les images
        Choisir 3 pour créer le fichier compressé des images
        Choisir 4 pour excécuter l'apprentissage de l'IA
        Choisir 5 pour tester l'IA
        Choisir 6 pour modifier la configuration
        Choisir 0 pour quitter
        """

menu_2 = """\n\nConfiguration
        Choisir 1 Définir blur
        Choisir 2 Définir learning rate
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
        """self.conf est le dict de la config définie dans global.ini"""

        self.root = MyTools().get_absolute_path(__file__)[:-12]
        print('Dossier de ce script:', self.root)

        super().__init__(self.root + "global.ini")


class Menu(SemaphoreConfig):
    """Menu de tout le projet semaphore"""

    global menu_1, menu_2

    def __init__(self):
        super().__init__()

        self.result = 0
        self.learning_rate = self.conf['ia']['learning_rate']
        self.size = self.conf['ia']['size']
        self.blur = self.conf['ia']['blur']
        self.train = self.conf['ia']['training']
        self.test = self.conf['ia']['testing']
        self.size = self.conf['ia']['size']
        self.gray = self.conf['ia']['gray']
        self.failed = self.conf['ia']['failed']

    def menu(self):
        global menu_1

        choice ='0'
        while choice == '0':
            if self.result:
                print("Result:", self.result)
            print(menu_1)

            choice = input("Votre choix: ")

            if choice == "1":  # Blender
                print("Création des images 320x320 en NB")
                blend = self.root + 'get_training_shot/get_training_shot.blend'

                # pb fini le script
                p = subprocess.run(["xterm",
                                    "-e",
                                    "blenderplayer",
                                    blend],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)

            elif choice == "2":  # resize
                print("Resize en 40x40 et blur des images du 1")
                rb = ResizeBlur(self.root, self.size, self.blur)
                rb.batch()
                clear()
                self.menu()

            elif choice == "3":  # Compression
                print("\nCompression des images de shots")
                sc = ShotsCompression(  self.root, self.train, self.test,
                                        self.size, self.gray)
                sc.create_semaphore_npz()
                clear()
                self.menu()

            elif choice == "4":  # IA training
                print("\nApprentissage de l'IA")
                sia = SemaphoreIA(self.root, self.learning_rate)
                self.result = sia.training()
                clear()
                self.menu()

            elif choice == "5":  # IA testing
                print("\nTest de l'IA")
                sia = SemaphoreIA(self.root, self.learning_rate, self.failed)
                self.result = sia.testing()
                clear()
                self.menu()

            elif choice == "6":  # config
                print("Modification de la configuration")
                self.config_menu()

            elif choice == "0":
                choice = 0

            else:
                clear()
                self.menu()

        print("\n\nLe chemin est long du projet à la chose. Molière")
        os._exit(0)

    def config_menu(self):
        global menu_2

        choice ='0'
        clear()
        print(menu_2)

        while choice == '0':
            choice = input("Votre choix: ")

            if choice == "1":
                print('Blur =', self.blur)
                b = input('\n    Saisir la nouvelle valeur: ')
                b = int(b)
                if 0 <= b <= 10:
                    self.blur = b
                    self.save_config('ia', 'blur', b)
                    sleep(5)
                clear()
                self.config_menu()

            elif choice == "2":
                print('Learning Rate =', self.learning_rate)
                l = input('\n    Saisir la nouvelle valeur: ')
                l = float(l)
                if 0 < l < 1:
                    self.learning_rate = l
                    self.save_config('ia', 'learning_rate', l)
                    sleep(5)
                clear()
                self.config_menu()

            elif choice == "0":
                clear()
                self.menu()



if __name__ == "__main__":
    m = Menu()
    m.menu()
