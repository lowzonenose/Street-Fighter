import pygame


setting = {
	"l_ecran": 1200,
	"titre": "STREET FIGHTER",
	"fps": 120,

	"posX_fond": 0,
	"speed": 3.5,
	"delai_reset_touche": 0.15,
	"vie": 100,


	"touche_joueur2": {
		"right": pygame.K_RIGHT,
		"left": pygame.K_LEFT,
		"up": pygame.K_UP,	
		"down": pygame.K_DOWN,
		"h_punch": pygame.K_KP1,
		"l_kick": pygame.K_KP2,
		"victory1": pygame.K_KP7,
		"victory2": pygame.K_KP8,
	},
	"touche_joueur1": {
		"right": pygame.K_d,
		"left": pygame.K_a,
		"up": pygame.K_w,
		"down": pygame.K_s,
		"h_punch": pygame.K_t,
		"l_kick": pygame.K_y,
		"victory1": pygame.K_g,
		"victory2": pygame.K_h,
	},


}