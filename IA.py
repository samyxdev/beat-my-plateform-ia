#-*- encoding: utf-8 -*-
import pygame as pyg
from pygame.locals import *

import random as rd
import math

from Common import *

class IA:
	game = None

	# Variables des input de l'IA
	dist = 0
	height = 0
	speed = 0

	bestScore = 0

	generated = -1
	usingGenome = 0

	gradDescent = 0

	# On commence avec des déscentes de 1, puis quand gradDescent à atteint le spread, à 0.1 etc
	descentMultiple = 1

	# Pour eviter de demander des sauts quand on est deja dedans
	jumpCalled = False

	# Les trois valeurs contenue par chaque genome sont les 3 coeff qui d'ajoute à l'output
	genomes = [[0 for i in range(3)] for j in range(NBR_GENOME)]

	# Score de chaque genome
	genomesResult = [0 for i in range(NBR_GENOME)]

	# Les seuils de géneration (2 bornes pour les 3 valeurs possibles)
	genBounds = [[0 for i in range(2)] for j in range(3)]
	for i in range(3):
		genBounds[i] = INIT_WEIGHTS_BOUNDS

	def __init__(self, game):
		print("IA Init")

		# On réference le game à l'IA (pour les différentes récup de données) (une sorte de pointeur à la py)
		self.game = game

		self.generateGenome()

		self.file = open("genomeScore.csv", "w")
		self.file.write("Generation;GenomeScore;HighestScore\r\n")

	# La valeur retournée ici (à Game.update) indique si l'on doit sauter ou non
	def update(self, distance, height, speed):
		#print("IA: Distance:" + str(distance) + " Height:" + str(height) + " Speed:" + str(speed))

		if distance != -1 and height != -1:
			self.dist = distance
			self.height = height
			self.speed = speed

			return self.useGenome()

	# Fonction appellée par le Game.reset()
	def nextGenome(self):
		#print("IA: Next genome called ")

		# Mise à jour du meilleur score
		if self.genomesResult[self.usingGenome] > self.bestScore:
			self.bestScore = self.genomesResult[self.usingGenome]
		#else:
			#print("IA: Not best score, genRes=", self.genomesResult[self.usingGenome], " best=", self.bestScore)

		# Ecriture dans le fichier
		writeCsv(self.file, (self.generated, self.genomesResult[self.usingGenome], self.bestScore))

		self.usingGenome += 1
		self.jumpCalled = False

		self.updateGradDescent()

		# On passe au prochain génome ou géneration
		if self.usingGenome < NBR_GENOME:
			return self.useGenome()
		else:
			print("New generation needed")
			self.generateNewGenomes()
			self.usingGenome = 0

	# Pour génener une géneration quand les seuils de géneration sont près
	def generateGenome(self):
		print("IA: Generation genomes:")
		for i in range(NBR_GENOME):
			for o in range(3):
				self.genomes[i][o] = round(rd.uniform(self.genBounds[o][0], self.genBounds[o][1]), 1 + int(math.log10(self.descentMultiple)))

			print("G" + str(i) + ": ", self.genomes[i])

		self.generated += 1

	# Pour préparer la géneration de la prochaine Generation
	def generateNewGenomes(self):
		print("IA: ----- Generation of new genomes --------")

		#Trouvons le meilleur genome de la génération, s'il y en a un
		bestGen = (-1, -1) #(numéro genome, resultat)
		bestFound = False

		for i in range(NBR_GENOME):
			if i == 0:
				bestGen = (i, self.genomesResult[i])

			# Premier meilleur
			elif not bestFound and self.genomesResult[i] > self.genomesResult[i - 1]:
				bestGen = (i, self.genomesResult[i])
				bestFound = True

			# Les suivant meilleurs
			elif bestFound and self.genomesResult[i] > bestGen[1]:
				bestGen = (i, self.genomesResult[i])
				bestFound = True

			#print("IA: Debug algo: ", self.genomesResult[i])

		#Aucun génome meilleur que les autres, on change pas les seuils
		if not bestFound:
			print("IA: NO BEST GENOME THIS GENERATION")
		else: # On génere des nouveaux genomes a partir du meilleur, s'i  existe
			print("IA: Genome ", bestGen[0], " best with ", bestGen[1], " pts.")
			print("IA: Best genome: ", self.genomes[bestGen[0]])

			self.gradDescent += 1

			tmpBounds = BOUNDS_SPREAD - (self.gradDescent / self.descentMultiple)
			print("IA: tmpBounds=", tmpBounds)

			for i in range(3):
				self.genBounds[i] = (self.genomes[bestGen[0]][i] - tmpBounds, self.genomes[bestGen[0]][i] + tmpBounds)
				print("IA: i=", i, "New generation bounds:", self.genBounds[i])

		# Dans tous les cas on appelle la géneration, nouveaux seuils ou pas
		self.generateGenome()

	# Fonction appelée à chaque tour de boucle, en tps réel
	def useGenome(self):
		resultDist = self.genomes[self.usingGenome][0] * self.dist
		resultHeight = self.genomes[self.usingGenome][1] * self.height
		resultSpeed = self.genomes[self.usingGenome][2] * self.speed

		ttResult = resultSpeed + resultHeight + resultDist

		# Attention, spam rapidement
		#print("Total input of genome " + str(self.usingGenome) + ": " + str(ttResult))

		if ttResult < THRESH and not self.jumpCalled:
			self.jumpCalled = True
			return True # SAUTE
		else:
			return False # Ne saute pas 

	# Appelé par Game() quand on a passé un obstacle
	def nextObstacle(self):
		self.jumpCalled = False
		#print("IA: Ready for next obstacle")

	# Quand on a deja fait 20 descentes
	def updateGradDescent(self):
		if self.gradDescent * self.descentMultiple == BOUNDS_SPREAD:
			self.gradDescent = 0
			self.descentMultiple *= 10

			print("IA: GradDescent / 10")

	# Accesseurs
	def getCurrGenoId(self):
		return self.usingGenome

	def getCurrGeno(self):
		strReturn = ','.join(str(e) for e in self.genomes[self.usingGenome])
		return strReturn

	def getCurrGene(self):
		return self.generated

	def setGenomeResult(self, points):
		self.genomesResult[self.usingGenome] = points
		print("Genome ", self.usingGenome, " set to ", points, " points.")

	def getGradial(self):
		return 1/self.descentMultiple

	def getHighScore(self):
		return self.bestScore

	def closeFile(self):
		self.file.close()
		print("IA: File closed")