# ======================================================================================================================
# ============================================   API VAN DE KLASSE networkGUI   ========================================
# ======================================================================================================================
# - initGUI                             zet 2 QWidgets boven elkaar, de bovenste bevat het netwerk gedeelte en de
#                                       onderste bevat het menselijke.
# - network                             zet in de network Widget 2 Widgets naast elkaar, een voor een visuele
#                                       voorstelling en 1 met uitleg
# - human                               doet hetzelfde als network (methode hierboven) en maar dan voor het menselijke
#                                       aspect
# - networkCanvas                       de widget die het visuele aspect van de uitleg bevat
# - networkExplanation                  de widget die de uitleg bevat
# - humanCanvas                         de widget die het visuele aspect van de uitleg bevat
# - humanExplanation                    de widget die de uitleg bevat

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from humanCanvas import humanCanvas
from Stukjes code.Egon.Trainen.NNVisualisatie import NNVisualisatie
#from .networkCanvas import networkCanvas


class networkGUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent = parent)

        self.setWindowTitle("Hoe denken wij, hoe denkt een neuraal netwerk")
        self.__initGUI()
        self.showMaximized()

    def __initGUI(self):
        layout = QVBoxLayout(self)

        layout.addWidget(self.__network())
        layout.addWidget(self.__human())

        self.setLayout(layout)

    #bovenste 22
    def __network(self):
        network = QWidget()
        layout = QHBoxLayout(self)

        layout.addWidget(NNVisualisatie(2,12))
        layout.addWidget(self.__networkExplanation())

        network.setLayout(layout)
        return network

    #onderste 2
    def __human(self):
        human = QWidget()
        layout = QHBoxLayout(self)

        canvas = humanCanvas()
        layout.addWidget(canvas)
        layout.addWidget(self.__humanExplanation())

        human.setLayout(layout)
        return human

    #linksboven
    def __networkCanvas(self):
        network = QWidget()
        network.setAutoFillBackground(True)
        p = network.palette()
        p.setColor(network.backgroundRole(), QColor(0,0,7))
        network.setPalette(p)
        return network

    #rechtsboven
    def __networkExplanation(self):
        network = QWidget()
        network.setAutoFillBackground(True)
        p = network.palette()
        p.setColor(network.backgroundRole(), QColor(0,0,7))
        network.setPalette(p)
        return network

    #rechtsonder
    def __humanExplanation(self):
        human = QWidget()
        human.setAutoFillBackground(True)
        p = human.palette()
        p.setColor(human.backgroundRole(), QColor(110,128,7))
        human.setPalette(p)
        return human

    def paintEvent(self,event):
        """
        Hier tekenen we een simpele vorm van een netwerk die de tekening van een cijfer opsplitst in
        verschillende stukken om dan het cijfer te bepalen.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = networkGUI()
    GUI.show()
    sys.exit(app.exec_())