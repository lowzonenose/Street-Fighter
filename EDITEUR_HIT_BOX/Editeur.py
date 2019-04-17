import pygame
import json

class Editeur:
	def __init__(self):
		self.direction = "ryu/ryu_right"
		self.path = "../image/" + self.direction + "/"
		self.save_path = "../hit_box" + self.direction + "/"
		self.image_ouverte = False
		self.taille = 7
		self.mouse_start = (0, 0)
		self.mouse_pressed = False
		self.hit_box = []
		self.nom_image = "image"


	def console(self):
		console = " "
		while console != "":
			console = input(">>> ")
			if console == "path":
				self.changer_path()
			elif console == "image":
				self.ouvrir_image()
			elif console == "taille":
				self.demander_taille()
			elif console == "clean":
				self.hit_box = []
			elif console == "save":
				self.save_ficher()
			elif console == "load":
				self.load_fichier()


	def changer_path(self):
		self.path = input("chemin vers vos images: ")


	def augmenter_taille_image(self):
		rect_image = self.image.get_rect()
		self.image = pygame.transform.scale(self.image, (int(rect_image.width * self.taille), int(rect_image.height * self.taille)))


	def ouvrir_image(self):
		self.nom_image = input("Image a ouvrir: ")
		try:
			self.image = pygame.image.load(self.path + self.nom_image + ".png")
			self.image_ouverte = True
			self.augmenter_taille_image()
		except:
			pass


	def demander_taille(self):
		try:
			self.taille = int(input("Multiplier la taille de l'image par : "))
			if self.image_ouverte:
				self.augmenter_taille_image()
		except:
			pass


	def draw_image(self, ecran):
		ecran.blit(self.image, (0,0))


	def cree_rect(self, ecran):
		pos_souris =  pygame.mouse.get_pos()
		self.Rect = (self.mouse_start[0], self.mouse_start[1], pos_souris[0] - self.mouse_start[0], pos_souris[1] - self.mouse_start[1])
		pygame.draw.rect(ecran, (0, 0, 0), self.Rect, 5)


	def save_rect(self):
		try:
			self.hit_box.append(self.Rect)
		except:
			pass


	def save_ficher(self):
		for i in range(len(self.hit_box)):
			x, y, w, h = self.hit_box[i]
			x = int(x / self.taille)
			y = int(y / self.taille)
			w = int(w / self.taille)
			h = int(h / self.taille)
			self.hit_box[i] = (x, y, w, h)

		with open(self.save_path + self.nom_image + ".json", "w") as write_file:
			json.dump(self.hit_box, write_file)


	def load_fichier(self):
		with open(self.save_path + self.nom_image + ".json", "r") as read_file:
			self.hit_box = json.load(read_file)
