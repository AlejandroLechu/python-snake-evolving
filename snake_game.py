import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 600
GRID_SIZE = 20
GRID_COUNT = WINDOW_SIZE // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialize window
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Snake Game')

class Snake:
    def __init__(self):
        self.positions = [(WINDOW_SIZE//2, WINDOW_SIZE//2)]
        self.direction = (GRID_SIZE, 0)
        self.grow_pending = False

    def move(self):
        current_head = self.positions[0]
        new_head = (current_head[0] + self.direction[0], current_head[1] + self.direction[1])
        
        # Check for wall collision
        if (new_head[0] < 0 or new_head[0] >= WINDOW_SIZE or
            new_head[1] < 0 or new_head[1] >= WINDOW_SIZE):
            return False

        # Check for self collision
        if new_head in self.positions[:-1]:
            return False

        self.positions.insert(0, new_head)
        if not self.grow_pending:
            self.positions.pop()
        else:
            self.grow_pending = False
        return True

    def grow(self):
        self.grow_pending = True

    def change_direction(self, new_direction):
        # Prevent 180-degree turns
        if (new_direction[0] != -self.direction[0] or 
            new_direction[1] != -self.direction[1]):
            self.direction = new_direction

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        
    def generate_food(self):
        while True:
            food = (random.randint(0, GRID_COUNT-1) * GRID_SIZE,
                   random.randint(0, GRID_COUNT-1) * GRID_SIZE)
            if food not in self.snake.positions:
                return food

    def update(self):
        if not self.snake.move():
            self.game_over = True
            return

        # Check for food collision
        if self.snake.positions[0] == self.food:
            self.snake.grow()
            self.food = self.generate_food()
            self.score += 1

    def draw(self):
        screen.fill(BLACK)
        
        # Draw snake
        for position in self.snake.positions:
            pygame.draw.rect(screen, GREEN, 
                           (position[0], position[1], GRID_SIZE-2, GRID_SIZE-2))

        # Draw food
        pygame.draw.rect(screen, RED,
                        (self.food[0], self.food[1], GRID_SIZE-2, GRID_SIZE-2))

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        if self.game_over:
            game_over_text = font.render('Game Over! Press R to restart', True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2))
            screen.blit(game_over_text, text_rect)

        pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    game = Game()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game.game_over and event.key == pygame.K_r:
                    game = Game()
                elif event.key == pygame.K_UP:
                    game.snake.change_direction((0, -GRID_SIZE))
                elif event.key == pygame.K_DOWN:
                    game.snake.change_direction((0, GRID_SIZE))
                elif event.key == pygame.K_LEFT:
                    game.snake.change_direction((-GRID_SIZE, 0))
                elif event.key == pygame.K_RIGHT:
                    game.snake.change_direction((GRID_SIZE, 0))

        if not game.game_over:
            game.update()
        game.draw()
        clock.tick(10)

if __name__ == '__main__':
    main()