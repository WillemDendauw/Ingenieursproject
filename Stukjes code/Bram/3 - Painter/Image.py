# Voor een samenvattende uitleg van Image, zie #Stukjes code\Bram\3 - Painter\Samenvattende uitleg - Painter en Image\
# ======================================================================================================================
# ============================================   API VAN DE KLASSE Image   =============================================
# ======================================================================================================================
# - width : int                     breedte van de image in pixels
# - height : int                    hoogte van de image in pixels
# - points : list(list(QPoint))     list(QPoint) stelt 1 continue lijn van QPoints voor, een verzameling van lijsten
#                                   omdat anders (bv.) het onderste punt van een geschreven 7 met het stokje verbonden
#                                   wordt
# - image : list(list(int))         een matrix van pixels, de waarden zijn de grijswaarden (0-255)
# - pen_width                       breedte die de virtuele pen heeft, beste waarde is waarschijnlijk 3
# ----------------------------------------------------------------------------------------------------------------------
# + addListOfPoints() : void        een deel van een cijfer kan toegevoegd worden met deze methode
# + getResizedImageToClosest...     deze methode past self.__points en self.__image zodanig aan dat self.__width en
#     ...Multiple() : Image         self.__height een geheel veelvoud worden van de meegegeven parameters
# + getImage() : list(list(int)     geeft een copy van de instantievariabele self.__image terug (grijswaarde tussen
#                                   0 en 255)
# + getNormalizedImage              geeft een genormaliseerde kopie van self.__image terug (grijswaarde tussen 0 en 1)
#       : list(list(int))           (deze methode is toegevoegd voor moest dit nodig blijken te zijn)
# - makeImage() : void              hulpmethode die zorgt dat alle punten in de instantievariabele self.__points
#                                   verwerkt wordt in het maken/updaten van
# - pointsToTreatAsPixels()         hulpmethode die de punten in self.__points overloopt om er zeker van te zijn dat
#       : list(QPoint)              alle punten behandeld worden
# - listOfPointsOnLine()             hulpmethode die een reeks punten teruggeeft op de rechte tussen de twee
#       : list(QPoint)              meegegeven punten
# - simulateRealPen() : void        hulpmethode die een reele pen simuleert door meerdere pixels rondom elk punt van
#                                   pointsToTreatAsPixels() ook als pixels te behandelen
# - pixelValue() : int              hulpmethode die de pixelwaarde van een punt bepaalt dat binnen de cirkel met straal
#                                   self.__pen_width/2 en middelpunt een punt uit pointsToTreatAsPixels() ligt
# - d() : float                     hulpmethode die de afstand berekent tussen twee meegegeven punten
# - first_non_empty_row() : int     geeft de eerste niet lege rij van self.__image terug van bovenaan bekeken
# - last_non_empty_row() : int      geeft de eerste niet lege rij van self.__image terug van onderaan bekeken
# - first_non_empty_col() : int     geeft de eerste niet lege kolom van self.__image terug van links bekeken
# - last_non_empty_col() : int      geeft de laatste niet lege kolom van self.__image terug van rechts bekeken

from PyQt5.QtCore import QPoint
import math
import random


