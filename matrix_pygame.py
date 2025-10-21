import pygame
import sys
import random

# Inicializuojam pygame
pygame.init()

# Nustatom lango dydį
WIDTH, HEIGHT = 800, 600
font_size = 32
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Matrix efektas")

font = pygame.font.Font("NotoSansJP-Thin.ttf", font_size)
katakana = ["ッ", "カ", "ヸ", "あ", "ば", "ざ", "ぱ", "だ", "な", "ま", "や", "ら", "わ"]
collums = WIDTH // font_size
drops = [random.randint(-20, 0) for _ in range (collums)]






# Pagrindinis ciklas
clock = pygame.time.Clock()
running = True
while running:
    keys = pygame.key.get_pressed()
    screen.fill((0, 0, 0)) 
    if keys[pygame.K_ESCAPE]:
        running = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for i in range(collums):
        char = random.choice(katakana)
        char_surface = font.render(char, True, (0, 255, 0))
        x = i * font_size
        y = drops[i] * font_size
        screen.blit(char_surface, (x, y))
        if y> HEIGHT and random.random() > 0.001:
            drops[i] = 0
        else:
            drops[i] += 1



    
    pygame.display.flip()
    clock.tick(35)

pygame.quit()
sys.exit()
