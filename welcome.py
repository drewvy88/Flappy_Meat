import pygame
import sys

pygame.init()

# Screen
FPS = 60
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

# Constants
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
rebound = 1.5
counter = 0

# Display
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Meat")
clock = pygame.time.Clock()

# Music
pygame.mixer.music.load("music/loading_screen.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)

class PressAnyKey:
    def __init__(self):
        self.size = 32
        self.font = pygame.font.Font('freesansbold.ttf', self.size)
        self.render = self.font.render("press space to start", True, WHITE)
        self.x = 350
        self.y = 400
        self.drop = 0.3

    def update(self):
        self.drop += 0.1
        self.y += self.drop
        if self.y == 403:
            self.drop = -rebound



def welcome_screen():

    pressanykey = PressAnyKey()

    # Sky
    welcome_screen_bg = pygame.image.load("game_images/welcome.png").convert()

    # Resize images
    welcome_screen_bg = pygame.transform.scale(welcome_screen_bg, (SCREEN_WIDTH, 500))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pygame.mixer.music.stop()
                pygame.mixer.music.load("music/game_audio.mp3")
                pygame.mixer.music.play(-1)
                return

        pressanykey.update()

        display.blit(welcome_screen_bg, (0, 0))
        display.blit(pressanykey.render, (pressanykey.x, pressanykey.y))

        pygame.display.flip()
        clock.tick(FPS)
