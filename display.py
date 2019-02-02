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
class pour affichage des images dans opencv

"""

import cv2
import numpy as np
import threading


class Display:

    def __init__(self, size, name):
        
        self.size = size
        self.name = name
        self.disp = True
        self.img = np.zeros((self.size, self.size), dtype=np.uint8)
        
    def display_thread(self):
        t = threading.Thread(target=self.display)
        t.start()        
        
    def display(self):
        cv2.namedWindow(self.name)
        while self.disp:
            cv2.imshow(self.name, self.img)
            # Echap
            if cv2.waitKey(33) == 27:  
                break
        self.disp = False
        cv2.destroyAllWindows()

                
if __name__ == "__main__":

    d = Display(100, 'toto')
    d.display_thread()
