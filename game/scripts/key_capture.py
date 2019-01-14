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

from bge import logic as gl

from scripts.keyboard_table import ALPHABET_KEYS


def keys():
    """ALPHABET_KEYS = { events.AKEY: 'A' ... """

    val = None
    for key, val in ALPHABET_KEYS.items():

        if gl.keyboard.events[key] == gl.KX_INPUT_JUST_ACTIVATED:
            print(val)

    return val
