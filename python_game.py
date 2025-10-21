import pygame
import random
import os
import math
from enemy import Enemy  # svarbu: importuojam klasę, ne modulį
pygame.init()

# --- Langas ---
screen = pygame.display.set_mode((1040, 940))
pygame.display.set_caption("Archer Game")

# --- Pagalbinė funkcija paveikslėliams ---
def load_image(name):
    if not os.path.exists(name):
        print(f"Klaida: nerastas failas {name}")
        exit()
    return pygame.image.load(name).convert_alpha()

# --- Iškerpame animacijos frame'us iš vieno sheet ---
def load_sprite_sheet(filename, num_frames):
    sheet = load_image(filename)
    sheet_width, sheet_height = sheet.get_size()
    frame_width = sheet_width // num_frames
    frame_height = sheet_height
    frames = []
    for i in range(num_frames):
        rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
        frame = sheet.subsurface(rect)
        frame = pygame.transform.scale(frame, (100, 150))
        frames.append(frame)
    return frames

# --- Sprites ---
background = load_image('walls_floor.png')
archer_attack_frames = load_sprite_sheet("Shot.png", 14)
idle_frames = load_sprite_sheet("idle.png", 9)
run_frames = load_sprite_sheet("run.png", 8)
enemy_image = load_image("Attack_1.png")
enemy_image = pygame.transform.scale(enemy_image, (100, 150))

arrow_img = load_image("arrow.png")
arrow_img = pygame.transform.scale(arrow_img, (40, 16))

# --- Pradiniai duomenys ---
x = 420
y = 320
base_speed = 3
speed = base_speed
clock = pygame.time.Clock()
running = True
attack = False
attack_timer = 0
frame = 0

idle_frame_duration = 120
run_frame_duration = 80
attack_frame_duration = 57

projectiles = []
enemies = []
enemy_spawn_timer = pygame.time.get_ticks()
enemy_spawn_interval = 3000  # kas 3 sekundes

# --- Strėlės klasė ---
class Projectile:
    def __init__(self, x, y, target_pos, image, speed=12):
        self.image = image
        self.x = x
        self.y = y
        tx, ty = target_pos
        dx = tx - x
        dy = ty - y
        dist = math.hypot(dx, dy) or 1.0
        self.vx = (dx / dist) * speed
        self.vy = (dy / dist) * speed
        self.angle = -math.degrees(math.atan2(self.vy, self.vx))

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, surf):
        rotated = pygame.transform.rotate(self.image, self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        surf.blit(rotated, rect.topleft)

    def offscreen(self, width, height):
        return self.x < -100 or self.x > width + 100 or self.y < -100 or self.y > height + 100

# --- Žaidimo ciklas ---
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            mx, my = pygame.mouse.get_pos()
            px = x + 50
            py = y + 75
            projectiles.append(Projectile(px, py, (mx, my), arrow_img, speed=14))
            attack = True
            attack_timer = pygame.time.get_ticks()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
        speed = base_speed * 2
        running_anim = True
    else:
        speed = base_speed
        running_anim = False

    moving = False
    if keys[pygame.K_w]: y -= speed; moving = True
    if keys[pygame.K_s]: y += speed; moving = True
    if keys[pygame.K_a]: x -= speed; moving = True
    if keys[pygame.K_d]: x += speed; moving = True
    if keys[pygame.K_ESCAPE]: running = False

    # Spawn enemy kas kelias sekundes
    now = pygame.time.get_ticks()
    if now - enemy_spawn_timer > enemy_spawn_interval:
        enemies.append(Enemy(x + 50, y + 75, enemy_image))
        enemy_spawn_timer = now

    current_img = idle_frames[0]
    if attack:
        elapsed = pygame.time.get_ticks() - attack_timer
        frame = (elapsed // attack_frame_duration)
        if frame >= len(archer_attack_frames):
            attack = False
            frame = 0
        else:
            current_img = archer_attack_frames[int(frame)]
    elif running_anim and moving:
        run_index = (pygame.time.get_ticks() // run_frame_duration) % len(run_frames)
        current_img = run_frames[int(run_index)]
    else:
        idle_index = (pygame.time.get_ticks() // idle_frame_duration) % len(idle_frames)
        current_img = idle_frames[int(idle_index)]

    for i in range(0, 1040, 41):
        for j in range(0, 940, 41):
            screen.blit(background, (i, j))

    x = max(0, min(x, 1040 - 100))
    y = max(0, min(y, 940 - 150))

    screen.blit(current_img, (x, y))

    for p in projectiles[:]:
        p.update()
        p.draw(screen)
        if p.offscreen(1040, 940):
            projectiles.remove(p)

    for e in enemies:
        e.update()
        e.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