class Image:
    def __init__(self, width=28, height=28, pen_width=3):
        self.__width = width
        self.__height = height

        self.__points = list(list())  # variabele die alle QPoints bijhoudt, zie addListOfPoints()
        self.__image = [[0 for x in range(0, width)] for y in range(0, height)]
        # dit is dan de effectieve image die op de beschreven manier ingevuld wordt (beschrijving bij __makeImage())

        self.__pen_width = pen_width  # dit is de breedte die de gesimuleerde pen moet hebben

    def addListOfPoints(self, punten=list()):
        # controleer dat alle punten binnen de afmetingen van deze image liggen
        for punt in punten:
            if (punt.x() < 0) or (punt.x() >= self.__width) or (punt.y() < 0) or (punt.y() >= self.__height):
                raise IndexError("Een punt buiten bereik van deze {}x{} Image werd meegegeven: ({},{})"
                                 "\n\tLet op: een foto van 28x28 heeft een width en height van "
                                 "28 maar pixels worden geindexeerd tussen 0 en 27, dus 28 pixels)"
                                 .format(self.__width, self.__height, punt.x(), punt.y()))
        self.__points.append(punten)

    def getResizedImageToClosestMultiple(self, width, height, rect=True):
        """
        Deze methode past self.__points en self.__image zodanig aan dat self.__width en self.__height het eerstvolgende
        geheel veelvoud worden van de meegegeven parameters (self.__width en self.__height worden dus ook aangepast)
        Dit gebeurt enkel indien self.__width of self.__height nog geen veelvoud van width of height zijn.

        Dankzij het feit dat met QPunten wordt gewerkt die beginnende bij self.__makeImage() verwerkt worden en omgezet
        worden naar een matrix van grijswaarden is het zeer eenvoudig dit te resaliseren: we moeten juist maar een
        nieuwe instantie van Image creeren met de bepaalde groottes en vervolgens alle QPoints in self.__points
        toevoegen met de juiste offset.

        Bovendien wordt dit niet zomaar gedaan, we proberen het cijfer te centreren omdat het neuraal netwerk
        ook met gecentreerde foto's getraind is. Vandaar dat we eerst op zoek moeten naar de eerste en laatste
        niet lege rij en kolom van self.__image

        Merk het volgende op: indien het aantal toe te voegen getallen voor elke rij een oneven getal blijkt, dan wordt
        vooraan een getal minder toegevoegd. Dit geldt ook voor de kolommen, dan wordt onderaan een getal minder
        toegevoegd. Dit komt omdat toe_te_voegen_per_... gedeeld wordt door 2 en gecast wordt naar een int.

        :return: Image
        """
        self.__makeImage()
        # eerst en vooral zorgen we ervoor dat we 100% zeker zijn dat alle punten in self.__points verwerkt zijn

        toe_te_voegen_per_rij, toe_te_voegen_per_kolom = 0, 0
        # deze variabelen geven resp. het aantal kolommen/rijen weer die toegevoegd moeten worden om aan het
        # eerstvolgend geheel veelvoud van width/height te komen indien dit al geen veelvoud is
        while ((self.__last_non_empty_col() - self.__first_non_empty_col() + 1) + toe_te_voegen_per_rij) % width != 0:
            toe_te_voegen_per_rij += 1
        while ((self.__last_non_empty_row() - self.__first_non_empty_row() + 1) + toe_te_voegen_per_kolom) % height != 0:
            toe_te_voegen_per_kolom += 1

        # indien de gebruiker verlangt dat het een temp (zie verder) een rechthoek moet zijn moeten de meegegeven
        # parameters even groot worden, de grootste wint
        temp_width = (self.__last_non_empty_col() - self.__first_non_empty_col() + 1) + toe_te_voegen_per_rij
        temp_height = (self.__last_non_empty_row() - self.__first_non_empty_row() + 1) + toe_te_voegen_per_kolom
        if rect:
            if  temp_width > temp_height:
                temp_height = temp_width
                toe_te_voegen_per_kolom = toe_te_voegen_per_rij
            else:
                temp_width = temp_height
                toe_te_voegen_per_rij = toe_te_voegen_per_kolom

        # we maken een nieuwe Image aan, de QPoints in self.punten zullen op dezelfde plaats worden gekopieerd maar
        # met de correcte bijhorende offsets
        temp = Image(width=temp_width, height=temp_height, pen_width=self.__pen_width)

        # alle QPoints met de juiste offset van self.__points worden toegevoegd aan temp.points
        for lijst in self.__points:
            temp.addListOfPoints([QPoint(lijst[i].x() - self.__first_non_empty_col() + int(toe_te_voegen_per_rij/2),
                                         lijst[i].y() - self.__first_non_empty_row() + int(toe_te_voegen_per_kolom/2))
                                  for i in range(0, len(lijst))])
        return temp

    def __first_non_empty_row(self):
        """
        Geeft de eerste niet nulrij terug van self.__image
        :return: int
        """
        eerste_niet_nul_rij = -1
        i, j = -1, -1
        # normaal begin ik van 0 en op het einde van een while-lus vermeerder ik met 1 maar nu niet
        # eerst gaan we op zoek naar de eerste niet nulrij (beginnende van bovenaan)
        while (i < self.__height - 1) and (eerste_niet_nul_rij == -1):
            i += 1
            j = -1
            while (j < self.__width - 1) and (eerste_niet_nul_rij == -1):
                j += 1
                if self.__image[i][j] != 0:
                    eerste_niet_nul_rij = i
        return eerste_niet_nul_rij

    def __last_non_empty_row(self):
        """
        Geeft de laatste niet nulrij van self.__image terug
        :return: int
        """
        laatste_niet_nul_rij = -1
        # dan gaan we op zoek naar de eerste niet nulrij beginnende van onderaan
        i, j = 0, 0  # normaal zou ik hier beginnen met 1 maar wegens positie van vermeerderen in while-lus niet
        while (i < self.__height) and (laatste_niet_nul_rij == -1):
            i += 1
            j = 0
            while (j < self.__width) and (laatste_niet_nul_rij == -1):
                j += 1
                if self.__image[-i][-j] != 0:
                    laatste_niet_nul_rij = self.__height - i
        return laatste_niet_nul_rij

    def __first_non_empty_col(self):
        """
        Geeft de eerste niet nulkolom van self.__image terug
        :return: int
        """
        eerste_niet_nul_kolom = -1
        # vervolgens gaan we op zoek naar de eerste niet nulkolom beginnende van links
        i, j = -1, -1
        while (j < self.__width - 1) and (eerste_niet_nul_kolom == -1):
            j += 1
            i = -1
            while (i < self.__height - 1) and (eerste_niet_nul_kolom == -1):
                i += 1
                if self.__image[i][j] != 0:
                    eerste_niet_nul_kolom = j
        return eerste_niet_nul_kolom

    def __last_non_empty_col(self):
        """
        Geeft de laatste niet nulkolom van self.__image terug
        :return: int
        """
        laatste_niet_nul_kolom = -1
        # en tot slot zoeken we naar de laatste niet nulkolom beginnende van rechts
        i, j = 0, 0
        while (j < self.__width) and (laatste_niet_nul_kolom == -1):
            j += 1
            i = 0
            while (i < self.__height) and (laatste_niet_nul_kolom == -1):
                i += 1
                if self.__image[-i][-j] != 0:
                    laatste_niet_nul_kolom = self.__width - j
        return laatste_niet_nul_kolom

    def getImage(self):
        """
        Geeft een kopie terug van de instantievariabele image (grijswaarde tussen 0 en 255)

        :return: list(list(int))
        """
        self.__makeImage()  # om er zeker van te zijn dat alle punten in self.punten verwerkt zijn
        temp = [[self.__image[i][j] for j in range(0, len(self.__image[i]))] for i in range(0, len(self.__image))]
        return temp

    def getNormalizedImage(self):
        """
        Geeft een genormalizeerde terug van de instantievariabele image (grijswaarde tussen 0 en 1)

        :return: list(list(float))
        """
        self.__makeImage()
        temp = [[self.__image[i][j]/255 for j in range(0, len(self.__image[i]))] for i in range(0, len(self.__image))]
        return temp

    def __makeImage(self):
        """
        Het volstaat niet om enkel en alleen om de QPoint's in self.__points om te zetten naar 255. We zouden veel
        te weinig punten hebben omdat de gebruiker meestal te snel met de muis over het scherm beweegt. Daarom worden
        alle punten tussen twee geregistreerde punten behandeld en toegevoegd aan self.__image

        Bovendien willen we ook het gebruik van een echte pen simuleren: daar loopt de inkt ook altijd een beetje uit,
        je schrijft niet met een oneindig dunne pen. Dit wordt gedaan omdat het neuraal netwerk getraind is met
        foto's van geschreven cijfers. Dit wordt gerealiseerd door voor elk punt de punten op een afstand kleiner
        dan self.__width ook als pixels te beschouwen.

        Om te vermijden dat eerder gemaakte pixels van self.__image zomaar overschreven worden, wordt enkel de hoogste
        grijswaarde van een eerder toegevoegde pixel bewaard. Ook zal ervoor gezorgd worden dat de randen zogezegd
        iets minder zwart zijn dan 255 om een gescheven cijfer goed te kunnen simuleren voor het neuraal netwerk

        :return: void
        """
        self.__image = [[0 for x in range(0, self.__width)] for x in range(0, self.__height)]
        # we maken self.__image opnieuw aan om zeker te zijn dat alle punten in self.__points zijn behandeld
        for point in self.__pointsToTreatAsPixels():
            self.__simulateRealPen(point.x(), point.y())

    def __pointsToTreatAsPixels(self):
        """
        Dit is een hulpmethode die een lijst samenstelt met alle punten die als pixels moeten beschouwd worden.
        Met "alle punten" wordt in eerste instantie alle punten bedoeld die in de instantievariabele self.__points zitten
        (dus de punten die reeds werden toegevoegd met self.addPieceOfNumber()) maar ook de punten die tussen
        twee door de gebruiker gezette punten (omdat wanneer we enkel met de geregistreerde punten werken, het er
        te weinig zijn. Dus we gebruiken ook punten op de rechte tussen twee geregistreerde punten)

        :return: list(QPoint)
        """
        temp = []
        for deel in self.__points:
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
        je schrijft niet met een oneindig dunne pen. Dit wordt gedaan omdat het neuraal netwerk getraind is met
        foto's van geschreven cijfers. Dit wordt gerealiseerd door voor elk punt de punten op een afstand kleiner
        dan self.__pen_width ook als pixels te beschouwen.

        Twee opmerkingen (zie eerst de code):
        - voor elke combinatie (x+dx[i], y+dy[j]) zien we dat er enkele combinaties resulteren in een
        __d(x, y, x+dx[i], y+dy[j]) groter dan self.__pen_width/2, dit is niet erg want dit wordt opgevangen
        in self.__pixelValue() (merk op: het is self.__pen_width/2 en niet self.__pen_width omdat self.__pen_width
        een diameter is)
        - het zou kunnen zijn dat (x+dx[i], y+dy[j]) resulteert in een pixel buiten het bereik van de QWidget. Dit zal
        dan resulteren in een IndexError -> die combinaties zullen genegeerd worden dankzij de if-clausule

        :return: void
        """
        dx = [i for i in range(int(-self.__pen_width/2), int(self.__pen_width/2) + 1)]
        dy = [i for i in range(int(-self.__pen_width/2), int(self.__pen_width/2) + 1)]
        for j in dy:
            for i in dx:
                if (y + j >= 0) and (y + j < self.__height) and (x + i >= 0) and (x + i < self.__width)\
                        and (self.__image[y + j][x + i] < round(self.__pixelValue(x+i, y+j, x, y))):
                    self.__image[y + j][x + i] = round(self.__pixelValue(x+i, y+j, x, y))

    def __pixelValue(self, x1, y1, x2, y2):
        """
        Dit is een hulpmethode om te bepalen welke grijswaarde op pixel (x1, y1) moet komen.
        Om dit te realiseren wordt ook de hulpfunctie __d() gebruikt die de afstand tussen twee punten bepaalt

        (x1, y1) is het te controleren pixel
        (x2, y2) is een getekend punt (gezet door gebruiker of extra toegevoegd in __pointsToTreatAsPixels

        :return: int
        """
        if self.__d(x1, y1, x2, y2) > self.__pen_width/2:
            return 0
        if self.__d(x1, y1, x2, y2) == 0:
            return random.randint(220, 255)
        temp = 220 / round(self.__pen_width/2)
        return random.randint(int(220 - (temp*int(self.__d(x1, y1, x2, y2)) + temp)),
                              int(220 - (temp*int(self.__d(x1, y1, x2, y2)))))

    def __d(self, x1, y1, x2, y2):
        """
        Deze methode geeft de afstand tussen punten (x1, y1) en (x2, y2)

        :return: float
        """
        return math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))

    def __repr__(self):
        temp = "Image of {}x{}:\n".format(self.__width, self.__height)
        for rij in self.getImage():
            for pixel in rij:
                temp += "{:4}".format(pixel)
            temp += "\n"
        return temp


if __name__ == "__main__":
    print("====================     BEGIN TESTEN VAN Image.py     ====================")

    img = Image(50, 50)

    temp1 = []
    for a in range(5, 28, 5):
        temp1.append(QPoint(20, a))
    temp2 = []
    for a in range(0, 10, 3):
        temp2.append(QPoint(0, a))
    img.addListOfPoints(temp1.copy())
    img.addListOfPoints(temp2.copy())

    print(img)
    print("===========================================================================")
    print(img.getResizedImageToClosestMultiple(28, 28))
    print("====================     EINDE TESTEN VAN Image.py     ====================")
