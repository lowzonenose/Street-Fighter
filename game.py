import pygame
import time
import os

import Player
import IA
import Interface
from setting import setting


def input_player(event, name_player, num_player):
	if event.type == pygame.KEYDOWN:
		if event.key == setting["touche_joueur" + str(num_player)]["right"]:						#DIRECTION
			name_player.direction = "right"
			name_player.last_direction = "right"
		elif event.key == setting["touche_joueur" + str(num_player)]["left"]:
			name_player.direction = "left"
			name_player.last_direction = "left"
			
		if event.key == setting["touche_joueur" + str(num_player)]["down"]:						#POSITION
			if name_player.position not in ["jump_up", "jump_down"]:
				name_player.position = "crouch"
			else: 
				name_player.position = "jump_down"
		elif event.key == setting["touche_joueur" + str(num_player)]["up"]:
			name_player.test_position_up()

		if event.key == setting["touche_joueur" + str(num_player)]["blocking"]:					#ACTION
			name_player.action = "blocking"
		elif event.key == setting["touche_joueur" + str(num_player)]["h_punch"]:					
			name_player.demander_attaque("h_punch")
		elif event.key == setting["touche_joueur" + str(num_player)]["l_kick"]:
			name_player.demander_attaque("l_kick")


		try:
			if event.key == setting["touche_joueur" + str(num_player)]["victory1"]:					#VICTOIRE
				name_player.victory1()
				name_player.action = "victory"
			elif event.key == setting["touche_joueur" + str(num_player)]["victory2"]:
				name_player.victory2()
				name_player.action = "victory"
		except:
			pass

	if event.type == pygame.KEYUP:
		if event.key == setting["touche_joueur" + str(num_player)]["right"] or event.key == setting["touche_joueur" + str(num_player)]["left"]:						#cancel direction
			name_player.direction = "idle"

		if event.key == setting["touche_joueur" + str(num_player)]["victory1"] or event.key == setting["touche_joueur" + str(num_player)]["victory2"]:
			name_player.action = None

		if event.key == setting["touche_joueur" + str(num_player)]["down"]:
			if name_player.position == "crouch":
				name_player.position = "idle"

		if event.key == setting["touche_joueur" + str(num_player)]["blocking"]:
			name_player.action = None



def main():
	pygame.init()
	os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 200)   #position la fenetre a un endroit precis pour l'ouverture
	ecran = pygame.display.set_mode([setting["l_ecran"], int((setting["l_ecran"] * 448) / 1242)])			 #cree l'écran
	pygame.display.set_caption(setting["titre"])			#change le titre de la fenetre

#---------------------------------------------- instanciation onjets ----------------------------------------------------------------------------------------

	
	interface = Interface.Interface(ecran)

#-------------------------------------------------- boucle du jeu --------------------------------------------------------------------------------------------

	continuer = True
	en_jeu_1v1 = False
	en_jeu_vsIA = False
	menu = True
	fin_de_partie = False
	while continuer:
		while menu:
			for event in pygame.event.get():					#recupere les evenements
				if event.type == pygame.QUIT:
					continuer = False
					menu = False

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						menu = False
						en_jeu_vsIA = True

				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1: 
						if interface.rect_play.collidepoint(event.pos):
							menu = False
							en_jeu_1v1 = True
						elif interface.rect_quit.collidepoint(event.pos):
							menu = False
							continuer = False

			interface.menu_principal()
			pygame.display.flip()

		interface = Interface.Interface(ecran)

		if en_jeu_1v1:
			joueur1 = Player.Player(ecran, "ken", 1, setting["speed"], (0,0,255))
			joueur2 = Player.Player(ecran, "cammy", 2, setting["speed"], (255,0,0))
		while en_jeu_1v1:
			for event in pygame.event.get():					#recupere les evenements
				if event.type == pygame.QUIT:
					continuer = False
					en_jeu_1v1 = False

				input_player(event, joueur1, 1)
				input_player(event, joueur2, 2)
					

			joueur1.recup_action_active()													
			joueur2.recup_action_active()	
			
			joueur1.update_hit_box()
			joueur2.update_hit_box()
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
				fin_de_partie = True
				en_jeu_1v1 = False
				time.sleep(2)

											#rafraichi l'écran 
						#limite la boucle a un nombre de fps precis evitant les accelerations


		if en_jeu_vsIA:
			joueur1 = Player.Player(ecran, "ryu", 1, setting["speed"], (0,0,255))
			joueur2 = IA.IA(ecran, "t_hawk", 2, setting["speed"], (255,0,0))
		while en_jeu_vsIA:
			for event in pygame.event.get():					#recupere les evenements
				if event.type == pygame.QUIT:
					continuer = False
					en_jeu_vsIA = False

				input_player(event, joueur1, 1)
			
			joueur2.mouvement_random()
			
			joueur2.recup_action_active()				
			joueur1.recup_action_active()

			joueur1.update_hit_box()
			joueur2.update_hit_box()
			joueur2.intercepter_input(joueur1)
			joueur2.update_hit_box()
			
			joueur1.gerer_degat(joueur2)
			joueur2.gerer_degat(joueur1)

			#joueur1.afficher()
			#joueur2.afficher()

			interface.draw_bg(1)
			interface.barre_de_vie(joueur1, joueur2)
			joueur1.draw()
			joueur2.draw()

			quitter = interface.temps()
			pygame.display.flip()								#rafraichi l'écran 
			pygame.time.Clock().tick(setting["fps"])			#limite la boucle a un nombre de fps precis evitant les accelerations

			if joueur1.vie <= 0 or joueur2.vie <= 0 or quitter:
				fin_de_partie = True
				en_jeu_vsIA = False
				time.sleep(2)

			



		while fin_de_partie:
			for event in pygame.event.get():					#recupere les evenements
				if event.type == pygame.QUIT:
					fin_de_partie = False
					continuer = False

				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1: 
						if interface.rect_menu.collidepoint(event.pos):
							menu = True
							fin_de_partie = False
							
						elif interface.rect_quit.collidepoint(event.pos):
							fin_de_partie = False
							continuer = False
			ecran.fill((0,0,0))

			interface.fin_de_partie2(joueur1, joueur2)
			pygame.display.flip()



if __name__ == '__main__':
	main()
