from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPainter, QPaintEvent, QPen, QColor, QBrush, QFont
from PyQt5.QtWidgets import QWidget


class OutputNode(QWidget):
    def __init__(self, number, outputValue=0.0, showLabel=True):
        super().__init__()
        self.__number = number

        if (outputValue < 0) or (outputValue > 1):
            raise ValueError("De output-waarde van het neurale netwerk ligt in het gesloten interval [0, 1], {} "
                             "behoort niet tot dat interval".format(outputValue))
        self.__outputValue = outputValue

        self.__labelColor = QColor()  # zwart

        # TODO: misschien moeten we met deze kleuren nog wat spelen (doe dit in GradientColorTest)
        # deze twee kleuren bepalen de overeenkomst van een kleur met een output-waarde 0 en 1 van het neuraal netwerk
        self.__color1 = QColor(255, 50, 50)  # stelt 0 voor als output van het neuraal netwerk
        self.__color2 = QColor(50, 255, 50)  # stelt 1 voor als output van het neuraal netwerk

        self.__showLabel = showLabel

    def changeValue(self, outputValue=0.0):
        if (outputValue < 0) or (outputValue > 1):
            raise ValueError("De output-waarde van het neurale netwerk ligt in het gesloten interval [0, 1], {:2} "
                             "behoort niet tot dat interval".format(outputValue))

        self.__outputValue = outputValue
        self.repaint()

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        diameterCircle = min(self.width(), self.height()) / 2
        self.__drawCircle(p, diameter=diameterCircle)
        if self.__showLabel:
            self.__drawNumber(p, diameter=diameterCircle)
        p.end()

    def __drawCircle(self, p, diameter):
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(self.__makePen())
        p.setBrush(self.__makeBrush())
        if self.__showLabel:
            # de cirkel maakt wat plaats voor het label, het bolletje begint in het midden,
            # het label komt gecentreerd in de eerste helft van de QWidget
            p.drawEllipse(self.width()/2, self.height()/2 - diameter/2, diameter, diameter)
        else:
            # als geen label getekend moet worden, dan heeft de cirkel alle plaats voor zich:
            # en dan komt die helemaal in het midden
            p.drawEllipse(self.width()/2 - diameter/2, self.height()/2 - diameter/2, diameter, diameter)

    def __drawNumber(self, p, diameter):
        p.setPen(QPen(self.__labelColor))
        fontSize = diameter / 2
        # de font size is de breedte van de zijde als je een vierkant rond een letter/cijfer zou zetten
        # (ik betwijfel of dit helemaal correct is maar het komt zeker aardig in de buurt en volstaat)

        x = self.width()/4 - fontSize/2
        # het vierkant moet horizontaal gecentreed staan in de linker helft van het QWidget
        y = self.height()/2 - fontSize/2
        # ook verticaal moet de tekst gecentreerd zijn

        font = QFont("Calibir", fontSize, QFont.Bold)
        p.setFont(font)

        p.drawText(x, y + fontSize, "{}".format(self.__number))
        if __name__ == "__main__":
            print("self.width() = {}\n"
                  "self.height() = {}\n"
                  "x={}\n"
                  "y={}\n"
                  "fontSize = {}\n"
                  "diameter = {}\n".format(self.width(), self.height(), x, y, fontSize, diameter))

    def __makePen(self):
        pen = QPen(self.getGradientColor())
        return pen

    def __makeBrush(self):
        brush = QBrush(self.getGradientColor())
        return brush

    def getGradientColor(self, value=-1.0):
        """
        Het neuraal netwerk geeft voor elk cijfer van 0 t.e.m. 9 een waarde tussen 0 en 1 dat weergeeft in welke
        mate het netwerk denkt dat het getekende cijfer overeenkomt met het betreffende cijfer. Om dit visueel
        voor te stellen worden gekleurde bolletjes getoond. De kleur rood, QColor(255, 50, 50), komt overeen met
        een outputValue 0 terwijl de kleur groen, QColor(50, 255, 50), overeenkomt met een outputValue 1

        Deze methode bepaalt voor elke waarde tussen 0 en 1 (outputValue) het juiste kleur dat lineair tussen
        color1 en color2 ligt.

        Een visuele voorstelling van de graduele transitie is te vinden in de klasse GradientColorTest

        :return: QColor
        """
        if value < 0 or value > 1:
            value = self.__outputValue
        red = (self.__color2.red() - self.__color1.red()) * value + self.__color1.red()
        green = (self.__color2.green() - self.__color1.green()) * value + self.__color1.green()
        blue = (self.__color2.red() - self.__color1.green()) * value + self.__color1.blue()
        return QColor(red, green, blue)

    def setLabelColor(self, color=QColor()):
        """
        Deze setter zet het kleur van de label in, indien de gebruiker hetzelfde kleur wil van het bolletje horende
        bij het cijfer, dan kan de gebruiker dit als volgt realiseren:
        objOutputNode.setLabelColor(objOutputNode.getGradientColor())

        :return: void
        """
        self.__labelColor = color


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    main = OutputNode(number=5, outputValue=0.730534523452345, showLabel=True)
    main.show()
    sys.exit(app.exec_())
