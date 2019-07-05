"""
Julien Verdun
12/06/2019
This file contains properties and methods of snake class.
"""

import random
import json
import numpy as np
global mutation_rate, nb_jeu, taille_grille, width_zone, height_zone,scale,len_gen,directions


def extract_parameters(file_name):
    with open(file_name,"r") as read_file:
        data = json.load(read_file)

        len_gen = int(data['len_gen'])
        directions = data['directions']
        scale = int(data['scale'])
        nb_jeu = int(data['nb_jeu'])
        mutation_rate = int(data['mutation_rate'])
        taille_grille = int(data['taille_grille'])
        width_zone = int(data['width_zone'])
        height_zone = int(data['height_zone'])

    return len_gen,directions,scale,nb_jeu,mutation_rate,taille_grille,width_zone,height_zone

len_gen,directions,scale,nb_jeu,mutation_rate,taille_grille,width_zone,height_zone = extract_parameters('project_parameters.json')

print("Parameters of the game : ",extract_parameters('project_parameters.json'))

Lx = width_zone//taille_grille
Ly = height_zone//taille_grille


def get(parametre):
    if parametre == "nb_jeu":
        return nb_jeu
    elif parametre == "len_gen":
        return len_gen
    elif parametre == "directions":
        return directions
    elif parametre == "scale":
        return scale
    elif parametre == "mutation_rate":
        return mutation_rate
    elif parametre == "taille_grille":
        return taille_grille
    elif parametre == "width_zone":
        return width_zone
    elif parametre == "height_zone":
        return height_zone
    elif parametre == "Lx":
        return Lx
    elif parametre == "Ly":
        return Ly
    else:
        return None

def sigmoide(x,a = 1):
    """
    Comput the sigmoid of the number of array x
    with the parameter a equal to 1 by default.
    """
    return 1/(1+np.exp(-a*x))

def l_in_l(liste1,liste2):
    """
    liste1 prochaine_case
    liste2 coordonnees
    Cette fonction permet de tester si la liste1 appartient à la liste 2, en sachant que ces listes
    sont des listes de coordonnées ont les comparent donc deux à deux
    """
    for i in range(0,len(liste2),2):
        if liste1[0]==liste2[i] and liste1[1] == liste2[i+1]:
            return True
    return False

def init_snake(x,y):
    liste_coordonnees = [x,y]
    for i in range(0,6,2):
        k = np.random.randint(0,2)
        if k == 0:
            y1 = liste_coordonnees[-1]
            j = [-1, 1][np.random.randint(0, 2)]
            if l_in_l([liste_coordonnees[-2]+j,y1],liste_coordonnees) == False:
                x1 = liste_coordonnees[-2] + j
            else :
                x1 = liste_coordonnees[-2] - j

        else :
            x1 = liste_coordonnees[-2]
            j = [-1,1][np.random.randint(0,2)]
            if l_in_l([x1,liste_coordonnees[-1]+j],liste_coordonnees) == False:
                y1 = liste_coordonnees[-1] + j
            else :
                y1 = liste_coordonnees[-1] - j
        liste_coordonnees += [x1,y1]
    return liste_coordonnees



