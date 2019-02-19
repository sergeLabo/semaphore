#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


import os
import numpy as np
import cv2

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

    def __init__(self, root, size):

        self.train = 0
        self.size = size

        # Mon objet avec mes outils perso
        self.mytools = MyTools()

        # Valable avec exec ici ou en import
        self.root = root
        print("Dossier semaphore", self.root)

        self.get_images_list()
        self.test  = len(self.images_list)
        print("Nombre d'images", self.test )

        self.images = np.zeros((self.train, self.size*self.size), dtype=np.uint8)
        self.images_test = np.zeros((self.test, self.size*self.size), dtype=np.uint8)
        self.labels = np.zeros((self.train), dtype=np.uint8)
        self.labels_test = np.zeros((self.test), dtype=np.uint8)

    def get_images_list(self):
        """Liste de toutes les images dans shot_resized avec leurs chemin absolu"""

        a = os.path.join(self.root, 'semaphore_apply', 'shot_resized')
        print("Dossier des images:", a)

        self.images_list = self.mytools.get_all_files_list(a, ".png")
        print("Nombre d'images =", len(self.images_list))

    def create_semaphore_npz(self):

        i = 0
        cv2.namedWindow('Image')
        for f in self.images_list:
            # Lecture de l'image f
            img = cv2.imread(f, 0)

            # #if i % 100 == 0:
                # #print(i)
                # #imgB = cv2.resize(img, (600, 600), interpolation=cv2.INTER_AREA)
                # #cv2.imshow('Image', imgB)
                # #cv2.waitKey(1)

            # Conversion du gris 0 à 255 en 0 à 1
            #img = np.true_divide(img, 255)

            # Retaillage sur une ligne soit 1600
            img = np.resize(img, (self.size * self.size))

            # Labels
            label = get_chars_label(f)

            # Insertion par lignes
            self.images_test[i - self.train] = img
            self.labels_test[i - self.train] =  label
            i += 1

        cv2.destroyAllWindows()
        self.save_npz()

    def save_npz(self):
        """Enregistre les arrays images et labels dans un fichier compressé
        ./semaphore_apply.npz
        training = 0 testing = 1000
        """

        outfile = os.path.join(self.root, 'semaphore_apply', 'test', 'semaphore_apply.npz')
        np.savez_compressed(outfile, **{"x_train": self.images,
                                        "y_train": self.labels,
                                        "x_test":  self.images_test,
                                        "y_test":  self.labels_test})

        print('Fichier compressé =', outfile, '\n\n\n')

    def verif_npz_file(self):
        f = os.path.join(self.root, 'semaphore_apply', 'test', 'semaphore_apply.npz')
        fichier = np.load(f)
        self.x_test, self.y_test = fichier['x_test'], fichier['y_test']
        i = 0
        cv2.namedWindow('Image')
        for vecteur_ligne, nombre_lettre in zip(self.x_test, self.y_test):
            # Affichage pour distraire les mangalores
            if i % 10 == 0:
                print("Image N°", i, "Numéro de la lettre", nombre_lettre)
                img = vecteur_ligne.reshape(40,40)# * 255
                img = cv2.resize(img, (600, 600), interpolation=cv2.INTER_AREA)
                cv2.imshow("img", img)
                cv2.waitKey(200)
            i += 1
        cv2.destroyAllWindows()


if __name__ == "__main__":
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

    size = 40

    # Compression des images
    sc = ShotsCompression(root, size)
    sc.create_semaphore_npz()
    #sc.verif_npz_file()
