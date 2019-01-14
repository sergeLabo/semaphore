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
Lancé à chaque frame durant tout le jeu.
"""

from time import sleep
import math
from bge import logic as gl
from bge import render
from scripts.key_capture import keys

"""
xyz = own.localOrientation.to_euler()
xyz[2] = math.radians(45)
own.localOrientation = xyz.to_matrix()
"""

def main():
    # Toujours partout
    gl.tempoDict.update()
    
    # Capture du clavier
    keys()
    
    # Les différentes phases du jeu
    if gl.tempoDict['shot'].tempo == 1:
        gl.chars = get_chars()
        display(gl.chars)
        
    if gl.tempoDict['shot'].tempo == 3:
        make_shot()

    # Avance de la video
    video_refresh()
    end()

def end():
    if gl.numero == 60001:
        gl.endGame()
    
def video_refresh():
    """call this function every frame to ensure update of the texture."""
    
    gl.my_video.refresh(True)

def display(chars):
    angles = get_angles(chars)

    xyz = gl.bras_central.worldOrientation.to_euler()
    xyz[1] = math.radians(angles[0])
    gl.bras_central.localOrientation = xyz.to_matrix()

    xyz = gl.bras_gauche.localOrientation.to_euler()
    xyz[1] = math.radians(angles[1])
    gl.bras_gauche.localOrientation = xyz.to_matrix()
    
    xyz = gl.bras_droit.localOrientation.to_euler()
    xyz[1] = math.radians(angles[2])
    gl.bras_droit.localOrientation = xyz.to_matrix()
    
def get_angles(chars):
    try:
        angles = gl.lettre_table[chars]
    except:
        angles = (0, 0, 0)
    return angles

def get_chars():
    chars = gl.text_str[gl.lettre]
    chars = chars.lower()
    gl.lettre += 1
    return chars
    
def make_shot():
    
    gl.name_file_shot = gl.shot_directory + '/shot_' + str(gl.numero) + '_' + gl.chars + '.png'
                        
    render.makeScreenshot(gl.name_file_shot)
    print(gl.chars, '--> shot ' + str(gl.numero))
    gl.numero += 1
