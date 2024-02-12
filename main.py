import pygame
import sys
import random
import welcome

# Initialize Flappy Meat
pygame.init()

# Screen
FPS = 60
WHITE = [255, 255, 255]
RED = [255, 0, 0]
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

# Draw Display
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Meat")
clock = pygame.time.Clock()

# Constants
gravity = 0.5
jump_height = 7
fire_width = 150
fire_gap = 200
player_score = 0
angle = 0

# Messages
font = pygame.font.Font('freesansbold.ttf', 32)
score = font.render("SCORE", True, WHITE)
font2 = pygame.font.Font('freesansbold.ttf', 75)
youLose = font2.render("YOU LOSE!", True, RED)
tryAgain = font.render("Press Space to Try Again!", True, WHITE)

# Images
top_fire_img = pygame.image.load("game_images/fire2.png").convert_alpha()

# Masks
top_fire_mask = pygame.mask.from_surface(top_fire_img)


class Meat:
    def __init__(self):
        self.image = pygame.image.load("game_images/my_meat1.png").convert_alpha()
        self.resized = pygame.transform.scale(self.image, (120, 120)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.resized)
        self.rect = self.resized.get_rect()
        self.x = 200
        self.y = 100
        self.velocity = 0.5

    def jump(self):
        self.velocity = -jump_height
        return True

    def update(self):
        self.velocity += gravity
        self.y += self.velocity


class Fire:
    def __init__(self):
        self.x = SCREEN_WIDTH + 50
        self.height = random.randint(80, 300)
        self.y = SCREEN_HEIGHT - self.height + 30
        self.y2 = -35
        self.image = pygame.image.load("game_images/fire1.png").convert_alpha()
        self.resized = pygame.transform.scale(self.image, (fire_width, self.height))
        self.mask = pygame.mask.from_surface(self.resized)
        self.topImage = pygame.image.load("game_images/fire2.png").convert_alpha()
        self.topResized = pygame.transform.scale(self.topImage, (fire_width, SCREEN_HEIGHT - self.height - 45))
        self.topMask = pygame.mask.from_surface(self.topResized)

    def update(self):
        self.x -= 5


class Background:
    def __init__(self):
        self.image = pygame.image.load("game_images/field.jpeg").convert()
        self.resized = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.x = 0
        self.y = 0


def check_collision(meat, fires):
    for fire in fires:
        if meat.mask.overlap(fire.mask, (fire.x - meat.x, fire.y - meat.y)):
            return True
        if meat.mask.overlap(fire.topMask, (fire.x - meat.x, fire.y2 - meat.y)):
            return True


def add_score(meat, fires):
    global player_score
    meat_pos = meat.x + 60
    for fire in fires:
        fire_pos = fire.x + fire_width / 2
        if meat_pos == fire_pos and meat.y < SCREEN_HEIGHT:
            player_score += 1
            return


def draw_images(meat, fires, background):
    display.blit(background.resized, (background.x, background.y))
    display.blit(meat.resized, (meat.x, meat.y))
    display.blit(score, (450, 50))
    points = font.render(f'{player_score}', True, WHITE)
    display.blit(points, (493, 100))

    for fire in fires:
        display.blit(fire.resized, (fire.x, fire.y))
        display.blit(fire.topResized, (fire.x, fire.y2))


def thegame():
    global player_score, gravity
    meat = Meat()
    background = Background()
    fires = []

    interval_counter = 0

    # Plays game audio
    pygame.mixer.music.load("music/game_audio.mp3")
    pygame.mixer.music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    meat.jump()

        meat.update()
        draw_images(meat, fires, background)

        # Fire spawn-rate
        if interval_counter % 60 == 0:
            new_fire = Fire()
            fires.append(new_fire)
            interval_counter = 0
        else:
            pass
        interval_counter += 1

        # Generates where fire will be
        for fire in fires:
            fire.update()
            if fire.height < 200:
                fire.y = SCREEN_HEIGHT - fire.height + 20
            if check_collision(meat, fires):
                meat.velocity += 10
                pygame.mixer.music.load("music/sizzle.mp3")
                pygame.mixer.music.play(0)

        # Draws messages on screen for when user dies
        if meat.y >= SCREEN_HEIGHT:
            display.blit(youLose, (300, 200))
            display.blit(tryAgain, (300, 400))

            # Resets the game if user presses space
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                player_score = 0
                thegame()
                return

        add_score(meat, fires)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    welcome.welcome_screen()
    thegame()
