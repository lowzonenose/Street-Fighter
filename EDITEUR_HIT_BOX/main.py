import pygame
import Editeur


def main():
	pygame.init()
	ecran = pygame.display.set_mode((800,800))
	pygame.display.set_caption("Editeur de hit box")

	editeur = Editeur.Editeur()
	

	continuer = True
	while continuer:
		ecran.fill((255,255,255))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				continuer = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					editeur.console()
				elif event.key == pygame.K_SPACE:
					editeur.ouvrir_image()
				elif event.key == pygame.K_KP0:
					editeur.save_ficher()

			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					editeur.mouse_start = event.pos
					editeur.mouse_pressed = True

				if event.button == 3:
					editeur.save_rect()

					

			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					editeur.mouse_pressed = False

					

		if editeur.image_ouverte:
			editeur.draw_image(ecran)
		for rect in editeur.hit_box:
			pygame.draw.rect(ecran, (0, 0, 255), rect, 5)

		if editeur.mouse_pressed:
			editeur.cree_rect(ecran)
		
			

		pygame.display.flip()

if __name__ == '__main__':
	main()
