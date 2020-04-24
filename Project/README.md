Project Team 6: een neuraal netwerk handgeschreven cijfers laten herkennen
======================================================================  
Dit project is gebaseerd op een boek geschreven door Michael Nielsen, genaamd `Neural Networks and Deep Learning`. In dit boek wordt gebruik gemaakt van de MNIST dataset waarin 60,000 foto's zitten van 28x28 pixels van geschreven cijfers. In het boek gaat Nielsen dieper in op wat neurale netwerken zijn, hoe ze te trainen en te gebruiken. Al in het eerste hoofdstuk wordt een eerste neuraal netwerk gemaakt en getraind met de data van de MNIST dataset. Nadat het getraind is herkent het netwerk handgeschreven cijfers. Dit heeft ons geïnspireerd om ook zo'n neuraal netwerk te maken en te trainen. De gebruiker kan zelf een cijfer tekenen op het scherm met de muis, vervolgens kan hij het netwerk laten 'raden' welk cijfer op het scherm getekend is.

Om het eindresultaat van dit project te bekijken kan u de executable `Main.exe` opstarten. Om dit te kunnen doen moet u er zeker van zijn dat er in de folder waar deze executable zich bevindt ook een mapje `Data` is. In dat mapje `Data` moet verplicht 4 submapjes zitten: `NetwerkParameters`, `TestData`, `TrainingData` en `TrainingGUIData`. Indien u zelf ook training- en/of test-data wil genereren moet ook de subfolder `Backup` aanwezig zijn (voor meer uitleg hierover, zie de laatste paragraaf van deze README). Het project kan ook geopend worden door met een Python-interpreter (versie 3) de Main.py module te openen:
`Project> python Main.py`

In het mapje `NetwerkParameters` moeten twee bestanden `biases.npy` en `weights.npy` zitten wat de parameters zijn van een getraind netwerk. Meestal zullen die parameters getraind zijn op basis van de data die in `TrainingData` zit. Tijdens het trainen wordt gebruik gemaakt van tesdata die in `TestData` moet zitten. In het mapje `TrainingGUIData` zit trainingdata en validatiedata afkomstig van de MNIST dataset (maar een klein deeltje ervan, resp. 1000 en 100 cijfers). Die laatste data hebben we nodig om in de educatieve GUI TrainingGUI lokaal een netwerk te kunnen laten trainen met enkele parameters ingesteld door de gebruiker.

De code van dit project is hoofdzakelijk opgesplitst in twee submappen `Algoritme`
en `GUI`. In `Algoritme` zit de code om een neuraal netwerk aan te maken (met al
of niet getrainde weights en biases) en te trainen. In `GUI` zit dan weer alle
code waarmee de gebruiker interageert. De hoofdpagina bestaat uit een Painter-object
(Painter is een zelfgeschreven klasse) waarin de gebruiker het cijfer kan tekenen.
Drukt de gebruiker vervolgens op de "Bereken Output"-drukknop, dan wordt het
getekende cijfer bepaald door het netwerk. De output komt tevoorschijn in de
bollen die in het midden van het scherm staan. Een rode bol wil zeggen dat het netwerk
van dat cijfer denkt dat dat helemaal niet het getekende cijfer is, een groene bol
wil zeggen dat het netwerk zeker is dat dat cijfer het getekende cijfer is.

