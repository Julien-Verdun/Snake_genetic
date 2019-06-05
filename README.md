# Snake_genetic

Snake trained with genetic algorithme and NN


Each snake has a NN with 24 input neurons, two hidden layers with 18 neurons and 4 output neurons (for the 4 directions).

The Snake looks in 8 directions. In each direction, it looks for : 

- distance to the food 
- distance to its tail 
- distance to the wall


Each generation contains a population of 2000 snakes.
For every generation some of the best snakes are selected to have mutations (the 30% better), some are selected for cross-over with the best snake (the following 40%) and the other (the last 30%) are undergone natural selection and are completely changed.

We stop a snake as soon as he cross the number of move we decided and we reset this number wwhen the snake take a point.
The snake cannot hit the wall.

We display the generation number, the best fitness, the best score and the neural network for the best snake.