# -*- coding: utf-8 -*-
"""
Created on Mon May 27 07:36:23 2019
@author: Julien Verdun
"""


"""
Each snake has a NN with 24 input neurons, 2 x 18 hiddens neurons, 4 output neurons (direction)
The Snake looks in 8 directions. In each directions it looks for : - distance to the food - 
distance to its tail - distance to the wall

Each generation contains a population of 2000 snakes.
For every generation some of the best snakes are selected to reproduce.

Affichage de la génération, de la meilleure fitness, du taux de mutation, du score, du meilleur score, du réseau de neurones
We stop a snake as soon as he cross the number of move to the left we decided and we reset this number wwhen
the snake take a point.
The snake cannot hit the wall.



Regarder dans les 4 coins et passer a une couche d'entree à 24 sinapses

Tester de remettre la sigmoide

Regarder les canvas.create_text(20, 30, anchor=W, font="Purisa",
    text="Most relationships seem so transitory")


"""


from tkinter import *
from tkinter.messagebox import *
import random
import numpy as np
from time import sleep


global taille_grille, width_zone, height_zone, len_gen, nb_jeu,directions
taille_grille = 20
width_zone = 810
height_zone = 610
len_gen = 50
nb_jeu = 200
directions = ["left","down","right","up"]
# --------------------------------------------------------

def sigmoide(x):
    return 1/(1+np.exp(-x))

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

def trier(old_generation,liste_indices):
    new_generation = [0 for k in range(len(old_generation))]
    #print("Old_generation : ",old_generation)
    #print("Liste indices : ",liste_indices)
    for i in range(len(old_generation)):
        new_generation[liste_indices[i]] = old_generation[i]
    return new_generation


def liste_to_txt(liste):
    txt = ""
    for elt in liste:
        txt += str(int(elt*100)/100) + " | "
    return txt[:-2]



