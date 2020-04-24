# ======================================================================================================================
# ======================================   API VAN DE KLASSE NeuronVisualization    ====================================
# ======================================================================================================================
# - weight0 : double                            Deze waarde zijn degene die op het label van de Neuron geplaatst worden.
# - weight1 : double                            
# - weight2 : double
# - bias : double
# ----------------------------------------------------------------------------------------------------------------------
# + paintEvent(Event : QPaintEvent) : void                  Deze methode tekent de Neuron, deze wordt elke keer getekend
#                                                           als er een slider van waarde veranderd. Dit zorgt voor een 
#                                                           goede visualisatie wat er precies veranderd bij de neuron.
# + changeParameters(double, double,                        De waarden van de Neuron worden hier verandered, deze worden
#                   double, double) : void                  meegegeven in de aanroep van de methode zelf. Daarna wordt 
#                                                           de NeuronVisualization hertekent zodat deze een goede 
#                                                           visualisatie geeft.


from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont
from PyQt5.QtWidgets import QWidget


class NeuronVisualization(QWidget):
    def __init__(self, parent, w0, w1, w2, b):
        super().__init__()
        self.setParent(parent)

        self.__weight0 = w0
        self.__weight1 = w1
        self.__weight2 = w2
        self.__bias = b

        self.setMinimumHeight(500)

    def paintEvent(self, event):
        """
        Deze methode tekent de Neuron, deze wordt elke keer getekend als er een slider van waarde veranderd.
        Dit zorgt voor een goede visualisatie wat er precies veranderd bij de neuron.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        d = 250
        x = 400
        y = d/2
        painter.setPen(QPen(QColor(0, 0, 0)))
        painter.drawLine(x-d, y, x-d/3+d, y+d/2)
        painter.drawLine(x-d-d/15, y+d/2, x+2*d, y+d/2)
        painter.drawLine(x-d, y+d, x-d/3+d, y+d/2)
        painter.setBrush(QBrush(QColor(169, 169, 169)))
        painter.drawEllipse(x, y, d, d)

        font = QFont("Calibir", 20, QFont.Bold)
        painter.setFont(font)
        painter.drawText(x-d-d/6, y, "{}".format(3))
        painter.drawText(x-d-d/3, y+d/2, "{}".format(-2))
        painter.drawText(x-d-d/6, y+d+d/15, "{}".format(1))

        painter.setPen(QPen(QColor(105, 105, 105)))
        painter.drawText(x-d/2, y+d/15, "{}".format('w0: ' + str(self.__weight0)))
        painter.drawText(x-d/2-d/6, y+d/2-d/15, "{}".format('w1: ' + str(self.__weight1)))
        painter.drawText(x-d/2-d/8, y+d, "{}".format('w2: ' + str(self.__weight2)))
        painter.drawText(x+d/3, y-d/15, "{}".format('b: ' + str(self.__bias)))
        painter.drawText(x+2*d-d/8, y+d/2-d/15, "{}".format('a'))

    def changeParameters(self, w0, w1, w2, b):
        """
        De waarden van de Neuron worden hier verandered, deze worden meegegeven in de aanroep van de methode zelf. Daarna wordt de NeuronVisualization 
        hertekent zodat deze een goede visualisatie geeft.
        """
        self.__weight0 = w0
        self.__weight1 = w1
        self.__weight2 = w2
        self.__bias = b

        self.repaint()