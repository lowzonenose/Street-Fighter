import pygame
import time
import os

import Player
import IA
import Interface
from setting import setting



def main():
	pygame.init()
	os.environ['SDL_VIDEO_WINDOW_POS'] = "{}, {}".format(50, 200)   #position la fenetre a un endroit precis pour l'ouverture
	ecran = pygame.display.set_mode([setting["l_ecran"], int((setting["l_ecran"] * 448) / 1242)])			 #cree l'ecran
	pygame.display.set_caption(setting["titre"])			#change le titre de la fenetre

#---------------------------------------------- instanciation onjets ----------------------------------------------------------------------------------------

	interface = Interface.Interface(ecran)

#-------------------------------------------------- boucle du jeu --------------------------------------------------------------------------------------------

	continuer = True
	menu_principal = True
	menu_choix_mode = False
	selecteur_perso = False
	init_player = False
	mode = False
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
						try:	
							if interface.rect_play.collidepoint(event.pos):
								menu_principal = False
								menu_choix_mode = True
							elif interface.rect_quit.collidepoint(event.pos):
								menu_principal = False
								continuer = False
						except Exception as e:
							print(e)

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
							selecteur_perso = True
							mode = "1v1"
						elif interface.rect_1vsIA.collidepoint(event.pos):
							menu_choix_mode = False
							selecteur_perso = True
							mode = "1vsIA"

			interface.menu_choix_mode()
			pygame.display.flip()


		while selecteur_perso:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					selecteur_perso = False
					continuer = False
					mode = False

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						selecteur_perso = False
						menu_choix_mode = True
						mode = False
						interface = Interface.Interface(ecran)

				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						if interface.rect_joueur1.collidepoint(event.pos):
							interface.choix_actif = "joueur1"
						elif interface.rect_joueur2.collidepoint(event.pos):
							interface.choix_actif = "joueur2"
						elif interface.rect_valider1.collidepoint(event.pos) and interface.choix_perso_joueur[0]:
							interface.validation[0] = True
							interface.choix_actif = "joueur2"
						elif interface.rect_valider2.collidepoint(event.pos) and interface.choix_perso_joueur[1]:
							interface.validation[1] = True
							interface.choix_actif = "joueur1"
						if interface.choix_actif:
							for perso in interface.rect_logo.keys():
								if interface.rect_logo[perso].collidepoint(event.pos) and interface.choix_actif == "joueur1":
									interface.choix_perso_joueur[0] = perso
									if interface.validation[0]:
										interface.validation[0] = False
								elif interface.rect_logo[perso].collidepoint(event.pos) and interface.choix_actif == "joueur2":
									interface.choix_perso_joueur[1] = perso
									if interface.validation[1]:
										interface.validation[1] = False

						try:
							if interface.validation_finale.collidepoint(event.pos):
								selecteur_perso = False
								init_player = True	
						except:
							pass				

			interface.selecteur_perso()
			interface.bouton_selecteur()
			interface.perso_selected()
			interface.bouton_validation()
			interface.check_validation()

			if not interface.init_ia and mode == "1vsIA":
				interface.choix_perso_IA()
				interface.init_ia = True
			pygame.display.flip()


		if init_player:	
			if mode == "1v1":
				joueur1 = Player.Player(ecran, interface.choix_perso_joueur[0], 1, setting["speed"], (0,0,255))
				joueur2 = Player.Player(ecran, interface.choix_perso_joueur[1], 2, setting["speed"], (255,0,0))
				init_player = False
			elif mode == "1vsIA":
				joueur1 = Player.Player(ecran, interface.choix_perso_joueur[0], 1, setting["speed"], (0,0,255))
				joueur2 = IA.IA(ecran, interface.choix_perso_joueur[1], 2, setting["speed"], (255,0,0))
			interface = Interface.Interface(ecran)
			interface.transition((255,255,255))
			init_player = False
			interface.timer_debut_partie(joueur1, joueur2)
			pygame.event.clear()

		while mode:
			for event in pygame.event.get():					
				if event.type == pygame.QUIT:
					continuer = False
					mode = False

				elif event.type == pygame.KEYDOWN:
					if event.key in [setting["touche_joueur1"]["pause"], setting["touche_joueur2"]["pause"]]:
						menu_pause = True
						mode = False

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
				mode = False
				interface.afficher_fin_de_partie(joueur1, joueur2)
				if joueur1.vie > joueur2.vie:
					interface.transition(joueur1.couleur)
				else:
					interface.transition(joueur2.couleur)


		while menu_pause:
			for event in pygame.event.get():					
				if event.type == pygame.QUIT:
					continuer = False
					menu_pause = False

				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						if interface.rect_continuer.collidepoint(event.pos):
							mode = True
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
						interface.transition((0,0,0))

				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1: 
						if interface.rect_menu.collidepoint(event.pos):
							menu_choix_mode = True
							menu_fin_partie = False
							interface.transition((255,255,255))
							
						elif interface.rect_quit.collidepoint(event.pos):
							menu_fin_partie = False
							continuer = False

			interface.fin_de_partie(joueur1, joueur2)
			pygame.display.flip()



if __name__ == '__main__':
	main()
