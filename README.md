# Snake_genetic

Snake trained with genetic algorithme and NN


Each snake has a NN with 24 input neurons (comput according to the environment), two hidden layers with 18 neurons and 4 output neurons (for the 4 directions).

The Snake looks in 8 directions. In each direction, it looks for : 

- distance to the food (mice)
- distance to its tail 
- distance to the wall


Each generation contains a population of 2000 snakes.
For every generation some of the best snakes are selected to have mutations (the 30% better), some are selected for cross-over with the best snake (the following 40%) and the other (the last 30%) are undergone natural selection and are completely changed.

We stop a snake as soon as he cross the number of move we decided and we reset this number wwhen the snake take a point.
The snake cannot hit the wall.

We display the generation number, the best fitness, the best score and the neural network for the best snake.



-----------------------


On entraîne le réseau de neurone d'un serpent avec un algorithme génétique de la manière suivante.

Chaque serpent possède un réseau de neurones dont la couche d'entrée possède 24 neurones (analyse de l'environnement), les deux couches cachées en possèdent 18 et la couche de sortie en possède 4.
Avant de se déplacer le serpent regarde dans 8 directions (4 côtés et 4 coins). Il regarde : 

- la distance à la nourriture (souris)
- la distance à sa queue 
- la distance au mur

Chaque génération contient 2000 serpents.
A chaque génération, une partie des serpents mutent (les 30% ayant la meilleure fitness), une partie des serpents subissent des croissements (les 40% suivants) et les autres (30 dernier %) sont renouvellés (sélection naturelle).

On arrête un serpent dès qu'il déplace le nombre de mouvements autorisés et on réinitialise ce nombre quand le serpent mange une souris. Le serpent n'a pas le droit de rentrer dans un mur.

On affiche la génération, la meilleure fitness, le meilleur score et le réseau neuronal du meilleur serpent.

Chaque génération contient une population de 2000 serpents.
A chaque génération ...

