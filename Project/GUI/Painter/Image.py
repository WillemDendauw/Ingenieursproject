# Voor een samenvattende uitleg van Image, zie #Stukjes code\Bram\3 - Painter\Samenvattende uitleg - Painter en Image\
# ======================================================================================================================
# ============================================   API VAN DE KLASSE Image   =============================================
# ======================================================================================================================
# # width : int                     breedte van de image in pixels
# # height : int                    hoogte van de image in pixels
# # points : list(list(QPoint))     list(QPoint) stelt 1 continue lijn van QPoints voor, een verzameling van lijsten
#                                   omdat anders (bv.) het onderste punt van een geschreven 7 met het stokje verbonden
#                                   wordt
# # image : list(list(int))         een matrix van pixels, de waarden zijn de grijswaarden (0-255)
# - pen_width                       breedte die de virtuele pen heeft, beste waarde is waarschijnlijk 20
# ----------------------------------------------------------------------------------------------------------------------
# + addListOfPoints() : void        een deel van een cijfer kan toegevoegd worden met deze methode
# + getImage() : list(list(int)     geeft een copy van de instantievariabele self._image terug (grijswaarde tussen
#                                   0 en 255)
# + getImageNormalized()            geeft een copy van de instantievariabele self._image terug maar genormaliseerd,
#       : list(list(float))         dus tussen 0 en 1 (getImage() / 255 dus)
# + makeImage() : void              hulpmethode die zorgt dat alle punten in de instantievariabele self._points
#                                   verwerkt wordt in het maken/updaten van
# - pointsToTreatAsPixels()         hulpmethode die de punten in self._points overloopt om er zeker van te zijn dat
#       : list(QPoint)              alle punten behandeld worden
# - listOfPointsOnLine()            hulpmethode die een reeks punten teruggeeft op de rechte tussen de twee
#       : list(QPoint)              meegegeven punten
# - simulateRealPen() : void        hulpmethode die een reele pen simuleert door meerdere pixels rondom elk punt van
#                                   pointsToTreatAsPixels() ook als pixels te behandelen
# - pixelValue() : int              hulpmethode die de pixelwaarde van een punt bepaalt dat binnen de cirkel met straal
#                                   self.__penWidth/2 en middelpunt een punt uit pointsToTreatAsPixels() ligt
# - d() : float                     hulpmethode die de afstand berekent tussen twee meegegeven punten
# # firstNonEmptyRow() : int        geeft de eerste niet lege rij van self._image terug van bovenaan bekeken
# # lastNonEmptyRow() : int         geeft de laatste niet lege rij van self._image terug van onderaan bekeken
# # firstNonEmptyCol() : int        geeft de eerste niet lege kolom van self._image terug van links bekeken
# # lastNonEmptyCol() : int         geeft de laatste niet lege kolom van self._image terug van rechts bekeken

from PyQt5.QtCore import QPoint
import math
import random


