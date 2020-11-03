#-*- encoding: utf-8 -*-
import pygame
from pygame.locals import *

import random as rd
import os

from Common import *

class Obstacle(pygame.sprite.Sprite):	#Définition de notre classe Obstacle
	accel = 0
	origPos = (0,0)

	id = 0						
	
	def __init__(self, x , y, id=-1): #Création de la méthode qui créée nos attributs
		pygame.sprite.Sprite.__init__(self)
		
		#pygame.draw.rect(self.image, [0, 0, ])
		self.image = pygame.image.load(os.path.join(IMG_FOLDER, "obs.png")).convert_alpha()
		
		self.rect = self.image.get_rect() #L'obstacle prend la taille de l'image
		
		self.rect.x = x
		self.rect.y = y

		self.id = id

	def randPos(self):
		return (rd.randint(MAXTOP_OBS,PLR_GROUND - self.rect.height))

	def setPos(self, x, y):
		self.rect.x = x
		self.rect.y = y
		
	def addAccel(self):
		self.accel += ACCEL
		#print("Obstacle: accel= " + str(self.accel))

	def resetAccel(self):
		self.accel = 0

	def getPos(self):
		return (self.rect.x, self.rect.y)

	def getSize(self):
		return (self.rect.width, self.rect.height)

	def update(self):
		self.rect.x = self.rect.x - (OBS_SPEED + self.accel)
		
		# Si l'obstacle est en dehors de l'écran, on le place a SCREEN_SIZE[0]
		if self.rect.x < -self.rect.width:
			#self.rect.x = GAME_SIZE[0]
			self.rect.x = round(round(rd.uniform(1, 1.1), 2)*GAME_SIZE[0],0)
			self.rect.y = self.randPos()
			#print("Obs: Resetted obs id: ", self.id, ", x=", self.rect.x)

	def setOrigPos(self, x, y):
		self.origPos = (x, y)
		self.setPos(x, y)

	def reset(self):
		self.setPos(self.origPos[0], self.randPos())