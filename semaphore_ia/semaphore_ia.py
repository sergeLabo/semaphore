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
"""


import numpy as np
import cv2
from pymultilame import MyTools


def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_prime(z):
    return z * (1 - z)

def relu(x):
    return np.maximum(0, x)

def relu_prime(z):
    return np.asarray(z > 0, dtype=np.float32)


class SemaphoreIA:

    def __init__(self, learningrate, root):
        self.root = root
        self.learningrate = learningrate
        self.tools = MyTools()

        # Dossier des ratés
        self.tools.create_directory(self.root + '/failed')

        self.layers = [1600, 100, 100, 27]
        self.activations = [relu, relu, sigmoid]

        fichier = np.load(self.root + '/semaphore.npz')
        self.x_train, self.y_train = fichier['x_train'], fichier['y_train']
        self.x_train = 1 - self.x_train
        self.x_test, self.y_test = self.x_train[50000:,:], self.y_train[50000:]
        self.x_train, self.y_train = self.x_train[:50000,:], self.y_train[:50000]

        # Affichage des images pour distraire
        cv2.namedWindow('img')

    def training(self):
        """Apprentissage avec 60 000 images
        Calcule des poids enregistré dans weights.npy
        """

        print("Training...")

        # Matrice diagonale de 1
        eye_diagonale = np.eye(27, 27)

        # globals() Return a dictionary representing the current global symbol table.
        self.activations_prime = [globals()[fonction.__name__ + '_prime'] for fonction in self.activations]

        node_dict = {}

        # Liste des poids
        weight_list = [np.random.randn(self.layers[k+1],
                       self.layers[k]) / np.sqrt(self.layers[k]) for k in range(len(self.layers)-1)]

        for i, (vecteur_colonne, nombre_lettre) in enumerate(zip(self.x_train, self.y_train)):
            # vecteur_colonne = image en colonne à la 1ère itération
            # nombre_lettre = nombre correspondant à la lettre de l'image

            # Affichage pour distraire
            if i % 10000 == 0:
                print(i, nombre_lettre)
                img = vecteur_colonne.reshape(40,40) * 255
                img = cv2.resize(img, (600, 600), interpolation=cv2.INTER_AREA)
                cv2.imshow("img", img)
                cv2.waitKey(1)

            vecteur_colonne = np.array(vecteur_colonne, ndmin=2).T
            node_dict[0] = vecteur_colonne

            for k in range(len(self.layers)-1):
                z = np.dot(weight_list[k], vecteur_colonne)
                vecteur_colonne = self.activations[k](z)
                node_dict[k+1] = vecteur_colonne

            delta_a = vecteur_colonne - eye_diagonale[:,[nombre_lettre]]

            for k in range(len(self.layers)-2, -1, -1):
                delta_z = delta_a * self.activations_prime[k](node_dict[k+1])
                delta_w = np.dot(delta_z, node_dict[k].T)
                delta_a = np.dot(weight_list[k].T, delta_z)
                weight_list[k] -= self.learningrate * delta_w

        # Dans un fichier
        np.save(self.root + '/weights.npy', weight_list)
        print('weights.npy enregistré')
        cv2.destroyAll()

    def testing(self):
        """Teste avec 10 000 images, retourne le ratio de bon résultats
        """

        print("Testing...")

        weight_list = np.load(self.root + '/weights.npy')

        # Nombre de bonnes reconnaissance
        success = 0

        # Dict avec le nommbre d'erreurs par lettre
        failed_dict = {}

        for vecteur_colonne, nombre_lettre in zip(self.x_test, self.y_test):
            # image en colonne au 1er passage pour les failed
            img = vecteur_colonne.copy()

            for k in range(len(self.layers)-1):
                vecteur_colonne = self.activations[k](np.dot(weight_list[k], vecteur_colonne))

            reconnu = np.argmax(vecteur_colonne)
            if reconnu == nombre_lettre:
                success += 1
            else:
                self.write_failed(img, nombre_lettre, reconnu, success)
                if nombre_lettre in failed_dict:
                    failed_dict[nombre_lettre] += 1
                else:
                    failed_dict[nombre_lettre] = 1

        sorted_by_value = sorted(failed_dict.items(), key=lambda kv: kv[1], reverse=True)
        print(sorted_by_value)

        res = 100.0 * success / len(self.x_test)
        print("Accuracy: {}%".format(round(res, 1)))
        return res

    def write_failed(self, img, d, reconnu, S):
        """Les images avec erreur de reconnaisance sont copiées dans
        /semaphore/failed/bad_11/11_6_9067.png
        11 est la lettre k, donc dans le dossier il ny a que la lettre k
        et le 2ème nombre est la lettre reconnue fausse
        """
        name = str(d) + '_' + str(reconnu) + '_'  + str(S) + '.png'
        mt = MyTools()
        mt.create_directory(self.root + '/failed' + '/bad_' + str(d))
        fichier = self.root + '/failed' + '/bad_' + str(d) + '/' + name
        print(fichier)
        img = img.reshape(40,40) * 255
        cv2.imwrite(fichier, img)


if __name__ == "__main__":

    print(MyTools().get_absolute_path(__file__))
    root = MyTools().get_absolute_path(__file__)[:-29]
    print("Current directory:", root)

    learningrate = 0.02
    sia = SemaphoreIA(learningrate, root)
    #sia.training()
    resp = sia.testing()
    print("Learningrate", learningrate, "Résultat", resp)
