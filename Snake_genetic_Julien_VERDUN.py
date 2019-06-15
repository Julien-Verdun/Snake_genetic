# -*- coding: utf-8 -*-
"""
Created on Mon May 27 07:36:23 2019
@author: Julien Verdun
"""


"""
TO-DO LIST

Le NN ne semble pas converger du tout..
Tester de remettre la sigmoide

"""


from tkinter import *
from tkinter.messagebox import *
import random
import numpy as np
from time import sleep
import class_snake as clsnk
import time

scale = clsnk.get("scale")
len_gen = clsnk.get("len_gen")
directions = clsnk.get("directions")
mutation_rate = clsnk.get("mutation_rate")
nb_jeu = clsnk.get("nb_jeu")
taille_grille = clsnk.get("taille_grille")
width_zone = clsnk.get("width_zone")
height_zone = clsnk.get ("height_zone")
Lx = clsnk.get("Lx")
Ly = clsnk.get("Ly")

global t0,t1
t0 = time.time()
t1 = time.time()
# --------------------------------------------------------

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
    def __init__(self, parent, w=clsnk.get("width_zone"), h=clsnk.get("height_zone"), _bg='white'):  # 500x400 : dessin final !
        self.__w = w
        self.__h = h
        # Terrain de 40 cas de hauteur et 30 de cote
        self.__fen_parent=parent
        Canvas.__init__(self, parent, width=w, height=h, bg=_bg, relief=RAISED, bd=5)
        self.create_rectangle(10,10,w,h,outline="black",width=2)
        for i in range(Ly):
            self.create_line(10,taille_grille*i+10,w,taille_grille*i+10,fill="black",width = 2)
        for j in range(Lx):
            self.create_line(taille_grille*j+10,10,taille_grille*j+10,h,fill="black",width = 2)