class Image:
    def __init__(self, width=28, height=28, penWidth=20):
        self._width = width
        self._height = height

        self._points = list(list())  # variabele die alle QPoints bijhoudt, zie addListOfPoints()
        self._image = [[0 for x in range(0, width)] for y in range(0, height)]
        # dit is dan de effectieve image die op de beschreven manier ingevuld wordt (beschrijving bij makeImage())

        self.__penWidth = penWidth  # dit is de breedte die de gesimuleerde pen moet hebben

    def addListOfPoints(self, points=list()):
        """
        Voeg de punten toe die je in deze image wil behandelen

        :return: void
        """
        # controleer dat alle punten binnen de afmetingen van deze image liggen
        for punt in points:
            if (punt.x() < 0) or (punt.x() >= self._width) or (punt.y() < 0) or (punt.y() >= self._height):
                points.remove(punt)
        self._points.append(points)

    def getImage(self, make=True):
        """
        Geeft een kopie terug van de instantievariabele image (grijswaarde tussen 0 en 255)

        :return: list(list(int))
        """
        # om er zeker van te zijn dat alle punten in self.punten verwerkt zijn
        self.makeImage()
        temp = [[self._image[i][j] for j in range(0, len(self._image[i]))] for i in range(0, len(self._image))]
        return temp

    def getImageNormalized(self):
        """
        Geeft een kopie terug van de instantievariabele image (grijswaarde tussen 0 en 1)

        :return: list(list(float))
        """
        # om er zeker van te zijn dat alle punten in self.punten verwerkt zijn
        self.makeImage()
        temp = [[self._image[i][j]/255 for j in range(0, len(self._image[i]))] for i in range(0, len(self._image))]
        return temp

    def makeImage(self):
        """
        Het volstaat niet om enkel en alleen om de QPoint's in self._points om te zetten naar 255. We zouden veel
        te weinig punten hebben omdat de gebruiker meestal te snel met de muis over het scherm beweegt. Daarom worden
        alle punten tussen twee geregistreerde punten behandeld en toegevoegd aan self._image

        Bovendien willen we ook het gebruik van een echte pen simuleren: daar loopt de inkt ook altijd een beetje uit,
        je schrijft niet met een oneindig dunne pen. Dit wordt gedaan omdat het neuraal netwerk getraind is met
        foto's van geschreven cijfers. Dit wordt gerealiseerd door voor elk punt de punten op een afstand kleiner
        dan self._width ook als pixels te beschouwen.

        Om te vermijden dat eerder gemaakte pixels van self._image zomaar overschreven worden, wordt enkel de hoogste
        grijswaarde van een eerder toegevoegde pixel bewaard. Ook zal ervoor gezorgd worden dat de randen zogezegd
        iets minder zwart zijn dan 255 om een gescheven cijfer goed te kunnen simuleren voor het neuraal netwerk

        :return: void
        """
        self._image = [[0 for x in range(0, self._width)] for x in range(0, self._height)]
        # we maken self._image opnieuw aan om zeker te zijn dat alle punten in self._points zijn behandeld
        for point in self.__pointsToTreatAsPixels():
            self.__simulateRealPen(point.x(), point.y())

    def __pointsToTreatAsPixels(self):
        """
        Dit is een hulpmethode die een lijst samenstelt met alle punten die als pixels moeten beschouwd worden.
        Met "alle punten" wordt in eerste instantie alle punten bedoeld die in de instantievariabele self._points zitten
        (dus de punten die reeds werden toegevoegd met self.addPieceOfNumber()) maar ook de punten die tussen
        twee door de gebruiker gezette punten (omdat wanneer we enkel met de geregistreerde punten werken, het er
        te weinig zijn. Dus we gebruiken ook punten op de rechte tussen twee geregistreerde punten)

        :return: list(QPoint)
        """
        temp = []
        for deel in self._points:
            for i in range(1, len(deel)):
                for punt in self.__listOfPointsOnLine(deel[i-1], deel[i]):
                    temp.append(punt)
        return temp

    def __listOfPointsOnLine(self, p1, p2):
        """
        Omdat de gebruiker relatief snel met de muis beweegt, worden veel muis-posities niet geregistreerd. Om dit op
        te vangen geeft deze functie een lijst van alle punten tussen twee geregistreerde punten p1 en p2 terug

        :return: list(QPoint)
        """
        temp = [p1]
        point = [p1.x(), p1.y()]  # punt dat verschoven wordt van p1 -> p2
        p1p2 = [(p2.x()-p1.x())/self.__d(p1.x(), p1.y(), p2.x(), p2.y()),
                (p2.y()-p1.y())/self.__d(p1.x(), p1.y(), p2.x(), p2.y())]
        # p1p2 is de eeheidsvector volgens lijnstuk [p1, p2]

        # zolang de afstand tussen p1 en point kleiner is dan p1 en p2, wil dat zeggen dat er nog mogelijks punten
        # zijn die moeten toegevoegd worden (Lijnstuk: p1--------point->-------p2 met point die steeds naar p2
        # verschoven wordt in eenheden volgens de eenheidsvector p1p2
        while self.__d(point[0], point[1], p1.x(), p1.y()) < self.__d(p1.x(), p1.y(), p2.x(), p2.y()):
            point = [point[0] + p1p2[0], point[1] + p1p2[1]]
            temp.append(QPoint(point[0], point[1]))
        temp.append(p2)
        return temp

    def __simulateRealPen(self, x, y):
        """
        We willen het gebruik van een echte pen simuleren: daar loopt de inkt ook altijd een beetje uit,
        je schrijft niet met een oneindig dunne pen. Dit wordt gerealiseerd door voor elk punt de punten op een afstand
        kleiner dan self.__penWidth ook als pixels te beschouwen. Dit doen we omdat anders te weinig punten
        punten zullen hebben om iets nuttig mee te doen.

        Twee opmerkingen (zie eerst de code):
        - voor elke combinatie (x+dx[i], y+dy[j]) zien we dat er enkele combinaties resulteren in een
        __d(x, y, x+dx[i], y+dy[j]) groter dan self.__penWidth/2, dit is niet erg want dit wordt opgevangen
        in self.__pixelValue() (merk op: het is self.__penWidth/2 en niet self.__penWidth omdat self.__penWidth
        een diameter is)
        - het zou kunnen zijn dat (x+dx[i], y+dy[j]) resulteert in een pixel buiten het bereik van de QWidget. Dit zal
        dan resulteren in een IndexError -> die combinaties zullen genegeerd worden dankzij de if-clausule

        :return: void
        """
        dx = [i for i in range(int(-self.__penWidth / 2), int(self.__penWidth / 2) + 1)]
        dy = [i for i in range(int(-self.__penWidth / 2), int(self.__penWidth / 2) + 1)]

        for j in dy:
            for i in dx:
                if (y + j >= 0) and (y + j < self._height) and (x + i >= 0) and (x + i < self._width)\
                        and (self._image[y + j][x + i] < round(self.__pixelValue(x+i, y+j, x, y))):
                    self._image[y + j][x + i] = round(self.__pixelValue(x+i, y+j, x, y))

    def __pixelValue(self, x1, y1, x2, y2):
        """
        Dit is een hulpmethode om te bepalen welke grijswaarde op pixel (x1, y1) moet komen.
        Om dit te realiseren wordt ook de hulpfunctie __d() gebruikt die de afstand tussen twee punten bepaalt

        (x1, y1) is het te controleren pixel
        (x2, y2) is een getekend punt (gezet door gebruiker of extra toegevoegd in __pointsToTreatAsPixels

        :return: int
        """
        if self.__d(x1, y1, x2, y2) > self.__penWidth/2:
            return 0
        # indien het te controleren punt dichter dan 25% van de penbreedte verwijderd is van het getekende punt, dan
        # wordt een relatief hoge grijswaarde gekozen
        if self.__d(x1, y1, x2, y2) < self.__penWidth*0.25:
            return random.randint(250, 255)
        temp = 220 / round(self.__penWidth / 2)
        return random.randint(200, 250)

    def __d(self, x1, y1, x2, y2):
        """
        Deze methode geeft de afstand tussen punten (x1, y1) en (x2, y2)

        :return: float
        """
        return math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))

    def _firstNonEmptyRow(self):
        """
        Geeft het kleinste y-coordinaat weer die in self._points zit, dit is de eerste niet nulrij

        :return: int
        """
        smallest_y = self._points[0][0].y()
        for points in self._points:
            for point in points:
                if smallest_y > point.y():
                    smallest_y = point.y()
        return int(smallest_y)

    def _lastNonEmptyRow(self):
        """
        Geeft het grootste y-coordinaat weer die in self._points zit, dit is de eerste niet nulrij gekeken van
        onderaan

        Het is de bedoeling dat self._lastNonEmptyRow() - self._firstNonEmptyRow) de hoogte terug geeft van alle
        punten die op dit ogenblik in self._points zit. Dit is noodzakelijk om de image te kunnen compresseren

        :return: int
        """
        biggest_y = self._points[0][0].y()
        for points in self._points:
            for point in points:
                if biggest_y < point.y():
                    biggest_y = point.y()
        return int(biggest_y)

    def _firstNonEmptyCol(self):
        """
        Geeft het kleinste x-coordinaat weer die op dit moment in self._points zit, dit is de eerste niet nul-kolom

        :return: int
        """
        smallest_x = self._points[0][0].x()
        for points in self._points:
            for point in points:
                if smallest_x > point.x():
                    smallest_x = point.x()
        return int(smallest_x)

    def _lastNonEmptyCol(self):
        """
        Geeft het grootste x-coordinaat weer die op dit moment in self._points zit, dit is de eerste niet nul-kolom
        van rechts bekeken

        Het is de bedoeling dat self._lastNonEmptyCol() - self._firstNonEmptyCol() de breedte terug geeft van alle
        punten die op dit ogenblik in self._points zit. Dit is noodzakelijk om de image te kunnen compresseren

        :return: int
        """
        biggest_x = self._points[0][0].x()
        for points in self._points:
            for point in points:
                if biggest_x < point.x():
                    biggest_x = point.x()
        return int(biggest_x)
