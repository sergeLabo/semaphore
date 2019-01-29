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
Principe:   A partir d'un lot d'image d'apprentissage,
            crée une reconnaissance de forme.

Plus de documentation à:
    https://ressources.labomedia.org/l_intelligence_du_semaphore

Etape 1:
    Un gros lot (ex. 60000) d'images identifiées avec une lettre dans le nom
    du fichier est compressé dans un fichier *.npz. Ce fichier contient un
    array avec les images sur une ligne.

Etape 2:
    Création de l'intelligence

Etape 3:
    Test de l'efficacité de l'intelligence

Etape 4:
    print("Je suis très très intelligent, au moins autant que Einstein")

"""


import os
import numpy as np
import cv2

from pymultilame import MyTools

def sigmoid(x):
    """la fonction sigmoïde est une courbe en S:
    https://fr.wikipedia.org/wiki/Sigmo%C3%AFde_(math%C3%A9matiques)"""
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(z):
    """La dérivée de la fonction sigmoid,
    soit sigmoid' comme f' !
    """
    return z * (1 - z)

def relu(x):
    """Rectified Linear Unit:

    In the context of artificial neural networks, the rectifier is an
    activation function defined as the positive part of its argument.
    https://bit.ly/2HyT4ZO sur Wikipedia en.

    Rectifie les négatifs à 0:
    -1 > 0
     1 > 1
     """
    return np.maximum(0, x)

def relu_derivative(z):
    """La fonction de Heaviside (également fonction échelon unité, fonction
    marche d'escalier) est la fonction indicatrice de R.
    Une fonction fonction indicatrice, est une fonction définie sur un
    ensemble E qui explicite l’appartenance ou non à un sous-ensemble F de E
    de tout élément de E.
    C'est donc la fonction H (discontinue en 0) prenant la valeur 1 pour tous
    les réels positifs et la valeur 0 pour les réels strictement négatifs.
    """
    return np.asarray(z > 0, dtype=np.float32)

def get_ACTIVATIONS_derivative():
    """globals(): Return a dictionary representing the current global symbol table.
    This is always the dictionary of the current module (inside a function or
    method, this is the module where it is defined, not the module from which
    it is called).

    De [relu, relu, sigmoid], retourne [relu: relu_derivative,
                                        relu: relu_derivative,
                                        sigmoid: sigmoid_derivative]
    """
    return [globals()[f.__name__ + '_derivative'] for f in ACTIVATIONS]


# Variable globale
LAYERS = [40*40, 100, 100, 27]
ACTIVATIONS = [relu, relu, sigmoid]
ACTIVATIONS_derivative = get_ACTIVATIONS_derivative()
LEARNING_RATE = 0.10

CHARS_DICT = {  "a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7,
                "i": 8, "j": 9, "k": 10, "l": 11, "m": 12, "n": 13,
                "o": 14, "p": 15, "q": 16, "r": 17, "s": 18, "t": 19, "u": 20,
                "v": 21, "w": 22, "x": 23, "y": 24, "z": 25, " ": 26 }


def get_chars_label(img_file_name):
    """img_file_name = ... /semaphore_ia/shots/shot_000/shot_0_a.png
    Retourne le a
    remplace les chars anormaux en " "
    """
    l = img_file_name[-5]
    if l not in CHARS_DICT.keys():
        l = " "
    c = CHARS_DICT[l]
    return c


class ShotsCompression:

    def __init__(self):

        # Mon objet avec mes outils perso
        self.mytools = MyTools()

        # Valable avec exec ici ou en import
        self.root = self.mytools.get_absolute_path(__file__)[:-5]

        self.get_images_list()
        self.images = np.zeros((60000, 1600), dtype=np.uint8)
        self.labels = np.zeros((60000), dtype=np.uint8)
        self.images_test = np.zeros((10000, 1600), dtype=np.uint8)
        self.labels_test = np.zeros((10000), dtype=np.uint8)

    def get_images_list(self):
        """Liste de toutes les images avec leurs chemin absolu"""

        a = self.root + 'shots'
        print("Dossier des images:", a)

        self.images_list = self.mytools.get_all_files_list(a, ".png")
        print("Nombre d'images =", len(self.images_list))

    def create_semaphore_npz(self):
        """Lit toutes les images de
        /media/data/3D/projets/semaphore/semaphore_ia/shots

        60 000 images 40x40
        transformation du array 40,40 en array 1, 1600
        conversion 0:255 en 0:1

        x_train = images = 60000x1600
        y_train = labels = 60000x1

        x_test = images = 10000x1600
        y_test = labels = 10000x1

        concatenate dans un gros array
        enregistrement
        """
        i = 0

        for f in self.images_list:

            # Lecture de l'image f
            img = cv2.imread(f, 0)

            # Conversion du gris 0 à 255 en 0 à 1
            img = np.true_divide(img, 255)

            # Retaillage sur une ligne
            img.resize((1, 1600))

            # Labels
            label = get_chars_label(f)

            # Insertion par lignes
            if i < 60000:
                self.images[i] = img
                self.labels[i] =  label
            else:
                self.images_test[i - 60000] = img
                self.labels_test[i - 60000] =  label

            # Pour faire patienter les mondoshawans et les mangalores
            if i % 100 == 0:
                print("Image:", i, "Taille:", self.images.shape)
            i += 1

        print("Vérification: taille des array:",
                self.images.shape,
                self.labels.shape,
                self.images_test.shape,
                self.labels_test.shape)

        self.save_train()

    def save_train(self):
        """Enregistre les arrays images et labels dans un fichier compressé
        ./semaphore.npz
        x_train = images = 60000x1600
        y_train = labels = 60000x1
        """

        outfile = self.root + 'semaphore.npz'
        np.savez_compressed(outfile, **{"x_train": self.images,
                                        "y_train": self.labels,
                                        "x_test":  self.images_test,
                                        "y_test":  self.labels_test})

        print('Fichier compressé =', outfile, '\n\n\n')


