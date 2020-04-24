# ======================================================================================================================
# ===========================================   API VAN DE KLASSE Network   ============================================
# ======================================================================================================================
# - numberOfLayers : int                    Houdt het aantal lagen van het netwerk bij.
# - sizes : list(int)                       Houdt voor elke laag bij hoeveel neuronen het bevat
# - biases : list(numpy.ndarray(float))     Houdt de biases van de neuronen bij
# - weights : list(numpy.ndarray(float))    Houdt de weights van de neuronen bij
# ----------------------------------------------------------------------------------------------------------------------
# + saveNetwork() : void                    Slaat de weights en biases van het (getrainde) netwerk op in de bestanden
#                                           "weights" en "biases".
# - sigmoid() : float                       De sigmoid functie zorgt er voor dat de uitkomst van een neuron een float
#                                           tussen 0 en 1 is.
# - derivativeSigmoid() : float             Dit is de afgeleide van de sigmoid functie. Dit wordt gebruikt in het
#                                           backpropagation algoritme.
# + output() : numpy.ndarray(float)         Dit berekend de output van het netwerk als de input wordt meegegeven.
# - backpropagation()                       Backpropagation geeft een tuple terug met de gradient van de kostfunctie
#      : tuple(list(numpy.ndarray(float)))  voor de biases en de weights.
# + gradientDescent() : void                gradientDescent traint het neuraal netwerk. De trainingSet wordt verdeeld in
#                                           verschillende miniBatches, voor elke miniBatch wordt apart de gradient
#                                           bepaald om het netwerk sneller te laten leren. Dit wordt het aantal epochs
#                                           herhaald.
# - updateNetwerk() : void                  Dit past de weights en biases van het netwerk aan met behulp van
#                                           backpropagation en gradientDescent.
# - deltaCost() : numpy.ndarray(float)      Dit geeft het foutverschil terug van de output laag.

import random

import numpy as np


class Network:

    def __init__(self, sizes, weightsFile=None, biasesFile=None):
        self.__numberOfLayers = len(sizes)
        self.__sizes = sizes
        if weightsFile is None and biasesFile is None:
            self.__biases = [np.random.randn(x, 1) for x in self.__sizes[1:]]
            self.__weights = [np.random.randn(x, y) for x, y in zip(self.__sizes[1:], self.__sizes[:-1])]
        else:
            self.__biases = np.load(biasesFile)
            self.__weights = np.load(weightsFile)

    def saveNetwork(self):
        np.save("../Data/NetwerkParameters/weights.npy", self.__weights)
        np.save("../Data/NetwerkParameters/biases.npy", self.__biases)

    def sigmoid(self, z):
        return 1.0 / (1.0 + np.exp(-z))

    def ___derivativeSigmoid(self, z):
        return self.sigmoid(z)*(1 - self.sigmoid(z))

    def output(self, a):
        for w, b in zip(self.__weights, self.__biases):
            a = self.sigmoid(np.dot(w, a) + b)
        return a

    def __backpropagation(self, x, y):
        nablaBiases = [np.zeros(b.shape) for b in self.__biases]
        nablaWeights = [np.zeros(w.shape) for w in self.__weights]
        activation = x
        activations = [x]
        zs = []
        for b, w in zip(self.__biases, self.__weights):
            z = np.dot(w, activation) + b
            zs.append(z)
            activation = self.sigmoid(z)
            activations.append(activation)
        delta = self.__deltaCost(activations[-1], y)
        nablaBiases[-1] = delta
        nablaWeights[-1] = np.dot(delta, activations[-2].transpose())
        for l in range(2, self.__numberOfLayers):
            z = zs[-l]
            ds = self.___derivativeSigmoid(z)
            npdot = np.dot(self.__weights[-l+1].transpose(), delta)
            delta = npdot * ds
            nablaBiases[-l] = delta
            nablaWeights[-l] = np.dot(delta, activations[-l-1].transpose())
        return (nablaBiases, nablaWeights)

    def gradientDescent(self, trainingSet, epochs, miniBatchSize, learningRate, evaluationData=None, lmbda=0.0, txtField=None):
        trainingSet = list(trainingSet)
        n = len(trainingSet)

        for i in range(epochs):
            random.shuffle(trainingSet)
            miniBatches = [trainingSet[k:k+miniBatchSize] for k in range(0, n, miniBatchSize)]
            for miniBatch in miniBatches:
                self.__updateNetwork(miniBatch, learningRate, lmbda, n)

            # de testdata door het netwerk laten gaan
            if evaluationData is not None:
                evaluationData = list(evaluationData)
                nEvalDat = len(evaluationData)
                correct = 0
                for testCijfer, expected in evaluationData:
                    testOutput = self.output(testCijfer)
                    networkOutput = np.argmax(testOutput)
                    if networkOutput == expected:
                        correct += 1
                if txtField is not None:
                    text = str(txtField.toPlainText())
                    text += "Na epoch {} haalt het netwerk {}/{}\n".format(i + 1, correct, nEvalDat)
                    txtField.setText(text)
                else:
                    print("Na epoch {} haalt het netwerk {}/{}".format(i + 1, correct, nEvalDat))

    def __updateNetwork(self, miniBatch, learningRate, lmbda, n):
        nablaBiases = [np.zeros(b.shape) for b in self.__biases]
        nablaWeights = [np.zeros(w.shape) for w in self.__weights]
        for x, y in miniBatch:
            deltaNablaBiases, deltaNablaWeights = self.__backpropagation(x, y)
            nablaBiases = [nb + dnb for nb, dnb in zip(nablaBiases, deltaNablaBiases)]
            nablaWeights = [nw + dnw for nw, dnw in zip(nablaWeights, deltaNablaWeights)]
        self.__biases = [b - (learningRate/len(miniBatch))*nb for b, nb in zip(self.__biases, nablaBiases)]
        self.__weights = [(1 - learningRate*(lmbda/n))*w - (learningRate/len(miniBatch))*nw for w, nw in zip(self.__weights, nablaWeights)]

    def __deltaCost(self, a, y):
        return a - y
