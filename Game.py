#-*- encoding: utf-8 -*-
import pygame as pyg
from pygame.locals import *
from random import randint
import os

from Sprite import Sprite
from Background import Background
from Common import *
from Obstacle import Obstacle
from IA import IA

#Définition de notre classe Game (qui n'hérite de rien, contrairement aux classe sprites)
class Game:
	#Booléens d'état
	inReset = False
	overObstacle = False
	inPause = False

	# Compteur à incrémenter pour chaque tour de boucle (ou chaque update par ex)
	# Servira à accélerer progressivement les obstacles et le back
	cptAccel = 0 #Compte le délai entre chaque accéleration
	accel = 0 #Niveau d'accéleration actuel

	# Pour l'animation de l'écran de reset
	cptResetAnim = 0
	resetImage = 0
	posDeadSprite = 0
	animDeadSprite = False

	#Explicite :)
	points = 0

	# Chaines de carractere pour les textes
	ptsString = "Pts: "
	speedString = "Speed: "

	distString = "Dist: "
	heightString = "Height: "
	currGenoString = "Genome: "
	currGenoIdString = "Current Genome: "
	currGeneString = "Current Generation: "

	bestPointsString = "Points record: "
	gradDescentString = "Gradial: "
	
	pyg.init()

	def __init__(self, screen):	
		print("Game start init ...")

		self.scr = screen

		self.ia = IA(self);

		# Chargement des différentes images que le jeu utilise
		self.imgBack = pyg.image.load(os.path.join(IMG_FOLDER, "background2.png")).convert()
		self.imgPerso = pyg.image.load(os.path.join(IMG_FOLDER, "perso4.png")) .convert_alpha()

		# Images pour l'animation de l'écran de reset
		self.imgReset1 = pyg.image.load(os.path.join(IMG_FOLDER, "gameover1.png")) .convert_alpha()
		self.imgReset2 = pyg.image.load(os.path.join(IMG_FOLDER, "gameover2.png")) .convert_alpha()
		self.imgReset3 = pyg.image.load(os.path.join(IMG_FOLDER, "gameover3.png")) .convert_alpha()
		self.imgReset4 = pyg.image.load(os.path.join(IMG_FOLDER, "gameover4.png")) .convert_alpha()
		self.imgDeadSprite = pyg.image.load(os.path.join(IMG_FOLDER, "deadSprite.png")) .convert_alpha()

		# Images boutons reset
		self.imgResetYes = pyg.image.load(os.path.join(IMG_FOLDER, "oui.png")) .convert_alpha()
		self.imgResetNo = pyg.image.load(os.path.join(IMG_FOLDER, "non.png")) .convert_alpha()

		self.imgRestart = pyg.image.load(os.path.join(IMG_FOLDER, "rejouer.png")) .convert_alpha()

		# Background
		self.backSpr1 = Background(self.imgBack, 0)
		self.backSpr2 = Background(self.imgBack, 1)

		self.backGroup = pyg.sprite.Group()
		self.backGroup.add(self.backSpr1)
		self.backGroup.add(self.backSpr2)

		# Personnage
		self.plrSpr = Sprite(self.imgPerso, 0, PURPLE)

		# Même si ce n'est que pour contenir un sprite, ca simplifie les draw
		self.plrGroup = pyg.sprite.Group()
		self.plrGroup.add(self.plrSpr)

		# Obstacles
		self.obsSpr1 = Obstacle(0,0, 1)
		self.obsSpr2 = Obstacle(0,0, 2)

		self.obsSpr1.setOrigPos(GAME_SIZE[0], randint(MAXTOP_OBS,PLR_GROUND - self.obsSpr1.getSize()[1]))
		self.obsSpr2.setOrigPos(DECAL_OBS*GAME_SIZE[0], randint(MAXTOP_OBS,PLR_GROUND - self.obsSpr1.getSize()[1]))

		self.obstacleGroup = pyg.sprite.Group()
		self.obstacleGroup.add(self.obsSpr1)
		self.obstacleGroup.add(self.obsSpr2)

		# Textes
		self.font20 = pyg.font.SysFont("arial", 20)
		self.font30 = pyg.font.SysFont("arial", 26)

		print("--- Game end init ---")


	# Rajoute une constante d'accéleration, appelée par update
	def addAccel(self):
		self.accel += ACCEL
		self.cptAccel = 0

		#self.backSpr1.addAccel()
		#self.backSpr2.addAccel()

		self.obsSpr1.addAccel()
		self.obsSpr2.addAccel()

		self.plrSpr.addAccel()

		#print("ACCELERATED ! (self.accel= " + str(self.accel) + ")")

	# Remet à zéro tout ce qui accelere (appelé par le game.reset())
	def resetAccel(self):
		self.accel = 0
		self.cptAccel = 0

		self.backSpr1.resetAccel()
		self.backSpr2.resetAccel()

		self.obsSpr1.resetAccel()
		self.obsSpr2.resetAccel()

		self.plrSpr.resetAccel()

	# Vérifie si on est au dessus d'un obstacle (pour compter les points)
	def checkOverObstacle(self):
		if inter(self.obsSpr1.getPos()[0], self.obsSpr1.getPos()[0] + self.obsSpr1.getSize()[0], self.plrSpr.getPos()[0]) or inter(self.obsSpr2.getPos()[0], self.obsSpr2.getPos()[0] + self.obsSpr1.getSize()[0], self.plrSpr.getPos()[0]):
			return True
		else:
			return False

	# Fonction qui retourne la distance du personnage au prochain obstacle (pour l'IA) (-1 si on est sur un obstacle)
	def getDistance(self):
		plrPosx = self.plrSpr.getPos()[0] + self.plrSpr.getRect().width
		dist = -1
		# Trouver le quel des obstacle est le prochain pour le personnage
		if plrPosx < self.obsSpr1.getPos()[0] :
			dist = self.obsSpr1.getPos()[0] - plrPosx
		elif plrPosx < self.obsSpr2.getPos()[0]:
			dist = self.obsSpr2.getPos()[0] - plrPosx

		#print("Distance to next obstacle: " + str(dist))
		return dist

	# Retourne la hauteur du prochain obstacle
	def getHeight(self):
		plrPosx = self.plrSpr.getPos()[0] + self.plrSpr.getRect().width
		height = -1
		nextObs = -1

		# Trouver le quel des obstacle est le prochain pour le personnage
		if plrPosx < self.obsSpr1.getPos()[0] :
			height = PLR_GROUND - self.obsSpr1.getPos()[1]
			nextObs = 1 
		elif plrPosx < self.obsSpr2.getPos()[0]:
			height = PLR_GROUND - self.obsSpr2.getPos()[1]
			nextObs = 2

		#Permet de detecter le bug
		#if height > 150:
			#print("BUG HEIGHT=", height, ", next=", nextObs, " plrPosx=", plrPosx, " obs1= ", self.obsSpr1.getPos()[0], " obs2=", self.obsSpr2.getPos()[0])

		return height

	def update(self):
		# Doit contenir tout les update des personnage, obstacle, background ....

		# On update l'IA et on saute si c'est ordonné par l'IA
		if not DISABLE_IA and self.ia.update(self.getDistance(), self.getHeight(), self.accel):
			self.plrSpr.launchJump()

		if not DISABLE_COLLISION: #On agit que si les collisions sont activées
			if pyg.sprite.collide_rect(self.plrSpr, self.obsSpr1) or pyg.sprite.collide_rect(self.plrSpr, self.obsSpr2):
				#print("Collision avec obs")
				# Si on est mode IA, on passe l'écran de mort et on retourne au jeu
				if not DISABLE_IA:
					self.inReset = False
					self.reset()
				else:
					self.inReset = True
					#self.youHadText = self.font20.render(self.youHadString[0] + str(self.points) + self.youHadString[1], True, WHITE)
					self.scr.fill(BLACK)

					self.posDeadSprite = self.plrSpr.getPos()[1]
	
		self.backGroup.update()
		self.plrGroup.update()
		self.obstacleGroup.update()

		# Gestion des passages d'obstacles
		if self.checkOverObstacle() and not self.overObstacle:
			self.overObstacle = True
			#print("Over an obstacle")
		if not self.checkOverObstacle() and self.overObstacle:
			self.overObstacle = False
			self.points += 1
			if not DISABLE_IA:
				self.ia.nextObstacle()
			#print("Not anymore over an obstacle")
			#print("Game: Points + 1")

		#self.getDistance()
		#self.getHeight()

		# Actualisation de tout les textes
		self.ptsText = self.font30.render(self.ptsString + str(self.points), True, GRAY)

		self.speedText = self.font20.render(self.speedString + str(1 + self.accel), True, WHITE)
		self.distText = self.font20.render(self.distString + str(self.getDistance()), True, WHITE)
		self.heightText = self.font20.render(self.heightString + str(self.getHeight()), True, WHITE)

		self.currGenoIdText = self.font20.render(self.currGenoIdString + str(self.ia.getCurrGenoId()), True, WHITE)
		self.currGenoText = self.font20.render(self.currGenoString + str(self.ia.getCurrGeno()), True, WHITE)
		self.currGeneText = self.font20.render(self.currGeneString + str(self.ia.getCurrGene()), True, WHITE)

		self.bestPointsText = self.font20.render(self.bestPointsString + str(self.ia.getHighScore()), True, WHITE)
		self.gradDescentText = self.font20.render(self.gradDescentString + str(self.ia.getGradial()), True, WHITE)

		if self.cptAccel > SEUIL_ACCEL:
			self.addAccel()

		self.cptAccel += 1

	# Appelée pour préparer la prochaine partie
	def reset(self):
		# On appelle le prochain génome
		if not DISABLE_IA:
			self.ia.setGenomeResult(self.points)
			self.ia.nextGenome()

		self.obsSpr1.reset()
		self.obsSpr2.reset()

		self.plrSpr.reset()

		self.inReset = False
		self.points = 0
		
		self.resetAccel()

		self.cptResetAnim = 0
		self.resetImage = 0
		self.posDeadSprite = 0

		self.animDeadSprite = False

		self.overObstacle = False

	# Pour les animations de l'écran de mort
	def updateResetAnim(self):
		if self.resetImage >= 4:
			self.resetImage = 0

		if self.cptResetAnim >= FPS*0.5:
			self.cptResetAnim = 0
			self.resetImage += 1 

		if self.posDeadSprite <= GAME_SIZE[1] + 100:
			self.posDeadSprite += 1.2
		else:
			self.animDeadSprite = True

		self.cptResetAnim += 1

	def goToMenu(self):
		print("Game: GoToMenu called -> LOUIS")

	def closeIAFile(self):
		self.ia.closeFile()

	#Est appelé suite à un clic pendant inReset dans le main
	# Return True quand on recommence une partie et false quand on va au menu
	def handleClick(self):
		if DISABLE_IA:
			if checkInRect(RESET_YES, self.imgResetYes.get_size(), pyg.mouse.get_pos()):
				print("RESET YES BUTTON PRESSED !")
				self.inReset = False
				self.reset()
				return True

			elif checkInRect(RESET_NO, self.imgResetNo.get_size(), pyg.mouse.get_pos()):
				print("RESET NO BUTTON PRESSED !")
				self.inReset = False
				self.goToMenu()
				return False
		else:
			if self.inPause:
				self.inPause = False
			else:
				self.inPause = True

			#print("New state pause: ", self.inPause)

	#Fonction d'affichage de tout (reset ou en jeu), appellée par le main.py
	def draw(self):
		if not self.inReset:
			""" Si on est en IA et qu'on est pause, pas d'update, 
			on fige le jeu (meme si on continue les draw)"""
			if not DISABLE_IA:
				if not self.inPause:
					self.update()
			else:
				self.update()

			self.backGroup.draw(self.scr)
			self.obstacleGroup.draw(self.scr)
			self.plrGroup.draw(self.scr)

			# Affichage des textes
			self.scr.blit(self.distText, (10, 485))
			self.scr.blit(self.heightText, (10, 505))
			self.scr.blit(self.speedText, (10, 525))

			if not DISABLE_IA:
				self.scr.blit(self.currGenoText, (150, 485))
				self.scr.blit(self.currGenoIdText, (150, 505))
				self.scr.blit(self.currGeneText, (150, 525))

				self.scr.blit(self.bestPointsText, (400, 485))
				self.scr.blit(self.gradDescentText, (400, 505))

				
			self.scr.blit(self.ptsText, (0,0))

		else:
			self.updateResetAnim()

			self.scr.blit(self.imgBack, (0,0))

			if not self.animDeadSprite:
				# Pour centrer le texte au millieu de la fenetre de jeu
				posGameOver = (GAME_SIZE[0]/2 - self.imgReset1.get_width()/2, GAME_SIZE[1]/2 - self.imgReset1.get_height()/2)

				# L'animation des graphismes de gameover
				if self.resetImage == 0:
					self.scr.blit(self.imgReset1, posGameOver)
				elif self.resetImage == 1:
					self.scr.blit(self.imgReset2, posGameOver)
				elif self.resetImage == 2:
					self.scr.blit(self.imgReset3, posGameOver)
				elif self.resetImage == 3:
					self.scr.blit(self.imgReset4, posGameOver)

				self.scr.blit(self.imgDeadSprite, (0.5*(GAME_SIZE[0] - self.imgDeadSprite.get_width()), self.posDeadSprite))

			else:
				self.scr.blit(self.imgRestart, (GAME_SIZE[0]/2 - self.imgRestart.get_size()[0]/2, GAME_SIZE[1]/2 - self.imgRestart.get_size()[1]/2))

				self.scr.blit(self.imgResetYes, RESET_YES)
				self.scr.blit(self.imgResetNo, RESET_NO)
