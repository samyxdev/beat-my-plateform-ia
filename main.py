#-*- encoding: utf-8 -*-

"""œ
ToDo (- à faire, x fait):
x Remplir toute la zone non couverte par le GAME_SIZE avec du noir
        pour ne pas afficher le background en défillement
- Ralentir l'animation qui fait marcher leur perso
x Desactiver le spam de sauts
x Classe JEU (le menu de selection ne sera pas dedans mais l'écran de mort si)
x Après un reset, RESET LES OBSTACLES et le plrSpr
x Proposer un bouton non au reset
x Obstacle accélerants
x Préparer le code pour le menu de Louis
x Corriger bug de la fermeture impossible par la croix
x Compter les points (passer des obstacles)
x Modulariser l'équation du saut
x Rajouter un mode pause quand on est en IA (en cliquant)
x Bug: point qui est compté au tout début de partie des fois 
        -> Le overObstacle n'était pas reset
x Bug: Height faux après avoir passé un obstacle
        -> Faute de frappe
x Ajouter la possibilité d'ajuster les fps en jeu (touches dir ou mollette)
        -> A la molette de souris (ou touches directionnelles ?)
x Bug: Best high score en IA n'affiche pas toujours la meilleure
        -> Un manque d'update de la variable

IA:
x Créer la classe, et les fonctions d'input pour le ML (distance, hauteur, vitesse)
x Génerer des génomes
x Generer les génerations
x Appliquer le treshold pour un saut ou non
x Retenir pour l'apprentissage
x Generer les nouvelles géneration en fonction des dernières
x Descente gradiale (1 puis 0.1 etc)

Infos:
- L'accéleration de la vitesse du personnage est ralentie pr rapport a celle des obs
- La bouncebox des sprites correspond à leur taille d'image 
        -> donc les bords de la bouncebox voulue doivent être collés aux bords de l'image
"""

import pygame as pyg
from pygame.locals import * 
import os

from Common import *
from Game import Game
from Menu import Menu

# Initialisation de base de pygame
pyg.init()

scr = pyg.display.set_mode(SCREEN_SIZE)
if not DISABLE_IA:
        pyg.display.set_caption("Samy & Louis: Projet Bac ISN - IA Enabled: Threshold: " + str(THRESH) + " - Click to pause")
else:
        pyg.display.set_caption("Samy & Louis: Projet Bac ISN - IA Disabled")

pyg.display.set_icon(pyg.image.load(os.path.join(IMG_FOLDER, "icon.png")))

# Gestion du temps (pour les FPS)
clock = pyg.time.Clock()

 # Chargement de la police
font30 = pyg.font.SysFont("arial", 30)

#Incrémenteur ou décrementeur des FPS (avec la mollette)
fpsCpt = 0

# --------------------------------

# On initialise la classe de jeu et on lui référence l'écran
game = Game(scr)

# Objet menu
menu = Menu(scr)

# Surface n'étant pas dans la partie de l'écran consacrée au jeu
# Gère pour l'instant l'unique différence sur l'axe des abscisses 
#(ne pas oublier de changer la ligne en bas: scr.blit(deltaSurface, (GAME_SIZE[0], 0)))
deltaSurface = pyg.Surface((SCREEN_SIZE[0], SCREEN_SIZE[1] - GAME_SIZE[1]))
deltaSurface.fill(BLACK)

#Booléens d'état
stopExec = False
clicking = False

# En jeu ou en menu
inGame = False

#La boucle de jeu
while not stopExec:
        #Limite les images par secondes au seuil de la constante FPS, ajustable
        clock.tick(FPS + fpsCpt)

        # -------------------- DEBUT EVENT ---------------------------
        for event in pyg.event.get():
                # Un éventuelle fermeture par la croix de la fenetre ?
                if event.type == QUIT:
                                stopExec = True

                # Pour les events avec touches
                if hasattr(event, "key"): 
                        if event.type == KEYDOWN:
                                if event.key == K_ESCAPE:
                                        stopExec = True
                                if event.key == K_SPACE:
                                        if DISABLE_IA:
                                                game.plrSpr.launchJump()
                                        else:
                                                print("Jump user input cancelled -> IA Enabled")
                                if event.key == K_r:
                                        #Pour l'instant on utilse cette touche pour simuler une mort
                                        inReset = True
                                        print("In Reset Screen entered")
                                        scr.fill(BLACK)

                if event.type == MOUSEBUTTONDOWN:
                        if pyg.mouse.get_pressed()[0]: #Si clic gauche
                                if inGame:
                                        if game.inReset:
                                                if not game.handleClick():
                                                        print("Main: Go To Menu")
                                                        inGame = False
                                        # Si on est en mode IA, ca veut dire qu'on demande une pause
                                        elif not DISABLE_IA:
                                                game.handleClick()

                                # On est en menu
                                else:
                                        # Appeler la fonction qui dit si on reste dans le menu
                                        if menu.clique():
                                                inGame = True
                                                game.reset()
                                        else:
                                                inGame = False

                        # Molette vers le haut, add fps
                        if event.button == 4:
                                fpsCpt += 10
                        # Molette vers le bas
                        elif event.button == 5:
                                fpsCpt -= 10
                                        
        #DEBUG - Pour des touches avec action quand on reste pressé
        keys = pyg.key.get_pressed()
        if keys[pyg.K_RIGHT]:
                game.plrSpr.move(1,0)
        elif keys[pyg.K_LEFT]:
                game.plrSpr.move(-1,0)
        # --------------------- FIN EVENT ---------------------------

        
        # Si on est dans le menu du jeu
        if not inGame and not game.inReset:
                menu.draw()

        else: # Sinon, qu'on soit mort (en reset) ou entrain de jouer
                #Agit comme un clean de la surface 
                scr.blit(deltaSurface, (0, GAME_SIZE[1]))
                game.draw()
                
        # Affichage des fps, avec des marges calculées en fonction de la taille du texte
        # Fonction perso définie dans Common
        printFps(font30, clock, scr)

        pyg.display.flip()

#On ferme le programme
print("Main: Fermeture du programme...")
game.closeIAFile()

os._exit(0) #Methode multi-plateforme d'extinction du programme
