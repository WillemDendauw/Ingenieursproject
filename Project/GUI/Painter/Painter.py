# Voor een samenvattende uitleg van Painter, zie #Stukjes code\Bram\3 - Painter\Samenvattende uitleg - Painter en Image
# ======================================================================================================================
# ===========================================   API VAN DE KLASSE Painter   ============================================
# ======================================================================================================================
# - points : list(list(QPoint))     houdt alle door de gebruiker geplaatste QPoints bij
# - currentDrawingPoints            houdt de QPoints van de huidige/laatste vloeiende lijn bij (tussen mousePressed-
#       : list(QPoint)              en mouseReleaseEvent
# - isPainting : bool               boolean die zegt of de gebruiker aan het tekenen is of niet
# - isCalculating : bool            wanneer Image en CompressedImage aan het rekenen zijn, mag Painter niet luisteren
#                                   naar events die binnenkomen
# - penWidth : int                  hoe dik de pen is die wordt gebruikt om te tekenen, in pixels
# - color : QColor                  variabele die de kleur van de pen bijhoudt die gebruikt wordt om te tekenen
#                                   (default kleur is zwart)
# ----------------------------------------------------------------------------------------------------------------------
# + mousePressEvent : void          bij het drukken op de muis, wil de gebruiker tekenen
# + mouseMoveEvent : void           als op de muis werd geklikt en de muis beweegt, dan tekent de gebruiker
# + mouseReleaseEvent : void        als de muis wordt losgelaten wil de gebruiker niet meer tekenen
# + paintEvent : void               hier staat de effectieve code voor het tekenen, het gebruikt de hulpmethode draw()
# - draw : void                     een hulmethode om te tekenen
# - makePen : QPen                  een hulmethode die de gewenste QPen maakt en teruggeeft
# + getInput() : list(float)        op basis van alle punten getekend in Painter, wordt het input gegenereerd voor het
#                                   neurale netwerk
# + getInputAsMatrix()              op basis van alle punten getekend in Painter, wordt het input gegenereerd maar
#       : list(list(float))           in plaats van een lijst, als matrix (handig voor te testen in command line)
# + clearPunten : void              bij het dubbelklikken wordt deze methode gebruikt
# - testOutput() : void             Om op de command line de output van deze Painterklasse eens te testen
# + getPunten() : list(list(tuple)  geeft een kopie van de instantievariabele self.__points maar als tuple van x- en
#                                   y- coordinaten i.p.v. QPoints

from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QPoint

from GUI.Painter.CompressedImage import CompressedImage


