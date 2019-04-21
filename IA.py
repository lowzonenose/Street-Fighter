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
			elif aleatoire > 80 and aleatoire <= 100:
				self.direction = "right"
			if aleatoire > 100 and aleatoire <= 110:
				if self.position not in ["jump_up", "jump_down"]:
					self.position = "jump_up"
			
			self.temporisation_mouvement = time.time()


	def intercepter_input(self, joueur):
		"""
		joueur.action
		joueur.position
		"""
		if joueur.action is not None:
			if joueur.position == "idle":
				if joueur.action == "h_punch":
					self.action = "blocking"
				elif joueur.action == "l_kick":
					self.action = "blocking"
			elif joueur.position == "crouch":
				if joueur.action == "h_punch":
					self.position = "crouch"
					self.action = "blocking"
				elif joueur.action == "l_kick":
					self.position = "crouch"
					self.action = "blocking"
			elif joueur.position in ["jump_up", "jump_down"] and self.position not in ["jump_up", "jump_down"]:
				if joueur.action == "h_punch":
					self.action = "blocking"
				elif joueur.action == "l_kick":
					self.action = "blocking"
		else:
			self.action = None

