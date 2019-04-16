import pygame
import time
from setting import setting

class Interface:
	def __init__(self, ecran):
		self.ecran = ecran
		self.image_map = {}
		self.image_active = None
		self.timer = 120
		self.debut = time.time()
		self.myfont = pygame.font.SysFont("monospace", 60)
		self.label = self.myfont.render(str(self.timer), 1, (0,0,0))
		self.rect = self.label.get_rect()

		self.init_interface()


	def init_interface(self):
		self.charger_images()
		self.agrandir_taille()


	def draw_bg(self, niveau):
		self.ecran.blit(self.image_map["map" + str(niveau)], [setting["posX_fond"], 0])


	def charger_images(self):
		self.image_map["map1"] = pygame.image.load("image/Map/Map1.png")
		self.image_map["map2"] = pygame.image.load("image/Map/Map2.png")
		self.image_map["map3"] = pygame.image.load("image/Map/Map3.png")
		self.image_map["map4"] = pygame.image.load("image/Map/Map4.png")
		self.image_map["map5"] = pygame.image.load("image/Map/Map5.png")
		self.image_map["map6"] = pygame.image.load("image/Map/Map6.png")


	def agrandir_taille(self):
		for key in self.image_map.keys():
			rect_image = self.image_map[key].get_rect()
			self.image_map[key] = pygame.transform.scale(self.image_map[key], [setting["l_ecran"], int((setting["l_ecran"] * 448) / 1242)])


	def temps(self):
		if time.time() - self.debut > 1:
			self.timer -= 1
			self.debut = time.time()
			self.label = self.myfont.render(str(self.timer), 1, (0,0,0))
			self.rect = self.label.get_rect()
		if self.timer < 0:
			return True

		rect_ecran = self.ecran.get_rect()
		self.rect.top = rect_ecran.top
		self.rect.centerx = rect_ecran.centerx
		pygame.draw.rect(self.ecran, (255,255,255), self.rect)
		self.ecran.blit(self.label, self.rect)


	def menu_principal(self):
		self.ecran.fill((0,0,0))
		rect_ecran = self.ecran.get_rect()
		play = self.myfont.render("JOUER", 1, (0,0,0))
		self.rect_play = play.get_rect()
		self.rect_play.x = 200
		self.rect_play.centery = rect_ecran.centery

		quit = self.myfont.render("QUITTER", 1, (0,0,0))
		self.rect_quit = quit.get_rect()
		self.rect_quit.right = rect_ecran.right - 200
		self.rect_quit.centery = rect_ecran.centery

		pygame.draw.rect(self.ecran, (255,255,255), self.rect_play)
		pygame.draw.rect(self.ecran, (255,255,255), self.rect_quit)
		self.ecran.blit(play, self.rect_play)
		self.ecran.blit(quit, self.rect_quit)


	def barre_de_vie(self, joueur1, joueur2):
		rect_ecran = self.ecran.get_rect()
		fond_barre_de_vie = pygame.Rect(50, 20, rect_ecran.centerx * 0.75, 50)
		fond_barre_de_vie2 = pygame.Rect(rect_ecran.width - rect_ecran.centerx * 0.75 - 50, 20, rect_ecran.centerx * 0.75, 50)
		pygame.draw.rect(self.ecran, (0,0,0), fond_barre_de_vie)
		pygame.draw.rect(self.ecran, (0,0,0), fond_barre_de_vie2)

		taille_vie = pygame.Rect(52, 22, (((rect_ecran.centerx * 0.75) * joueur1.vie)/ 1000)-4, 46)
		taille_vie2 = pygame.Rect(rect_ecran.width - rect_ecran.centerx * 0.75 - 48, 22, (((rect_ecran.centerx * 0.75) * joueur2.vie)/ 1000)-4, 46)
		pygame.draw.rect(self.ecran, (0,255,0), taille_vie)
		pygame.draw.rect(self.ecran, (0,255,0), taille_vie2)


	def fin_de_partie2(self, joueur1, joueur2):
		rect_ecran = self.ecran.get_rect()
		menu = self.myfont.render("MENU", 1, (0,0,0))
		self.rect_menu = menu.get_rect()
		self.rect_menu.x = 200
		self.rect_menu.centery = rect_ecran.centery + 100

		quit = self.myfont.render("QUITTER", 1, (0,0,0))
		self.rect_quit = quit.get_rect()
		self.rect_quit.right = rect_ecran.right - 200
		self.rect_quit.centery = rect_ecran.centery + 100

		pygame.draw.rect(self.ecran, (255,255,255), self.rect_menu)
		pygame.draw.rect(self.ecran, (255,255,255), self.rect_quit)
		self.ecran.blit(menu, self.rect_menu)
		self.ecran.blit(quit, self.rect_quit)

		if joueur1.vie > joueur2.vie :
			win = self.myfont.render("JOUEUR 1 WIN", 1, (0,0,255))
		else :
			win = self.myfont.render("JOUEUR 2 WIN", 1, (255,0,0))

		self.rect_win = win.get_rect()
		self.rect_win.centerx = rect_ecran.centerx
		self.rect_win.y = 100
		pygame.draw.rect(self.ecran, (255,255,255), self.rect_win)
		self.ecran.blit(win, self.rect_win) 
							

		

		

		


