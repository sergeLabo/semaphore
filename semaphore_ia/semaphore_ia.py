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
Training: Calcule le fichier 'd'intelligence' weight.npy avec 60 000 images

Testing: Teste avec 10 000 images

Le PEP 8 80 colonnes n'est pas respecté pour donner la priorité aux explications
"""


import shutil
import numpy as np
import cv2
from pymultilame import MyTools


def sigmoid(x):
    """La fonction sigmoïde est une courbe en S:
    https://fr.wikipedia.org/wiki/Sigmo%C3%AFde_(math%C3%A9matiques)
    """

    return 1 / (1 + np.exp(-x))

def sigmoid_prime(z):
    """La dérivée de la fonction sigmoid,
    soit sigmoid' comme f' !
    """

    return z * (1 - z)

def relu(x):
    """Rectifie les négatifs à 0:
    -1 > 0
     1 > 1
     Rectified Linear Unit:

    In the context of artificial neural networks, the rectifier is an
    activation function defined as the positive part of its argument.
    https://bit.ly/2HyT4ZO sur Wikipedia en.
     """

    return np.maximum(0, x)

def relu_prime(z):
    """Fonction: 1 pour tous les réels positifs ou nuls et 0 pour les réels négatifs.

    La fonction de Heaviside (également fonction échelon unité, fonction
    marche d'escalier) est la fonction indicatrice de R.
    Une fonction fonction indicatrice, est une fonction définie sur un
    ensemble E qui explicite l’appartenance ou non à un sous-ensemble F de E
    de tout élément de E.
    """

    return np.asarray(z > 0, dtype=np.float32)


class SemaphoreIA:
    """Réseau de neuronnes Perceptron multicouches."""

    def __init__(self, root, learningrate, failed=0):
        self.root = root
        self.learningrate = learningrate
        self.failed = failed
        self.tools = MyTools()

        # Dossier des ratés
        if self.failed:
            # Suppression du dossier failed et recréation pour le vider
            try:
                shutil.rmtree(self.root + 'failed')
            except:
                print('Pas de dossier failed')
            self.tools.create_directory(self.root + 'failed')

        # Réseau de neurones: colonne 1600 en entrée, 2 nodes de 100, sortie de 27 caractères
        self.layers = [1600, 100, 100, 27]
        # Fonction d'activation: imite l'activation d'un neuronne
        self.activations = [relu, relu, sigmoid]

        fichier = np.load(self.root + 'semaphore.npz')
        self.x_train, self.y_train = fichier['x_train'], fichier['y_train']
        self.x_train = 1 - self.x_train
        self.x_test, self.y_test = self.x_train[50000:,:], self.y_train[50000:]
        self.x_train, self.y_train = self.x_train[:50000,:], self.y_train[:50000]

        # Affichage des images pour distraire
        cv2.namedWindow('img')

    def training(self):
        """Apprentissage avec 60 000 images
        Poids enregistré dans weights.npy
        """

        print("Training...")

        # Matrice diagonale de 1
        diagonale = np.eye(27, 27)

        # globals() Return a dictionary representing the current global symbol table.
        self.activations_prime = [globals()[fonction.__name__ + '_prime'] for fonction in self.activations]

        node_dict = {}

        # Liste des poids
        # Initialisation des poids des nodes, pour ne pas à être à 0
        # Construit 3 matrices (100x1600, 100x100, 27x100)
        # /np.sqrt() résultat expérimental de l'initialisation de Glorot He Xavier
        weight_list = [np.random.randn(self.layers[k+1], self.layers[k]) / \
                       np.sqrt(self.layers[k]) for k in range(len(self.layers)-1)]

        # vecteur_ligne = image en ligne à la 1ère itération
        # nombre_lettre = nombre correspondant à la lettre de l'image
        # i pour itération, vecteur_colonne = x_train de i, nombre_lettre = y_train de i
        for i, (vecteur_ligne, nombre_lettre) in enumerate(zip(self.x_train, self.y_train)):

            # Affichage pour distraire les mangalore
            # TODO: mettre ça dans un truc à l'ext de cette méthode
            if i % 10000 == 0:
                print(i, nombre_lettre)
                img = vecteur_ligne.reshape(40,40) * 255
                img = cv2.resize(img, (600, 600), interpolation=cv2.INTER_AREA)
                cv2.imshow("img", img)
                cv2.waitKey(1)

            # la ligne devient colonne
            vecteur_colonne = np.array(vecteur_ligne, ndmin=2).T

            # Forward propagation
            node_dict[0] = vecteur_colonne
            for k in range(len(self.layers)-1):
                # weight_list[k] (100x1600, 100x100 27x100) vecteur_colonne (1600,)
                # z de format 100 x 1
                z = np.dot(weight_list[k], vecteur_colonne)

                # self.activations = non linéaire sinon sortie fonction linéaire de l'entrée
                # imite le seuil d'activation électrique du neuronne
                vecteur_colonne = self.activations[k](z)

                node_dict[k+1] = vecteur_colonne

            # Retro propagation, delta_a = écart entre la sortie réelle et attendue
            delta_a = vecteur_colonne - diagonale[:,[nombre_lettre]]
            # Parcours des nodes en sens inverse pour corriger proportionnellemnt
            # les poids en fonction de l'erreur par rapport à la valeur souhaitée
            # Descente du Gradient stochastique
            for k in range(len(self.layers)-2, -1, -1):
                delta_z = delta_a * self.activations_prime[k](node_dict[k+1])
                delta_w = np.dot(delta_z, node_dict[k].T)
                delta_a = np.dot(weight_list[k].T, delta_z)
                # Pour converger vers le minimum d'erreur
                weight_list[k] -= self.learningrate * delta_w

        # Dans un fichier
        np.save(self.root + 'weights.npy', weight_list)
        print('weights.npy enregistré')
        cv2.destroyAllWindows()

    def testing(self):
        """Teste avec 10 000 images, retourne le ratio de bon résultats"""

        print("Testing...")

        weight_list = np.load(self.root + 'weights.npy')

        # Nombre de bonnes reconnaissance
        success = 0

        # Dict avec le nommbre d'erreurs par lettre
        failed_dict = {}

        for vecteur_ligne, nombre_lettre in zip(self.x_test, self.y_test):
            # image en ligne au 1er passage pour les failed
            img = vecteur_ligne.copy()

            for k in range(len(self.layers)-1):
                vecteur_ligne = self.activations[k](np.dot(weight_list[k],
                                                      vecteur_ligne))

            reconnu = np.argmax(vecteur_ligne)
            if reconnu == nombre_lettre:
                success += 1
            else:
                # TODO: mettre ça dans un truc à l'ext de cette méthode
                if self.failed:
                    self.write_failed(img, nombre_lettre, reconnu, success)
                if nombre_lettre in failed_dict:
                    failed_dict[nombre_lettre] += 1
                else:
                    if self.failed:
                        self.tools.create_directory(self.root + 'failed' + '/bad_' + str(nombre_lettre))
                        failed_dict[nombre_lettre] = 1

        if self.failed:
            sorted_by_value = sorted(failed_dict.items(), key=lambda kv: kv[1], reverse=True)
            print(sorted_by_value)

        resp = 100.0 * success / len(self.x_test)
        return resp

    def write_failed(self, img, nombre_lettre, reconnu, S):
        """Les images avec erreur de reconnaisance sont copiées dans
        /semaphore/failed/bad_11/11_6_9067.png
        11 est la lettre k, donc dans le dossier il ny a que la lettre k
        et le 2ème nombre est la lettre reconnue fausse
        """
        name = str(nombre_lettre) + '_' + str(reconnu) + '_'  + str(S) + '.png'
        fichier = self.root + 'failed' + '/bad_' + str(nombre_lettre) + '/' + name
        img = img.reshape(40,40) * 255
        cv2.imwrite(fichier, img)


if __name__ == "__main__":

    print(MyTools().get_absolute_path(__file__))
    root = MyTools().get_absolute_path(__file__)[:-28]
    print("Current directory:", root)

    for i in range(5):
        print("Petit test de l'influence du random dans la liste des poids")
        learningrate = 0.022
        failed = 0
        sia = SemaphoreIA(root, learningrate, failed)
        sia.training()
        resp = sia.testing()
        print("Learningrate: {} Résultat {}".format(learningrate, round(resp, 1)))
