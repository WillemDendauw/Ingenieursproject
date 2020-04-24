Handige websites
================
**Neural Networks and Deep learning**  
Gratis online boek, geschreven door Michael Nielsen (http://michaelnielsen.org/)  
Website: http://neuralnetworksanddeeplearning.com/index.html  
Github: https://github.com/mnielsen/neural-networks-and-deep-learning  
  
Een pdf-versie van de website is terug te vinden op: https://github.com/antonvladyka/neuralnetworksanddeeplearning.com.pdf  
  
**Youtube afspeellijst: Neural Networks and Deep learning**
Afspeellijst van 3Blue1Brown over neurale netwerken en deep learning, gebaseerd
op het boek van Michael Nielsen.  
https://www.youtube.com/watch?v=aircAruvnKk&list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi  
  
**Verschil tussen _Gradient Descent_ en _Backpropagation_**  
Op beide websites vind je een goeie uitleg over wat gradient descent en backpropagation zijn,
begin met de tweede link (die is het meest duidelijk, het gebruikt stochastic gradient descent
wat wil zeggen dat de som niet over de hele training data ineens wordt berekend, wat te veel tijd
zou kosten, maar steeds over een steekproef)  
https://qr.ae/TW7mUM  
https://machinelearningmastery.com/difference-between-a-batch-and-an-epoch/  
  
**Verschil tussen _batch_ en _epoch_**  
Merk op: dit zijn twee hyperparamters, i.e. paramters horende bij een neuraal netwerk en zijn training.  
Conclusie:  
>  You can think of a for-loop over the number of epochs where each loop proceeds over the training dataset.
Within this for-loop is another nested for-loop that iterates over each batch of samples, where one batch has
the specified “batch size” number of samples.  
  
```C++
for (int i = 0; i < epoch; i++) {
	for (Mini-Batch mb : trainingSet) {
		CF = calculateCostFunction(mb);
		changeParametersInNN(CF); // parameters are weights and biases
	}
}
```
  
https://machinelearningmastery.com/difference-between-a-batch-and-an-epoch/  

**Globale informatie over neurale netwerken**  
https://brilliant.org/wiki/artificial-neural-network/  
  
**Visualisatie van neurale netwerken**  
Zie het antwoord op een vraag op StackOverflow:  
https://stackoverflow.com/a/37366154/9356123