class Painter(QWidget):
    """
    Painter is de klasse waarin de gebruiker van de applicatie kan tekenen. Elk punt die de event handler kan opvangen
    wordt in deze klasse bijgehouden. Elke lijn die de gebruiker tekent zonder de muis los te laten, i.e. een vloeiende
    lijn, wordt in een aparte lijst bijgehouden zodat alle vloeiende lijnen apart worden getekend en niet met
    elkaar worden verbonden.

    De gebruiker van deze klasse maakt een object van deze klasse zoals hij elke andere QWidget zou aanmaken. Aan
    de constructor van deze klasse kan worden meegegeven wie de ouder is, indien None wordt het object als een
    stand-alone venster aangemaakt. Daarnaast kan meegegeven worden hoe dik de getekende lijnen moeten zijn in pixel-
    waarde, dit doe je door een waarde aan penWidth mee te geven (de default-waarde is 3). Tot slot kan ook het
    kleur meegegeven worden in dewelke de lijn wordt getekend, standaard is deze zwart.
    """
    def __init__(self, parent=None, penWidth=3, color=QColor(0, 0, 0)):
        super(Painter, self).__init__()
        self.setParent(parent)

        self.__points = []  # elke lijst in punten bevat een reeks QPoint's. Ik heb een lijst van
        # lijsten gemaakt zodat wanneer de gebruiker de muisknop loslaat en vervolgens
        # opnieuw een deeltje wil tekenen (zoals bij een en 4, 7) dat geen lijnen van
        # het laatst en eerste QPoint getekend  worden
        self.__currentDrawingPoints = []  # deze wordt na elke mouseReleaseEvent aan punten toegevoegd

        self.__isPainting = False
        self.__isCalculating = False  # indien Painter aan Image de opdracht heeft om de Image te maken,
        #                                mag Painter niet meer reageren op mouse events

        self.__penWidth = penWidth  # de diamter voor de getekende punten
        self.__color = color  # de kleur van de getekende punten

    def mousePressEvent(self, event):
        """
        Wanneer op de muis geklikt wordt in deze QWidget, wil dit zeggen dat de gebruiker wil tekenen

        :return: void
        """
        if not self.__isCalculating:
            self.__isPainting = True
            self.__currentDrawingPoints = []

    def mouseMoveEvent(self, event):
        """
        Wanneer de muis ingedrukt is (en ingedrukt blijft, self.__isPainting is niet op False gezet door
        mouseReleaseEvent()) en de gebruiker beweegt de muis wil dit zeggen dat de gebruiker aan het tekenen is.

        Het is noodzakelijk te controleren of de muis wel effectief binnen deze widget is. Zo niet zal Image een
        exceptie opgooien wanneer de punten worden toegevoegd. Als de gebruiker buiten het scherm blijkt te gaan, dan
        wordt een mouseReleaseEvent() gesimuleerd.

        :return: void
        """
        if not self.__isCalculating:
            if (event.x() > self.width()) or (event.x() < 0) or (event.y() > self.height()) or (event.y() < 0):
                self.mouseReleaseEvent(event)
            elif self.__isPainting:
                self.__currentDrawingPoints.append(QPoint(event.x(), event.y()))
                self.repaint()

    def mouseReleaseEvent(self, event):
        """
        Wanneer de muis niet meer wordt ingedrukt, wil dat zeggen dat de gebruiker tijdelijk niet wil tekenen
        wanneer hij/zij de muis verschuift in deze QWidget.

        Hier is het van groot belang dat alle continue lijnen in een aparte lijst worden gestoken omdat de hulpmethode
        self.__draw() anders elk punt die volgt op elkaar in de lijst self.__points met elkaar zal verbinden waardoor
        de onderkant van een 7 zal verbonden worden met het horizontale streepje dat in het midden van het cijfer
        wordt getekend. De variabele self.__isPainting moet ook op False gezet worden zodat self.mouseMoveEvent() niet
        meer reageert op mouse-events tot de gebruiker weer met de muis in deze Painter heeft geklikt.

        De lijst self.__huidigePunten wordt pas gecleard in self.mousePressEvent voor performatieredenen: als de
        gebruiker niet meer wil tekenen is het niet nodig dat deze lijst nog eens leeg wordt gemaakt

        :return: void
        """
        if not self.__isCalculating:
            self.__isPainting = False
            self.__points.append(self.__currentDrawingPoints.copy())  # alle gezette punten moeten getekend worden

    def paintEvent(self, event):
        """
        De methode paintEvent() van QWidget wordt hier overschreven zodat de punten getekend worden op deze QWidget.
        Het echte tekenwerk wordt in de hulpmethode self.__draw() verwerkt.

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

        for punten in self.__points:
            for i in range(1, len(punten)):
                p.drawLine(punten[i - 1], punten[i])
        for i in range(1, len(self.__currentDrawingPoints)):
            p.drawLine(self.__currentDrawingPoints[i - 1], self.__currentDrawingPoints[i])

    def __makePen(self):
        """
        Dit is een hulpmethode om de gepaste pen te maken die dan wordt teruggegeven

        :return: QPen
        """
        pen = QPen()
        pen.setColor(self.__color)
        pen.setBrush(QBrush(self.__color))
        pen.setWidth(self.__penWidth)
        return pen

    def getInput(self):
        """
        Alle punten die op dit moment in self.__points zitten, worden door de klasse CompressedImage omgezet naar een
        lijst van grijswaarden die als input bedoeld zijn voor het neurale netwerk.

        :return: list(float)
        """
        compressedImage = CompressedImage(width=self.width(), height=self.height(), penWidth=20)

        for lijst in self.__points:
            compressedImage.addListOfPoints(lijst)
        # hier niet gewoon image teruggeven, want dan is de image nog niet "gemaakt"

        # als de interpreter bezig is met rekenen om de image te maken, dan mag Painter niet meer reageren op
        # mouse events
        self.__isCalculating = True
        ret = compressedImage.toList()
        self.__isCalculating = False
        return ret

    def getInputAsMatrix(self):
        """
        Dit doet hetzelfde als self.getInput() maar geeft geen lijst maar matrix terug. Dit is handig als je deze
        input wil controleren in de command line (wordt overigens gebruikt door de hulpmethode self.__testOutput(),
        zie verder).

        :return: list(list(float))
        """
        compressedImage = CompressedImage(width=self.width(), height=self.height(), penWidth=20)

        for lijst in self.__points:
            compressedImage.addListOfPoints(lijst)
        # hier niet gewoon image teruggeven, want dan is de image nog niet "gemaakt"

        # als de interpreter bezig is met rekenen om de image te maken, dan mag Painter niet meer reageren op
        # mouse events
        self.__isCalculating = True
        ret = compressedImage.compressImage()
        self.__isCalculating = False
        return ret

    def clearPunten(self, print=False):
        """
        Reset de noodzakelijke instantievariabelen om opnieuw te tekenen en te beginnen van een lege Painter.
        Daarna wordt een repaint() uitgevoerd zodat ook de 'inkt' (van de QPen) van de QWidget verdwijnt.

        Tijdens de ontwikkeling van deze klasse was het noodzakelijk te weten wat de exacte output van deze klasse
        zou zijn, dus net voordat het Painter-object wordt gereset krijgt de gebruiker van deze klasse de mogelijkheid
        om met de boolean variabele 'print' alle punten in matrix-vorm uit te printen met behulp van de hulpmethode
        self.__testOutput()

        :return: void
        """
        if print:
            self.__testOutput()
        self.__points.clear()
        self.__currentDrawingPoints.clear()
        self.repaint()

    def __testOutput(self):
        """
        Private methode om de output uit te testen, de output
        wordt naar de command line geschreven.

        :return: void
        """
        #Om te testen:
        output = self.getInputAsMatrix()
        te_printen = ""
        for i in range(len(output)):
            for j in range(len(output[i])):
                te_printen += "{:4}".format(int(output[i][j]*255))
            te_printen += "\n"
        print(te_printen)

    def getPunten(self):
        """
        Deze methode geeft een tuple van x- en y-coordinaten terug van
        alle punten die in de instantievariabele self.__points zit.

        De reden waarom lijsten van lijsten van tuples worden teruggegeven
        en niet van QPoints is omdat op deze manier MainGUI de omzetting
        niet meer moet doen, bovendien kan er zo met zekerheid ook geen
        privacy leak zijn.

        Deze methode wordt dus door MainGUI gebruikt om de verzameling
        van de getekende punten op te vragen om vervolgens deze lijst
        om te zetten naar de juiste numpy.ndarray structuur. En dat dan
        mee te geven als input voor het neuraal netwerk.

        :return: list(list(tuple))
        """
        ret = []
        for lijst in self.__points:
            temp = []
            for punt in lijst:
                temp.append((punt.x(), punt.y()))
            ret.append(temp)
        return ret
