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
from random import uniform

from bge import logic as gl
from bge import render

from scripts.key_capture import keys

"""
xyz = own.localOrientation.to_euler()
xyz[2] = math.radians(45)
own.localOrientation = xyz.to_matrix()
"""

def main():
    # Capture du clavier
    keys()

    # glissement permanent du socle
    glissement_socle()

    #print(gl.tempoDict['shot'].tempo , gl.chars)
    
    # Les différentes phases du jeu
    if gl.tempoDict['shot'].tempo == gl.chars_change:
        gl.chars = get_chars()
        display(gl.chars)
        #change_socle_position()
        
    if gl.tempoDict['shot'].tempo == gl.make_shot:
        make_shot()

    # Avance de la video
    video_refresh()
    end()

    # Toujours partout, tempo 'shot' commence à 0
    gl.tempoDict.update()
    
def glissement_socle():

    k = 0.08
    
    gl.x += gl.sensx * k
    if gl.x < -5 or gl.x > 5:
        gl.sensx = -gl.sensx
         
    gl.y += gl.sensy * k
    if gl.y < -5 or gl.y > 100:
        gl.sensy = -gl.sensy
    
    gl.z += gl.sensz * k
    if gl.z < -2 or gl.z > 5:
        gl.sensz = -gl.sensx

    gl.socle.worldPosition[0] = gl.x
    gl.socle.worldPosition[1] = gl.y
    gl.socle.worldPosition[2] = gl.z
    
def change_socle_position():
    """socle position au centre = 0, 0, -6"""

    x = uniform(-10, 10)
    y = uniform(-5, 50)
    z = uniform(-4, 10)

    gl.socle.worldPosition[0] = x
    gl.socle.worldPosition[1] = y
    gl.socle.worldPosition[2] = z

def end():
    if gl.numero == gl.nombre_shot_total:
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
    
    
    name_file_shot = get_name_file_shot()
    print(gl.name_file_shot)
    render.makeScreenshot(name_file_shot)
    
    #print(gl.chars, '--> shot ' + str(gl.numero))
    gl.numero += 1

def get_name_file_shot():
    """/media/data/3D/projets/semaphore/game/shot/shot_0/shot_a_0.png
    60000
    4000
    je suis à gl.numero = 5555
    numero du dossier = n = 1 = int(5555/4000)

    """

    n = int(gl.numero / gl.nombre_de_fichiers_par_dossier)
    
    gl.name_file_shot = gl.shot_directory + '/shot_' + str(n).zfill(3) +\
                        '/shot_' + str(gl.numero) + '_' + gl.chars + '.png'

    return gl.name_file_shot
