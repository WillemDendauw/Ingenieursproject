# Voor een samenvattende uitleg van Painter, zie #Stukjes code\Bram\3 - Painter\Samenvattende uitleg - Painter en Image\
# ======================================================================================================================
# ===========================================   API VAN DE KLASSE Painter   ============================================
# ======================================================================================================================
# - punten : list(list(QPoint))     houdt alle door de gebruiker geplaatste QPoints bij
# - huidige_punten                  houdt de QPunten van de huidige/laatste vloeiende lijn blij (tussen mousePressed-
#       : list(QPoint)              en mouseReleaseEvent
# - is_painting : bool              boolean die zegt of de gebruiker aan het tekenen is of niet
# - pen_width : int                 hoe dik de pen is die wordt gebruikt om te tekenen, in pixels
# - color : QColor                  variabele die de kleur van de pen bijhoudt die gebruikt wordt om te tekenen
#                                   (default kleur is zwart)
# ----------------------------------------------------------------------------------------------------------------------
# + mousePressEvent : void          bij het drukken op de muis, wil de gebruiker tekenen
# + mouseMoveEvent : void           als op de muis werd geklikt en de muis beweegt, dan tekent de gebruiker
# + mouseReleaseEvent : void        als de muis wordt losgelaten wil de gebruiker niet meer tekenen
# + mouseDoubleClickEvent : void    als de gebruiker dubbelklikt, dan wordt het cijfer verwijderd
# + paintEvent : void               hier staat de effectieve code voor het tekenen, het gebruikt de hulpmethode draw()
# + getImage : Image                geeft een Image terug van de huidige tekening
# - draw : void                     een hulmethode om te tekenen
# - makePen : QPen                  een hulmethode die de gewenste QPen maakt en teruggeeft
# - clearPunten : void              bij het dubbelklikken wordt deze methode gebruikt

import sys

from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from PyQt5.QtWidgets import QWidget, QDialog, QApplication, QHBoxLayout
from PyQt5.QtCore import Qt, QPoint, QSize
import math

from Image import Image


