#-*- encoding: utf-8 -*-
import pygame
import math

from Common import *

#Classe sprite qui hérite de la classe Sprite de Pygame
class Sprite(pygame.sprite.Sprite):
	inJump = False
	jumpCpt = 0

	origPos = (0,0)

	jetpCpt = 0

	accel = 0

	initJump = -1

	#Surface pour l'image ou la surface du Spite, alphaColor pour la couleur de transp
	#plr si c'est un personnage (qu'on ne fera pas sortir de l'écran)
	def __init__(self, surface, alphaColor=None, x=0, y=0):
		pygame.sprite.Sprite.__init__(self)

		self.image = surface

		if alphaColor is not None:
			self.image.set_colorkey(alphaColor)

		# On centre le personnage horizontalement et au dessus du sol verticalement
		self.rect = self.image.get_rect()
		self.rect.x = GAME_SIZE[0] / 2
		self.rect.y = (PLR_GROUND - self.rect.height)

		#print("Sprite: Plr init pos:", self.getPos())

		self.origPos = (self.rect.x, self.rect.y)
		
	def setPos(self, x, y):
		self.rect.x = x
		self.rect.y = y

	def getPoints(self):
		return str(self.points)

	def getRect(self):
		return self.rect

	def getPos(self):
		return (self.rect.x, self.rect.y)

	def move(self, x=0, y=0):
		self.rect.x += x
		self.rect.y += y

	# A appeler quand on veut lancer un saut
	def launchJump(self):
		if self.inJump == False: #On vérifie qu'on n'était pas déjà en saut
			self.inJump = True
			self.jumpCpt = 0
			self.initJump = self.rect.y
		else:
			print("Already in jump...")

	#Gravité: y=-0.5*9.81*(t - x1)² - hSaut (voir papier/geogebra pour expl)
	def jump(self):
		#jumpNewPos = int(0.5*GRAV*math.pow((self.jumpCpt - math.sqrt(5886)/GRAV), 2)) + JUMP_HEIGHT
		jumpNewPos = int(0.5*GRAV*math.pow((self.jumpCpt - math.sqrt(4*0.5*GRAV*JUMP_HEIGHT)/GRAV), 2)) + JUMP_HEIGHT
		self.setPos(self.rect.x, jumpNewPos)

		#print("Grav: ", jumpNewPos, ", jumpCpt: ", self.jumpCpt, ", DeltaPos= ", PLR_GROUND - jumpNewPos)
		self.jumpCpt += (JUMP_SPEED + self.accel)

		# On va pas plus bas que le sol (sol ou au dessus -> <300) donc fin du saut
		if self.rect.y > self.initJump:
			#print("End of the jump, jumpCpt= ", self.jumpCpt)
			self.rect.y = self.initJump
			self.inJump = False
			self.initJump = -1

	def update(self):
		# D'abord on vérifie si on est pas en dehors de l'écran
		"""
		if self.rect.x < 0 or self.rect.x > GAME_SIZE[0]:
			self.rect.x = 0
			print("Out of screen bounding X")
		if self.rect.y < 0 or self.rect.y > GAME_SIZE[1]:
			self.rect.y = 0
			print("Out of screen bounding Y")
		"""
		
		#On effectue le saut si on est dedans
		if self.inJump:
			self.jump()

		#Pour l'effet flottant (jet-pack like)
		else:
			if self.jetpCpt <= ANIM_SPEED:
				self.rect.y -= 1
				#print("Adding")

			elif self.jetpCpt <= ANIM_SPEED*2:
				self.rect.y += 1
				#print("Sub")

			elif self.jetpCpt == ANIM_SPEED*3:
				self.jetpCpt = 0
				#print("Reset jetpack")

			self.jetpCpt += JETPACK

	def reset(self):
		self.inJump = False
		self.jumpCpt = 0

		self.setPos(self.origPos[0], self.origPos[1])

		#print("Plr Sprite RESETED")

	def addAccel(self):
		self.accel += ACCEL/DECAL_ACCELPLR
		#print("PlrSpr: accel= " + str(self.accel))

	def resetAccel(self):
		self.accel = 0