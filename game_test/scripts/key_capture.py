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


def input_one_chars():
    """ALL_KEYS = { events.AKEY: 'A',  ... """

    for key, val in ALL_KEYS.items():
        if gl.keyboard.events[key] == gl.KX_INPUT_JUST_ACTIVATED:
            gl.captured_text += val
            if len(gl.captured_text) % 22 == 0:
                gl.captured_text += "\n"

def special_keys():
    if gl.keyboard.events[events.PAD1] == gl.KX_INPUT_JUST_ACTIVATED:
        gl.one = 1
        gl.two = 0
        gl.enter = 0
        print("gl.one", gl.one)
        
    if gl.keyboard.events[events.PAD2] == gl.KX_INPUT_JUST_ACTIVATED:
        gl.two = 1
        gl.one = 0
        gl.enter = 0
        gl.captured_text = ""
        gl.captured_lettre = 0
        print("gl.two", gl.two)

def enter():
    if gl.keyboard.events[events.ENTERKEY] == gl.KX_INPUT_JUST_ACTIVATED:
        gl.enter = 1
        print("gl.enter", gl.enter)

def backspace():
    if gl.keyboard.events[events.BACKSPACEKEY] == gl.KX_INPUT_JUST_ACTIVATED:
        gl.backspace = 1
        print("gl.backspace", gl.backspace)
        try:
            gl.captured_text = gl.captured_text[:-1]
        except:
            gl.captured_text = ""
        
def input_text():
    input_one_chars()
    backspace()
    enter()
