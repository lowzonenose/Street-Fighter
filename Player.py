import pygame
import time
import json
from setting import setting
from hit_box import hit_box

class Player:
	def __init__(self, ecran, nom, num_joueur, speed, couleur):
		self.ecran = ecran
		self.num_joueur = num_joueur
		self.nom = nom
		self.couleur = couleur
		self.image_perso = {}
		self.image_active = None
		self.nom_image_active = None
		self.last_direction = "right"
		self.direction = "idle"
		self.position = "idle"
		self.action = None
		self.debut_direction = None
		self.debut_position = None
		self.debut_action = time.time()
		self.posX = 0
		self.posY = 0
		self.speed = (speed * setting["l_ecran"]) / 1200
		self.hit_box_perso = []
		self.ordre_hit_box = {}
		self.hit_box_active = []
		self.hit_box_attaque_perso = []
		self.ordre_attaque_hit_box = {}
		self.attaque_hit_box = None
		self.vie = setting["vie"]
		self.toucher = False
		self.premiere_attaque = True
		
		self.init_perso()


	def init_perso(self):
		self.charger_images()
		self.charger_hit_box()
		self.convertir_hit_box(self.hit_box_perso)
		self.convertir_hit_box(self.hit_box_attaque_perso)
		self.agrandir_taille()
		self.pos_start(self.num_joueur)


	def afficher(self):								
		print(f"joueur: {self.num_joueur} __ {self.rect_image} __ {self.vie}")


	def draw(self):
		#pygame.draw.rect(self.ecran, (255,255,255), self.rect_image)
		self.ecran.blit(self.image_active, self.rect_image)
		self.afficher_triangle()
		"""for i in self.hit_box_active:
			pygame.draw.rect(self.ecran, (0,0,255), i, 5)	
		if self.attaque_hit_box:
			for i in self.attaque_hit_box:
				pygame.draw.rect(self.ecran, (255,0,0), i, 5)"""
			
		
	def charger_images(self):
		try:							
			self.image_perso["victory1"] = pygame.image.load("image/" + self.nom + "/" + self.nom + "_right/victory1.png")
			self.image_perso["victory2"] = pygame.image.load("image/" + self.nom + "/" + self.nom + "_right/victory2.png")
		except:
			pass

		self.image_perso["r_idle"] = pygame.image.load("image/" + self.nom + "/" + self.nom + "_right/idle.png")
		self.image_perso["r_walking_left"] = pygame.image.load("image/" + self.nom + "/" + self.nom + "_right/walking_left.png")
		self.image_perso["r_walking_right"] = pygame.image.load("image/" + self.nom + "/" + self.nom + "_right/walking_right.png")
		self.image_perso["r_jump_up"] = pygame.image.load("image/" + self.nom + "/" + self.nom + "_right/jump_up.png")
		self.image_perso["r_jump_down"] = pygame.image.load("image/" + self.nom + "/" + self.nom + "_right/jump_down.png")
		self.image_perso["r_crouch"] = pygame.image.load("image/" + self.nom + "/" + self.nom + "_right/crouch.png")
		self.image_perso["r_h_punch"] = pygame.image.load("image/" + self.nom + "/" + self.nom + "_right/h_punch.png")
		self.image_perso["r_jump_punch"] = pygame.image.load("image/" + self.nom + "/" + self.nom + "_right/jump_punch.png")
		self.image_perso["r_crouch_l_punch"] = pygame.image.load("image/" + self.nom + "/" + self.nom + "_right/crouch_l_punch.png")
		self.image_perso["r_l_kick"] = pygame.image.load("image/" + self.nom + "/" + self.nom + "_right/l_kick.png")
		self.image_perso["r_crouch_h_kick"] = pygame.image.load("image/" + self.nom + "/" + self.nom + "_right/crouch_h_kick.png")
		self.image_perso["r_jump_l_kick"] = pygame.image.load("image/" + self.nom + "/" + self.nom + "_right/jump_l_kick.png")
		self.image_perso["r_blocking_up"] = pygame.image.load("image/" + self.nom + "/" + self.nom + "_right/blocking_up.png")
		self.image_perso["r_blocking_crouch"] = pygame.image.load("image/" + self.nom + "/" + self.nom + "_right/blocking_crouch.png")

		self.image_perso["l_idle"] = pygame.image.load("image/" + self.nom + "/" + self.nom + "_left/idle.png")
		self.image_perso["l_walking_left"] = pygame.image.load("image/" + self.nom + "/" + self.nom + "_left/walking_left.png")
		self.image_perso["l_walking_right"] = pygame.image.load("image/" + self.nom + "/" + self.nom + "_left/walking_right.png")
		self.image_perso["l_jump_up"] = pygame.image.load("image/" + self.nom + "/" + self.nom + "_left/jump_up.png")
		self.image_perso["l_jump_down"] = pygame.image.load("image/" + self.nom + "/" + self.nom + "_left/jump_down.png")
		self.image_perso["l_crouch"] = pygame.image.load("image/" + self.nom + "/" + self.nom + "_left/crouch.png")
		self.image_perso["l_h_punch"] = pygame.image.load("image/" + self.nom + "/" + self.nom + "_left/h_punch.png")
		self.image_perso["l_jump_punch"] = pygame.image.load("image/" + self.nom + "/" + self.nom + "_left/jump_punch.png")
		self.image_perso["l_crouch_l_punch"] = pygame.image.load("image/" + self.nom + "/" + self.nom + "_left/crouch_l_punch.png")
		self.image_perso["l_l_kick"] = pygame.image.load("image/" + self.nom + "/" + self.nom + "_left/l_kick.png")
		self.image_perso["l_crouch_h_kick"] = pygame.image.load("image/" + self.nom + "/" + self.nom + "_left/crouch_h_kick.png")
		self.image_perso["l_jump_l_kick"] = pygame.image.load("image/" + self.nom + "/" + self.nom + "_left/jump_l_kick.png")
		self.image_perso["l_blocking_up"] = pygame.image.load("image/" + self.nom + "/" + self.nom + "_left/blocking_up.png")
		self.image_perso["l_blocking_crouch"] = pygame.image.load("image/" + self.nom + "/" + self.nom + "_left/blocking_crouch.png")


	def charger_hit_box(self):
		for key in self.image_perso.keys():
			try:
				if key[0] == "r":
					with open("hit_box/" + self.nom + "/" + self.nom + "_right/" + key[2:] + ".json", "r") as read_file:
						self.hit_box_perso.append(json.load(read_file))
						self.ordre_hit_box[key] = len(self.hit_box_perso) - 1

					with open("hit_box/" + self.nom + "/attaque_" + self.nom + "_right/" + key[2:] + ".json", "r") as read_file:
						self.hit_box_attaque_perso.append(json.load(read_file))
						self.ordre_attaque_hit_box[key] = len(self.hit_box_attaque_perso) - 1

				elif key[0] == "l":
					with open("hit_box/" + self.nom + "/" + self.nom + "_left/" + key[2:] + ".json", "r") as read_file:
						self.hit_box_perso.append(json.load(read_file))
						self.ordre_hit_box[key] = len(self.hit_box_perso) - 1

					with open("hit_box/" + self.nom + "/attaque_" + self.nom + "_left/" + key[2:] + ".json", "r") as read_file:
						self.hit_box_attaque_perso.append(json.load(read_file))
						self.ordre_attaque_hit_box[key] = len(self.hit_box_attaque_perso) - 1
			except:
				pass


	def convertir_hit_box(self, hit_box):
		"""converti les hit_box créé via l'éditeur afin d'avoir longueur et largeur de rectangle positif
			pour pouvoir appliquer  rect.colliderect(rect2)"""
		for i in range(len(hit_box)):
			for j in range(len(hit_box[i])):
				x, y, w, h = hit_box[i][j]
				if w < 0:
					x += w
					w = -w
					
				if h < 0:
					y += h
					h = -h
				hit_box[i][j] = (x, y, w, h)


	def agrandir_taille(self):					#conserve les bonnes proportions    
		hauteur = int((setting["l_ecran"] * 448) / 1242)	
		for key in self.image_perso.keys():
			rect_image = self.image_perso[key].get_rect()
			self.image_perso[key] = pygame.transform.scale(self.image_perso[key], [int((rect_image.width * (hauteur *2 ) / 448) / setting["diminution"][self.nom]), 
																				   int((rect_image.height * (hauteur * 2) / 448) / setting["diminution"][self.nom])])

		for i in range(len(self.hit_box_perso)):
			for j in range(len(self.hit_box_perso[i])):
				x, y, w, h = self.hit_box_perso[i][j]
				x = int((x * (hauteur * 2 ) / 448) / setting["diminution"][self.nom])
				y = int((y * (hauteur * 2 ) / 448) / setting["diminution"][self.nom])

				w = int((w * (hauteur * 2 ) / 448) / setting["diminution"][self.nom])
				h = int((h * (hauteur * 2 ) / 448) / setting["diminution"][self.nom])
				self.hit_box_perso[i][j] = (x, y, w, h)

		for i in range(len(self.hit_box_attaque_perso)):
			for j in range(len(self.hit_box_attaque_perso[i])):
				x, y, w, h = self.hit_box_attaque_perso[i][j]
				x = int(x * (hauteur * 2 ) / 448 / setting["diminution"][self.nom])
				y = int(y * (hauteur * 2 ) / 448 / setting["diminution"][self.nom])

				w = int(w * (hauteur * 2 ) / 448 / setting["diminution"][self.nom])
				h = int(h * (hauteur * 2 ) / 448 / setting["diminution"][self.nom])
				self.hit_box_attaque_perso[i][j] = (x, y, w, h)


	def afficher_triangle(self):
		posX = self.rect_image.centerx 
		posY = self.rect_image.top - 20
		pygame.draw.polygon(self.ecran, self.couleur, [(posX, posY), (posX - 10, posY - 15), (posX + 10, posY - 15)])


	def pos_start(self, joueur):					#initialise les position de chaque joueur en debut de partie
		rect_ecran = self.ecran.get_rect()
		hauteur = int((setting["l_ecran"] * 448) / 1242)
		if joueur == 1:
			self.image_active = self.image_perso["r_idle"]
			self.nom_image_active = "r_idle"
			self.rect_image = self.image_active.get_rect()
			self.rect_image.bottom = rect_ecran.bottom - hauteur * 0.05
			self.rect_image.left = rect_ecran.left + setting["l_ecran"] * 0.35
			self.last_direction = "right"

		elif joueur == 2:
			self.image_active = self.image_perso["l_idle"]
			self.nom_image_active = "l_idle"
			self.rect_image = self.image_active.get_rect()
			self.rect_image.bottom = rect_ecran.bottom - hauteur * 0.05
			self.rect_image.left = rect_ecran.left + setting["l_ecran"] * 0.65
			self.last_direction = "left"
		self.posX = self.rect_image.centerx
		self.posY = self.rect_image.bottom
		self.sol = self.posY


	def update_hit_box(self, joueur):
		hauteur = int((setting["l_ecran"] * 448) / 1242)
		self.hit_box_active = []
		for i in range(len(self.hit_box_perso[self.ordre_hit_box[self.nom_image_active]])):
			x, y, w, h = self.hit_box_perso[self.ordre_hit_box[self.nom_image_active]][i]	
			x += self.rect_image.left
			y += self.rect_image.top
			self.hit_box_active.append((x, y, w, h))

		try:
			self.attaque_hit_box = []
			for i in range(len(self.hit_box_attaque_perso[self.ordre_attaque_hit_box[self.nom_image_active]])):
				x, y, w, h = self.hit_box_attaque_perso[self.ordre_attaque_hit_box[self.nom_image_active]][i]
				x += self.rect_image.left 
				y += self.rect_image.top 
				self.attaque_hit_box.append((x, y, w, h))
		except:
			self.attaque_hit_box = None


	def gerer_degat(self, ennemi):
		if self.premiere_attaque:
			if self.attaque_hit_box:
				for attaque in self.attaque_hit_box:
					n_attaque_hit_box = pygame.Rect(attaque[0], attaque[1], attaque[2], attaque[3])

					for hit_box in ennemi.hit_box_active:
						n_hit_box = pygame.Rect(hit_box[0], hit_box[1], hit_box[2], hit_box[3])

						if n_hit_box.colliderect(n_attaque_hit_box):
							ennemi.toucher = True
							self.premiere_attaque = False

				if ennemi.toucher:
					ennemi.vie -= setting["degat"]
					if ennemi.vie < 0:
						ennemi.vie = 0
					ennemi.toucher = False


	def placer_rect(self):								#recup taille image + placer l'image sur posX et posY
		self.rect_image = self.image_active.get_rect()
		self.rect_image.centerx = self.posX
		self.rect_image.bottom = self.posY


	def test_position_up(self):							#test la position du joueur pour choisir l'usage du jump
		if self.position == "crouch":
			self.position = "idle"
			self.idle()
		elif self.position == "idle":
			self.position = "jump_up"
			self.jump()


	def test_action(self):								# cancel l'action apres le delai dépassé
		if time.time() - self.debut_action < setting["delai_reset_touche"] * 1.5:
			return True
		else:
			self.action = None
			self.premiere_attaque = True
			if self.position == "idle":
				self.idle()
				return False
			elif self.position == "crouch":
				self.crouch()


	def demander_attaque(self, attaque):
		if time.time() - self.debut_action > setting["cooldown_attaque"]:
			self.action = attaque
			self.debut_action = time.time()


	def input_player(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == setting["touche_joueur" + str(self.num_joueur)]["right"]:						#DIRECTION
				self.direction = "right"
				self.last_direction = "right"
			elif event.key == setting["touche_joueur" + str(self.num_joueur)]["left"]:
				self.direction = "left"
				self.last_direction = "left"
				
			if event.key == setting["touche_joueur" + str(self.num_joueur)]["down"]:						#POSITION
				if self.position not in ["jump_up", "jump_down"]:
					self.position = "crouch"
				else: 
					self.position = "jump_down"
			elif event.key == setting["touche_joueur" + str(self.num_joueur)]["up"]:
				self.test_position_up()

			if event.key == setting["touche_joueur" + str(self.num_joueur)]["blocking"]:					#ACTION
				self.action = "blocking"
			elif event.key == setting["touche_joueur" + str(self.num_joueur)]["h_punch"]:					
				self.demander_attaque("h_punch")
			elif event.key == setting["touche_joueur" + str(self.num_joueur)]["l_kick"]:
				self.demander_attaque("l_kick")

			try:
				if event.key == setting["touche_joueur" + str(self.num_joueur)]["victory1"]:					#VICTOIRE
					self.victory1()
					self.action = "victory"
				elif event.key == setting["touche_joueur" + str(self.num_joueur)]["victory2"]:
					self.victory2()
					self.action = "victory"
			except:
				pass

		if event.type == pygame.KEYUP:
			if event.key == setting["touche_joueur" + str(self.num_joueur)]["right"] or event.key == setting["touche_joueur" + str(self.num_joueur)]["left"]:						#cancel direction
				self.direction = "idle"

			if event.key == setting["touche_joueur" + str(self.num_joueur)]["victory1"] or event.key == setting["touche_joueur" + str(self.num_joueur)]["victory2"]:
				self.action = None

			if event.key == setting["touche_joueur" + str(self.num_joueur)]["down"]:
				if self.position == "crouch":
					self.position = "idle"

			if event.key == setting["touche_joueur" + str(self.num_joueur)]["blocking"]:
				self.action = None


	def recup_action_active(self):						#recupere les action du joueur pour choisir les bonnes attaques selon les combos de touches
		if self.direction == "idle" and self.position == "idle" and not self.action:
			self.idle()
			return
		if self.direction == "right":
			self.walking_right()
		elif self.direction == "left":
			self.walking_left()
		if self.position == "crouch":
			self.crouch()
		elif self.position in ["jump_up", "jump_down"]:
			self.jump()
		if self.action == "blocking" and self.position == "idle":
			self.blocking_up()
		elif self.action == "blocking" and self.position == "crouch":
			self.blocking_crouch()
		elif self.action == "h_punch":
			if self.test_action() and self.position == "idle":
				self.h_punch()
			elif self.test_action() and self.position in ["jump_up", "jump_down"]:
				self.jump_punch()
			elif self.test_action() and self.position == "crouch":
				self.crouch_l_punch()
		elif self.action == "l_kick":
			if self.test_action() and self.position == "idle":
				self.l_kick()
			elif self.test_action() and self.position in ["jump_up", "jump_down"]:
				self.jump_l_kick()
			elif self.test_action() and self.position == "crouch":
				self.crouch_h_kick()



#------------------------------------------------------- ACTION DU JOUEUR ----------------------------------------------------------------------------------------------------
	
	def idle(self):	
		if self.last_direction == "right":					
			self.image_active = self.image_perso["r_idle"]
			self.nom_image_active = "r_idle"
		else: 
			self.image_active = self.image_perso["l_idle"]
			self.nom_image_active = "l_idle"
		self.placer_rect()


	def jump(self):
		hauteur = int((setting["l_ecran"] * 448) / 1242)
		if self.position == "jump_up":
			if self.last_direction == "right":	
				self.image_active = self.image_perso["r_jump_up"]
				self.nom_image_active = "r_jump_up"
			else :
				self.image_active = self.image_perso["l_jump_up"]
				self.nom_image_active = "l_jump_up"
			self.placer_rect()
			self.posY -= self.speed
			if self.posY < self.sol - hauteur * 0.4:
				self.position = "jump_down"

		elif self.position == "jump_down":
			if self.last_direction == "right":
				self.image_active = self.image_perso["r_jump_down"]
				self.nom_image_active = "r_jump_down"
			else:
				self.image_active = self.image_perso["l_jump_down"]
				self.nom_image_active = "l_jump_down"
			self.placer_rect()
			self.posY += self.speed
			if self.posY > self.sol:
				self.posY = self.sol 
				self.position = "idle"
				self.idle()


	def crouch(self):
		if self.last_direction == "right":
			self.image_active = self.image_perso["r_crouch"]
			self.nom_image_active = "r_crouch"
		else:
			self.image_active = self.image_perso["l_crouch"]
			self.nom_image_active = "l_crouch"
		self.placer_rect()
		

	def walking_right(self):
		if self.last_direction == "right":
			self.image_active = self.image_perso["r_walking_right"]
			self.nom_image_active = "r_walking_right"
		else:
			self.image_active = self.image_perso["l_walking_right"]
			self.nom_image_active = "l_walking_right"
		self.placer_rect()
		if self.rect_image.right > self.ecran.get_rect().width:
			self.rect_image.right = self.ecran.get_rect().width
		else:
			self.posX += self.speed


	def walking_left(self):
		if self.last_direction == "right":
			self.image_active = self.image_perso["r_walking_left"]
			self.nom_image_active = "r_walking_left"
		else:
			self.image_active = self.image_perso["l_walking_left"]
			self.nom_image_active = "l_walking_left"
		self.placer_rect()
		if self.rect_image.left < 0:
			self.rect_image.left = 0
		else:
			self.posX -= self.speed


	def blocking_up(self):
		if self.last_direction == "right":
			self.image_active = self.image_perso["r_blocking_up"]
			self.nom_image_active = "r_blocking_up"
		else:
			self.image_active = self.image_perso["l_blocking_up"]
			self.nom_image_active = "l_blocking_up"
		self.placer_rect()


	def blocking_crouch(self):
		if self.last_direction == "right":
			self.image_active = self.image_perso["r_blocking_crouch"]
			self.nom_image_active = "r_blocking_crouch"
		else:
			self.image_active = self.image_perso["l_blocking_crouch"]
			self.nom_image_active = "l_blocking_crouch"
		self.placer_rect()


	def l_kick(self):
		if self.last_direction == "right":
			self.image_active = self.image_perso["r_l_kick"]
			self.nom_image_active = "r_l_kick"
		else:
			self.image_active = self.image_perso["l_l_kick"]
			self.nom_image_active = "l_l_kick"
		self.placer_rect()


	def h_punch(self):
		if self.last_direction == "right":
			self.image_active = self.image_perso["r_h_punch"]
			self.nom_image_active = "r_h_punch"
		else:
			self.image_active = self.image_perso["l_h_punch"]
			self.nom_image_active = "l_h_punch"
		self.placer_rect()
	

	def jump_punch(self):
		if self.last_direction == "right":
			self.image_active = self.image_perso["r_jump_punch"]
			self.nom_image_active = "r_jump_punch"
		else:
			self.image_active = self.image_perso["l_jump_punch"]
			self.nom_image_active = "l_jump_punch"
		self.placer_rect()


	def jump_l_kick(self):
		if self.last_direction == "right":
			self.image_active = self.image_perso["r_jump_l_kick"]
			self.nom_image_active = "r_jump_l_kick"
		else:
			self.image_active = self.image_perso["l_jump_l_kick"]
			self.nom_image_active = "l_jump_l_kick"
		self.placer_rect()		


	def crouch_l_punch(self):
		if self.last_direction == "right":
			self.image_active = self.image_perso["r_crouch_l_punch"]
			self.nom_image_active = "r_crouch_l_punch"
		else:
			self.image_active = self.image_perso["l_crouch_l_punch"]
			self.nom_image_active = "l_crouch_l_punch"
		self.placer_rect()


	def crouch_h_kick(self):
		if self.last_direction == "right":
			self.image_active = self.image_perso["r_crouch_h_kick"]
			self.nom_image_active = "r_crouch_h_kick"
		else:
			self.image_active = self.image_perso["l_crouch_h_kick"]
			self.nom_image_active = "l_crouch_h_kick"
		self.placer_rect()


	def victory1(self):
		self.image_active = self.image_perso["victory1"]
		self.placer_rect()


	def victory2(self):
		self.image_active = self.image_perso["victory2"]
		self.placer_rect()
