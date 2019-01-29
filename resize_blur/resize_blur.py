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


import numpy as np
import cv2
import shutil

# Mes outils personnels
# à https://ressources.labomedia.org/pymultilame
from pymultilame import MyTools


"""
Je crée le dossier ./shot_resize

Je lis le dossier /media/data/3D/projets/semaphore/shot_NB,
        les sous dossiers, les images de chaque sous-dossier,
        ex /media/data/3D/projets/semaphore/shot_NB/shot_000/shot_0_a.png

Pour chaque image *.png, je lis, convertit en 40x40,
    enregistre dans ./shot_resize/shot_0xx/
        avec le même nom soit ./shot_resize/shot_0xx/shot_0_a.png

Puis comprime le dossier shot_resize en shot_resize.zip"""


SIZE = 40
BLUR = 2

class ResizeBlur:

    def __init__(self, size, blur):
        self.size = int(size)
        self.size = max(20, self.size)
        self.size = min(800, self.size)

        # Flou
        self.blur = blur
        
        # Mes outils personnels
        self.tools = MyTools()

        self.current_dir = self.tools.get_absolute_path("")

        print("Current directory:", self.current_dir)

        # Le terrain de jeu
        self.create_shot_resize_dir()
        
        # Liste
        self.shot_list = self.get_shot_list()
        
        self.create_sub_folders()

    def create_shot_resize_dir(self):

        directory = self.current_dir + "/shot_resize"
        print("Dossier shot_resize:", directory)
        self.tools.create_directory(directory)

    def create_sub_folders(self):
        """Création de n dossiers shot_000
        """
        # Nombre de dossiers nécessaires
        n = len(self.tools.get_all_sub_directories(self.current_dir + "/shot_NB/")) -1
        print("Nombre de sous répertoires", n)
        for i in range(n):
            directory = self.current_dir + "/shot_resize" + '/shot_' + str(i).zfill(3)
            self.tools.create_directory(directory)
        
    def get_new_name(self, shot):
        """ de
        /media/data/3D/projets/semaphore/shot_NB/shot_000/shot_0_a.png
        à
        /media/data/3D/projets/semaphore/shot_resize/shot_000/shot_0_a.png
        j'ai
        /media/data/3D/projets/semaphore/shot_resize/shot_000/shot_3921_h.png
        """
        
        t = shot.partition("shot_NB")
        # t = ('/media/data/3D/projets/semaphore/', 'shot_NB', '/shot_000/shot_1054_s.png')
        name = self.current_dir  + "/shot_resize" + t[2]

        return name

    def change_resolution(self, img, x, y):
        """Une image peut-être ratée"""
        
        try:
            res = cv2.resize(img, (x, y), interpolation=cv2.INTER_AREA)
        except:
            res = np.zeros([self.size, self.size, 1], dtype=np.uint8)
        return res

    def batch(self):
        """Liste des images, lecture, conversion, save"""

        # Pour chaque image
        for shot in self.shot_list:
            # Lecure
            img = cv2.imread(shot, 0)

            # ResizeBlur
            img = self.change_resolution(img, self.size, self.size)

            # Flou
            img = apply_blur(img, self.blur)

            # Save
            new_shot = self.get_new_name(shot)
            cv2.imwrite(new_shot, img)

    def get_shot_list(self):
        """Liste des images"""

        # Liste
        shot = self.current_dir + "/shot_NB"
        shot_list = self.tools.get_all_files_list(shot, ".png")
        print("Nombre d'images:", len(shot_list))
        return shot_list

    def compression(self):
        """Pas utile"""
        
        dir_name = self.current_dir  + "/shot_resize"
        output_filename = self.current_dir  + "/shot_resize"
        shutil.make_archive(output_filename, 'zip', dir_name)

    
def apply_blur(img, k):
    
    return cv2.blur(img, (k, k))


def main():
    print("ResizeBlur de toutes les images dans le dossier shot")
    rsz = ResizeBlur(SIZE, BLUR)
    rsz.batch()
    print("Done")


if __name__ == "__main__":
    main()
