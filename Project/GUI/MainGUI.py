from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QGridLayout, QLabel, QTextEdit
from GUI.Painter.Painter import Painter
from GUI.Output.Output import Output
from GUI.Neuron.NeuronGUI import NeuronGui
from GUI.Trainen.TrainingGUI import TrainingGUI
from GUI.Network.NetworkGUI import NetworkGUI
from Algoritme.Network import Network


class MainGUI(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)

        #  Configuratie van MainGUI
        self.setWindowTitle("Project team 6")

        # Initialiseer alle componenten
        self.__initGUI()

        fileWeights = "Data/NetwerkParameters/weights.npy"
        fileBiases = "Data/NetwerkParameters/biases.npy"
        self.__network = Network([784, 30, 10], fileWeights, fileBiases)

        self.showMaximized()

    def __initGUI(self):
        layout = QHBoxLayout(self)

        self.__outputGUI = self.__initOutput()

        layout.addWidget(self.__initPainterContainer())
        layout.addWidget(self.__outputGUI)
        layout.addWidget(self.__btnContainerEducationGUI())

        self.setLayout(layout)

    def __initPainterContainer(self):
        painterContainter = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(self.__initPainter())
        layout.addWidget(self.__initPartUnderPainter())

        painterContainter.setLayout(layout)

        return painterContainter

    def __initOutput(self):
        output = Output(self)
        return output

    def __btnContainerEducationGUI(self):
        education = QWidget()

        educationButtons = QWidget()
        vbox = QVBoxLayout()
        grid = QGridLayout()

        font = QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)

        labelMain = QLabel()
        labelMain.setFont(font)

        labelMain.setText(
            "Voor de meeste mensen is het gemakkelijk om een getal te herkennen. Voor ons lijkt\n"
            "dit zeer gemakkelijk aangezien we in onze hersenen een netwerk hebben met miljoenen\n"
            "neuronen die dit voor ons doen, maar de moeilijkheid om een visueel patroon te\n"
            "herkennen wordt duidelijk wanneer je een computerprogramma probeert te schrijven\n" 
            "dat in staat is dit te doen.\n"
            "\n"
            "Wij hebben dus een artificieel neuraal netwerk gemaakt dat, net zoals onze hersenen,\n"
            "getallen kan herkennen. Indien u dit netwerk wilt testen kan u op het canvas links\n"
            "hiervan een getal tekenen en op 'Output berekenen' drukken. De uitkomst van het\n"
            "netwerk wordt dan hiernaast weergegeven. Door op 'Clear Canvas' te drukken kan u\n"
            "een nieuw getal ingeven.\n"
            "\n"
            "Er komt veel kijken bij het maken van een neuraal netwerk, daarom hebben we een\n"
            "aantal infopagina's gemaakt om het allemaal duidelijk uit te leggen. Voor meer\n"
            "informatie over het het netwerk precies in elkaar zit, hoe de neuronen van het\n"
            "netwerk precies werken of hoe het netwerk getraind wordt kan u bij de onderstaande\n"
            "knoppen terecht.\n"
        )


        NeuronButton = QPushButton("Neuron...")
        labelNeuron = QLabel("Hier kan je meer leren over een Neuron op zichzelf.\nHoe deze zijn waarde berekent.")
        TrainenButton = QPushButton("Trainen van het Netwerk...")
        labelTrainen = QLabel("Voor meer informatie over het trainen van het Netwerk, moet je hier zijn.")
        NetwerkButton = QPushButton("Netwerk...")
        labelNetwerk = QLabel("Hoe dit netwerk een getal herkent, kan je hier vinden.")

        NeuronButton.clicked.connect(lambda: self.__openNeuronGUI())
        TrainenButton.clicked.connect(lambda: self.__openTrainenGUI())
        NetwerkButton.clicked.connect(lambda: self.__openNetworkGUI())

        grid.addWidget(NeuronButton, 0, 0)
        grid.addWidget(labelNeuron, 0, 1)
        grid.addWidget(TrainenButton, 1, 0)
        grid.addWidget(labelTrainen, 1, 1)
        grid.addWidget(NetwerkButton, 2, 0)
        grid.addWidget(labelNetwerk, 2, 1)

        educationButtons.setLayout(grid)

        vbox.addWidget(labelMain)
        vbox.addWidget(educationButtons)
        education.setLayout(vbox)
        return education

    def __initPainter(self):
        self.painterWidget = Painter()
        self.painterWidget.setAutoFillBackground(True)
        p = self.painterWidget.palette()
        p.setColor(self.painterWidget.backgroundRole(), QColor(200, 200, 200))
        self.painterWidget.setPalette(p)
        return self.painterWidget

    def __initPartUnderPainter(self):
        widget = QWidget()
        layout = QHBoxLayout()

        buttonClear = QPushButton("Clear Canvas")
        buttonCalculate = QPushButton("Output berekenen")
        buttonClear.clicked.connect(lambda: self.__clearCanvas(self.painterWidget))
        buttonCalculate.clicked.connect(lambda: self.__calculate(self.painterWidget))

        layout.addWidget(buttonCalculate)
        layout.addWidget(buttonClear)

        widget.setLayout(layout)
        return widget

    def __openNeuronGUI(self):
        # NeuronGUI opent zich vanzelf: in de constructor wordt showFullScreen() opgeroepen
        self.neuronGUI = NeuronGui((3, -2, 1))

    def __openTrainenGUI(self):
        # TrainenGUI opent zich vanzelf: in de constructor wordt showFullScreen() opgeroepen
        self.trainingGUI = TrainingGUI(None)

    def __openNetworkGUI(self):
        # NetworkGUI opent zich vanzelf: in de constructor wordt showFullScreen() opgeroepen
        self.nertworkGUI = NetworkGUI(None)

    def __clearCanvas(self, p):
        p.clearPunten()

    def __calculate(self, p):
        import numpy
        if len(p.getPunten()) != 0:
            input = numpy.reshape(numpy.array(p.getInput()), (784, 1))
            output = self.__network.output(input)
            _output = [output[i][0] for i in range(len(output))]
            self.__outputGUI.setOutputNodes(_output)
        else:
            self.__outputGUI.setOutputNodes([0 for x in range(10)])
