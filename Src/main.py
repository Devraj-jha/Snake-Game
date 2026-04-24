import pygame
pygame.init()

screen = pygame.display.set_mode((400,400))
# clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,0))
    pygame.display.update()

pygame.quit()