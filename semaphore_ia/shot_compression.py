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
Lit les images dans shot_resize
Convertit en une ligne
Convertit le gris de 0 à 1
Ajoute la lettre de l'image
Met tout dans train et test
Compresse

Variable:
train = 60000
test = 10000
size = 40
"""


import os
import numpy as np
import cv2
import threading

from pymultilame import MyTools


CHARS_DICT = {  "a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7,
                "i": 8, "j": 9, "k": 10, "l": 11, "m": 12, "n": 13,
                "o": 14, "p": 15, "q": 16, "r": 17, "s": 18, "t": 19, "u": 20,
                "v": 21, "w": 22, "x": 23, "y": 24, "z": 25, " ": 26 }


def get_chars_label(img_file_name):
    """img_file_name = ... /semaphore_ia/shots/shot_000/shot_0_a.png
    Retourne le a
    remplace les chars anormaux en " "
    """
    l = img_file_name[-5]
    if l not in CHARS_DICT.keys():
        l = " "
    c = CHARS_DICT[l]
    return c


class ShotsCompression:

    def __init__(self, root, train, test, size):

        self.train = train
        self.test  = test
        self.size = size

        # Mon objet avec mes outils perso
        self.mytools = MyTools()

        # Valable avec exec ici ou en import
        self.root = root
        print("Dossier semaphore", self.root)

        self.get_images_list()

        self.images = np.zeros((self.train, self.size*self.size), dtype=float)
        self.labels = np.zeros((self.train), dtype=np.uint8)
        self.images_test = np.zeros((self.test, self.size*self.size), dtype=float)
        self.labels_test = np.zeros((self.test), dtype=np.uint8)

        # display
        self.disp = True
        self.img = np.zeros((self.size, self.size), dtype=np.uint8)
        self.display_thread()

    def get_images_list(self):
        """Liste de toutes les images dans shot_resize avec leurs chemin absolu
        """

        a = self.root + 'shot_resize/'
        print("Dossier des images:", a)

        self.images_list = self.mytools.get_all_files_list(a, ".png")
        print("Nombre d'images =", len(self.images_list))

    def create_semaphore_npz(self):
        """Lit toutes les images de
        /media/data/3D/projets/semaphore/semaphore_ia/shots

        60 000 images 40x40
        transformation du array 40,40 en array 1, 2500
        conversion 0:255 en 0:1

        x_train = images = 60000x2500
        y_train = labels = 60000x1

        x_test = images = 10000x2500
        y_test = labels = 10000x1

        concatenate dans un gros array
        enregistrement
        """
        i = 0

        for f in self.images_list:
            # Lecture de l'image f
            img = cv2.imread(f, 0)
            self.mangalore(i, img)

            # Conversion du gris 0 à 255 en 0 à 1
            # img = np.reshape() / 255.0
            img = np.true_divide(img, 255)

            # Retaillage sur une ligne
            img = np.resize(img, (self.size * self.size))

            # Labels
            label = get_chars_label(f)

            # Insertion par lignes
            if i < self.train:
                self.images[i] = img
                self.labels[i] =  label
            else:
                self.images_test[i - self.train] = img
                self.labels_test[i - self.train] =  label
            i += 1

        self.save_train()
        # Fin du thread
        self.disp = False

    def mangalore(self, i, img):
        # Affichage pour faire patienter les mondoshawans et les mangalores
        if i % 1000 == 0:
            print(i)
            self.img = img.copy()

    def save_train(self):
        """Enregistre les arrays images et labels dans un fichier compressé
        ./semaphore.npz
        x_train = images = 60000x2500
        y_train = labels = 60000x1
        """

        outfile = self.root + 'semaphore.npz'
        np.savez_compressed(outfile, **{"x_train": self.images,
                             "y_train": self.labels,
                             "x_test":  self.images_test,
                             "y_test":  self.labels_test})

        print('Fichier compressé =', outfile, '\n\n\n')

    def display_thread(self):
        t = threading.Thread(target=self.display)
        t.start()

    def display(self):
        cv2.namedWindow('Image')
        while self.disp:
            cv2.imshow('Image', self.img)
            # Echap
            if cv2.waitKey(33) == 27:
                break
        cv2.destroyAllWindows()


if __name__ == "__main__":
    print(MyTools().get_absolute_path(__file__))
    root = MyTools().get_absolute_path(__file__)[:-32]
    print("Current directory:", root)

    train, test, size = 60000, 10000, 40

    # Compression des images
    sc = ShotsCompression(root, train, test, size)
    sc.create_semaphore_npz()
