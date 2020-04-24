Info over de de klasse Painter en Image
=======================================
De specifieke uitleg over de werking van de klassen is terug te vinden
in de subdirectory "Samenvattende uitleg - Painter en Image".  
  
Het doel van de klasse Painter is om de gebruiker in een gebied op
het scherm een cijfer te laten tekenen, uiteraard kan de gebruiker
tekenen wat hij/zij wil maar het neuraal netwerk kan enkel cijfers
herkennen. Nadat het cijfer getekend is moet de gebruiker op een
Button kunnen drukken (of dubbel klikken met de muis binnen de regio
waarin getekend wordt) waardoor het reeds getrainde neurale netwerk
met zijn berekeneningen begint en een output geeft.  
 
De klasse Painter zal enkel instaan voor het tekenen en het verwerken
van de gezette punten naar een matrix van pixels. Om dat laatste te
realiseren wordt een aparte klasse Image voorzien die de pixels bijhoudt
van dat wat de gebruiker heeft getekend.  
  
Het netwerk zelf krijgt een eigen package in het project, daar maken
we ons hier in de Painter dus geen zorgen over. Alsook de knop die
zal zorgen dat het netwerk begint met zijn berekeningen wordt niet
behandeld door de klasse Painter maar door de klasse MainGUI. 