Naast de hierboven beschreven mappen `Algoritme` en `GUI` die de core-business zijn
van dit project, zijn er ook nog twee modules in de submap `CollectTrainingData`
in het Project-mapje van deze Github repository. Deze twee modules zijn eigenlijk
twee stand-alone-programma's en zijn niet tot onmiddellijk onderdeel van het
afgewerkte product van dit project. Maar ze zijn onontbeerlijk geweest in de weg
naar dat afgewerkte product. De module `MakeTrainingData.py` is een hulpapplicatie
waarin de gebruiker/ontwikkelaar zelf data kan maken die het netwerk gebruikt om
zijn weights en biases te trainen. De gebruiker kiest ofwel om trainingdata ofwel
om testdata te genereren. Die keuze is nodig omdat testdata in een ander formaat moet opgeslagen worden: trainingdata is steeds een lijst van tuples (x, y) met als x een 784-dimensionale `numpy.ndarray` en y een 10-dimensionale `numpy.narray`. De eerste ingang van elke tuple, x, bevat alle pixel-waarden tussen 0 en 1 van een 28x28 foto (= 784 pixels). De tweede ingang van elke tuple is de verwachte output van het neurale netwerk horende bij die
welbepaalde ingang, dit moet dus een vector zijn van 10 ingangen omdat er 10 cijfers
zijn. Bij de testdata, die gebruikt wordt om het netwerk tijdens het trainen te testen
op hoe goed/slecht het al presteert, wordt elk cijfer (x-waarde van de tuples)
op dezelfde manier bijgehouden als bij de trainingdata. De y-waarde van elke tuple
is bij de testdata wel verschillend. Dit hoeft geen vector te zijn omdat het enkel
maar moet aangeven welke waarde bij het cijfer hoort, en niet de volledige verwachte
output van het netwerk. Elke keer dat de gebruiker training- en/of testdata wil
maken wordt een nieuw bestand aangemaakt met de gepicklede lijst van tuples.
De gebruiker geeft in het tekstveld aan waar die de data wil opslaan. De string
die in het tekstveld komt moet het pad zijn relatief t.o.v. de `Data`-submap van de
Project-folder. Indien de gebruiker trainingdata wil maken moet de gebruiker
`TrainingData/file_name.bin` in het tekstveld schrijven en de checkbox uitgevinkt
laten. Wil de gebruiker echter testdata maken, dan moet hij `TestData/file_name.bin`
invullen in het tekstveld en de checkbox aanvinken.  
Bovendien is er een veiligheidsmechanisme voorzien voor moest het programma om de
een of andere reden crashen terwijl je data aan het produceren bent, het zou niet
aangenaam zijn om 500 cijfers getekend te hebben en die door een lege batterij
allemaal te verliezen. Daarom wordt telkens wanneer twee nieuwe cijfers getekend
zijn een backup-file aangemaakt in de `Backup`-folder die aanwezig moet zijn in
de `Data`-folder van het `Project`-folder.  
Wanneer de trainingdata gemaakt is moeten de parameters van een neuraal netwerk
getraind worden op deze data. Dit doet u door de module `TrainNetwerk.py` te laten
lopen. Die module verwacht dat er minstens 1 bestand in `Data/TrainingData/` en
`Data/TestData/` zit, zo niet kan het netwerk niet getraind worden. De module overloopt
eerst alle bestanden in de beide submappen en verzamelt alle data in alle bestanden
die in de mappen zitten. Hierdoor kan u gemakkelijk in verschillende sessies de
training- en/of testdata aanmaken en hoeft het niet allemaal opgeslagen te worden in
1 groot bestand. Beide modules moeten vanuit de commandline of terminal uitgevoerd
worden met een Python versie 3-interpreter:

- `Project/CollectTrainingData> python MakeTrainingData.py`
- `Project/CollectTrainingData> python TrainNetwerk.py`

De laatste twee beschreven modules hebben we niet voorzien als executable files
omdat die eigenlijk geen deel uitmaken van het eindproduct van het project.
We hebben die wel in de repository gelaten omdat het voor programmeurs of
gebruikers leuk kan zijn om het netwerk verder te trainen, of om het zelfs
helemaal opnieuw te trainen. Met eigen training- en/of testdata.

Het blijkt dus uit bovenstaande tekst dat het mapje `Data` onontbeerlijk is om
dit project te gebruiken. Om de programmeur die dit project wil gebruiken toch
de vrijheid te verlenen om de data ergens anders op te slaan vermelden we hieronder
de lijnen in de bijhorende modules die moeten aangepast worden als u ervoor kiest
om de data ergens anders op te slaan. De modules zijn opgesomd relatief t.o.v. de
`Project`-folder

- `Algoritme/Network.py:` lijnen 46, 47
- `GUI/MainGUI.py`: lijnen 21, 22
- `GUI/TrainingGUI.py`: lijnen 371, 373
- `CollectTrainingData/TrainNetwerk`: lijnen 27, 28
- `CollectTrainingData/MakeTrainingData`: lijnen 142, 148
