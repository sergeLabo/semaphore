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
Ce script est appelé par main_init.main dans blender
Il ne tourne qu'une seule fois pour initier lss variables
qui seront toutes des attributs du bge.logic (gl)
Seuls les attributs de logic sont stockés en permanence.
"""


import os
from time import sleep

from bge import logic as gl
from bge import texture
from bge import render

from pymultilame import blendergetobject
from pymultilame import Tempo, MyConfig, MyTools

from scripts.get_texte import get_text_str_from_blender
from scripts.angleSemaphore import lettre_table


def get_conf():
    """Récupère la configuration depuis le fichier *.ini."""

    # Chemin courrant
    abs_path = MyTools().get_absolute_path(__file__)
    print("Chemin courrant", abs_path)

    # Nom du script
    name = os.path.basename(abs_path)
    print("Nom de ce script:", name)

    # Abs path de semaphore sans / à la fin
    parts = abs_path.split("semaphore")
    gl.root = os.path.join(parts[0], "semaphore")
    print("Path de semaphore:", gl.root)

    # Dossier *.ini
    ini_file = os.path.join(gl.root, "global.ini")
    gl.ma_conf = MyConfig(ini_file)
    gl.conf = gl.ma_conf.conf

    print("\nConfiguration du jeu semaphore:")
    print(gl.conf, "\n")

def set_variable():
    # Numero de shot de 0 à infini
    gl.numero = 0

    # Numéro du cycle de lecture des textes
    gl.cycle = 0

    # nombre de shot total
    gl.nombre_shot_total = gl.conf['ia']['training'] + gl.conf['ia']['testing']

    # conversion lettre vers angle
    gl.lettre_table = lettre_table

    # Nombre d'images par dossier
    gl.nombre_de_fichiers_par_dossier = gl.conf['blend']['nombre_de_fichiers_par_dossier']

    # Numéro de frame dans le cycle de chaque lettre
    gl.chars = ""
    gl.chars_change = gl.conf['blend']['chars_change']

    # Numéro de frame dans le cycle de chaque lettre
    gl.make_shot = gl.conf['blend']['make_shot']

    # Position de départ du socle
    gl.x = 0
    gl.y = 0
    gl.z = 0

    # Déplacement du socle
    gl.static = gl.conf['blend']['static']
    gl.rotation_socle = gl.conf['blend']['rotation_socle']
    gl.glissement_socle = gl.conf['blend']['glissement_socle']

def create_directories():
    """
    Création de n dossiers
    un fichier = ./semaphore/shot/shot_0/shot_a_0.png
    """

    # Dossier d'enregistrement des images
    gl.shot_directory = os.path.join(gl.root, 'training_shot')
    print("Dossier des shots:", gl.shot_directory)

    # Si le dossier n'existe pas, je le crée
    mt = MyTools()
    mt.create_directory(gl.shot_directory)

    # Nombre de dossiers nécessaires
    n = int(gl.nombre_shot_total / gl.nombre_de_fichiers_par_dossier) + 1

    for i in range(n):
        directory = os.path.join(gl.shot_directory, 'shot_' + str(i).zfill(3))
        mt.create_directory(directory)

def set_tempo():
    tempo_liste = [ ("shot", int(gl.conf['blend']['shot_every'])),
                    ("frame", 999999999)]

    # Comptage des frames par lettre
    gl.tempoDict = Tempo(tempo_liste)

def get_texte():
    # Récup des textes du dossier texte
    dossier = gl.root + '/get_training_shot/scripts/texte/'

    # Le texte à lire
    gl.text_str = get_text_str_from_blender(dossier)
    print('Longueur du texte =', len(gl.text_str))

    # L'indice de la lettre à lire
    gl.lettre = 0

def get_semaphore_objet():
    all_obj = blendergetobject.get_all_objects()
    gl.bras_central = all_obj['main']
    gl.bras_gauche = all_obj['gauche']
    gl.bras_droit = all_obj['droit']
    gl.socle = all_obj['socle']

# #def solution_max():
    # #gl.CHARS_DICT = {   "a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6,
                        # #"h": 7, "i": 8, "j": 9, "k": 10, "l": 11, "m": 12,
                        # #"n": 13, "o": 14, "p": 15, "q": 16, "r": 17, "s": 18,
                        # #"t": 19, "u": 20, "v": 21, "w": 22, "x": 23, "y": 24,
                        # #"z": 25, " ": 26 }


def main():
    """Lancé une seule fois à la 1ère frame au début du jeu par main_once."""

    print("Initialisation des scripts lancée un seule fois au début du jeu.")

    # Récupération de la configuration
    get_conf()

    # l'ordre est important
    set_variable()
    create_directories()
    set_tempo()
    get_texte()
    get_semaphore_objet()

    print("Le bonjour des mondoshawan !")
