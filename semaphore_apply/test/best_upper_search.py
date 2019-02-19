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
from resize_blur_test import ResizeBlur
from compression_test import ShotsCompression
from semaphore_test import SemaphoreIA

MAXI = [250,250,250]
LOWER = [122, 90, 90]
DELTA = 25
NOMBRE = 10
NOMBRE_DE_PASSE = 1
GRAY = 0
SIZE = 40
BLUR = 6
TRAIN, TEST = 0, 1000
LEARNINGRATE = 0.022

def improve_ia(root):
    """Hyperparameter tuning"""

    mt = MyTools()
    all_res = {}
    upper = [0, 0, 0]

    for u in range(NOMBRE):
        for v in range(NOMBRE):
            for w in range(NOMBRE):
                upper[0] = MAXI[0] - u * DELTA
                upper[1] = MAXI[1] - v * DELTA
                upper[2] = MAXI[2] - w * DELTA

                # resize BLUR
                rb = ResizeBlur(root, SIZE, BLUR, LOWER, upper)
                rb.batch()
                del rb

                # compression
                sc = ShotsCompression(root, SIZE)
                sc.create_semaphore_npz()
                del sc

                for k in range(NOMBRE_DE_PASSE):
                    sia = SemaphoreIA(root, LEARNINGRATE, failed=0)
                    resp = sia.testing()
                    print("Result:", resp)
                    save_test(root, resp, GRAY, BLUR, LEARNINGRATE, LOWER, upper)

def save_test(root, resp, GRAY, BLUR, LEARNINGRATE, LOWER, upper):
    mt = MyTools()
    t = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    a = "{}   Date: {}  Gray: {}  Blur: {}  Learningrate: {}  Lower: {}  Upper: {}\n"
    line = a.format(format( round(resp, 2), '.2f'), t,
                            GRAY,
                            BLUR,
                            round(LEARNINGRATE, 3),
                            LOWER,
                            upper)
    print(line)
    fichier = os.path.join(root,  'semaphore_apply', 'test', "best_upper.txt")

    mt.write_data_in_file(line, fichier, "a")


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

    d = os.path.join(root)
    improve_ia(d)
