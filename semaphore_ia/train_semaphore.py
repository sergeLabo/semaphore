import numpy as np
import cv2
from pymultilame import MyTools

def sigmoid(x): return 1 / (1 + np.exp(-x))
def sigmoid_prime(z): return z * (1 - z)
def relu(x): return np.maximum(0, x)
def relu_prime(z): return np.asarray(z > 0, dtype=np.float32)

def int_art(root, learningrate):
    layers = [1600, 100, 100, 27]
    activations = [relu, relu, sigmoid]

    f = np.load(root + '/semaphore.npz')
    x_train, y_train = f['x_train'], f['y_train']
    x_train = 1 - x_train
    x_test, y_test = x_train[50000:,:], y_train[50000:]
    x_train, y_train = x_train[:50000,:], y_train[:50000]
    # #Y = np.eye(27, 27)
    # #activations_prime = [globals()[f.__name__ + '_prime'] for f in activations]
    # #A = {}
    # #W = [np.random.randn(layers[k+1], layers[k]) / np.sqrt(layers[k]) for k in range(len(layers)-1)]
    # #cv2.namedWindow('img')
    # #print("Training...")
    # #for i, (a, d) in enumerate(zip(x_train, y_train)):
        # #if i % 200 == 0:
            # #print(i, d)
            # #img = a.reshape(40,40) * 255
            # #img = cv2.resize(img, (600, 600), interpolation=cv2.INTER_AREA)
            # #cv2.imshow("img", img)
            # #cv2.waitKey(1)
        # #a = np.array(a, ndmin=2).T
        # #A[0] = a
        # #for k in range(len(layers)-1):
            # #z = np.dot(W[k], a)
            # #a = activations[k](z)
            # #A[k+1] = a
        # #delta_a = a - Y[:,[d]]
        # #for k in range(len(layers)-2, -1, -1):
            # #dz = delta_a * activations_prime[k](A[k+1])
            # #dW = np.dot(dz, A[k].T)
            # #delta_a = np.dot(W[k].T, dz)
            # #W[k] -= learningrate * dW

    # #np.save('weights', W)

    W = np.load('weights.npy')
    print("Testing...")

    S = 0
    failed_dict = {}
    for a, d in zip(x_test, y_test):
        img = a.copy()
        for k in range(len(layers)-1):
            a = activations[k](np.dot(W[k], a))
        if np.argmax(a) == d:
            S += 1
        else:
            write_failed(img, np.argmax(a), S, root)
            if np.argmax(a) in failed_dict:
                failed_dict[np.argmax(a)] += 1
            else:
                failed_dict[np.argmax(a)] = 0

    sorted_by_value = sorted(failed_dict.items(), key=lambda kv: kv[1])
    print(sorted_by_value)

    res = 100.0 * S / len(x_test)
    print("Accuracy: {}%".format(round(res, 1)))
    return res

def write_failed(img, d, S, root):
    name = str(d) + '_' + str(S) + '.png'
    f = root + '/failed/' + name
    print(f)
    img = img.reshape(40,40) * 255
    cv2.imwrite(f, img)


if __name__ == "__main__":
    print(MyTools().get_absolute_path(__file__))
    root = MyTools().get_absolute_path(__file__)[:-32]
    print("Current directory:", root)

    learningrate = 0.05
    res = int_art(root, learningrate)
    print("Learningrate", learningrate, "Résultat", res)

"""
Blur 4
Learningrate 0.05
Résultat 93.15

(21, 1), (15, 2), (5, 2), (7, 3), (3, 5), (6, 12), (11, 12), (12, 13), (17, 13), (13, 20), (0, 21), (14, 23), (2, 25), (19, 30), (20, 32), (8, 33), (16, 42), (26, 90),

(4, 107),
(18, 179)


"""
