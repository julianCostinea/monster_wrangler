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
    def __init__(self, player, monster_group):
        self.score = 0
        self.round_number = 0

        self.round_time = 0
        self.frame_count = 0

        self.player = player
        self.monster_group = monster_group

        self.next_level_sound = pygame.mixer.Sound("next_level.wav")

        self.font = pygame.font.Font("Abrushow.ttf", 24)

        blue_image = pygame.image.load("blue_monster.png")
        green_image = pygame.image.load("green_monster.png")
        purple_image = pygame.image.load("purple_monster.png")
        yellow_image = pygame.image.load("yellow_monster.png")

        self.target_monster_images = [blue_image, green_image, purple_image, yellow_image]

        self.target_monster_type = random.randint(0, 3)
        self.target_monster_image = self.target_monster_images[self.target_monster_type]

        self.target_monster_rect = self.target_monster_image.get_rect()
        self.target_monster_rect.centerx = WINDOW_WIDTH // 2
        self.target_monster_rect.top = 30

    def update(self):
        self.round_time += 1
        self.check_collisions()

    def draw(self):
        WHITE = (255, 255, 255)
        BLUE = (20, 176, 235)
        GREEN = (80, 201, 47)
        PURPLE = (226, 73, 243)
        YELLOW = (243, 157, 20)

        colors = [BLUE, GREEN, PURPLE, YELLOW]

        catch_text = self.font.render("Catch:", True, WHITE)
        catch_rect = catch_text.get_rect()
        catch_rect.center = (WINDOW_WIDTH // 2, 15)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (10, 10)

        lives_text = self.font.render(f"Lives: {self.player.lives}", True, WHITE)
        lives_rect = lives_text.get_rect()
        lives_rect.topleft = (10, 40)

        round_text = self.font.render(f"Round: {self.round_number}", True, WHITE)
        round_rect = round_text.get_rect()
        round_rect.topleft = (10, 70)

        time_text = self.font.render(f"Time: {self.round_time // FPS}", True, WHITE)
        time_rect = time_text.get_rect()
        time_rect.topright = (WINDOW_WIDTH - 10, 10)

        warp_text = self.font.render(f"Warps: {self.player.warps}", True, WHITE)
        warp_rect = warp_text.get_rect()
        warp_rect.topright = (WINDOW_WIDTH - 10, 40)

        # Blit HUD
        display_surface.blit(catch_text, catch_rect)
        display_surface.blit(score_text, score_rect)
        display_surface.blit(lives_text, lives_rect)
        display_surface.blit(round_text, round_rect)
        display_surface.blit(time_text, time_rect)
        display_surface.blit(warp_text, warp_rect)
        display_surface.blit(self.target_monster_image, self.target_monster_rect)

        # Draw target monster
        pygame.draw.rect(display_surface, colors[self.target_monster_type], (WINDOW_WIDTH // 2 - 32, 30, 64, 64), 2)
        pygame.draw.rect(display_surface, colors[self.target_monster_type], (0, 100, WINDOW_WIDTH, WINDOW_HEIGHT - 200),
                         2)

    def check_collisions(self):
        collided_monster = pygame.sprite.spritecollideany(self.player, self.monster_group)
        if collided_monster:
            if collided_monster.type == self.target_monster_type:
                self.score += 100 * self.round_number
                collided_monster.remove(self.monster_group)
                if (self.monster_group):
                    self.player.catch_sound.play()
                    self.choose_new_target()
                else:
                    self.player.reset()
                    self.next_level_sound.play()
                    self.start_new_round()
            else:
                self.player.lives -= 1
                self.player.die_sound.play()
                self.player.reset()
                if self.player.lives <= 0:
                    self.pause_game()
                    self.reset_game()

    def start_new_round(self):
        self.score += 1000 * self.round_number / (1 + self.round_time)

        self.round_time = 0
        self.frame_count = 0
        self.round_number += 1
        self.player.warps += 1

        for monster in self.monster_group:
            self.monster_group.remove(monster)

    def choose_new_target(self):
        pass

    def pause_game(self):
        pass

    def reset_game(self):
        pass


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("knight.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT

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
            self.rect.centerx = WINDOW_WIDTH // 2
            self.rect.bottom = WINDOW_HEIGHT

    def reset(self):
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT)


class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, image, monster_type):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.type = monster_type

        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])
        self.velocity = random.randint(2, 4)

    def update(self):
        self.rect.x += self.dx * self.velocity
        self.rect.y += self.dy * self.velocity

        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.dx *= -1
        if self.rect.top <= 0 or self.rect.bottom >= WINDOW_HEIGHT:
            self.dy *= -1


my_player_group = pygame.sprite.Group()
my_player = Player()
my_player_group.add(my_player)

my_monster_group = pygame.sprite.Group()

my_game = Game(my_player, my_monster_group)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the display
    display_surface.fill((0, 0, 0))

    # Update and draw sprites
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
