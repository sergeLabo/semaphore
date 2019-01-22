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
Capture d'un texte au clavier
"""

from time import sleep

from bge import events
from bge import logic as gl

from scripts.keyboard_table import ALL_KEYS

""" 
if gl.keyboard.events[events.WKEY]     == gl.KX_INPUT_JUST_ACTIVATED:
"""

def keyboard_text():
    """ALL_KEYS = { events.AKEY: 'A',  ... """

    gl_text = ""

    if gl.keyboard.events[events.ENTERKEY] == gl.KX_INPUT_JUST_ACTIVATED:
        gl.enter = 1
        print("gl.enter", gl.enter)

    if gl.keyboard.events[events.BACKSPACEKEY] == gl.KX_INPUT_JUST_ACTIVATED:
        gl.backspace = 1
        print("gl.backspace", gl.backspace)
        try:
            gl_text = gl_text[:-1]
        except:
            gl_text = ""
        
    for key, val in ALL_KEYS.items():
        if gl.keyboard.events[key] == gl.KX_INPUT_JUST_ACTIVATED:
            print(val)
            gl_text += val
            
    print(gl_text)

def special_keys():
    if gl.keyboard.events.ONEKEY == gl.KX_INPUT_JUST_ACTIVATED:
        gl.one = 1
        print("gl.one", gl.one)
        
    if gl.keyboard.events.TWOKEY == gl.KX_INPUT_JUST_ACTIVATED:
        gl.two = 1
        print("gl.two", gl.two)
