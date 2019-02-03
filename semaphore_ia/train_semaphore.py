import numpy as np
import cv2

def sigmoid(x): return 1 / (1 + np.exp(-x))
def sigmoid_prime(z): return z * (1 - z)
def relu(x): return np.maximum(0, x)
def relu_prime(z): return np.asarray(z > 0, dtype=np.float32)

def int_art(learningrate):
    layers = [1600, 100, 100, 27]
    activations = [relu, relu, sigmoid]

    f = np.load('/media/data/3D/projets/semaphore/semaphore.npz')
    x_train, y_train = f['x_train'], f['y_train']
    x_train = 1 - x_train
    x_test, y_test = x_train[50000:,:], y_train[50000:]
    x_train, y_train = x_train[:50000,:], y_train[:50000]
    Y = np.eye(27, 27)
    activations_prime = [globals()[f.__name__ + '_prime'] for f in activations]
    A = {}
    W = [np.random.randn(layers[k+1], layers[k]) / np.sqrt(layers[k]) for k in range(len(layers)-1)]
    cv2.namedWindow('img')
    print("Training...")
    for i, (a, d) in enumerate(zip(x_train, y_train)):
        if i % 200 == 0:
            print(i, d)
            img = a.reshape(40,40) * 255
            img = cv2.resize(img, (600, 600), interpolation=cv2.INTER_AREA)
            cv2.imshow("img", img)
            cv2.waitKey(1)
        a = np.array(a, ndmin=2).T
        A[0] = a
        for k in range(len(layers)-1):
            z = np.dot(W[k], a)
            a = activations[k](z)
            A[k+1] = a
        delta_a = a - Y[:,[d]]
        for k in range(len(layers)-2, -1, -1):
            dz = delta_a * activations_prime[k](A[k+1])
            dW = np.dot(dz, A[k].T)
            delta_a = np.dot(W[k].T, dz)
            W[k] -= learningrate * dW

    print("Testing...")
    S = 0
    for a, d in zip(x_test, y_test):
        for k in range(len(layers)-1):
            a = activations[k](np.dot(W[k], a))
        if np.argmax(a) == d:
            S += 1
    res = 100.0 * S / len(x_test)
    print("Accuracy: {}%".format(round(res, 1)))
    np.save('weights', W)
    return res

if __name__ == "__main__":
    # #all_res = []
    # #for learningrate in [0.005, 0.01, 0.02, 0.05, 0.1, 0.2]:
        # #res = int_art(learningrate)
        # #all_res.append((learningrate, res))
    # #for r in all_res:
        # #print("Learningrate", r[0], "Résultat", r[1])

    learningrate = 0.05
    res = int_art(learningrate)
    print("Learningrate", learningrate, "Résultat", res)
