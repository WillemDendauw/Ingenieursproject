Notes to self
=============
**Ideeën voor implementatie van het project**  
*  Het hoofddoel is om de gebruiker een nummer te laten schrijven op een GUI en het neuraal netwerk
achterhaalt welk
    * Remember: klassen mogen niet te ingewikkeld zijn
    *  klassen: Netwerk, GUI, image_compressor
*  Daarnaast moet iets educatief toegevoegd worden, start met de samenvattende conclusie die hieronder vermeld is,
daaruit kan heel simplistisch een neuraal netwerk getoond worden bestaande uit 3 layers (input - hidden - output)
waarin elk 1-5 neuronen getoond worden, en een soort debug-strategie wordt getoond (berekeningen worden stap voor
stap getoond voor 1 neuron want voor alle andere gebeurt letterlijk hetzelfde)
    *  misschien zelfs gewoon eerst beginnen met 3 layers van elk 1 neuron
*  In de klasse Painter wordt een geschreven cijfer gesimuleerd door getImage(). We kunnen deze simulatie met 
het uitgrijzen van de randen misschien eens weglaten en kijken hoe goed het netwerk hierop reageert
  
**Opmerkingen tijdens coderen**
*  Ik heb op 16/04/19 vlug self.image als instantievariabele uit Painter weggelaten -> enkel maken tijdens getImage() 
-> performatie. Werkt nog niet helemaal
*  De klasse Compressor_IMG zou beter afgeleid worden van de klasse Image -> CompressedImage, dan moet deze klasse
enkel instaan voor het omzetten van een XxX image naar een 28x28 image
  
**Samenvattende conclusie over backpropagation en gradient descent:**  
*  _gradient descent_ is een algemene methode om van een gegeven functie (meestal een complexe 
functie met zeer veer variabelen) een lokaal minimum te vinden. Als we _gradient descent_ gebruiken
in een neuraal netwerk, dan is de functie waarvoor we dit toepassen de "_cost function_" (wordt ook 
wel "_loss function_" genoemd). We spreken van een lokaal minimum omdat we at random een punt
van de functie kiezen en van daaruit naar het laagste punt gaan alsof we een bal van dat gekozen punt
naar een minimum laten vallen (dit is uitgedrukt in 2 dimensies zodat je het gemakkelijk kan visualiseren 
maar het principe geldt ook voor functies met een miljoen variabelen, wat in neurale netwerken niet ongewoon is).  
*  _backpropagation_ is de methode die gebruikt wordt om _gradient descent_ toe te passen op alle 
weights en biases van het neurale netwerk.  

Link: https://qr.ae/TW7mUM  
Lees ook dit nog eens: goede, beknopte uitleg over SGD, batches en epochs: 
https://machinelearningmastery.com/difference-between-a-batch-and-an-epoch/
  
**Stappen in het trainen van een neuraal netwerk**  
Stel een neuraal netwerk voor met input-vector _x_, uitput-vector _a(x)_ en verwachtingsvector _y(x)_  
1.  bij aanmaak van een neuraal netwerk stellen we alle weights en biases at random in
2.  het algoritme _backpropagation_ wordt gebruikt om alle weights en biases van het neurale
netwerk een klein beetje aan te passen in de richting zodat de uitkomst _a(x)_ dichter bij _y(x)_
komt te liggen. Om dit te realiseren wordt _gradient descent_ gebruikt op alle weights en biases van het netwerk.  
  
**Mogelijke problemen die kunnen optreden**  
1. Het zou kunnen zijn dat bij rescalen van het mainwindow dat het tekenen dan mislukt -> *dit is opgelost*  
  