class ZoneAffichage(Canvas):
    def __init__(self, parent, w=width_zone, h=height_zone, _bg='white'):  # 500x400 : dessin final !
        self.__w = w
        self.__h = h
        # Terrain de 40 cas de hauteur et 30 de cote
        self.__fen_parent=parent
        Canvas.__init__(self, parent, width=w, height=h, bg=_bg, relief=RAISED, bd=5)
        self.create_rectangle(10,10,w,h,outline="black",width=2)
        for i in range(h//taille_grille):
            self.create_line(10,taille_grille*i+10,w,taille_grille*i+10,fill="black",width = 2)
        for j in range(w//taille_grille):
            self.create_line(taille_grille*j+10,10,taille_grille*j+10,h,fill="black",width = 2)
        
class FenPrincipale(Tk):
    def __init__(self):
        Tk.__init__(self)
        
        self.__generation = 1
        self.__text_generation = Label(self)
        self.__text_generation.pack(side = TOP)
        self.__text_generation.config(text = "Generation : {}".format(self.__generation))
        
        self.__score = 0
        self.__text_score = Label(self)
        self.__text_score.pack(side = TOP)
        self.__text_score.config(text = "Current score : {}".format(self.__score))
        
        self.__fitness = 0
        self.__text_fitness = Label(self)
        self.__text_fitness.pack(side = TOP)
        self.__text_fitness.config(text = "Best fitness : {}".format(self.__fitness))
        
        self.__NN = Label(self,width=100,height = 5)
        self.__NN.pack(side = TOP)
        self.__NN.config(text = "Neural Network")
        
        self.title('SNAKE - GENETIQUE')
        self.__zoneAffichage = ZoneAffichage(self)
        self.__zoneAffichage.pack(padx = 5,pady=5)
        
        self.__best_snake = []
        self.__generation_snake = [self.generer_snake() for i in range(len_gen)]
        # Création d'un widget Button (bouton Effacer)
        #self.__boutonNextGeneration = Button(self, text = 'Next Generation',command = self.next_generation).pack(side = LEFT,padx=5,pady = 5)
        self.__boutonEffacer = Button(self, text='Effacer', command=self.effacer).pack(side=LEFT, padx=5, pady=5)
        # Création d'un widget Button (bouton Quitter)
        self.__boutonQuitter = Button(self, text='Quitter', command=self.destroy).pack(side=LEFT, padx=5, pady=5)
        self.__souris_display = []
        self.__snake_display = []
        
        self.focus_set()
        self.bind("<Key>",self.next_generation)
        
    def effacer(self):
        self.__zoneAffichage.delete(ALL)
    def affiche_best_snake_souris1(self,best_snake):
        liste_coordonnees = best_snake.get_liste_coordonnees()
        #liste_coordonnees = [15, 19, 15, 18,15, 20, 15, 21,16,21,17,21,18,21,19,21,19,22,20,22]
        print("Coordonnees of the best snake : {}".format(liste_coordonnees))
        liste_souris = best_snake.get_liste_souris()
        #liste_souris = [[30,30],[20,15]]
        i_souris = 1
        if self.__souris_display != 0:
            self.__zoneAffichage.delete(self.__souris_display)
        if self.__snake_display != 0:
            for elt in self.__snake_display:
                self.__zoneAffichage.delete(elt)
        sleep(2)
        self.__souris_display = self.__zoneAffichage.create_oval(liste_souris[0][0]*taille_grille-taille_grille//2,liste_souris[0][1]*taille_grille-taille_grille//2,liste_souris[0][0]*taille_grille+taille_grille//2,liste_souris[0][1]*taille_grille+taille_grille//2,fill="red",outline="yellow")
        self.__snake_display = [self.__zoneAffichage.create_rectangle(10 + taille_grille*liste_coordonnees[0],10 + taille_grille*liste_coordonnees[1],10 + taille_grille*(liste_coordonnees[0]+1),10 + taille_grille*(liste_coordonnees[1]+1),fill = "black",outline="green"),self.__zoneAffichage.create_rectangle(10 + taille_grille*liste_coordonnees[2],10 + taille_grille*liste_coordonnees[3],10 + taille_grille*(liste_coordonnees[2]+1),10 + taille_grille*(liste_coordonnees[3]+1),fill = "black",outline="green"),self.__zoneAffichage.create_rectangle(10 + taille_grille*liste_coordonnees[4],10 + taille_grille*liste_coordonnees[5],10 + taille_grille*(liste_coordonnees[4]+1),10 + taille_grille*(liste_coordonnees[5]+1),fill = "black",outline="green"),self.__zoneAffichage.create_rectangle(10 + taille_grille*liste_coordonnees[6],10 + taille_grille*liste_coordonnees[7],10 + taille_grille*(liste_coordonnees[6]+1),10 + taille_grille*(liste_coordonnees[7]+1),fill = "black",outline="green")]
        sleep(2)
        if len(liste_coordonnees) > 8:
            for i in range(8,len(liste_coordonnees),2):
                self.__zoneAffichage.delete(self.__snake_display[0])
                self.__snake_display.append(self.__zoneAffichage.create_rectangle(10 + taille_grille*liste_coordonnees[i],10 + taille_grille*liste_coordonnees[i+1],10 + taille_grille*(liste_coordonnees[i]+1),10 + taille_grille*(liste_coordonnees[i+1]+1),fill = "black",outline="green"))
                if liste_coordonnees[i:i+2] == liste_souris[i_souris]:
                    self.__zoneAffichage.delete(self.__souris_display)
                    self.__souris_display = self.__zoneAffichage.create_oval(liste_souris[i_souris][0]*taille_grille-taille_grille//2,liste_souris[i_souris][1]*taille_grille-taille_grille//2,liste_souris[i_souris][0]+taille_grille//2,liste_souris[i_souris][1]*taille_grille+taille_grille//2,fill="red",outline="yellow")
                    i_souris += 1
                sleep(1)
        else:
            print("Snake didn't move !!")
        print("Best snake displayed, you can go to the next generation")
        
    def affiche_best_snake_souris(self,best_snake):
        liste_coordonnees = best_snake.get_liste_coordonnees()
        print("Coordonnees of the best snake : {}".format(liste_coordonnees))
        liste_souris = best_snake.get_liste_souris()
        if self.__souris_display != []:
            for elt in self.__souris_display:
                self.__zoneAffichage.delete(elt)
            self.__souris_display = []
        if self.__snake_display != []:
            for elt in self.__snake_display:
                self.__zoneAffichage.delete(elt)
            self.__snake_display = []
        for i in range(0,len(liste_coordonnees)-2,2) : 
            self.__snake_display.append(self.__zoneAffichage.create_rectangle(10 + taille_grille*liste_coordonnees[i],10 + taille_grille*liste_coordonnees[i+1],10 + taille_grille*(liste_coordonnees[i]+1),10 + taille_grille*(liste_coordonnees[i+1]+1),fill = "black",outline="green"))
        self.__snake_display.append(self.__zoneAffichage.create_rectangle(10 + taille_grille*liste_coordonnees[-2],10 + taille_grille*liste_coordonnees[-1],10 + taille_grille*(liste_coordonnees[-2]+1),10 + taille_grille*(liste_coordonnees[-1]+1),fill = "green",outline="green"))
        for i in range(len(liste_souris)):
            self.__souris_display.append(self.__zoneAffichage.create_oval(10 + liste_souris[i][0]*taille_grille,10 + liste_souris[i][1]*taille_grille,10 + (liste_souris[i][0]+1)*taille_grille,10 + (liste_souris[i][1]+1)*taille_grille,fill="red",outline="yellow"))
        print("Best snake displayed, you can go to the next generation")
        
    def generer_snake(self):
        return Snake(4,0)
    def new_generation(self,old_generation):
        liste_fitness = []
        for snake in old_generation :
            liste_fitness.append(snake.get_fitness())
        liste_indices = np.argsort(liste_fitness)
        new_generation = trier(old_generation,liste_indices)
        for i in range(int(0.3*len(new_generation))+1,int(0.7*len(new_generation))):
            new_generation[i].crossover(new_generation[0])
        for i in range(int(0.7*len(new_generation)),len(new_generation)):
            new_generation[i].selection()
        for i in range(0,int(0.3*len(new_generation))+1):
            new_generation[i].mutation()
        return new_generation
    def next_generation(self,event):
        touche = event.keysym
        
        #deplacement de tout les serpents
        #j = 0
        for snake in self.__generation_snake :
            #j += 1
            #print("Snake : ",j)
            while snake.can_play():
                snake.move()
                #print("Coordonnees Snake : ",snake.get_coordonnees())
            
        #recherche du meilleur element
        best_fitness = 0
        best_snake = 0
        for snake in self.__generation_snake:
            #print("Fitness :",snake.get_fitness())
            if snake.get_fitness() >= best_fitness:
                best_snake = snake
                best_fitness = snake.get_fitness()
        print("Best snake : ",best_snake.get_coordonnees())
        print("Best fitness : ",best_fitness)
        print("Best score :",best_snake.get_score())
        if best_snake == 0:
            print("Error fonction next generation")
            best_snake = new_gene[0] # pas ouf
        
        #affichage du seprent et mise à jour des textes
        self.affiche_best_snake_souris(best_snake)
        self.__generation += 1
        self.__text_generation.config(text = "Generation : {}".format(self.__generation))
        self.__score = best_snake.get_score()
        self.__text_score.config(text="Current score : {}".format(self.__score))
        self.__fitness = best_snake.get_fitness()
        self.__text_fitness.config(text = "Best fitness : {}".format(self.__fitness))
        [input_layer,hidden_layer1,hidden_layer2,output_layer] = best_snake.get_NN()
        self.__NN.config(text = "Input layer : " + liste_to_txt(input_layer) + "\n" + "Hidden layer1 : " + liste_to_txt(hidden_layer1) + "\n" + "Hidden layer2 : " + liste_to_txt(hidden_layer2) + "\n" + "Output_layer : " + liste_to_txt(output_layer))
        
        #calcul de la prochaine generation
        self.__generation_snake = self.new_generation(self.__generation_snake)
        print("New population generated")
        
        
class Snake:
    def __init__(self,len_snake=4,score = 0):#x0,y0 coordonnées de la tête x1,y1 coordonnées de la queue
        self.__score = score
        self.__fitness = 1
        self.__nb_jeu = nb_jeu
        self.__len_snake = len_snake
        self.__coordonnees = [width_zone//(2*taille_grille)-2,height_zone//(2*taille_grille),width_zone//(2*taille_grille)-1,height_zone//(2*taille_grille),width_zone//(2*taille_grille),height_zone//(2*taille_grille),width_zone//(2*taille_grille)+1,height_zone//(2*taille_grille)]#[20,10,19,10,18,10,17,10]
        self.__parcours = self.__coordonnees[::-1]
        self.__can_play = 1 #variable à 1 si le serpent est vivant et à 0 sinon
        self.__souris = [np.random.randint(0,(width_zone-10)//taille_grille-1),np.random.randint(0,(height_zone-10)//taille_grille-1)]
        self.__liste_souris = [self.__souris]
        
        self.__input_layer = self.set_input_layer()#np.array([0,0,0,0,0,100,0,0,0,0,0,0]) #souris queue mur
        
        self.__theta1 = 10*(np.random.random((12,18))-0.5)
        self.__hidden_layer1 = np.dot(self.__input_layer,self.__theta1)#sigmoide(np.dot(self.__input_layer,self.__theta1))
        self.__theta2 = 10*(np.random.random((18,18))-0.5)
        self.__hidden_layer2 = np.dot(self.__hidden_layer1,self.__theta2)#sigmoide(np.dot(self.__hidden_layer1,self.__theta2))
        self.__theta3 = 10*(np.random.random((18,4))-0.5)
        self.__output_layer = np.dot(self.__hidden_layer2,self.__theta3)#sigmoide(np.dot(self.__hidden_layer2,self.__theta3))
        
    def comput_fitness(self):
        #fitness prend en compte le nombre de souris attrapé (coeeficient important)
        #inversement proportionnelle à la distance a la nourriture
        #penalisé si contacte avec un mur
        fitness = self.__fitness
        fitness += 100*self.__score**4
        fitness /= (np.sqrt((self.__coordonnees[0]-self.__souris[0])**2 + (self.__coordonnees[1]-self.__souris[1])**2))
        if self.__coordonnees[0] < 2 or self.__coordonnees[0]>width_zone//taille_grille-2 or self.__coordonnees[1] < 2 or self.__coordonnees[1]>height_zone//taille_grille-2:
            fitness = 0
        fitness += np.abs(nb_jeu - self.__nb_jeu)
        return fitness
    def get_fitness(self):
        return self.__fitness
    def get_NN(self):
        return [self.__input_layer,self.__hidden_layer1,self.__hidden_layer2,self.__output_layer]
    def get_layers(self):
        return [self.__theta1,self.__theta2,self.__theta3]
    def set_layers(self,layers):
        self.__theta1 = layers[0]
        self.__theta2 = layers[1]
        self.__theta3 = layers[2]
    def mutation(self,rate=0.1):
        layers = self.get_layers()
        for i in range(len(layers)):
            layers[i]+= rate*(np.random.random((np.size(layers[i],0),np.size(layers[i],1)))-0.5)
        self.remise_a_zero()
    def crossover(self,snake2):
        layers1 = self.get_layers()
        layers2 = snake2.get_layers()
        new_layers = []
        for i in range(len(layers1)):
            new_layers.append((layers1[i]+layers2[i])/2)
        self.set_layers(new_layers)
        self.remise_a_zero()
    def selection(self):
        self.__theta1 = 10*(np.random.random((12,18))-0.5)
        self.__theta2 = 10*(np.random.random((18,18))-0.5)
        self.__theta3 = 10*(np.random.random((18,4))-0.5)
        self.remise_a_zero()
    def remise_a_zero(self):
        self.__score = 0
        self.__fitness = 1
        self.__coordonnees = [width_zone//(2*taille_grille)-2,height_zone//(2*taille_grille),width_zone//(2*taille_grille)-1,height_zone//(2*taille_grille),width_zone//(2*taille_grille),height_zone//(2*taille_grille),width_zone//(2*taille_grille)+1,height_zone//(2*taille_grille)]#[20,10,19,10,18,10,17,10]
        self.__nb_jeu = nb_jeu
        self.__can_play = 1
        self.__parcours = self.__coordonnees[::-1]
        self.__souris = [np.random.randint(0,(width_zone-10)//taille_grille-1),np.random.randint(0,(height_zone-10)//taille_grille-1)]
        self.__liste_souris = [self.__souris]
    def get_direction(self):
        self.set_input_layer()
        self.__hidden_layer1 = np.dot(self.__input_layer,self.__theta1)#sigmoide(np.dot(self.__input_layer,self.__theta1))
        self.__hidden_layer2 = np.dot(self.__hidden_layer1,self.__theta2)#sigmoide(np.dot(self.__hidden_layer1,self.__theta2))
        self.__output_layer = np.dot(self.__hidden_layer2,self.__theta3)#sigmoide(np.dot(self.__hidden_layer2,self.__theta3))
        maximum = np.max(self.__output_layer)
        direction = 4
        #print("output_layer : ",self.__output_layer)
        for i in range(np.size(self.__output_layer)):
            if self.__output_layer[i] == maximum:
                direction = i
                #print("Direction : ",directions[i])
        if direction == 4:
            print("Probleme avec le NN")
        return direction
    def set_input_layer(self):#left down right up
        self.__input_layer = np.zeros(12)
        distance_souris = np.zeros(4)
        n = 50
        #ditsance souris
        if self.__coordonnees[0]>self.__souris[0]:
            if self.__coordonnees[1]>self.__souris[1]:
                distance_souris = [np.sqrt((self.__coordonnees[0]-self.__souris[0])**2),n,n,np.sqrt((self.__coordonnees[1]-self.__souris[1])**2)]
            elif self.__coordonnees[1]<self.__souris[1]:
                distance_souris = [np.sqrt((self.__coordonnees[0]-self.__souris[0])**2),np.sqrt((self.__coordonnees[1]-self.__souris[1])**2),n,n]
            else:
                distance_souris = [np.sqrt((self.__coordonnees[0]-self.__souris[0])**2),0,n,0]
        elif self.__coordonnees[0]<self.__souris[0]:
            if self.__coordonnees[1]>self.__souris[1]:
                distance_souris = [n,n,np.sqrt((self.__coordonnees[0]-self.__souris[0])**2),np.sqrt((self.__coordonnees[1]-self.__souris[1])**2)]
            elif self.__coordonnees[1]<self.__souris[1]:
                distance_souris = [n,np.sqrt((self.__coordonnees[1]-self.__souris[1])**2),np.sqrt((self.__coordonnees[0]-self.__souris[0])**2),n]
            else:
                distance_souris = [n,0,np.sqrt((self.__coordonnees[0]-self.__souris[0])**2),0]
        else :
            if self.__coordonnees[1]>self.__souris[1]:
                distance_souris = [0,n,0,np.sqrt((self.__coordonnees[1]-self.__souris[1])**2)]
            elif self.__coordonnees[1]<self.__souris[1]:
                distance_souris = [0,np.sqrt((self.__coordonnees[1]-self.__souris[1])**2),0,n]
            else:
                distance_souris = [0,0,0,0]
        
        #distance murs
        distance_murs = [self.__coordonnees[0],(height_zone-10)//taille_grille-self.__coordonnees[1],(width_zone-10)//taille_grille-self.__coordonnees[0],self.__coordonnees[1]]
        
        #distance queue
        distance_queue = np.zeros(4)
        for i in range(2,len(self.__coordonnees),2):
            if self.__coordonnees[0] == self.__coordonnees[i] and self.__coordonnees[1] <= self.__coordonnees[i+1]:
                distance_queue[0] = n
            if self.__coordonnees[0] == self.__coordonnees[i] and self.__coordonnees[1] >= self.__coordonnees[i+1]:
                distance_queue[2] = n
            if self.__coordonnees[0] <= self.__coordonnees[i] and self.__coordonnees[1] == self.__coordonnees[i+1]:
                distance_queue[1] = n
            if self.__coordonnees[0] >= self.__coordonnees[i] and self.__coordonnees[1] == self.__coordonnees[i+1]:
                distance_queue[3] = n
        
        for i in range(4):
            #input layer size 12
            self.__input_layer[i] = distance_souris[i]
            self.__input_layer[i+4] = distance_queue[i]
            self.__input_layer[i+8] = distance_murs[i]
        return self.__input_layer
    
    def move(self):
        dirct = self.get_direction()
        self.__nb_jeu -= 1
        if self.can_move(dirct):
            #print("Snake moved :")
            #tete = self.__coordonnees[0:2]
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
            #print("New coordonnees : {}".format(self.__coordonnees))
            #si le serpent a attrapé la souris
            if self.__coordonnees[0:2] == self.__souris:
                self.__score += 1
                self.__souris = [np.random.randint(0,(width_zone-10)//taille_grille-1),np.random.randint(0,(height_zone-10)//taille_grille-1)]
                self.__liste_souris.append(self.__souris)
        else:
            print("Serpent out : ",self.__parcours)
            print("nb_jeu :",nb_jeu-self.__nb_jeu)
            self.__can_play = 0
        self.__fitness = self.comput_fitness()
        #print("Current fitness : ",self.__fitness)
        #0 left 1 down 2 right 3 up
    def get_liste_coordonnees(self):
        return self.__parcours
    def get_liste_souris(self):
        return self.__liste_souris
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
        if self.__nb_jeu <= 0 or self.__coordonnees[0] < 0 or self.__coordonnees[0] > (width_zone-10)//taille_grille-1 or self.__coordonnees[1] < 0 or self.__coordonnees[1] > (height_zone-10)//taille_grille-1 or self.__can_play == 0:
            self.__can_play = 0
            return False
        return True
    def can_move(self,direction):
        coordonnees = self.__coordonnees
        prochaine_case = []
        
        #print("Le serpent peut-il bouger ?")
        #print("Direction : ",directions[direction])
        #print("Coordonnees : ",coordonnees)
        
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
        if prochaine_case[0] < 0 or prochaine_case[0] > (width_zone-10)//taille_grille or prochaine_case[1] < 0 or prochaine_case[1] > (height_zone-10)//taille_grille:
            self.__can_play == 0
            return False
        if l_in_l(prochaine_case,coordonnees):
            self.__can_play == 0
            return False
        return True
        
        
        
        
# --------------------------------------------------------
if __name__ == "__main__":
    fen = FenPrincipale()
    fen.mainloop()
