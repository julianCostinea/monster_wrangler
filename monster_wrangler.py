import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Monster Wrangler")

# Set fps and clock
FPS = 60
clock = pygame.time.Clock()


# Define classes
class Game():
    def __init__(self):
        self.monsters = []

    def update(self):
        pass

    def draw(self):
        pass

    def check_collisions(self):
        pass

    def start_new_round(self):
        pass

    def choose_new_target(self):
        pass

    def pause_game(self):
        pass

    def _reset_game(self):
        pass


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pass

    def update(self):
        pass

    def warp(self):
        pass

    def reset(self):
        pass


class Monster(pygame.sprite.Sprite):
    def __init__(self):
        pass

    def update(self):
        pass

my_player_group = pygame.sprite.Group()
my_player = Player()
my_player_group.add(my_player)

my_monster_group = pygame.sprite.Group()


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the display
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
