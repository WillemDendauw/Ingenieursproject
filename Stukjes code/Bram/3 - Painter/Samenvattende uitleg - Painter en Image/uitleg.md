Samenvattende info van klassen Painter en Image
===============================================  
In de klasse Painter worden de punten van het cijfer dat getekend wordt
door de gebruiker geregistreerd in de methode mouseMoveEvent()
indien de muis ingedrukt is. Op het moment dat de muis niet meer ingedrukt
is, wil dat zeggen dat de gebruiker (tijdelijk) niet meer wil tekenen
om bijvoorbeeld de muis ergens anders te zetten. Dit is het geval bij het 
horizontale stokje die je zet bij een geschreven 7, dan is het niet de 
bedoeling dat het onderste punt van de 7 verbonden wordt met het horizontale 
stokje. Op het moment dat de gebruiker de muisknop los laat, wordt het
getekende deel toegevoegd aan een object van de klasse Image (bijgehouden
als instantievarbiabele in de klasse Painter).  
  
Op het moment men ergens het getekende cijfer wil opvragen, dan moeten alle
punten die de gebruiker tekende omgezet worden in een matrix die grijswaarden
bevat die allemaal samen het cijfer voorstellen (zie Cijfer.png). Dit wordt 
gerealiseerd dankzij een instantie van de klasse Image dat bijgehouden wordt
in de klasse Painter.  
  
Het is vanzelfsprekend dat een handgeschreven cijfer niet overal even donker is,
zeker niet aan de randen. Dit is niet het geval bij cijfers die getekend
worden op een computerscherm. Dit is een probleem omdat het neuraal netwerk
getraind is met cijfers die handgeschreven zijn, ingescand en omgezet naar
een 28x28 image. Dit effect moeten we dus simuleren. Dit wordt geregeld in
de klasse Image, beginnend bij de methode simulateRealPen().  
  
Concreet kunnen we alle punten in elke cirkel met een gekozen penbreedte<sup>[1]</sup> als
straal en met middelpunt elk geregistreerd punt<sup>[2]</sup>, als pixel van de image zullen
beschouwen. Om nu een echte pen te simuleren moeten we op een of andere manier
aan elke pixel in die cirkel een grijswaarde toekennen. De grijswaarde wordt
bepaald in de methode pixelValue() die twee punten meekrijgt (twee x-waarden
en twee y-waarden). Het tweede punt dat meegegeven wordt als parameter is het 
middelpunt van een cirkel, het eerste is een punt binnen de hierboven beschreven 
cirkel<sup>[3]</sup>. De methode pixelValue() zal dan uiteindelijk de doorslag geven. Dit
gebeurt als volgt: we verdelen een lijnstuk tussen het middelpunt en het 
te controleren punt in pen_width delen. Het middelpunt krijgt een random waarde
tussen 220 en 255, het eerste deeltje (dichtst bij middelpunt) van het lijnstuk 
krijgt een random waarde tussen 220 en 220-220/pen_width, het tweede deeltje 
tussen 220-220/pen_width en 220-2*(220/pen_width), enz.
  
<sup>[1]</sup> de penbreedte is een gekozen variabele die bijgehouden wordt als instantievariabele
in de klasse Image, deze zegt hoeveel pixels ver van een geregistreerd punt we 
als pixel mogen beschouwen.  
<sup>[2]</sup> een geregistreerd punt is een punt dat ofwel door de klasse Painter in de
methode mouseMoveEvent() werd geregistreerd ofwel werd toegevoegd in de hulpmethode
pointsToTreatAsPixels() van de klasse Image. In die laatste wordt met behulp van 
de hulpmethode listOfPointsOnLine() alle punten tussen twee punten geregistreerd
door mouseMoveEvent() ook als punten toegevoegd. Dit wordt gedaan omdat we anders
te weinig punten hebben, de muis van de gebruiker gaat doorgaans te snel
om alle punten te registreren in mouseMoveEvent().  
<sup>[3]</sup> het zijn eigenlijk niet alleen de punten in de beschreven cirkel die de 
methode pixelValue() als eerste punt meekrijgt. In de methode simulateRealPen()
die gebruik maakt van de methode pixelValue(), worden alle punten in het vierkant
met zijde pen_width*2 en met het middelpunt van de gewenste cirkel als snijpunt
van de diagonalen overlopen en daarvan wordt de grijswaarde bepaald in pixelValue().
De beschreven cirkel is dus ingesloten door het vierkant. In de methode pixelValue()
wordt dit opgevangen door 0 te returnen indien het te controleren punt verder dan
pen_width verwijderd is van het middelpunt van de cirkel.
