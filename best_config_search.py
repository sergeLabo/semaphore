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
from resize_blur.resize_blur import ResizeBlur
from semaphore_ia.shot_compression import ShotsCompression
from semaphore_ia.semaphore_ia import SemaphoreIA

# 0 ou 1
GRAY = [0]  # [0, 1]
# 0 à 10
BLUR = [3, 4, 5, 6]  # [0, 1, 2, 3, 4, 5, 6]
# 0.005 à 0.5, paramètre important
LEARNINGRATE = [0.018,
                0.020, 0.022, 0.024, 0.026, 0.028,
                0.030, 0.032]
                # [0.01, 0.02, 0.03, 0.04]
NOMBRE_DE_PASSE = 5

def improve_ia():
    """Hyperparameter tuning"""
    mt = MyTools()
    root = mt.get_absolute_path(__file__)[:-21]
    print("Current directory:", root)

    imshow = 0
    mt.create_directory(root + "weights")

    # liste de [gray, blur, learningrate, res]
    all_res = {}

    size = 40  # fixe
    for gray in GRAY:
        print("gray", gray)
        all_res[gray] = {}
        for blur in BLUR:
            print("blur", blur)
            all_res[gray][blur] = []
            # resize blur
            rb = ResizeBlur(root, size, blur, imshow)
            rb.batch()
            del rb

            # compression
            train, test = 60000, 10000
            sc = ShotsCompression(root, train, test, size, gray, imshow)
            sc.create_semaphore_npz()
            del sc

            for learningrate in LEARNINGRATE:
                print("learningrate", learningrate)
                failed = 0
                for k in range(NOMBRE_DE_PASSE):
                    sia = SemaphoreIA(root, learningrate, failed, imshow)
                    weight_list = sia.training()
                    resp = sia.testing()
                    all_res[gray][blur].append([learningrate, resp])
                    print("Result:", resp)
                    save_test(root, resp, weight_list, gray, blur, learningrate)

    for key, val in all_res.items():
        print("Gray", key)
        for k, v_l in val.items():
            print("    Blur:", k)
            for item in v_l:
                print(  "        Learningrate:",
                        item[0],
                        "Résultat:   ",
                        item[1])

def save_test(root, resp, weight_list, gray, blur, learningrate):
    mt = MyTools()
    t = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    line = str(resp) + "    " + t + " " + str(gray) + " " + str(blur) + " " + str(learningrate) + "\n"
    fichier = root + "hyperparameter_tuning.txt"

    mt.write_data_in_file(line, fichier, "a")

    name = str(resp)
    np.save(root + 'weights/weights_' + name + '.npy', weight_list)

def compression(root, folder):
    t = datetime.today().strftime("%Y-%m-%d %H:%M")
    date = t.replace(" ", "_").replace(":", "_").replace("-", "_")
    name = root + "training_shot_" + date
    shutil.make_archive(name, 'zip', folder)


if __name__ == "__main__":
    # #t = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    # #line = str(90.3) + t + str(0)
    # #fichier = "/media/data/3D/projets/semaphore/" + "hyperparameter_tuning.txt"
    # #mt = MyTools()
    # #mt.write_data_in_file(line, fichier, "a")

    improve_ia()
