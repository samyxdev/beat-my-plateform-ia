#-*- encoding: utf-8 -*-
"""

Fichier contenant toutes les constantes de l'application anisi
que des fonction diverses

"""
# ----------- CONSTANTES -------------------------------
# Dossier des images
IMG_FOLDER = "img"

# Booleens d'activation de fonctionnalité -> Debug
DISABLE_COLLISION = False
DISABLE_IA = False

# Tailles de l'applications 
SCREEN_SIZE = (640,560) # Fenetre de l'application (la plus grande taille)
GAME_SIZE = (640,480) # Zone de jeu, qui est enfait la taille du background JUSQU'AU SOL(+ sol, si séparés)
MAXTOP_OBS = 320 # Plafond supérieur Y de géneration des obstacles 
PLR_GROUND = 428 #Position en Y du sol pour le personnage

# Couleurs
BLACK = (0,0,0)
WHITE = (255, 255, 255)
GRAY = (127,127,127)
PURPLE = (255,0,255)

FPS = 120 #Limite initiale des fps
BACK_SPEED = 2 #Vitesse intiale background
OBS_SPEED = 3 #Vitesse initiale obstacles

# Saut
GRAV = 15 #Constante de gravité (saut + ou - ample)
JUMP_SPEED = 0.15
JUMP_HEIGHT = 150

# Accéleration
SEUIL_ACCEL = 200 #Seuil en tour de boucle à dépasser pour augmenter l'accel
ACCEL = 0.1 #Incrémentation des objets accélérants
DECAL_ACCELPLR = 50 #Coefficient diviseur pour l'accéleration du personnage

# Correspond au tours de boucle nécessaire pour monter et descendre 
# Par ex pour 5, une montée, déscente puis montée prend donc 5*3=15 Frames
ANIM_SPEED = 3
JETPACK = 0.5

# Décalage des obstacles (en multiples de GAME_SIZE[0])
DECAL_OBS = 1.5

#Positions du menu
JOUER_POS = (197,214)
JOUER_SIZE = (278,56)

# Constantes pour l'IA
NBR_GENOME = 8 # Nombre de génomes par géneration
INIT_WEIGHTS_BOUNDS = (20, 40) # Seuils de géneration des poids
BOUNDS_SPREAD = 20
THRESH = 3000 # Seuil pour le saut

# Positions image restart 
RESET_YES = (GAME_SIZE[0]/2 - 180, GAME_SIZE[1] - 130)
RESET_NO = (GAME_SIZE[0]/2 + 70, GAME_SIZE[1] - 130)

#----------------------------
#Si boundsMode = 1 alors les conditions sont en infEgal et supEgal
def inter(b1, b2, varTest, boundsMode = 0):
	if varTest + boundsMode > b1 and varTest < b2 + boundsMode:
		return True
	else:
		return False

def checkInRect(pos, size, posTest):
	if inter(pos[0], pos[0] + size[0], posTest[0]) and inter(pos[1], pos[1] + size[1], posTest[1]):
		return True
	else:
		return False

def printFps(font, clock, scr):
	fpsValue = str(int(clock.get_fps()))
	fpsText = font.render(str(int(clock.get_fps())), True, GRAY)
	scr.blit(fpsText, (GAME_SIZE[0] - font.size(fpsValue)[0] - 5, 5))

def writeCsv(file, data):
	strw = ""
	for i in data:
		strw += str(i) + ";"

	file.write(strw + "\r\n")