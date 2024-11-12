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
        super().__init__()
        self.image = pygame.image.load("knight.png")
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT)

        self.lives = 3
        self.warps = 2
        self.velocity = 8

        self.catch_sound = pygame.mixer.Sound("catch.wav")
        self.die_sound = pygame.mixer.Sound("die.wav")
        self.warp_sound = pygame.mixer.Sound("warp.wav")

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.velocity
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN] and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.y += self.velocity

    def warp(self):
        if self.warps > 0:
            self.warps -= 1
            self.warp_sound.play()
            self.rect.center = WINDOW_HEIGHT

    def reset(self):
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT)


class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, image, monster_type):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.type = monster_type

    def update(self):
        pass


my_player_group = pygame.sprite.Group()
my_player = Player()
my_player_group.add(my_player)

my_monster_group = pygame.sprite.Group()

my_game = Game()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the display
    display_surface.fill((0, 0, 0))

    #Update and draw sprites
    my_player_group.update()
    my_player_group.draw(display_surface)
    my_monster_group.update()
    my_monster_group.draw(display_surface)
    my_game.update()
    my_game.draw()

    # Update the display
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
