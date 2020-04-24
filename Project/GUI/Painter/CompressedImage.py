# ======================================================================================================================
# ============================================   API VAN DE KLASSE CompressorIMG   =====================================
# ======================================================================================================================
# - compressedResolution: int           de lengte van 1 zijde van de eindafbeelding (in pixels)
# ----------------------------------------------------------------------------------------------------------------------
# + compressImage(): list(list(float))  de methode die de afbeelding compresseert in 28X28 pixels
# + toList(): list(float)               geeft een meegegeven list(list(int)) weer als 1 lange list
from PyQt5.QtCore import QPoint

from GUI.Painter.Image import Image


class CompressedImage(Image):
    """
    Het neurale netwerk verwacht een lijst van 784 decimale waarden tussen 0 en 1 als input. De betekenis hiervan
    is een 28x28 matrix van pixels, de pixels zijn grijswaarden tussen 0 en 1. Alle rijen achter elkaar gezet levert
    een lijst van 784.

    Deze klasse CompressedImage, afgeleid van Image, zet alle punten (die op het moment van oproepen in self._points
    zit) om in een 28x28 formaat. We kunnen moeilijk aan de gebruiker van deze applicatie vragen om een cijfer
    te tekenen in een veldje van 28x28, dat zou veel te klein zijn. Daarom zetten we met wat eenvoudige wiskunde
    alle punten om. De coordinaten van elk punt in de lijsten van self._points wordt gewoon op een nieuw assenstelsel
    gemapt. Dit gebeurt op basis van de breedte en hoogte van het getekende cijfer wat door de methodes lastNonEmptyRow,
    lastNonEmptyCol, firstNonEmptyRow en firstNonEmptyCol kan worden berekend, elk punt wordt dus gewoon herschaald
    en verschoven.

    De methode compressImage() doet precies wat in de vorige paragraaf staat beschreven, de methode toList() voert
    eerst een compressImage() uit en maakt van de teruggegeven matrix een lange lijst van de punten die in elke rij zit.
    """
    def __init__(self, width=28, height=28, penWidth=3, compressedResolution=28):
        super().__init__(width, height, penWidth)
        self.__compressedResolution = compressedResolution

    def compressImage(self):
        """
        Voor de uitleg, zie uitleg bij de klasse. Die bevat alles wat nodig is om te weten over de twee methodes
        van deze klasse.

        :return: list(list(float))
        """
        temp_width = self._lastNonEmptyCol() - self._firstNonEmptyCol()
        temp_height = self._lastNonEmptyRow() - self._firstNonEmptyRow()
        img = Image(28, 28, 3)

        if temp_width == 0 or temp_height == 0:
            return img.getImageNormalized()

        for points in self._points:
            # temp houdt alle punten in tuple bij van een continue lijn, dit is om gemakkelijk te kijken of er geen
            # duplicaten in temp_qpoint zouden terechtkomen
            temp = []
            temp_qpoints = []
            for point in points:
                # de x- en y- coordinaten van gezette punten herberekenen naar een 28x28 matrix i.p.v. een
                # temp_width x temp_height matrix
                x = int(((point.x() - self._firstNonEmptyCol())/temp_width) * 18) + 4
                y = int(((point.y() - self._firstNonEmptyRow()) / temp_height) * 18) + 4

                if not (x, y) in temp:
                    temp.append((x, y))
                    temp_qpoints.append((QPoint(x, y)))
            img.addListOfPoints(temp_qpoints)

        return img.getImageNormalized()

    def toList(self):
        """
        omdat het makkelijker werken is in het netwerk van ons project met 1 lange list van Integers is deze methode
        er om van een tweedimensionale matrix een lange list te maken en deze dan terug te geven.

        :return: list(float)
        """
        compressedMatrix = self.compressImage()
        list = []
        for row in compressedMatrix:
            for value in row:
                list.append(value)
        return list
