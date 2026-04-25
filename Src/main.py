import pygame
from pygame.math import Vector2
pygame.init()

GREEN = (173,204,96)
DARK_GREEN = (43, 51, 24)

cell_size = 30
numbers_of_cells = 25 

class Food:
    def __init__(self):
        self.position = Vector2(5,6)

    def draw(self):
        food_rect = pygame.Rect(self.position.x *cell_size,self.position.y * cell_size,cell_size,cell_size)
        screen.blit(food_surface,food_rect)
screen = pygame.display.set_mode((cell_size * numbers_of_cells,cell_size* numbers_of_cells))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

food = Food()
food_surface = pygame.image.load("img/heart.png").convert_alpha()
food_surface = pygame.transform.scale(food_surface, (cell_size, cell_size))
alpha = 0
fade_speed = 5
direction = 1

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    alpha += fade_speed * direction

    if alpha >= 255:
        alpha = 255
        direction = -1

    elif alpha <= 0:
        alpha = 0
        direction = 1

    food_surface.set_alpha(alpha)

    screen.fill(GREEN)

    food.draw()

    pygame.display.update()
    clock.tick(60)

pygame.quit()