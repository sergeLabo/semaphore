

import numpy as np
import cv2
def sigmoid(x): return 1 / (1 + np.exp(-x))
def sigmoid_prime(z): return z * (1 - z)
def relu(x): return np.maximum(0, x)
def relu_prime(z): return np.asarray(z > 0, dtype=np.float32)
layers = [40*40, 100, 100, 27]
activations = [relu, relu, sigmoid]

def ia_original(learningrate):

    f = np.load('/media/data/3D/projets/semaphore/semaphore.npz')

    x_train, y_train = f['x_train'], f['y_train']
    x_test, y_test = f['x_test'], f['y_test']

    Y = np.eye(27, 27)
    activations_prime = [globals()[f.__name__ + '_prime'] for f in activations]
    A = {}
    W = [np.random.randn(layers[k+1], layers[k]) / np.sqrt(layers[k]) for k in range(len(layers)-1)]
    print("Training...", "learningrate", learningrate)
    for i, (a, d) in enumerate(zip(x_train, y_train)):
        # #if i % 1000 == 0:
            # #print(i)
        a = np.array(a, ndmin=2).T
        A[0] = a
        for k in range(len(layers)-1):
            z = np.dot(W[k], a)
            a = activations[k](z)
            A[k+1] = a
        da = a - Y[:,[d]]
        for k in range(len(layers)-2, -1, -1):
            dz = da * activations_prime[k](A[k+1])
            dW = np.dot(dz, A[k].T)
            da = np.dot(W[k].T, dz)
            W[k] -= learningrate * dW
    print("Testing...")
    S = 0
    for a, d in zip(x_test, y_test):
        for k in range(len(layers)-1):
            a = activations[k](np.dot(W[k], a))
        if np.argmax(a) == d:
            S += 1
    res = 100.0 * S / len(x_test)
    print("Accuracy: %.1f %%" % (res))
    np.save('weights', W)
    return res

if __name__ == "__main__":
    learningrate = 0.04
    ia_original(learningrate)
