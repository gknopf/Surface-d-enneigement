# Surface-d-enneigement
ette technique de de délimitation  d'enneigement et de calcul des surface d'un bassin versant en présence de uages est une variante de l'élaboration de l''enneigement d'un bassin présenté  ici

https://nivo06.knobuntu.fr/index.php/technique/63-technique/340-surfaces-d-enneigement-d-un-bassin-versant

Avec les nouvelles versions  de PYTHON 3 et QGIS 3.10 il a été nécessaire de réécrire le script python pour l'adapter à la nnouvelle version.  D'autre part la vectorisation dans QGIS 3.10 provoque des erreurs de polygones qu'il a fallut corriger.
Ce qui change
Calcul de la surface Raster

La polygonisation des trames (raster) provoque des erreurs dans le cas de formes complexes .

S'il est possible de simplifier la geometrie pour lle Modele Numerique  duTerrain ( MNT )des Alpes et recuperer un polygone sans erreur, ce n'est plus le cas pour les formes complexes de repartion de la neige cartes FSC (fractional snow cover).

La vectorisation de ces trames provoque des auto-intsections, ,polygones emmelés,  moeuds doubles , que QGIS ne peut résoudre.

Les différentes tecniques de simplification de géométrie, remodelage des entités, découpe de polygones ne donnent pas de résultas probants. Et la résolution manuelle est t bien trop longue ,contraignante et fastidieuse. Et le resultat n'est pas garanti.

La solution retenue sera donc de calculer la surface des cellules élementaires du raster FSC et je vais appliquer lun script équivalent au calcul des surfaces de bassin au dessus d'une altitude donnée.

Voici un extrait du code du traitement des surfaces de neige visible

 
neigevisiblepythonLe principe:

    decouper le raster FSC au dimensions du bassin( ligne 245-252)
    demander le nb de cellules en X et Y( lignes 259 et 260)
    Calcul de la dimension des cellules ( ligne 261 265 et 266)
    Une double boucle en X etY permet de lire tous les contenus des cellules (269-277
    On compte ensuite celles qui ont un code 82 ou celles >99 qui sont les codes neige
    La surface est obtenue en multipliant le nb de cellules selectionnées par la hauteur et la la largeur des cellules Le resultat est divisé par 1000000 pour obtenir la surface en km2 ( ligne 278)

 
Réécriture du code en PYTHON 3

La version précédente était écctite en python2 . Il a fallut réécrire le code pour l'adapter à QGIS 3 et Python 3

notamment utilisation de QgsProject ,changement des algorithme processing .....
