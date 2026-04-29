import pygame
from pygame.math import Vector2
import random
import os
pygame.init()

GREEN = (173, 204, 96)
DARK_GREEN = (43, 51, 24)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

base_path = os.path.dirname(__file__)  # points to Src/
image_path = os.path.join(base_path, "..", "img", "heart.png")

cell_size = 30
numbers_of_cells = 25
OFFSET = 50  # Offset for score display

class Food:
    def __init__(self, snake_body):
        self.position = self.generate_random_pos(snake_body)

    def draw(self):
        food_rect = pygame.Rect(self.position.x * cell_size, 
                                self.position.y * cell_size + OFFSET, 
                                cell_size, cell_size)
        screen.blit(food_surface, food_rect)

    def generate_random_cell(self):
        x = random.randint(0, numbers_of_cells - 1)
        y = random.randint(0, numbers_of_cells - 1)
        return Vector2(x, y)

    def generate_random_pos(self, snake_body):
        position = self.generate_random_cell()
        while position in snake_body:
            position = self.generate_random_cell()
        return position

class Snake:
    def __init__(self):
        self.body = [Vector2(5, 3), Vector2(4, 3), Vector2(3, 3)]
        self.direction = Vector2(1, 0)
        self.add_segment = False

    def draw(self):
        for segment in self.body:
            segment_rect = (segment.x * cell_size, 
                          segment.y * cell_size + OFFSET, 
                          cell_size, cell_size)
            pygame.draw.rect(screen, DARK_GREEN, segment_rect, 0, 7)

    def update(self):
        self.body.insert(0, self.body[0] + self.direction)
        if self.add_segment:
            self.add_segment = False
        else:
            self.body = self.body[:-1]

    def reset(self):
        self.body = [Vector2(5, 3), Vector2(4, 3), Vector2(3, 3)]
        self.direction = Vector2(1, 0)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = "RUNNING"
        self.score = 0
        self.high_score = 0

    def draw(self):
        self.food.draw()
        self.snake.draw()
        self.draw_score()
        
        if self.state == "GAME_OVER":
            self.draw_game_over()

    def update(self):
        if self.state == "RUNNING":
            self.snake.update()
            self.check_collision_with_food()
            self.check_collision_with_edges()
            self.check_collision_with_tail()

    def check_collision_with_food(self):
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.snake.add_segment = True
            self.score += 1

    def check_collision_with_edges(self):
        if self.snake.body[0].x == numbers_of_cells or self.snake.body[0].x == -1:
            self.game_over()
        if self.snake.body[0].y == numbers_of_cells or self.snake.body[0].y == -1:
            self.game_over()

    def check_collision_with_tail(self):
        headless_body = self.snake.body[1:]
        if self.snake.body[0] in headless_body:
            self.game_over()

    def game_over(self):
        self.state = "GAME_OVER"
        if self.score > self.high_score:
            self.high_score = self.score

    def reset(self):
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.score = 0
        self.state = "RUNNING"

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        high_score_text = font.render(f"High Score: {self.high_score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 30))

    def draw_game_over(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((cell_size * numbers_of_cells, cell_size * numbers_of_cells))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, OFFSET))
        
        # Game Over text
        font = pygame.font.Font(None, 74)
        game_over_text = font.render("GAME OVER", True, RED)
        text_rect = game_over_text.get_rect(center=(cell_size * numbers_of_cells // 2, 
                                                    cell_size * numbers_of_cells // 2 + OFFSET))
        screen.blit(game_over_text, text_rect)
        
        # Restart instruction
        font_small = pygame.font.Font(None, 36)
        restart_text = font_small.render("Press SPACE to restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(cell_size * numbers_of_cells // 2, 
                                                      cell_size * numbers_of_cells // 2 + OFFSET + 50))
        screen.blit(restart_text, restart_rect)

# Initialize screen with extra space for score
screen = pygame.display.set_mode((cell_size * numbers_of_cells, 
                                  cell_size * numbers_of_cells + OFFSET))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

game = Game()

# Load and prepare food image
food_surface = pygame.image.load(os.path.abspath(image_path)).convert_alpha()
food_surface = pygame.transform.scale(food_surface, (cell_size, cell_size))
alpha = 0
fade_speed = 5
direction = 1

# Game loop variables
running = True
SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 200)

while running:
    for event in pygame.event.get():
        if event.type == SNAKE_UPDATE:
            game.update()
        
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game.state == "GAME_OVER":
                if event.key == pygame.K_SPACE:
                    game.reset()
            
            if game.state == "RUNNING":
                if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
                    game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
                    game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
                    game.snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
                    game.snake.direction = Vector2(1, 0)

    # Update heart alpha for pulsing effect
    alpha += fade_speed * direction
    if alpha >= 255:
        alpha = 255
        direction = -1
    elif alpha <= 0:
        alpha = 0
        direction = 1
    food_surface.set_alpha(alpha)

    # Draw everything
    screen.fill(GREEN)
    game.draw()
    pygame.display.update()
    clock.tick(60)

pygame.quit()