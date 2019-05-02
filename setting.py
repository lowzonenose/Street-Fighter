import pygame


setting = {
	"l_ecran": 1200,
	"titre": "STREET FIGHTER",
	"fps": 120,

	"speed": 3.5,
	"delai_reset_touche": 0.15,
	"cooldown_attaque": 0.5,
	"degat": 50,
	"vie": 10,


	"touche_joueur2": {
		"pause": pygame.K_KP0,
		"right": pygame.K_RIGHT,
		"left": pygame.K_LEFT,
		"up": pygame.K_UP,	
		"down": pygame.K_DOWN,
		"h_punch": pygame.K_KP1,
		"l_kick": pygame.K_KP2,
		"blocking": pygame.K_KP3,
		"victory1": pygame.K_KP4,
		"victory2": pygame.K_KP5,
	},
	"touche_joueur1": {
		"pause": pygame.K_g,
		"right": pygame.K_d,
		"left": pygame.K_a,
		"up": pygame.K_w,
		"down": pygame.K_s,
		"h_punch": pygame.K_t,
		"l_kick": pygame.K_y,
		"blocking": pygame.K_u,
		"victory1": pygame.K_5,
		"victory2": pygame.K_6,
	},

	"diminution": {
		"ken": 1,
		"ryu": 1,
		"cammy": 1,
		"t_hawk": 1.3,
	}


}