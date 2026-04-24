import pygame
pygame.init()

screen = pygame.display.set_mode((400,400))
clock = pygame.time.Clock()
running = True
x = 100
y = 100
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0,0,0))

    x -= 1
    y -= 1
    pygame.draw.rect(screen, "white", (x, y, 25, 25))

    pygame.display.update()
    clock.tick(60)

pygame.quit()