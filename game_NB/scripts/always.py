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
from random import uniform, choice

from bge import logic as gl
from bge import render


def main():
    if gl.numero % 100 == 0:
        print("Shot n°", gl.numero)

    # Les différentes phases du jeu
    if gl.tempoDict['shot'].tempo == gl.chars_change:
        gl.chars = get_chars()
        display(gl.chars)
        # glissement rotation à chaque nouveau caractère du socle
        if not gl.static:
            #glissement_socle()
            change_socle_position()
            rotation_socle()

    if gl.tempoDict['shot'].tempo == gl.make_shot:
        make_shot()

    # Fin du jeu à nombre_shot_total
    end()

    # Toujours partout, tempo 'shot' commence à 0
    gl.tempoDict.update()

def change_socle_position():
    """socle position au centre = 0, 0, -6"""

    x = uniform(-4, 4)
    y = uniform(1, 10)
    z = uniform(-4, 3)

    gl.socle.worldPosition[0] = x
    gl.socle.worldPosition[1] = y
    gl.socle.worldPosition[2] = z

def rotation_socle():
    angle = uniform(-gl.rotation_socle, gl.rotation_socle)
    xyz = gl.socle.localOrientation.to_euler()
    xyz[1] = math.radians(angle)
    gl.socle.worldOrientation = xyz.to_matrix()

def glissement_socle():
    """Y = random
    coeff sur x et z pour avoir des varitions mais pas trop
    TODO: calcul stupide !
    si y = -1: x = -0.7 à 0.7, z = 1.25 à 0.6
    si y = 5 : x = -3.5 à 3.5, z = -6.25 à - 3.1
    """

    # Position au hazard sur y
    gl.y = uniform(-1, 5)

    # x et z dépendent de y
    gl.x = 0.70 * gl.y * uniform(-1, 1)
    gl.z = 0.50 * gl.y * uniform(-2.5, -1.2)

    # J'applique
    gl.socle.worldPosition[0] = gl.x
    gl.socle.worldPosition[1] = gl.y
    gl.socle.worldPosition[2] = gl.z

def end():
    if gl.numero == gl.nombre_shot_total:
        gl.endGame()

def display(chars):
    """Affichage de la lettre par rotation des bras.
    Variations des angles avec random
    """

    # 180, 90, 0
    angles = get_angles(chars)

    # Variation sur les angles
    # #angles[0] = angles[0] + uniform(-10, 10)
    # #angles[1] = angles[1] + uniform(-10, 10)
    # #angles[2] = angles[2] + uniform(-10, 10)

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
