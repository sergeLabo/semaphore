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


import os, sys
import subprocess
from datetime import datetime
import numpy as np

from pymultilame import MyTools
from semaphore_ia.resize_blur import ResizeBlur
from semaphore_ia.shot_compression import ShotsCompression
from semaphore_ia.semaphore_ia import SemaphoreIA

# 0 ou 1
GRAY = [0]  # [0, 1]

# 0 à 10
BLUR = [4, 5, 6, 7]

# 0.005 à 0.5, paramètre important
LEARNINGRATE = [0.0200, 0.0210, 0.0215, 0.0220, 0.0225, 0.0230, 0.0240]

# Test du random: 1 à 20
NOMBRE_DE_PASSE = 5

# Total = 70000
TRAIN, TEST = 60000, 10000

def improve_ia(root):
    """Hyperparameter tuning"""
    mt = MyTools()

    imshow = 1

    # Création du dossier weights si besoin
    mt.create_directory(os.path.join(root, 'weights'))

    size = 40  # fixe
    for gray in GRAY:
        print("gray", gray)
        for blur in BLUR:
            print("blur", blur)
            # resize blur
            rb = ResizeBlur(root, size, blur, imshow)
            rb.batch()
            del rb

            # compression
            sc = ShotsCompression(root, TRAIN, TEST, size, gray, imshow)
            sc.create_semaphore_npz()
            del sc

            for learningrate in LEARNINGRATE:
                print("learningrate", learningrate)
                failed = 0
                for k in range(NOMBRE_DE_PASSE):
                    sia = SemaphoreIA(root, TRAIN, learningrate, failed, imshow)
                    weight_list = sia.training()
                    resp = sia.testing()
                    print("Result:", resp)
                    save_test(root, resp, weight_list, gray, blur, learningrate)

def save_test(root, resp, weight_list, gray, blur, learningrate):
    mt = MyTools()
    t = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    a = "{} Date: {}  TRAIN: {} TEST: {} Gray: {} Blur: {} Learningrate: {}\n"
    line = a.format(format(round(resp, 2), '.2f'), t, TRAIN, TEST, gray, blur,
                            round(learningrate, 4))
    print(line)
    fichier = os.path.join(root, "hyperparameter_tuning.txt")

    mt.write_data_in_file(line, fichier, "a")

    name = str(round(resp, 2))
    np.save(os.path.join(root,
                         'weights', 'weights_' + name + '.npy'),
                          weight_list)


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

    improve_ia(root)
