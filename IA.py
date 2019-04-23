import pygame
import time
import random
import Player


class IA(Player.Player):
	def __init__(self, ecran, nom, num_joueur, speed):
		Player.Player.__init__(self, ecran, nom, num_joueur, speed)
		self.temporisation_mouvement = time.time() - 10


	def mouvement_random(self):
		if time.time() - self.temporisation_mouvement > 0.2:
			aleatoire = random.randrange(111)
			if aleatoire <= 60:
				self.direction = "idle"
			elif aleatoire > 60 and aleatoire <= 80:
				self.direction = "left"
				self.last_direction = "left"
			elif aleatoire > 80 and aleatoire <= 100:
				self.direction = "right"
				self.last_direction = "right"
			if aleatoire > 100 and aleatoire <= 110:
				if self.position not in ["jump_up", "jump_down"]:
					self.position = "jump_up"
			
			self.temporisation_mouvement = time.time()


	def tester_degat(self, joueur):
		for ordre_attaque in self.ordre_attaque_hit_box.values():
			attaque = self.hit_box_attaque_perso[ordre_attaque]
			for i in attaque:
				x, y, w, h = i
				hauteur = self.ecran.get_rect().width
				x = int(x * (hauteur * 2 ) / 448) + self.rect_image.left 
				y = int(y * (hauteur * 2 ) / 448) + self.rect_image.top 

				w = int(w * (hauteur * 2 ) / 448) 
				h = int(h * (hauteur * 2 ) / 448)
				n_attaque_hit_box = pygame.Rect(x, y, w, h)

				for hit_box in joueur.hit_box_active:
					n_hit_box = pygame.Rect(hit_box[0], hit_box[1], hit_box[2], hit_box[3])

					if n_attaque_hit_box.colliderect(n_hit_box):
						self.attaque_touche = ordre_attaque
						return True


	def tester_toucher(self, joueur):
		if joueur.attaque_hit_box:
			for attaque in joueur.attaque_hit_box:
				n_attaque_hit_box = pygame.Rect(attaque[0], attaque[1], attaque[2], attaque[3])

				for hit_box in self.hit_box_active:
					n_hit_box = pygame.Rect(hit_box[0], hit_box[1], hit_box[2], hit_box[3])

					if n_hit_box.colliderect(n_attaque_hit_box):
						return True


	def intercepter_input(self, joueur):
		if joueur.premiere_attaque:
			if joueur.action:
				if self.tester_toucher(joueur):
					if random.randrange(100) < 50:					
						if joueur.position == "idle":
							if joueur.action == "h_punch":
								self.action = "blocking"
							elif joueur.action == "l_kick":
								self.action = "blocking"
						elif joueur.position == "crouch" and self.position not in ["jump_up", "jump_down"]:
							if joueur.action == "h_punch":
								self.position = "crouch"
								self.action = "blocking"
							elif joueur.action == "l_kick":
								self.position = "crouch"
								self.action = "blocking"
			elif self.tester_degat(joueur):
				if random.randrange(1000) < 50:
					self.action = list(self.ordre_attaque_hit_box.keys())[list(self.ordre_attaque_hit_box.values()).index(self.attaque_touche)][2:]
					self.demander_attaque(self.action)
			else:
				self.action = None