def get_weight():
    """LAYERS = [1600, 100, 100, 27]
    np.random.randn(a, b)
    Retourne un array de shape=(a, b) from the standard normal distribution.
    """
    return [np.random.randn(LAYERS[k + 1], LAYERS[k]) / np.sqrt(LAYERS[k])\
                                              for k in range(len(LAYERS) - 1)]
    
def get_eye():
    """An array where all elements are equal to zero, except for the k-th
    diagonal, whose values are equal to one.
    Crée une diagonale de 1
    1 0 0
    0 1 0
    0 0 1
    """
    return np.eye(27, 27)

def transpose(img):
    """Same as self.transpose(), except that self is returned if self.ndim < 2.
    ndmin : int, optional
    Specifies the minimum number of dimensions that the resulting
    array should have. Ones will be pre-pended to the shape as
    needed to meet this requirement.
    """
    return np.array(img, ndmin=2).T

def get_dot(a, b):
    """ np.dot
    In mathematics, the dot product or scalar product is an algebraic
    operation that takes two equal-length sequences of numbers
    (usually coordinate vectors) and returns a single number.

    Returns the dot product of a and b. If a and b are both scalars
    or both 1-D arrays then a scalar is returned;
    otherwise an array is returned.
    If out is given, then it is returned.
    """
    return np.dot(a, b)


class SemaphoreIA:
    """Training:
    A partir des images stockées dans semaphore.npz
    qui contient:
    x_train = images = 60000x1600 avec valeur de gris entre 0 et 1
    y_train = labels = 60000x1 = une lettre de l'alphabet sémaphore

    Testing:
    Avec un jeu de n shots à faire
    """

    def __init__(self):
        """semaphore.npz doit être dans le même dossier que ce script"""
        
        # Mon objet avec mes outils perso
        self.mytools = MyTools()
        
        # Valable avec exec ici ou en import
        self.root = self.mytools.get_absolute_path(__file__)[:-5]
        
        npz_file = np.load(self.root + 'semaphore.npz')
        self.x_train, self.y_train = npz_file['x_train'], npz_file['y_train']
        self.x_test, self.y_test = npz_file['x_test'], npz_file['y_test']

        # list de array (100, 1600) (100, 100) (27, 100)
        self.weight = get_weight()
        
    def ia_training(self):
        """Apprentissage avec les images de semaphore.npz"""

        print("Training...")

        # Oeil ?: array 27x27 avec diagonale de 1
        eye = get_eye()

        # Un dict pour stocker quoi ?
        A_dict = {}

        for i, (img, val) in enumerate(zip(self.x_train, self.y_train)):
            img = transpose(img)

            A_dict[0] = img
            for k in range(len(LAYERS)-1):
                z = get_dot(self.weight[k], img)
                img = ACTIVATIONS[k](z)
                A_dict[k + 1] = img

            da = img - eye[:,[val]]

            for k in range(len(LAYERS)-2, -1, -1):
                dz = da * ACTIVATIONS_derivative[k](A_dict[k+1])
                dW = get_dot(dz, A_dict[k].T)
                da = np.dot(self.weight[k].T, dz)
                self.weight[k] -= LEARNING_RATE * dW[1,:]
                
            # Pour faire patienter les mondoshawans et les mangalores
            if i % 100 == 0:
                print("Image:", i)
                
        # Save
        np.save(self.root + 'weights', self.weight)
        
    def ia_testing(self):
        print("Testing...")
        # Load weights
        weight = np.load(self.root + 'weights.npy')
        
        S = 0
        for a, d in zip(self.x_test, self.y_test):
            for k in range(len(LAYERS)-1):
                a = ACTIVATIONS[k](np.dot(weight[k], a))
            if np.argmax(a) == d:
                S += 1
                
        print("Accuracy: {}".format(round((100.0 * S / len(self.x_test)), 1)))


def test_0():
    for x in [2, 5, -2.5, -0.25, 44, -77, -7.01]:
        a = relu(x)
        b = relu_derivative(x)
        print("relu de", x, "=", a, "de type =", type(a))
        print("relu_derivative de", x, "=", b, "de type =", type(b))

def test_1():
    """
    [0 1 2 3 4]
    (5,)
    [[0]
     [1]
     [2]
     [3]
     [4]]
    (5, 1)
    """
    img = np.arange(5)
    print(img)
    print(img.shape)
    a = transpose(img)
    print(a)
    print(a.shape)

if __name__ == "__main__":
    # Test de fonctions
    #test_0()
    #test_1()

    # Compression des images
    # #sc = ShotsCompression()
    # #sc.create_semaphore_npz()

    # ia
    sia = SemaphoreIA()
    sia.ia_training()
    sia.ia_testing()