class Painter(QWidget):
    def __init__(self, parent=None, pen_width=3):
        super(Painter, self).__init__()
        self.setParent(parent)

        self.__punten = list(list())  # elke lijst in punten bevat een reeks QPoint's. Ik heb een lijst van
        # lijsten gemaakt zodat wanneer de gebruiker de muisknop loslaat en vervolgens
        # opnieuw een deeltje wil tekenen (zoals bij een en 4, 7) dat geen lijnen van
        # het laatst en eerste QPoint getekend  worden
        self.__huidige_punten = list()  # deze wordt na elke mouseReleaseEvent aan punten toegevoegd
        self.__is_painting = False

        self.__pen_width = pen_width  # de diamter voor de getekende punten
        self.__color = QColor(0, 0, 0)  # de kleur van de getekende punten

        self.__is_calculating = False  # indien Painter aan Image de opdracht heeft om de Image te maken,
        #                                mag Painter niet meer reageren op mouse events

    def mousePressEvent(self, event):
        """
        Wanneer op de muis geklikt wordt in deze QWidget, wil dit zeggen dat de gebruiker wil tekenen

        :return: void
        """
        if not self.__is_calculating:
            self.__is_painting = True
            self.__huidige_punten = list()

    def mouseMoveEvent(self, event):
        """
        Wanneer de muis ingedrukt is (en ingedrukt blijft, self.__is_painting is niet op False gezet door
        mouseReleaseEvent()) en de gebruiker beweegt de muis wil dit zeggen dat de gebruiker aan het tekenen is.

        Het is noodzakelijk te controleren of de muis wel effectief binnen deze widget is. Zo niet zal Image een
        exceptie opgooien wanneer de punten worden toegevoegd. Als de gebruiker buiten het scherm blijkt te gaan, dan
        wordt een mouseReleaseEvent() gesimuleerd.

        :return: void
        """
        if not self.__is_calculating:
            if (event.x() > self.width()) or (event.x() < 0) or (event.y() > self.height()) or (event.y() < 0):
                self.mouseReleaseEvent(event)
            elif self.__is_painting:
                self.__huidige_punten.append(QPoint(event.x(), event.y()))
                print("mouse = ({}, {})".format(event.x(), event.y(),))
                self.repaint()

    def mouseReleaseEvent(self, event):
        """
        Wanneer de muis niet meer wordt ingedrukt, wil dat zeggen dat de gebruiker tijdelijk niet wil tekenen
        wanneer hij/zij de muis verschuift in deze QWidget

        :return: void
        """
        if not self.__is_calculating:
            self.__is_painting = False
            self.__punten.append(self.__huidige_punten.copy())  # alle gezette punten moeten getekend worden

    def mouseDoubleClickEvent(self, event):
        """
        Wanneer de gebruiker dubbel klikt (de tijd tussen twee keer klikken is hier gedefinieerd door het systeem
        van de gebruiker), dan wordt clearPunten() opgeroepen waardoor alle punten verdwijnen

        :return: void
        """
        if not self.__is_calculating:
            self.__clearPunten()

    def paintEvent(self, event):
        """
        De methode paintEvent() van QWidget wordt hier overschreven zodat de punten getekend worden op deze QWidget.
        Het echte tekenwerk wordt in de methode draw() verwerkt.

        :return: void
        """
        p = QPainter()
        p.begin(self)
        self.__draw(p)
        p.end()

    def __draw(self, p):
        """
        Deze methode wordt gebruikt om effectief alle punten op het scherm te tekenen. Aangezien de gebruiker relatief
        snel met de muis beweegt kunnen niet alle posities bij de beweging geregistreerd worden door de event handler
        van QApplication. Daarom wordt een rechte getekend tussen twee wel geregistreerde punten.

        :return: void
        """
        p.setRenderHint(QPainter.Antialiasing)  # dit is om, indien mogelijk, geen hoekige randen zichtbaar te hebben
        p.setPen(self.__makePen())

        for punten in self.__punten:
            for i in range(1, len(punten)):
                p.drawLine(punten[i - 1], punten[i])
        for i in range(1, len(self.__huidige_punten)):
            p.drawLine(self.__huidige_punten[i - 1], self.__huidige_punten[i])

    def __makePen(self):
        """
        Dit is een hulpmethode om de gepaste pen te maken die dan wordt teruggegeven

        :return: QPen
        """
        pen = QPen()
        pen.setColor(self.__color)
        pen.setBrush(QBrush(self.__color))
        pen.setWidth(self.__pen_width)
        return pen

    def getImage(self):
        """
        Deze methode gebruikt de getImage() van de klasse Image om aan de buitenwereld een getter te voorzien
        van het getekende cijfer voor verdere verwerking. De methode in Image voorziet al kopieren, dit hoeft niet nog
        eens gedaan te worden.

        :return: Image
        """
        image = Image(width=self.width(), height=self.height(), pen_width=self.__pen_width)
        print(len(self.__punten))
        for lijst in self.__punten:
            print(len(lijst))
            image.addListOfPoints(lijst)
        # hier niet gewoon image teruggeven, want dan is de image nog niet "gemaakt"

        # als de interpreter bezig is met rekenen om de image te maken, dan mag Painter niet meer reageren op
        # mouse events
        self.__is_calculating = True
        ret = image.getResizedImageToClosestMultiple(28, 28, True)
        self.__is_calculating = False
        return ret

    def __clearPunten(self):
        """
        Clear de noodzakelijke instantievariabelen om opnieuw te tekenen.
        Daarna wordt een repaint() uitgevoerd zodat ook de 'inkt' (van de QPen) van de QWidget verdwijnt

        :return: void
        """
        # TODO: in hoofdprogramma, als dit of getImage() opgeroepen wordt -> aan de gebruiker laten weten dat er
        #  berekeningen bezig zijn!
        print(self.getImage())  # TODO: haal deze print weg
        self.__punten = list(list())
        self.repaint()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Painter()
    main.show()
    sys.exit(app.exec_())
