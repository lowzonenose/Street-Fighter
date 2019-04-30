import pygame
import time
import os

import Player
import IA
import Interface
from setting import setting



def main():
	pygame.init()
	os.environ['SDL_VIDEO_WINDOW_POS'] = "{}, {}".format(100, 200)   #position la fenetre a un endroit precis pour l'ouverture
	ecran = pygame.display.set_mode([setting["l_ecran"], int((setting["l_ecran"] * 448) / 1242)])			 #cree l'ecran
	pygame.display.set_caption(setting["titre"])			#change le titre de la fenetre

#---------------------------------------------- instanciation onjets ----------------------------------------------------------------------------------------

	interface = Interface.Interface(ecran)

#-------------------------------------------------- boucle du jeu --------------------------------------------------------------------------------------------

	continuer = True
	menu_principal = True
	menu_choix_mode = False
	init_player = False
	en_jeu_1v1 = False
	en_jeu_vsIA = False
	menu_pause = False
	menu_fin_partie = False

	while continuer:
		while menu_principal:
			for event in pygame.event.get():					#recupere les evenements
				if event.type == pygame.QUIT:
					continuer = False
					menu_principal = False

				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1: 
						if interface.rect_play.collidepoint(event.pos):
							menu_principal = False
							menu_choix_mode = True
						elif interface.rect_quit.collidepoint(event.pos):
							menu_principal = False
							continuer = False

			interface.menu_principal()
			pygame.display.flip()


		while menu_choix_mode:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					menu_choix_mode = False
					continuer = False

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						menu_choix_mode = False
						menu_principal = True

				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						if interface.rect_1v1.collidepoint(event.pos):
							menu_choix_mode = False
							en_jeu_1v1 = True
							init_player = True
						elif interface.rect_1vsIA.collidepoint(event.pos):
							menu_choix_mode = False
							en_jeu_vsIA = True
							init_player = True

			interface.menu_choix_mode()
			pygame.display.flip()


		if init_player:	
			interface = Interface.Interface(ecran)
			if en_jeu_1v1:
				joueur1 = Player.Player(ecran, "ken", 1, setting["speed"], (0,0,255))
				joueur2 = Player.Player(ecran, "cammy", 2, setting["speed"], (255,0,0))
				init_player = False
			elif en_jeu_vsIA:
				joueur1 = Player.Player(ecran, "ryu", 1, setting["speed"], (0,0,255))
				joueur2 = IA.IA(ecran, "t_hawk", 2, setting["speed"], (255,0,0))
				init_player = False


		while en_jeu_1v1 or en_jeu_vsIA:
			for event in pygame.event.get():					
				if event.type == pygame.QUIT:
					continuer = False
					en_jeu_1v1 = False
					en_jeu_vsIA = False

				elif event.type == pygame.KEYDOWN:
					if event.key in [setting["touche_joueur1"]["pause"], setting["touche_joueur2"]["pause"]]:
						menu_pause = True
						en_jeu_1v1 = False
						en_jeu_vsIA = False

				joueur1.input_player(event)
				joueur2.input_player(event)

			joueur1.recup_action_active()													
			joueur2.recup_action_active()	
			
			joueur1.update_hit_box(joueur2)
			joueur2.update_hit_box(joueur1)
			joueur1.gerer_degat(joueur2)
			joueur2.gerer_degat(joueur1)

			#joueur1.afficher()
			#joueur2.afficher()

			interface.draw_bg(1)
			interface.barre_de_vie(joueur1, joueur2)
			joueur1.draw()
			joueur2.draw()
			
			quitter = interface.temps()
			pygame.display.flip()
			pygame.time.Clock().tick(setting["fps"])

			if joueur1.vie <= 0 or joueur2.vie <= 0 or quitter:
				menu_fin_partie = True
				en_jeu_1v1 = False
				en_jeu_vsIA = False
				time.sleep(2)


		while menu_pause:
			for event in pygame.event.get():					
				if event.type == pygame.QUIT:
					continuer = False
					menu_pause = False

				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						if interface.rect_continuer.collidepoint(event.pos):
							en_jeu_1v1 = True
							menu_pause = False
							
						elif interface.rect_quitter.collidepoint(event.pos):
							menu_pause = False
							menu_principal = True

			interface.menu_pause()
			pygame.display.flip()


		while menu_fin_partie:
			for event in pygame.event.get():					#recupere les evenements
				if event.type == pygame.QUIT:
					menu_fin_partie = False
					continuer = False

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						menu_fin_partie = False
						menu_principal = True

				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1: 
						if interface.rect_menu.collidepoint(event.pos):
							menu_choix_mode = True
							menu_fin_partie = False
							
						elif interface.rect_quit.collidepoint(event.pos):
							menu_fin_partie = False
							continuer = False

			interface.fin_de_partie(joueur1, joueur2)
			pygame.display.flip()



if __name__ == '__main__':
	main()
