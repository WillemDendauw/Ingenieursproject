from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtWidgets import QWidget


class NNVisualisatie(QWidget):
    def __init__(self, layers=2, layerNodes=12):
        super().__init__()
        self.__layers = layers
        self.__layerNodes = layerNodes


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.begin(self)

        if self.__layerNodes > 10:
            diameterCircle = self.height() / (self.__layerNodes * 2)
            spacing = self.height() / self.__layerNodes
        else:
            diameterCircle = self.height() / (10 * 2)
            spacing = self.height() / 10

        
        self.__drawLinesInput(painter, diameter=diameterCircle, nodes=self.__layerNodes, spacing=spacing)
        self.__drawLinesInner(painter, diameter=diameterCircle, nodes=self.__layerNodes, layer=1, spacing=spacing)
        self.__drawLinesToOutput(painter, diameterCircle, self.__layerNodes, spacing=spacing)
        
        self.__drawInput(painter, diameter=diameterCircle)

        painter.setBrush(QBrush(Qt.gray, Qt.SolidPattern))
        for i in range(self.__layers):
            self.__drawLayer(painter, diameter=diameterCircle, nodes=self.__layerNodes, counter=(
                i + 1), spacing=spacing)

        painter.setBrush(QBrush(Qt.green, Qt.SolidPattern))
        self.__drawLayer(painter, diameterCircle, nodes=10, counter=3, spacing=spacing)
        
        painter.end()

    
    # Lines tekenen
    def __drawLinesInput(self, p, diameter, nodes, spacing):
        p.setRenderHint(QPainter.Antialiasing)
        diameter = diameter * 3 / 2
        begingap = (self.height() - nodes * spacing) / 2
        for i in range(nodes):
            p.drawLine(diameter, self.height() / 2, diameter / 2 + (self.width()/4), begingap + diameter / 2 + i * spacing)

    def __drawLinesInner(self, p, diameter, nodes, layer, spacing):
        p.setRenderHint(QPainter.Antialiasing)
        beginX = diameter + layer * (self.width() / 4)
        begingap = (self.height() - nodes * spacing) / 2
        for i in range(nodes):
            beginY = begingap + diameter + i * spacing
            self.__drawLinesFromInnerNode(p, diameter, nodes, beginX, beginY, begingap, spacing)

    def __drawLinesFromInnerNode(self, p, diameter, nodes, beginX, beginY, begingap, spacing):
        for i in range(nodes):
            p.drawLine(beginX, beginY, diameter + 2*(self.width() / 4),
                       begingap + diameter + i * spacing)

    def __drawLinesToOutput(self, p, diameter, nodes, spacing):
        p.setRenderHint(QPainter.Antialiasing)

        begingap = (self.height() - nodes * spacing) / 2

        beginX = diameter + self.__layers * (self.width() / 4)
        for i in range(nodes):
            beginY = begingap + diameter + i * spacing
            eindX = diameter + self.__layers + 3 * (self.width() / 4)
            for j in range(10):
                if nodes < 10:
                    eindY = diameter + (j) * spacing
                else:
                    eindY = diameter + (j+1) * spacing
                p.drawLine(beginX, beginY, eindX, eindY)

    # Nodes tekenen
    def __drawInput(self, p, diameter):
        p.setRenderHint(QPainter.Antialiasing)
        diameter = diameter * 3 / 2
        p.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        p.drawEllipse(diameter / 2, self.height() / 2 - diameter / 2, diameter, diameter)

    def __drawLayer(self, p, diameter, nodes, counter, spacing):
        p.setRenderHint(QPainter.Antialiasing)
        begingap = (self.height() - nodes * spacing) / 2
        for i in range(nodes):
            p.drawEllipse(diameter / 2 + counter * (self.width() / 4), begingap + diameter / 2 + i * spacing,
                          diameter, diameter)