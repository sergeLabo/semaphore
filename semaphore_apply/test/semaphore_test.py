#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


import os
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
                shutil.rmtree(os.path.join(self.root, 'semaphore_apply', 'test', 'failed'))
            except:
                print('Pas de dossier failed')
            self.tools.create_directory(os.path.join(self.root, 'semaphore_apply', 'test', 'failed'))

        # Réseau de neurones: colonne 1600 en entrée, 2 nodes de 100, sortie de 27 caractères
        self.layers = [1600, 100, 100, 27]
        # Fonction d'activation: imite l'activation d'un neuronne
        self.activations = [relu, relu, sigmoid]

        fichier = np.load(os.path.join(self.root, 'semaphore_apply', 'test', 'semaphore_apply.npz'))
        self.x_test, self.y_test = fichier['x_test'], fichier['y_test']

        # Affichage des images pour distraire
        #cv2.namedWindow('image')

    def testing(self):
        """Teste avec 1 000 images, retourne le ratio de bon résultats"""

        print("Testing...")

        weight_list = np.load(os.path.join(self.root, 'semaphore_apply', 'test', 'weights.npy'))

        # Nombre de bonnes reconnaissance
        success = 0

        i = 0
        for vecteur_ligne, nombre_lettre in zip(self.x_test, self.y_test):
            # Affichage pour distraire les mangalores
            # #if i % 1 == 0:
                # #image = vecteur_ligne.reshape(40,40)
                # #image = cv2.resize(image, (600, 600), interpolation=cv2.INTER_AREA)
                # #image = image * 255
                # #cv2.imshow("image", image)
                # #cv2.waitKey(30)

            # image en ligne au 1er passage pour les failed
            img = vecteur_ligne.copy()

            for k in range(len(self.layers)-1):
                vecteur_ligne = self.activations[k](np.dot(weight_list[k],
                                                      vecteur_ligne))
            reconnu = np.argmax(vecteur_ligne)
            if reconnu == nombre_lettre:
                success += 1
            else:
                if self.failed:
                    self.tools.create_directory(os.path.join(self.root,
                                                'semaphore_apply',
                                                'test',
                                                'failed',
                                                'bad_' + str(nombre_lettre)))
                    self.write_failed(img, nombre_lettre, reconnu, success)
            i += 1

        try:
            resp = 100.0 * success / len(self.x_test)
        except: resp = 0
        return resp

    def write_failed(self, img, nombre_lettre, reconnu, S):
        """Les images avec erreur de reconnaisance sont copiées dans
        /semaphore/semaphore_apply/test/failed/bad_11/11_6_9067.png
        11 est la lettre k, donc dans le dossier il ny a que la lettre k
        et le 2ème nombre est la lettre reconnue fausse
        """
        name = str(nombre_lettre) + '_' + str(reconnu) + '_'  + str(S) + '.png'
        fichier = os.path.join(self.root, 'semaphore_apply', 'test', 'failed', 'bad_' + str(nombre_lettre), name)
        img = img.reshape(40,40) * 255
        cv2.imwrite(fichier, img)


if __name__ == "__main__":

    # Chemin courrant
    abs_path = MyTools().get_absolute_path(__file__)
    print("Chemin courrant", abs_path)

    # Nom du script
    name = os.path.basename(abs_path)
    print("Nom de ce script:", name)

    # Abs path de semaphore sans / à la fin
    parts = abs_path.split("semaphore")
    root = os.path.join(parts[0], "semaphore")
    print("Path de semaphore:", root)

    learningrate = 0.022
    failed = 1
    sia = SemaphoreIA(root, learningrate, failed)
    resp = sia.testing()
    print("Learningrate: {} Résultat {}".format(learningrate, round(resp, 1)))
