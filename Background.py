#-*- encoding: utf-8 -*-
import pygame

from Common import *

#Classe sprite qui hérite de la classe Sprite de Pygame
class Background(pygame.sprite.Sprite):
	#Contient la position du fond (0 ou 1, le premier à gauche étant le 0)
	index = -1

	accel = 0

	#Surface pour l'image ou la surface du Spite, alphaColor pour la couleur de transp
	#plr si c'est un personnage (qu'on ne fera pas sortir de l'écran)
	def __init__(self, surface, backIndex):
		pygame.sprite.Sprite.__init__(self)

		self.image = surface
		self.rect = self.image.get_rect()

		self.index = backIndex

		if self.index == 0:
			self.rect.x = 0
			#self.rect.y = 0
		else:
			self.rect.x = GAME_SIZE[0]
			#self.rect.y = 0

	def move(self, x=0, y=0):
		self.rect.x += x
		self.rect.y += y

	def update(self):
		self.move(-(BACK_SPEED + self.accel))

		if self.index == 0:
			if self.rect.x < -GAME_SIZE[0]:
				self.rect.x = 0
		else:
			if self.rect.x < 0:
				self.rect.x = GAME_SIZE[0]

	def addAccel(self):
		self.accel += ACCEL
		print("Background: accel= " + str(self.accel))

	def resetAccel(self):
		self.accel = 0