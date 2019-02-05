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
from time import sleep

from pymultilame import MyTools
from resize_blur.resize_blur import ResizeBlur
from semaphore_ia.shot_compression import ShotsCompression
from semaphore_ia.train_semaphore import int_art
from semaphore_ia.ia_original import ia_original


def first_ia():
    """Avec le 1er script"""

    root = MyTools().get_absolute_path(__file__)[:-22]
    print("Current directory:", root)

    # liste de [gray, blur, learningrate, res]
    all_res = {}

    size = 40  # fixe
    for gray in [0, 1]:
        print("Gray", gray)
        all_res[gray] = {}
        for blur in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            print("Blur", blur)
            all_res[gray][blur] = []
            # resize blur
            rb = ResizeBlur(root, size, blur)
            rb.batch()
            del rb

            # compression
            train, test = 60000, 10000
            sc = ShotsCompression(root, train, test, size, gray)
            sc.create_semaphore_npz()
            del sc

            for learningrate in [0.001, 0.003, 0.005, 0.01, 0.02, 0.04,
                                 0.05, 0.06, 0.07, 0.1, 0.2, 0.3, 0.4]:
                print("Learningrate", learningrate)
                res = ia_original(learningrate)
                all_res[gray][blur].append([learningrate, res])

    print(all_res)
    for key, val in all_res.items():
        print("Gray", key)
        for k, v_l in val.items():
            print("    Blur:", k)
            for item in v_l:
                print(  "        Learningrate:",
                        item[0],
                        "Résultat:   ",
                        item[1])


def second_ia():
    """Avec le script train_semaphore.py"""

    root = MyTools().get_absolute_path(__file__)[:-22]
    print("Current directory:", root)

    # liste de [gray, blur, learningrate, res]
    all_res = {}

    size = 40  # fixe
    for gray in [0, 1]:
        all_res[gray] = {}
        for blur in [0, 1, 2, 3, 4, 5]:
            all_res[gray][blur] = []
            # resize blur
            rb = ResizeBlur(root, size, blur)
            rb.batch()
            del rb

            # compression
            train, test = 60000, 10000
            sc = ShotsCompression(root, train, test, size, gray)
            sc.create_semaphore_npz()
            del sc

            for learningrate in [0.001, 0.003, 0.005, 0.01, 0.02, 0.04,
                                 0.05, 0.06, 0.07, 0.1, 0.2, 0.3, 0.4]:
                res = int_art(learningrate)
                all_res[gray][blur].append([learningrate, res])

    print(all_res)
    for key, val in all_res.items():
        print("Gray", key)
        for k, v_l in val.items():
            print("    Blur:", k)
            for item in v_l:
                print(  "        Learningrate:",
                        item[0],
                        "Résultat:   ",
                        item[1])


if __name__ == "__main__":
    second_ia()
    #first_ia()