class FenPrincipale(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.__advices = Label(self)
        self.__advices.pack(side=TOP)
        self.__advices.config(text = "Press the button Up/Down/Left/Down to simulate one/five/ten/fifty generations")

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
        self.__boutonEffacer = Button(self, text='Effacer', command=self.effacer).pack(side=LEFT, padx=5, pady=5)
        # Création d'un widget Button (bouton Quitter)
        self.__boutonQuitter = Button(self, text='Quitter', command=self.destroy).pack(side=LEFT, padx=5, pady=5)
        self.__mouse_display = []
        self.__snake_display = []

        self.__is_reproducing = 1

        self.focus_set()
        #self.bind("<Key>",self.next_generation)
        self.bind("<Key>",self.next_generation)
    def effacer(self):
        self.__zoneAffichage.delete(ALL)



    def affiche_best_snake_mouse(self,best_snake,color_snake,color_head,color_mouse):
        liste_coordonnees = best_snake.get_liste_coordonnees()
        print("Coordonnees of the best snake : {}".format(liste_coordonnees))
        liste_mouse = best_snake.get_liste_mouse()
        if self.__mouse_display != []:
            for elt in self.__mouse_display:
                self.__zoneAffichage.delete(elt)
            self.__mouse_display = []
        if self.__snake_display != []:
            for elt in self.__snake_display:
                self.__zoneAffichage.delete(elt)
            self.__snake_display = []
        for i in range(0,len(liste_coordonnees)-2,2) :
            self.__snake_display.append(self.__zoneAffichage.create_rectangle(10 + taille_grille*liste_coordonnees[i],10 + taille_grille*liste_coordonnees[i+1],10 + taille_grille*(liste_coordonnees[i]+1),10 + taille_grille*(liste_coordonnees[i+1]+1),fill = color_snake,outline="green"))
        self.__snake_display.append(self.__zoneAffichage.create_rectangle(10 + taille_grille*liste_coordonnees[-2],10 + taille_grille*liste_coordonnees[-1],10 + taille_grille*(liste_coordonnees[-2]+1),10 + taille_grille*(liste_coordonnees[-1]+1),fill = color_head,outline="green"))
        for i in range(len(liste_mouse)):
            self.__mouse_display.append(self.__zoneAffichage.create_oval(10 + liste_mouse[i][0]*taille_grille,10 + liste_mouse[i][1]*taille_grille,10 + (liste_mouse[i][0]+1)*taille_grille,10 + (liste_mouse[i][1]+1)*taille_grille,fill=color_mouse,outline="yellow"))
        print("Best snake displayed, you can go to the next generation")
    """
    def affiche_best_snake_mouse_step_by_step(self,best_snake,color_snake,color_head,color_mouse):
        liste_coordonnees = best_snake.get_liste_coordonnees()
        print("Coordonnees of the best snake : {}".format(liste_coordonnees))
        liste_mouse = best_snake.get_liste_mouse()
        if self.__mouse_display != []:
            for elt in self.__mouse_display:
                self.__zoneAffichage.delete(elt)
            self.__mouse_display = []
        if self.__snake_display != []:
            for elt in self.__snake_display:
                self.__zoneAffichage.delete(elt)
            self.__snake_display = []

        self.__snake_display.append(self.__zoneAffichage.create_rectangle(10 + taille_grille * liste_coordonnees[0],10 + taille_grille * liste_coordonnees[1],10 + taille_grille * (liste_coordonnees[0] + 1),10 + taille_grille * (liste_coordonnees[1] + 1),fill=color_snake, outline="green"))
        self.__snake_display.append(self.__zoneAffichage.create_rectangle(10 + taille_grille * liste_coordonnees[2],
                                                                          10 + taille_grille * liste_coordonnees[3],
                                                                          10 + taille_grille * (
                                                                                      liste_coordonnees[2] + 1),
                                                                          10 + taille_grille * (
                                                                                      liste_coordonnees[3] + 1),
                                                                          fill=color_snake, outline="green"))
        self.__snake_display.append(self.__zoneAffichage.create_rectangle(10 + taille_grille * liste_coordonnees[4],
                                                                          10 + taille_grille * liste_coordonnees[5],
                                                                          10 + taille_grille * (
                                                                                      liste_coordonnees[4] + 1),
                                                                          10 + taille_grille * (
                                                                                      liste_coordonnees[5] + 1),
                                                                          fill=color_snake, outline="green"))
        self.__snake_display.append(self.__zoneAffichage.create_rectangle(10 + taille_grille * liste_coordonnees[6],
                                                                          10 + taille_grille * liste_coordonnees[7],
                                                                          10 + taille_grille * (
                                                                                      liste_coordonnees[6] + 1),
                                                                          10 + taille_grille * (
                                                                                      liste_coordonnees[7] + 1),fill=color_snake, outline="green"))
        print(len(liste_coordonnees))
        for i in range(8,len(liste_coordonnees)-7,2) :
            self.__zoneAffichage.move(self.__snake_display[3], (liste_coordonnees[i] - liste_coordonnees[i-2])*taille_grille, (liste_coordonnees[i+1] - liste_coordonnees[i-1])*taille_grille)
            self.__zoneAffichage.move(self.__snake_display[2], (liste_coordonnees[i-2] - liste_coordonnees[i-4])*taille_grille, (liste_coordonnees[i-1] - liste_coordonnees[i-3])*taille_grille)
            self.__zoneAffichage.move(self.__snake_display[1], (liste_coordonnees[i-4] - liste_coordonnees[i-6])*taille_grille, (liste_coordonnees[i-3] - liste_coordonnees[i-5])*taille_grille)
            self.__zoneAffichage.move(self.__snake_display[0], (liste_coordonnees[i-6] - liste_coordonnees[i-8])*taille_grille, (liste_coordonnees[i-5] - liste_coordonnees[i-7])*taille_grille)
            print("Affichage du serpent, étape ",i)
            #sleep(0.5)
        for i in range(len(liste_mouse)):
            self.__mouse_display.append(self.__zoneAffichage.create_oval(10 + liste_mouse[i][0]*taille_grille,10 + liste_mouse[i][1]*taille_grille,10 + (liste_mouse[i][0]+1)*taille_grille,10 + (liste_mouse[i][1]+1)*taille_grille,fill=color_mouse,outline="yellow"))
        print("Best snake displayed, you can go to the next generation")
    """
    def generer_snake(self):
        return clsnk.Snake(4,0)
    def new_generation(self,old_generation):
        liste_fitness = []
        for snake in old_generation :
            liste_fitness.append(snake.get_fitness())
        liste_indices = np.argsort(liste_fitness)
        new_generation = trier(old_generation,liste_indices)
        for i in range(int(0.4*len(new_generation))+1,int(0.8*len(new_generation))):
            new_generation[i].crossover(new_generation[0])
        for i in range(int(0.8*len(new_generation)),len(new_generation)):
            new_generation[i].selection()
        for i in range(int(0.1*len(new_generation))+1,int(0.4*len(new_generation))+1):
            new_generation[i].mutation()
        return new_generation

    def next_generation(self,event):
        t0 = time.time()
        touche = event.keysym
        if touche == "Up":
            self.next_generation_one_step()
        elif touche == "Down":
            self.next_generation_n_step(5)
        elif touche == "Left":
            self.next_generation_n_step(10)
        elif touche == "Right":
            self.next_generation_n_step(50)
        t1 = time.time()
        print("Temps de génération :", t1-t0)

    def next_generation_one_step(self):
        #deplacement de tout les serpents
        for snake in self.__generation_snake :
            while snake.can_play():
                snake.move()

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
        print("Dead reason : ",best_snake.get_dead_reason())
        if best_snake == 0:
            print("Error fonction next generation")
            best_snake = self.__generation_snake[0] # pas ouf

        #affichage du seprent et mise à jour des textes
        self.affiche_best_snake_mouse(best_snake,"pink","magenta","red")
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


    def next_generation_n_step(self,n_step):
        for i in range(n_step): #mettre une variable globale ici
            #deplacement de tout les serpents
            for snake in self.__generation_snake :
                while snake.can_play():
                    snake.move()

            #recherche du meilleur element
            best_fitness = 0
            best_snake = 0
            for snake in self.__generation_snake:
                if snake.get_fitness() >= best_fitness:
                    best_snake = snake
                    best_fitness = snake.get_fitness()
            print("Best snake : ",best_snake.get_coordonnees())
            print("Best fitness : ",best_fitness)
            print("Best score :",best_snake.get_score())
            print("Dead reason : ",best_snake.get_dead_reason())
            if best_snake == 0:
                print("Error fonction next generation")
                best_snake = self.__generation_snake[0] # pas ouf

            self.__generation += 1
            # calcul de la prochaine generation
            self.__generation_snake = self.new_generation(self.__generation_snake)

        self.affiche_best_snake_mouse(best_snake, "pink","magenta","cyan")
        self.__text_generation.config(text="Generation : {}".format(self.__generation))
        self.__score = best_snake.get_score()
        self.__text_score.config(text="Current score : {}".format(self.__score))
        self.__fitness = best_snake.get_fitness()
        self.__text_fitness.config(text="Best fitness : {}".format(self.__fitness))
        [input_layer, hidden_layer1, hidden_layer2, output_layer] = best_snake.get_NN()
        self.__NN.config(text="Input layer : " + liste_to_txt(input_layer) + "\n" + "Hidden layer1 : " + liste_to_txt(
            hidden_layer1) + "\n" + "Hidden layer2 : " + liste_to_txt(
            hidden_layer2) + "\n" + "Output_layer : " + liste_to_txt(output_layer))



# --------------------------------------------------------
if __name__ == "__main__":
    fen = FenPrincipale()
    fen.mainloop()
