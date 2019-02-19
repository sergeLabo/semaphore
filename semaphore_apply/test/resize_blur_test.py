#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


import os
import numpy as np
import cv2

from pymultilame import MyTools


class ResizeBlur:

    def __init__(self, root, size, blur, lower, upper):
        self.size = int(size)
        self.size = max(20, self.size)
        self.size = min(800, self.size)
        self.lower = lower
        self.upper = upper
        # Flou
        self.blur = blur

        # Mes outils personnels
        self.tools = MyTools()

        self.root = root

        print("Current directory:", self.root)

        # Le terrain de jeu
        self.shot_resized()

        # Liste
        self.shot_list = self.get_shot_list()

        self.create_sub_folders()

    def shot_resized(self):

        directory = os.path.join(self.root, 'semaphore_apply', 'shot_resized')
        print("Dossier shot_resized:", directory)
        self.tools.create_directory(directory)

    def create_sub_folders(self):
        """Création de n dossiers shot_000
        """
        # Nombre de dossiers nécessaires
        d = os.path.join(self.root, 'semaphore_apply', 'shot')
        n = len(self.tools.get_all_sub_directories(d)) -1
        print("Nombre de sous répertoires", n)
        for i in range(n):
            d = os.path.join(self.root, 'semaphore_apply', 'shot_resized', 'shot_' + str(i).zfill(3))
            self.tools.create_directory(d)

    def get_new_name(self, shot):
        """ de
        /media/data/3D/projets/semaphore/semaphore_apply/shot/shot_000/shot_0_a.png
        à
        /media/data/3D/projets/semaphore/semaphore_apply/shot_resized/shot_000/shot_0_a.png
        """
        # t[2] = /shot_000/shot_280_j.png
        t = shot.partition("shot")
        name = os.path.join(self.root, 'semaphore_apply', 'shot_resized', t[2][1:])

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

        i = 0
        cv2.namedWindow('Image In')
        cv2.namedWindow('Image Out')
        # Pour chaque image
        for shot in self.shot_list:
            # Lecture
            rgb = cv2.imread(shot, 1)
            hsv = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)

            # Threshold
            img = self.apply_mask(hsv)

            # ResizeBlur
            img_out = self.change_resolution(img, self.size, self.size)

            # Flou
            img_out = self.apply_blur(img_out, self.blur)

            # Gris en blanc
            ret, img_out = cv2.threshold(img_out, 2, 255, cv2.THRESH_BINARY)

            # Inversion
            #img_out = 255 - img_out

            # ## Affichage
            # #if i % 10 == 0:
                # #print(i)
                # #imgB = self.change_resolution(img_out, 600, 600)
                # #cv2.imshow('Image In', rgb)
                # #cv2.imshow('Image Out', imgB)
                # #cv2.waitKey(1)
            # #i += 1

            # Save
            new_shot = self.get_new_name(shot)
            cv2.imwrite(new_shot, img_out)

        cv2.destroyAllWindows()

    def apply_mask(self, hsv):
        """ h_min = 0
            s_min = 255
            v_min = 255
            h_max = 50
            s_max = 255
            v_max = 255
        """
        lower = np.array(self.lower)
        upper = np.array([255, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)
        return mask

    def get_shot_list(self):
        """Liste des images"""

        # Liste
        shot = os.path.join(self.root, 'semaphore_apply', 'shot')
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
    BLUR = 6

    # Chemin courrant
    abs_path = MyTools().get_absolute_path(__file__)
    print("Chemin courrant", abs_path)

    # Nom du script
    name = os.path.basename(abs_path)
    print("Nom de ce script:", name)

    # Abs path de semaphore sans / à la fin
    parts = abs_path.split("semaphore")
    root = os.path.join(parts[0], "semaphore")
    print("Path de semaphore:", root)

    lower = [122, 90, 90]  # [120, 80, 80]
    upper = [255, 255, 255]
    rsz = ResizeBlur(root, SIZE, BLUR, lower, upper)
    rsz.batch()
    print("Done")
