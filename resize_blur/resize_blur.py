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
Je crée le dossier ./training_shot_resized

Je lis le dossier /media/data/3D/projets/semaphore/training_shot,
        les sous dossiers, les images de chaque sous-dossier,
        ex /media/data/3D/projets/semaphore/training_shot/shot_000/shot_0_a.png

Pour chaque image *.png,
    je lis
    verif_shot_integrity avec TAILLE_MINI_FICHIER_IMAGE
    convertit en 40x40
    enregistre dans ./training_shot_resized/shot_0xx/
        avec le même nom soit ./training_shot_resized/shot_0xx/shot_0_a.png
"""


import os
import numpy as np
import cv2

# Mes outils personnels
# à https://ressources.labomedia.org/pymultilame
from pymultilame import MyTools

TAILLE_MINI_FICHIER_IMAGE = 999


class ResizeBlur:

    def __init__(self, root, size, blur):
        self.size = int(size)
        self.size = max(20, self.size)
        self.size = min(800, self.size)

        # Flou
        self.blur = blur

        # Mes outils personnels
        self.tools = MyTools()

        self.root = root

        print("Current directory:", self.root)

        # Le terrain de jeu
        self.create_training_shot_resized_dir()

        # Liste
        self.shot_list = self.get_shot_list()

        self.create_sub_folders()

    def create_training_shot_resized_dir(self):

        directory = self.root + "/training_shot_resized"
        print("Dossier training_shot_resized:", directory)
        self.tools.create_directory(directory)

    def create_sub_folders(self):
        """Création de n dossiers shot_000
        """
        # Nombre de dossiers nécessaires
        n = len(self.tools.get_all_sub_directories(self.root + "/training_shot/")) -1
        print("Nombre de sous répertoires", n)
        for i in range(n):
            directory = self.root + "/training_shot_resized" + '/shot_' + str(i).zfill(3)
            self.tools.create_directory(directory)

    def get_new_name(self, shot):
        """ de
        /media/data/3D/projets/semaphore/training_shot/shot_000/shot_0_a.png
        à
        /media/data/3D/projets/semaphore/training_shot_resized/shot_000/shot_0_a.png
        j'ai
        /media/data/3D/projets/semaphore/training_shot_resized/shot_000/shot_3921_h.png
        """

        t = shot.partition("training_shot")
        # t = ('/media/data/3D/projets/semaphore/', 'training_shot',
        #                                       '/shot_000/shot_1054_s.png')
        name = self.root  + "/training_shot_resized" + t[2]

        return name

    def change_resolution(self, img, x, y):
        """Une image peut-être ratée"""

        try:
            res = cv2.resize(img, (x, y), interpolation=cv2.INTER_AREA)
        except:
            res = np.zeros([self.size, self.size, 1], dtype=np.uint8)
        return res

    def verif_shot_integrity(self, shot):
        """Vérifie si la taille de l'image est cohérente"""

        info = os.path.getsize(shot)
        if info < TAILLE_MINI_FICHIER_IMAGE:
            print("Intégrité - image à vérifier:", shot)
            os._exit(0)

    def batch(self):
        """Liste des images, lecture, conversion, save"""

        i = 0
        cv2.namedWindow('Image In')
        cv2.namedWindow('Image Out')
        # Pour chaque image
        for shot in self.shot_list:
            # Lecture
            img = cv2.imread(shot, 0)

            # Vérification
            self.verif_shot_integrity(shot)

            # ResizeBlur
            img_out = self.change_resolution(img, self.size, self.size)

            # Flou
            img_out = self.apply_blur(img_out, self.blur)

            # Affichage
            if i % 500 == 0:
                print(i)
                imgB = self.change_resolution(img_out, 600, 600)
                cv2.imshow('Image In', img)
                cv2.imshow('Image Out', imgB)
                cv2.waitKey(1)
            i += 1

            # Save
            new_shot = self.get_new_name(shot)
            cv2.imwrite(new_shot, img_out)

        cv2.destroyAllWindows()


    def get_shot_list(self):
        """Liste des images"""

        # Liste
        shot = self.root + "/training_shot"
        shot_list = self.tools.get_all_files_list(shot, ".png")

        print("Dossier des images NB:", shot)
        print("Nombre d'images:", len(shot_list))

        return shot_list

    def apply_blur(self, img, k):
        if self.blur:
            img = cv2.blur(img, (k, k))
        return img


if __name__ == "__main__":

    SIZE = 40
    BLUR = 4

    print("ResizeBlur de toutes les images dans le dossier training_shot")
    root = MyTools().get_absolute_path(__file__)[:-27]
    print("Current directory:", root)
    rsz = ResizeBlur(root, SIZE, BLUR)
    rsz.batch()
    print("Done")