class Snake:
    def __init__(self,len_snake=4,score = 0):#x0,y0 coordonnées de la tête x1,y1 coordonnées de la queue
        self.__score = score
        self.__fitness = 1
        self.__nb_jeu = nb_jeu
        self.__nb_move = 0
        self.__len_snake = len_snake
        self.__dead_reason = " "
        Tx = np.random.randint(0,Lx)
        Ty = np.random.randint(0,Ly)
        self.__coordonnees = init_snake(Tx,Ty)
        self.__parcours = self.__coordonnees[::-1]
        self.__can_play = 1 #variable à 1 si le serpent est vivant et à 0 sinon
        self.__mouse = [np.random.randint(0,Lx),np.random.randint(0,Ly)]
        self.__liste_mouse = [self.__mouse]

        self.__input_layer = self.set_input_layer()

        self.__theta1 = scale*(np.random.random((24,18))-0.5)
        self.__hidden_layer1 = sigmoide(np.dot(self.__input_layer,self.__theta1))
        self.__theta2 = scale*(np.random.random((18,18))-0.5)
        self.__hidden_layer2 = sigmoide(np.dot(self.__hidden_layer1,self.__theta2))
        self.__theta3 = scale*(np.random.random((18,4))-0.5)
        self.__output_layer = sigmoide(np.dot(self.__hidden_layer2,self.__theta3))

    def comput_fitness(self):
        #fitness prend en compte le nombre de mouse attrapé (coeeficient important)
        #inversement proportionnelle à la distance a la nourriture
        #penalisé si contacte avec un mur
        fitness = self.__fitness
        fitness += self.__nb_move*10
        fitness += 100*self.__score**4
        fitness += (np.sqrt((self.__coordonnees[0] - self.__mouse[0]) ** 2 + (self.__coordonnees[1] - self.__mouse[1]) ** 2))
        if self.__coordonnees[0] < 2 or self.__coordonnees[0]>Lx-2 or self.__coordonnees[1] < 2 or self.__coordonnees[1]>Ly-2:
            fitness /= 100
        fitness += np.abs(nb_jeu - self.__nb_jeu)
        return fitness
    def get_nb_move(self):
        return self.__nb_move
    def get_len_snake(self):
        return self.__len_snake
    def get_fitness(self):
        return self.__fitness
    def get_dead_reason(self):
        return self.__dead_reason
    def get_mouse(self):
        return self.__mouse
    def get_liste_snake(self):
        return self.__liste_mouse
    def get_NN(self):
        return [self.__input_layer,self.__hidden_layer1,self.__hidden_layer2,self.__output_layer]
    def get_layers(self):
        return [self.__theta1,self.__theta2,self.__theta3]
    def set_layers(self,layers):
        self.__theta1 = layers[0]
        self.__theta2 = layers[1]
        self.__theta3 = layers[2]
    def mutation(self,rate=mutation_rate):
        layers = self.get_layers()
        for i in range(len(layers)):
            layers[i]+= rate*(np.random.random((np.size(layers[i],0),np.size(layers[i],1)))-0.5)
        self.remise_a_zero()
    def crossover(self,snake2):
        layers1 = self.get_layers()
        layers2 = snake2.get_layers()
        new_layers = []
        ## Ce n'est pas forcement pertinent faire la moyenne des deux
        for i in range(len(layers1)):
            layers_bis = np.zeros((np.size(layers1[i],0),np.size(layers1[i],1)))
            for j in range(np.size(layers1[i],0)):
                for k in range(np.size(layers1[i],1)):
                    p = np.random.randint(0,101)
                    layers_bis[j][k] = p/100*layers1[i][j][k] + (1-p)/100*layers2[i][j][k]
            new_layers.append(layers_bis)
        self.set_layers(new_layers)
        self.remise_a_zero()
    def selection(self):
        self.__theta1 = scale*(np.random.random((24,18))-0.5)
        self.__theta2 = scale*(np.random.random((18,18))-0.5)
        self.__theta3 = scale*(np.random.random((18,4))-0.5)
        self.remise_a_zero()
    def remise_a_zero(self):
        self.__score = 0
        self.__fitness = 1
        self.__nb_move = 0
        x = np.random.randint(0, Lx)
        y = np.random.randint(0, Ly)
        self.__coordonnees = init_snake(x,y)
        self.__nb_jeu = nb_jeu
        self.__can_play = 1
        self.__parcours = self.__coordonnees[::-1]
        self.__mouse = [np.random.randint(0,Lx),np.random.randint(0,Ly)]
        self.__liste_mouse = [self.__mouse]
    def get_direction(self):
        self.set_input_layer()
        self.__hidden_layer1 = sigmoide(np.dot(self.__input_layer,self.__theta1))
        self.__hidden_layer2 = sigmoide(np.dot(self.__hidden_layer1,self.__theta2))
        self.__output_layer = sigmoide(np.dot(self.__hidden_layer2,self.__theta3))
        maximum = np.max(self.__output_layer)
        direction = 4
        for i in range(np.size(self.__output_layer)):
            if self.__output_layer[i] == maximum:
                direction = i
        if direction == 4:
            print("Probleme avec le NN")
        return direction
    def set_input_layer(self):#left down right up #haut gauche bas gauche bas droite bas droite
        self.__input_layer = np.zeros(24)
        n = Lx

        #ditsance mouse
        if self.__coordonnees[0]>self.__mouse[0]:
            if self.__coordonnees[1]>self.__mouse[1]:
                distance_mouse = [np.sqrt((self.__coordonnees[0]-self.__mouse[0])**2),n,n,np.sqrt((self.__coordonnees[1]-self.__mouse[1])**2)]
                distance_mouse_coin = [np.sqrt((self.__coordonnees[0]-self.__mouse[0])**2+(self.__coordonnees[1]-self.__mouse[1])**2),np.sqrt(self.__coordonnees[0]**2+(self.__coordonnees[1]-height_zone)**2),np.sqrt((self.__coordonnees[0]-width_zone)**2+(self.__coordonnees[1]-height_zone)**2), np.sqrt((self.__coordonnees[0]**2-width_zone)**2+self.__coordonnees[1])]
            elif self.__coordonnees[1]<self.__mouse[1]:
                distance_mouse = [np.sqrt((self.__coordonnees[0]-self.__mouse[0])**2),np.sqrt((self.__coordonnees[1]-self.__mouse[1])**2),n,n]
                distance_mouse_coin = [np.sqrt(self.__coordonnees[0]**2+self.__coordonnees[1]**2),np.sqrt((self.__coordonnees[0]-self.__mouse[0])**2+(self.__coordonnees[1]-self.__mouse[1])**2),np.sqrt((self.__coordonnees[0]-width_zone)**2+(self.__coordonnees[1]-height_zone)**2), np.sqrt((self.__coordonnees[0]**2-width_zone)**2+self.__coordonnees[1])]
            else:
                distance_mouse = [np.sqrt((self.__coordonnees[0]-self.__mouse[0])**2),0,n,0]
                distance_mouse_coin = [0,0,0,0]
        elif self.__coordonnees[0]<self.__mouse[0]:
            if self.__coordonnees[1]>self.__mouse[1]:
                distance_mouse = [n,n,np.sqrt((self.__coordonnees[0]-self.__mouse[0])**2),np.sqrt((self.__coordonnees[1]-self.__mouse[1])**2)]
                distance_mouse_coin = [np.sqrt(self.__coordonnees[0] ** 2 + self.__coordonnees[1] ** 2),np.sqrt((self.__coordonnees[0]) ** 2 + (self.__coordonnees[1] - height_zone) ** 2),np.sqrt((self.__coordonnees[0] - width_zone) ** 2 + self.__coordonnees[1]**2),np.sqrt((self.__coordonnees[0] - self.__mouse[0]) ** 2 + (self.__coordonnees[1] - self.__mouse[1]) ** 2)]
            elif self.__coordonnees[1]<self.__mouse[1]:
                distance_mouse = [n,np.sqrt((self.__coordonnees[1]-self.__mouse[1])**2),np.sqrt((self.__coordonnees[0]-self.__mouse[0])**2),n]
                distance_mouse_coin = [np.sqrt(self.__coordonnees[0] ** 2 + self.__coordonnees[1] ** 2),np.sqrt(self.__coordonnees[0] ** 2 + (self.__coordonnees[1] - height_zone) ** 2),np.sqrt((self.__coordonnees[0] - self.__mouse[0]) ** 2 + (self.__coordonnees[1] - self.__mouse[1]) ** 2),np.sqrt((self.__coordonnees[0] - width_zone) ** 2 + self.__coordonnees[1] ** 2)]
            else:
                distance_mouse = [n,0,np.sqrt((self.__coordonnees[0]-self.__mouse[0])**2),0]
                distance_mouse_coin = [0,0,0,0]
        else :
            distance_mouse_coin = [0, 0, 0, 0]
            if self.__coordonnees[1]>self.__mouse[1]:
                distance_mouse = [0,n,0,np.sqrt((self.__coordonnees[1]-self.__mouse[1])**2)]
            elif self.__coordonnees[1]<self.__mouse[1]:
                distance_mouse = [0,np.sqrt((self.__coordonnees[1]-self.__mouse[1])**2),0,n]
            else:
                distance_mouse = [0,0,0,0]
        distance_mouse += distance_mouse_coin

        #distance murs
        distance_murs = [self.__coordonnees[0],Ly-self.__coordonnees[1],Lx-self.__coordonnees[0],self.__coordonnees[1]]
        #coin haut gauche, bas gauche, bas droit, haut droit
        distance_coin = [np.sqrt(self.__coordonnees[0]**2+self.__coordonnees[1]**2),np.sqrt(self.__coordonnees[0]**2+(height_zone-self.__coordonnees[1])**2),np.sqrt((width_zone-self.__coordonnees[0])**2+(height_zone-self.__coordonnees[1])**2),np.sqrt((width_zone-self.__coordonnees[0])**2+self.__coordonnees[1]**2)]
        distance_murs += distance_coin

        #distance queue
        distance_queue = np.zeros(8)
        for i in range(2,len(self.__coordonnees),2):
            if self.__coordonnees[0] == self.__coordonnees[i] and self.__coordonnees[1] <= self.__coordonnees[i+1]:
                distance_queue[0] = n
            if self.__coordonnees[0] == self.__coordonnees[i] and self.__coordonnees[1] >= self.__coordonnees[i+1]:
                distance_queue[2] = n
            if self.__coordonnees[0] <= self.__coordonnees[i] and self.__coordonnees[1] == self.__coordonnees[i+1]:
                distance_queue[1] = n
            if self.__coordonnees[0] >= self.__coordonnees[i] and self.__coordonnees[1] == self.__coordonnees[i+1]:
                distance_queue[3] = n
            if self.__coordonnees[0] == self.__coordonnees[i]-1 and self.__coordonnees[1] == self.__coordonnees[i+1]-1:
                distance_queue[4] = 1
            if self.__coordonnees[0] == self.__coordonnees[i] - 1 and self.__coordonnees[1] == self.__coordonnees[i + 1] + 1:
                distance_queue[5] = 1
            if self.__coordonnees[0] == self.__coordonnees[i]+1 and self.__coordonnees[1] == self.__coordonnees[i+1]+1:
                distance_queue[6] = 1
            if self.__coordonnees[0] == self.__coordonnees[i]+1 and self.__coordonnees[1] == self.__coordonnees[i+1]-1:
                distance_queue[7] = 1

        for i in range(8):
            #input layer size 24
            self.__input_layer[i] = distance_mouse[i]
            self.__input_layer[i+8] = distance_queue[i]
            self.__input_layer[i+16] = distance_murs[i]

        return self.__input_layer

    def move(self):
        dirct = self.get_direction()
        self.__nb_jeu -= 1
        if self.can_move(dirct):
            for i in range(1,len(self.__coordonnees)-2,2):
                self.__coordonnees[len(self.__coordonnees)-i-1] = self.__coordonnees[len(self.__coordonnees)-i-3]
                self.__coordonnees[len(self.__coordonnees)-i] = self.__coordonnees[len(self.__coordonnees)-i-2]
            if dirct == 0: #left
                self.__coordonnees[0],self.__coordonnees[1] = self.__coordonnees[2]-1,self.__coordonnees[3]
            elif dirct == 1:#down
                self.__coordonnees[0],self.__coordonnees[1] = self.__coordonnees[2],self.__coordonnees[3]-1
            elif dirct == 2:#right
                self.__coordonnees[0],self.__coordonnees[1] = self.__coordonnees[2]+1,self.__coordonnees[3]
            elif dirct == 3:#up
                self.__coordonnees[0],self.__coordonnees[1] = self.__coordonnees[2],self.__coordonnees[3]+1
            else:
                print("Error")
            self.__parcours.append(self.__coordonnees[1])
            self.__parcours.append(self.__coordonnees[0])

            #si le serpent a attrapé la mouse
            if self.__coordonnees[0:2] == self.__mouse:
                self.__score += 1
                self.__nb_jeu = nb_jeu
                self.__mouse = [np.random.randint(0,Lx),np.random.randint(0,Ly)]
                self.__liste_mouse.append(self.__mouse)
            self.__nb_move += 1
        else:
            self.__can_play = 0
        self.__fitness = self.comput_fitness()
    def get_liste_coordonnees(self):
        return self.__parcours
    def get_liste_mouse(self):
        return self.__liste_mouse
    def get_score(self):
        return self.__score
    def set_score(self,score):
        self.__score = score
    def get_coordonnees(self):
        return self.__coordonnees
    def grow_up(self):
        return
    def get_nb_jeu(self):
        return self.__nb_jeu
    def set_nb_jeu(self,n):
        self.__nb_jeu = n
    def get_can_play(self):
        return self.__can_play
    def set_can_play(self,i):
        if i == 0 or i == 1:
            self.__can_play = i
        else:
            print("Error : fonction set_can_play")
    def can_play(self):
        if self.__nb_jeu <= 0 or self.__coordonnees[0] < 0 or self.__coordonnees[0] > Lx-1 or self.__coordonnees[1] < 0 or self.__coordonnees[1] > Ly-1 or self.__can_play == 0:
            self.__can_play = 0
            return False
        return True
    def can_move(self,direction):
        coordonnees = self.__coordonnees
        prochaine_case = []
        if direction == 0:#left
            prochaine_case = [coordonnees[0]-1,coordonnees[1]]
        elif direction == 1:#down
            prochaine_case = [coordonnees[0],coordonnees[1]-1]
        elif direction == 2:#right
            prochaine_case = [coordonnees[0]+1,coordonnees[1]]
        elif direction == 3:#up
            prochaine_case = [coordonnees[0],coordonnees[1]+1]
        else:
            print("Error : fonction can_move")
        #test si prochaine_case dans le snake ou en dehors de la zone
        if prochaine_case[0] < 0 or prochaine_case[0] > Lx or prochaine_case[1] < 0 or prochaine_case[1] > Ly:
            self.__can_play == 0
            self.__dead_reason = "Snake out of the grid"
            return False
        if l_in_l(prochaine_case,coordonnees):
            self.__can_play == 0
            self.__dead_reason = "Snake eat its tail"
            return False
        return True



class Register:
    def __init__(self,best_snake_parameters_file_name):
        self.__file_name = best_snake_parameters_file_name
        data = self.read_parameters_best_snake()
    def get_data(self):
        data = self.read_parameters_best_snake()
        return data

    def read_parameters_best_snake(self):
        with open(self.__file_name, "r",encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data

    def write_parameters_best_snake(self,new_data):
        data = self.read_parameters_best_snake()
        for i in range(0,len(new_data),2):
            data[new_data[i]] = new_data[i+1]
        with open(self.__file_name, "w") as json_file:
            json.dump(data, json_file)