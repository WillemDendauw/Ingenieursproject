import sys

from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QWidget, QSlider, QGroupBox, QLabel,
                             QTextEdit, QPushButton, QGridLayout)
from PyQt5.QtCore import Qt
from NNVisualisatie import NNVisualisatie


# noinspection PyArgumentList
class TrainingGUI(QWidget):
    def __init__(self, parent=None):
        super(TrainingGUI, self).__init__(parent)

        self.setWindowTitle("Training of a neural network")

        self.__logOutput = QTextEdit()
        self.__initGUI()

        self.showMaximized()

    def __initGUI(self):
        layout = QHBoxLayout(self)

        layout.addWidget(self.__initSliderContainer())
        layout.addWidget(self.tekenNN())
        layout.addWidget(self.__initOutput())

        self.setLayout(layout)

    def __initSliderContainer(self):
        sliderContainer = QWidget()
        layout = QVBoxLayout()

        sliders = QWidget()
        sliderLayout = QGridLayout()

        label0 = QLabel("Learning rate η:")
        label1 = QLabel("Number of epochs:")
        label2 = QLabel("Mini-batch size:")

        self.labelS0 = QLabel("0")
        self.labelS1 = QLabel("0")
        self.labelS2 = QLabel("0")

        labelSliderMin0 = QLabel("0")
        labelSliderMax0 = QLabel("100")

        labelSliderMin1 = QLabel("0")
        labelSliderMax1 = QLabel("100")

        labelSliderMin2 = QLabel("0")
        labelSliderMax2 = QLabel("100")

        self.slider0 = self.makeSlider(0, 100)
        self.slider1 = self.makeSlider(0, 100)
        self.slider2 = self.makeSlider(0, 100)

        self.slider0.valueChanged.connect(lambda: self.sliderChange(0))
        self.slider1.valueChanged.connect(lambda: self.sliderChange(1))
        self.slider2.valueChanged.connect(lambda: self.sliderChange(2))

        buttonRun = QPushButton("Run")
        buttonRun.setFixedWidth(100)

        buttonRun.clicked.connect(self.run)

        sliderLayout.addWidget(label0, 0, 0)
        sliderLayout.addWidget(self.labelS0, 0, 2, Qt.AlignRight)
        sliderLayout.addWidget(self.slider0, 1, 0, 1, 3)
        sliderLayout.addWidget(labelSliderMin0, 2, 0)
        sliderLayout.addWidget(labelSliderMax0, 2, 2, Qt.AlignRight)

        sliderLayout.addWidget(label1, 3, 0)
        sliderLayout.addWidget(self.labelS1, 3, 2, Qt.AlignRight)
        sliderLayout.addWidget(self.slider1, 4, 0, 1, 3)
        sliderLayout.addWidget(labelSliderMin1, 5, 0)
        sliderLayout.addWidget(labelSliderMax1, 5, 2, Qt.AlignRight)

        sliderLayout.addWidget(label2, 6, 0)
        sliderLayout.addWidget(self.labelS2, 6, 2, Qt.AlignRight)
        sliderLayout.addWidget(self.slider2, 7, 0, 1, 3)
        sliderLayout.addWidget(labelSliderMin2, 8, 0)
        sliderLayout.addWidget(labelSliderMax2, 8, 2, Qt.AlignRight)

        sliderLayout.addWidget(buttonRun, 10, 2)

        sliderLayout.setRowMinimumHeight(9, 50)

        sliders.setFixedHeight(400)
        sliders.setLayout(sliderLayout)

        explanation = QLabel()
        explanation.setText("Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
                            " Sed semper neque vel erat efficitur, non interdum ipsum blandit.\n"
                            " Nulla id suscipit elit, nec congue risus.\n"
                            " Etiam posuere libero quis accumsan egestas.\n"
                            " Curabitur vitae risus at nisl mollis tincidunt.\n"
                            " Sed rhoncus et ligula et tincidunt.\n\n"
                            "hier komt uitleg over de variabelen")

        buttonBack = QPushButton("Back")
        buttonBack.setFixedWidth(100)

        layout.addWidget(sliders)
        layout.addStretch(1)
        layout.addWidget(explanation)
        layout.addStretch(1)
        layout.addWidget(buttonBack)

        sliderContainer.setFixedWidth(500)
        sliderContainer.setLayout(layout)

        return sliderContainer

    # def __initNeuralNet(self):
    #     groupBox = QWidget()
    #
    #     layout = QHBoxLayout()
    #
    #     nodes = QVBoxLayout()
    #     inputnode = Node()
    #     nodes.addWidget(inputnode)
    #     layout.addLayout(nodes, 1)
    #
    #     for i in range(2):
    #         nodes = QVBoxLayout()
    #         for j in range(10):
    #             node = Node()
    #             nodes.addWidget(node)
    #         layout.addLayout(nodes, 2)
    #     nodes = QVBoxLayout()
    #     for i in range(10):
    #         node = OutputNode(i, showLabel=True)
    #         nodes.addWidget(node)
    #     layout.addLayout(nodes, 2)
    #     groupBox.setLayout(layout)
    #
    #     return groupBox

    def __initOutput(self):  # https://stackoverflow.com/questions/16568451/pyqt-how-to-make-a-textarea-to-write-messages-to-kinda-like-printing-to-a-co
        groupBox = QGroupBox("Output:")

        hor = QHBoxLayout()

        self.__logOutput.setReadOnly(True)
        self.__logOutput.setLineWrapMode(QTextEdit.NoWrap)

        font = self.__logOutput.font()
        font.setFamily("Courier")
        font.setPointSize(10)

        hor.addWidget(self.__logOutput)
        groupBox.setFixedWidth(400)
        groupBox.setLayout(hor)

        return groupBox

    def makeSlider(self, min, max):
        slider = QSlider(Qt.Horizontal)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(10)
        slider.setSingleStep(0.1)
        slider.setRange(min, max)
        return slider

    def sliderChange(self, i):
        if i == 0:
            string = str(self.slider0.value())
            self.labelS0.setText(string)
        elif i == 1:
            string = str(self.slider1.value())
            self.labelS1.setText(string)
        elif i == 2:
            string = str(self.slider2.value())
            self.labelS2.setText(string)

    def run(self):
        i = 0
        # hier moet de code komen die een nieuw neural net traint

    def tekenNN(self):
        box = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(NNVisualisatie())
        box.setLayout(layout)

        return box


if __name__ == '__main__':
    app = QApplication(sys.argv)
    trainingGUI = TrainingGUI()
    trainingGUI.show()
    sys.exit(app.exec_())
