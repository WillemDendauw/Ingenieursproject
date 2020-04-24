# ======================================================================================================================
# ===========================================   API VAN DE KLASSE Network   ============================================
# ======================================================================================================================
#
#

import numpy as np
from Data import Data


class Network:

    def __init__(self, sizes, weightsFile=None, biasesFile=None):
        self.numberOfLayers = len(sizes)
        self.sizes = sizes
        if weightsFile is None and biasesFile is None:
            self.biases = [np.random.randn(x, 1) for x in self.sizes[1:]]
            self.weights = [np.random.randn(x, y) for x, y in zip(self.sizes[1:], self.sizes[:-1])]
        else:
            self.biases = np.load(biasesFile)
            self.weights = np.load(weightsFile)

    def saveNetwork(self):
        np.save("weights", self.weights)
        np.save("biases", self.biases)

    def sigmoid(self, z):
        return 1.0 / (1.0 + np.exp(-z))

    def derivativeSigmoid(self, z):
        return self.sigmoid(z)*(1 - self.sigmoid(z))

    def output(self, a):
        for w, b in zip(self.weights, self.biases):
            a = self.sigmoid(np.dot(w, a) + b)
        return a

    def backpropagation(self, x, y):
        nablaBiases = [np.zeros(b.shape) for b in self.biases]
        nablaWeights = [np.zeros(w.shape) for w in self.weights]
        activation = x
        activations = [x]
        zs = []
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation) + b
            zs.append(z)
            activation = self.sigmoid(z)
            activations.append(activation)
        delta = self.deltaCost(activations[-1], y)
        nablaBiases[-1] = delta
        nablaWeights[-1] = np.dot(delta, activations[-2].transpose())
        for l in range(2, self.numberOfLayers):
            z = zs[-1]
            ds = self.derivativeSigmoid(z)
            delta = np.dot(self.weights[-l+1].transpose(), delta) * ds
            nablaBiases[-1] = delta
            nablaWeights[-1] = np.dot(delta, activations[-l-1].transpose())
        return (nablaBiases, nablaWeights)

    def gradientDescent(self, trainingSet, epochs, miniBatchSize, learningRate, lmbda):
        trainingSet = list(trainingSet)
        n = len(trainingSet)
        for i in range(epochs):
            miniBatches = [trainingSet[k:k+miniBatchSize] for k in range(0, n, miniBatchSize)]
            for miniBatch in miniBatches:
                self.updateNetwork(miniBatch, learningRate, lmbda, n)
        return

    def updateNetwork(self, miniBatch, learningRate, lmbda, n):
        nablaBiases = [np.zeros(b.shape) for b in self.biases]
        nablaWeights = [np.zeros(w.shape) for w in self.weights]
        for x, y in miniBatch:
            deltaNablaBiases, deltaNablaWeights = self.backpropagation(x, y)
            nablaBiases = [nb + dnb for nb, dnb in zip(nablaBiases, deltaNablaBiases)]
            nablaWeights = [nw + dnw for nw, dnw in zip(nablaWeights, deltaNablaWeights)]
        self.biases = [b - (learningRate/len(miniBatch))*nb for b, nb in zip(self.biases, nablaBiases)]
        self.weights = [(1 - learningRate*(lmbda/n))*w - (learningRate/len(miniBatch))*nw for w, nw in zip(self.weights, nablaWeights)]
        return

    def evaluation(self, validationSet):
        results = [(np.argmax(self.output(x)), np.argmax(y)) for (x, y) in validationSet]
        resultAccuracy = sum(int(x == y) for (x, y) in results)
        return resultAccuracy

    def deltaCost(self, a, y):
        return a - y

    def cost(self, data, lmbda):
        data = list(data)
        cost = 0.0
        for x, y in data:
            a = self.output(x)
            cost += -(1/len(data))*np.sum(np.fromiter(np.nan_to_num(y*np.log(a)+(1-y)*np.log(1-a)), float))
        cost += lmbda/(2*len(data))*np.sum(np.fromiter((np.linalg.norm(w)**2 for w in self.weights), float))
        return cost
