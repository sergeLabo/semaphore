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
from semaphore_ia.semaphore_ia import SemaphoreIA


def improve_ia():
    """Avec le script train_semaphore.py"""

    root = MyTools().get_absolute_path(__file__)[:-21]
    print("Current directory:", root)

    # liste de [gray, blur, learningrate, res]
    all_res = {}

    size = 40  # fixe
    for gray in [0, 1]:
        print("gray", gray)
        all_res[gray] = {}
        for blur in [0, 1, 2, 3, 4, 5, 6]:
            print("blur", blur)
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

            for learningrate in [0.0210, 0.0215, 0.0220, 0.0225, 0.0230]:
                print("learningrate", learningrate)
                failed = 0
                sia = SemaphoreIA(root, learningrate, failed)
                sia.training()
                res = sia.testing()
                all_res[gray][blur].append([learningrate, res])

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
    improve_ia()
