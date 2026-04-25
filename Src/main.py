import pygame
from pygame.math import Vector2
import random
pygame.init()

GREEN = (173,204,96)
DARK_GREEN = (43, 51, 24)

cell_size = 30
numbers_of_cells = 25 

class Food:
    def __init__(self ,snake_body):
        self.position = self.generate_random_pos(snake_body)

    def draw(self):
        food_rect = pygame.Rect(self.position.x *cell_size,self.position.y * cell_size,cell_size,cell_size)
        screen.blit(food_surface,food_rect)

    def generate_random_cell(self):
        x  = random.randint(0,24)
        y  = random.randint(0,24)
        return Vector2(x,y)


    def generate_random_pos(self,snake_body): 
      
        position = self.generate_random_cell()
        while position in snake_body:
            position = self.generate_random_cell()
        return position
    

class Snake:


    def __init__(self):
        self.body = [Vector2(5,3),Vector2(4,3),Vector2(3,3)]
        self.direction = Vector2(1,0)
    def draw(self):
        for segment in self.body:
            segment_rect =  (segment.x * cell_size, segment.y * cell_size, cell_size, cell_size)   
            pygame.draw.rect(screen,DARK_GREEN, segment_rect ,0,7)
    
    def update(self):
       self.body = self.body[:-1] 
       self.body.insert(0,self.body[0] + self.direction)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)

    def draw(self):
        self.food.draw()
        self.snake.draw()

    def update(self):
        self.snake.update()
        self.check_collision_with_food()

    def check_collision_with_food(self):
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.generate_random_pos(self.snake.body)

screen = pygame.display.set_mode((cell_size * numbers_of_cells,cell_size* numbers_of_cells))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

game = Game()

food_surface = pygame.image.load("img/heart.png").convert_alpha()
food_surface = pygame.transform.scale(food_surface, (cell_size, cell_size))
alpha = 0
fade_speed = 5
direction = 1

running = True

SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE,200)
while running:
    for event in pygame.event.get():
        if event.type == SNAKE_UPDATE:
            game.update()
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game.snake.direction != Vector2(0,1):
                game.snake.direction = Vector2(0,-1)    
            if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0,-1):
                game.snake.direction = Vector2(0,1)    
            if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1,0):
                game.snake.direction = Vector2(-1,0)    
            if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1,0):
                game.snake.direction = Vector2(1,0)    
            
                

    alpha += fade_speed * direction

    if alpha >= 255:
        alpha = 255
        direction = -1

    elif alpha <= 0:
        alpha = 0
        direction = 1

    food_surface.set_alpha(alpha)

    screen.fill(GREEN)
    game.draw()
    pygame.display.update()
    clock.tick(60)

pygame.quit()