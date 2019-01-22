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

    # Le dossier courrant est le dossier dans lequel est le *.blend
    gl.current_dir = gl.expandPath('//')
    print('Dossier courant depuis once.py {}'.format(gl.current_dir))

    # Configuration dans *.ini
    gl.ma_conf = MyConfig(gl.current_dir + "scripts/semaphore.ini")
    gl.conf = gl.ma_conf.conf

    print("\nConfiguration du jeu semaphore:")
    print(gl.conf, "\n")

def set_variable():
    # Numero de shot de 0 à infini
    gl.numero = 0

    # Numéro du cycle de lecture des textes
    gl.cycle = 0

    # nombre de shot total
    gl.nombre_shot_total = gl.conf['modifiable']['nombre_shot_total']
    
    # Nom du fichier: les dossiers changent mais les indices continuent
    gl.name_file_shot = gl.current_dir + 'shot/shot_' + str(gl.numero) + '.png'

    # conversion lettre vers angle
    gl.lettre_table = lettre_table

    # Dossier d'enregistrement des images
    gl.shot_directory = gl.conf['modifiable']['path']

    # Nombre d'images par dossier
    gl.nombre_de_fichiers_par_dossier = gl.conf['modifiable']['nombre_de_fichiers_par_dossier']

    # Numéro de frame dans le cycle de chaque lettre
    gl.chars = ""
    gl.chars_change = gl.conf['modifiable']['chars_change']

    # Numéro de frame dans le cycle de chaque lettre 
    gl.make_shot = gl.conf['modifiable']['make_shot']

    # Position de départ du socle
    gl.x = 0
    gl.y = 0
    gl.z = 0

    # Déplacement du socle
    gl.static = gl.conf['modifiable']['static']
    gl.rotation_socle =gl.conf['modifiable']['rotation_socle']
    
def keys_init():
    gl.one = 0
    gl.two = 0
    gl.enter = 0
    gl.backspace = 0
    gl.keyboard_text = ""
    
def test_path_to_shot_directory():
    if os.path.exists(gl.shot_directory) and gl.shot_directory[-4:] == "shot":
        print()
    else:
        print("Le dossier /shot n'existe pas !")
        print("Vous devez le créer et définir son chemin dans semaphore.ini")
        print("Pas de slash à la fin de shot")
        sleep(10)
        os._exit(0)
  
def create_shot_directory():
    """Non utilisé, ce dossier doit être défini dans le *.ini"""
    # Création du dossier shot
    mt = MyTools()
    mt.create_directory(gl.current_dir + 'shot')
    
def create_directories():
    """
    Création de n dossiers
    /media/data/3D/projets/semaphore/game/shot/shot_0/shot_a_0.png
    """
    mt = MyTools()
    
    # Nombre de dossiers nécessaires
    n = int(gl.nombre_shot_total / gl.nombre_de_fichiers_par_dossier)
    
    for i in range(n):
        directory = gl.shot_directory + '/shot_' + str(i).zfill(3)
        mt.create_directory(directory)
    
def set_tempo():
    tempo_liste = [("shot", int(gl.conf['modifiable']['shot_every']))]

    # Comptage des frames par lettre
    gl.tempoDict = Tempo(tempo_liste)

def get_texte():
    # Récup des textes du dossier texte
    dossier = gl.current_dir + 'scripts/texte/'

    # Le texte à lire
    gl.text_str = get_text_str_from_blender(dossier)
    print('Longueur du texte =', len(gl.text_str))

    # L'indice de la lettre à lire
    gl.lettre = 0

def film_error():
    print("Une video valide doit être définie dans semaphore.ini")
    print("Le fichier doit être dans game/scripts/video/")
    sleep(10)
    os._exit(0)
        
def set_video():
    # identify a static texture by name
    #matID = texture.materialID(gl.plane, 'IMlogo-labomedia.png')
    matID = texture.materialID(gl.plane, 'MAblack')
    
    # create a dynamic texture that will replace the static texture
    gl.my_video = texture.Texture(gl.plane, matID)

    # define a source of image for the texture, here a movie
    try:
        movie = gl.expandPath('//scripts/video/' + gl.conf['modifiable']['film'])
        print('Movie =', movie)
    except:
        film_error()
            
    try:
        s = os.path.getsize(movie)
        print("Taille du film:", s)
    except:
        film_error()
    
    gl.my_video.source = texture.VideoFFmpeg(movie)
    gl.my_video.source.scale = False

    # Infinite loop
    gl.my_video.source.repeat = -1

    # Vitesse normale: < 1 ralenti, > 1 accélère
    gl.my_video.source.framerate = 1.0
    
    # quick off the movie, but it wont play in the background
    gl.my_video.source.play()

def get_semaphore_objet():
    all_obj = blendergetobject.get_all_objects()
    gl.bras_central = all_obj['main']
    gl.bras_gauche = all_obj['gauche']
    gl.bras_droit = all_obj['droit']
    gl.socle = all_obj['socle']

    if gl.conf['modifiable']['video']:
        gl.plane = all_obj['Plane']
        
def main():
    """Lancé une seule fois à la 1ère frame au début du jeu par main_once."""

    print("Initialisation des scripts lancée un seule fois au début du jeu.")

    # Récupération de la configuration
    get_conf()

    # l'ordre est important
    set_variable()
    keys_init()
    test_path_to_shot_directory()
    create_directories()
    set_tempo()
    get_texte()
    get_semaphore_objet()
    
    if gl.conf['modifiable']['video']:
        set_video()
    
    print("Le bonjour des mondoshawan !")
