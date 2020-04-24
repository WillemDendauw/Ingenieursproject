"""
Dit is een testklasse om een getraind netwerk te testen, deze moet bij het afleveren verschuiven naar
#Stukjes code/Bram/6 - TestGetraindNetwerk
"""

# noodzakelijk om de imports vanuit command line goed te laten verlopen
import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_GUI = dir_path[0:dir_path.rfind("CollectTrainingData")]
sys.path.append(dir_GUI)

from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton
from GUI.Painter.Painter import Painter
from GUI.Output.Output import Output
import numpy as np
from Algoritme.Network import Network
# from CollectTrainingData.Network import Network

dirNetwerkParameters = "./NetwerkParameters/"


def feedforward(net=Network, p=Painter, o=Output):
    input = np.reshape(np.array(p.getInput()), (784, 1))
    _output = net.output(np.array(input))

    output = []
    for i in _output:
        output.append(i[0]) # / grootste binnen append
    print(output)
    print("==========================================")

    o.setOutputNodes(output)

def printOutput(p=Painter):
    _input = p.getInput()

    # te_printen = ""
    # for i in range(0, 28):
    #    for j in range(0, 28):
    #        te_printen += "{:4}".format(int(_input[i*28 + j]*255))
    #    te_printen += "\n"
    # print(te_printen)


class Main(QWidget):
    def __init__(self):
        super().__init__()

        fileBiases = dirNetwerkParameters + "biases.npy"
        fileWeights = dirNetwerkParameters + "weights.npy"

        self.net = Network([784, 30, 10], fileWeights, fileBiases)

        layout = QGridLayout()

        painter = Painter(parent=self)
        output = Output()

        btnFeedforward = QPushButton("Feed forward")
        btnFeedforward.clicked.connect(lambda: feedforward(self.net, painter, output))

        btnPrint = QPushButton("Print")
        btnPrint.clicked.connect(lambda: printOutput(painter))

        btnClearPainter = QPushButton("Clear")
        btnClearPainter.clicked.connect(lambda: painter.clearPunten())

        layout.addWidget(painter, 0, 0, 1, 3)
        layout.addWidget(btnFeedforward, 1, 0)
        layout.addWidget(btnClearPainter, 1, 1)
        layout.addWidget(btnPrint, 1, 2)
        layout.addWidget(output, 0, 3, 2, 1)

        layout.setRowMinimumHeight(0, 420)
        layout.setColumnMinimumWidth(0, 230)
        layout.setColumnMinimumWidth(1, 230)
        layout.setColumnMinimumWidth(2, 230)
        layout.setColumnMinimumWidth(3, 320)

        self.setLayout(layout)
        self.show()     


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())