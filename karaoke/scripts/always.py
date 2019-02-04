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

'''
Lancé à chaque frame durant tout le jeu.
'''


from bge import logic as gl
from pymultilame import UdpClient
import ast

def main():
    gl.data = network()
    print(gl.data)
    # Toujours partout, tempo 'toto' commence à 0
    gl.tempoDict.update()
    gl.text_obj.resolution = 64

def network():
    """Le message reçu est:
    {"text": "texte latin", "indice":10}
    """
    gl.clt = UdpClient()
    try:
        data, addr = gl.clt.listen()
        data = ast.litteral_eval(data)
    except:
        data = ""
    return data
