#-*- encoding: utf-8 -*-
from Common import *
import pygame as pyg

import os

pyg.init()


class Menu:
	
	#myfont = pyg.font.SysFont(Helvetic, 20)
	
	def __init__(self, screen):
		self.scr = screen	#Afficher le screen
		
		#Image du menu
		self.imgmenu= pyg.image.load(os.path.join(IMG_FOLDER, "trumprun.png")).convert_alpha()
		#Image bouton Jouer
		self.imgjouer= pyg.image.load(os.path.join(IMG_FOLDER, "jouer.png")).convert_alpha()
	
	
	def draw(self):
		self.scr.fill(BLACK)
		#On centre le titre en haut
		posMenu = (0,0)
		#On centre le bouton jouer
		posJouer= (GAME_SIZE[0]/2 - self.imgjouer.get_width()/2, GAME_SIZE[1]/2 - self.imgjouer.get_height()/2)
		
		
		#Affichage des images
		self.scr.blit(self.imgmenu, posMenu)
		self.scr.blit(self.imgjouer, posJouer)
	
	def clique(self):
		if checkInRect(JOUER_POS, JOUER_SIZE, pyg.mouse.get_pos()):
			return True
		else:
			return False
	
	
	
	
	
	
	
	
	'''def gerer_events_principale ():
		for event in pyg.event.get():'''
		
	'''def menu(self):
		self.menu
		self.rect = self.image.get_rect()
		
		self.rect.x = x
		self.rect.y = y
	 
		gerer_mouse_menu(rect)
	
	def jeu():
		rect = pyg.draw.rect(fenetre,(0,255,0))
		pyg.Rect(100, 200, 100, 100))
	 
		text = myfont.render(Jouer2, False, (255,255,255))
		fenetre.blit(text, (100,200))
	 
		gerer_mouse_jeu(rect)'''
		 
	'''def gerer_mouse_jeu(self,rect):
	
		mouse = pyg.mouse.get_pressed()
		
		if mouse[0]: # UP
			mouse_pos = pyg.mouse.get_pos()
			
		if rectangle.collidepoint(mouse_pos):
			
	def gerer_mouse_menu(rectangle):
		global afficher
		 
		mouse = pyg.mouse.get_pressed()
		if mouse[0]: # UP
			mouse_pos = pyg.mouse.get_pos()
			 
			if rectangle.collidepoint(mouse_pos):'''
