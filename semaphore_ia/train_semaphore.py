import numpy as np, cv2

def sigmoid(x): return 1 / (1 + np.exp(-x))
def sigmoid_prime(z): return z * (1 - z)
def relu(x): return np.maximum(0, x)
def relu_prime(z): return np.asarray(z > 0, dtype=np.float32)
layers = [1600, 100, 100, 27]
activations, learningrate = [relu, relu, sigmoid], 0.05


if __name__ == "__main__":
    f = np.load('/media/data/3D/projets/semaphore/semaphore.npz')

    x_train, y_train = f['x_train'], f['y_train']
    x_train = 1 - x_train

    #y_train = y_train[:,0] # avec ancien fichier, erreur (1600, 1)

    x_test, y_test = x_train[50000:,:], y_train[50000:]
    x_train, y_train = x_train[:50000,:], y_train[:50000]

    Y = np.eye(27, 27)
    activations_prime = [globals()[f.__name__ + '_prime'] for f in activations]
    A = {}
    W = [np.random.randn(layers[k+1], layers[k]) / np.sqrt(layers[k]) for k in range(len(layers)-1)]

    print("Training...")
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    for epoch in range(1):
        for i, (a, d) in enumerate(zip(x_train, y_train)):
            if i % 100 == 0:
                print(epoch, i, d)
                cv2.imshow("img", a.reshape(40,40) * 255)
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
    print("Accuracy: %.1f %%" % (100.0 * S / len(x_test)))
    np.save('weights', W)
