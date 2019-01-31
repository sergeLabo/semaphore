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

Etape 1:
    Création de l'intelligence

Etape 2:
    Test de l'efficacité de l'intelligence

Etape 3:
    print("Je suis très très intelligent, au moins autant que Einstein")

"""


import os
import numpy as np
import cv2
import threading

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

    def __init__(self, root, size, learning_rate):
        """semaphore.npz doit être dans le même dossier que ce script"""

        self.size = size
        self.learning_rate = learning_rate
        
        # Mon objet avec mes outils perso
        self.mytools = MyTools()
        
        # Valable avec exec ici ou en import
        self.root = root
        print("Dossier semaphore", self.root)
        
        npz_file = np.load(self.root + 'semaphore.npz')
        self.x_train, self.y_train = npz_file['x_train'], npz_file['y_train']
        self.x_test, self.y_test = npz_file['x_test'], npz_file['y_test']

        self.activations = [relu, relu, sigmoid]
        self.activations_derivative = self.get_activations_derivative()
        self.layers = [self.size**2, 100, 100, 27]
        self.weight = self.get_weight()
        
        # display
        self.disp = True
        self.img = np.zeros((self.size, self.size), dtype=np.uint8)
        self.display_thread()

    def get_weight(self):
        """self.layers = [1600, 100, 100, 27]
        np.random.randn(a, b)
        Retourne un array de shape=(a, b) from the standard normal distribution.
        """
        return [np.random.randn(self.layers[k + 1], self.layers[k]) / np.sqrt(self.layers[k])\
                                                  for k in range(len(self.layers) - 1)]

    def get_activations_derivative(self):
        """globals(): Return a dictionary representing the current global symbol table.
        This is always the dictionary of the current module (inside a function or
        method, this is the module where it is defined, not the module from which
        it is called).

        De [relu, relu, sigmoid], retourne [relu: relu_derivative,
                                            relu: relu_derivative,
                                            sigmoid: sigmoid_derivative]
        """
        return [globals()[f.__name__ + '_derivative'] for f in self.activations]
    
    def ia_training(self):
        """Training: Apprentissage avec les images de semaphore.npz"""

        # Oeil ?: array 27x27 avec diagonale de 1
        eye = get_eye()
        # Un dict pour stocker quoi ?
        A_dict = {}

        for i, (img, val) in enumerate(zip(self.x_train, self.y_train)):
            # Affichage               
            self.mangalore(i, img)
            
            img = transpose(img)

            A_dict[0] = img
            for k in range(len(self.layers)-1):
                z = get_dot(self.weight[k], img)
                img = self.activations[k](z)
                A_dict[k + 1] = img

            da = img - eye[:,[val]]

            for k in range(len(self.layers)-2, -1, -1):
                dz = da * self.activations_derivative[k](A_dict[k+1])
                dW = get_dot(dz, A_dict[k].T)
                da = np.dot(self.weight[k].T, dz)
                self.weight[k] -= learning_rate * dW[1,:]
                  
        # Save
        np.save(self.root + 'weights', self.weight)
        # Fin du thread
        self.disp = False

    def ia_testing(self):
        print("Testing...")
        # Load weights
        weight = np.load(self.root + 'weights.npy')
        
        S = 0
        for a, d in zip(self.x_test, self.y_test):
            for k in range(len(self.layers)-1):
                a = self.activations[k](np.dot(weight[k], a))
            if np.argmax(a) == d:
                S += 1
                
        print("Accuracy: {}%".format(round((100.0 * S / len(self.x_test)), 1)))

    def mangalore(self, i, img):  
        # Pour faire patienter les mondoshawans et les mangalores
        if i % 1000 == 0:
            # img.shape = (1600,)
            img_show = np.reshape(img, (self.size, self.size))
            img_show = cv2.resize(img_show, (600, 600), interpolation=cv2.INTER_AREA)
            self.img = img_show
            print("Image:", i)
                
    def display_thread(self):
        t = threading.Thread(target=self.display)
        t.start()        
        
    def display(self):
        cv2.namedWindow('Image')
        while self.disp:
            cv2.imshow('Image', self.img)
            # Echap
            if cv2.waitKey(33) == 27:  
                break
        cv2.destroyAllWindows()
                

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
    root = MyTools().get_absolute_path(__file__)[:-18]
    print("Current directory:", root)

    # ia
    size = 40
    
    # Variable globale
    learning_rate = 0.2

    sia = SemaphoreIA(root, size, learning_rate)
    sia.ia_training()
    sia.ia_testing()
