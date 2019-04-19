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
			aleatoire = random.randrange(121)
			if aleatoire <= 40:
				self.direction = "idle"
			elif aleatoire > 40 and aleatoire <= 70:
				self.direction = "left"
			elif aleatoire > 70 and aleatoire <= 100:
				self.direction = "right"
			if aleatoire > 100 and aleatoire <= 120:
				if self.position not in ["jump_up", "jump_down"]:
					self.position = "jump_up"
				if self.position in ["jump_up", "jump_down"]:
					print("bbb")
					self.jump()
			self.temporisation_mouvement = time.time()

