import pygame, random, string, sys, time
 
# mania_proto.py
import pygame, random, string, sys, time

# --- Konfigūracija ---
WIDTH, HEIGHT = 640, 480
FPS = 60
TIME_LIMIT = 2.0   # laikas (s) per kuri reikia paspausti raidę
FONT_NAME = None   # None = default font
LETTER_SIZE = 200  # raidės dydis

# --- Inicializacija ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mania prototipas")
clock = pygame.time.Clock()
font_big = pygame.font.Font(FONT_NAME, LETTER_SIZE)
font_med = pygame.font.Font(FONT_NAME, 36)
font_small = pygame.font.Font(FONT_NAME, 20)

# --- Žaidimo kintamieji ---
score = 0
streak = 0
total = 0
current_letter = None
spawn_time = 0.0
message = ""       # "Pataikei!" arba "Nepataikei!"
message_timer = 0.0
MESSAGE_DURATION = 0.5  # sekundžių
running = True

def spawn_letter():
    global current_letter, spawn_time
    Allowed_letters = ["E", "R", "U", "I"] # Galimos raidės (pakeisk kaip nori)
    current_letter = random.choice(Allowed_letters)
    spawn_time = time.time()

def draw_centered_text(surface, text, font, y):
    r = font.render(text, True, (255,255,255))
    rect = r.get_rect(center=(WIDTH//2, y))
    surface.blit(r, rect)

# pirmas spawn
spawn_letter()

while running:
    dt = clock.tick(FPS) / 1000.0
    now = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            # paliest keisciau 'escape' uzdaryti
            if event.key == pygame.K_ESCAPE:
                running = False
                break

            # normalizuojam nuspausta klavisa i raidę (A-Z)
            if event.unicode and event.unicode.isalpha():
                pressed = event.unicode.upper()
                total += 1
                # patikrinam ar pataike per laika
                if current_letter is not None and pressed == current_letter and (now - spawn_time) <= TIME_LIMIT:
                    score += 1
                    streak += 1
                    message = "Hit!"
                    message_timer = now
                    # iš karto spawn nauja raidė
                    spawn_letter()
                else:
                    streak = 0
                    message = "Miss!"
                    message_timer = now
                    # taip pat spawn nauja raidė (tu gali pakeist elgesį)
                    spawn_letter()

    # timeout? jei per TIME_LIMIT praėjo ir dar nepaspausta -> miss
    if current_letter is not None and (now - spawn_time) > TIME_LIMIT:
        total += 1
        streak = 0
        message = "Miss!"
        message_timer = now
        spawn_letter()

    # nupiešimas
    screen.fill((30, 30, 40))

    # raidė centre
    if current_letter:
        letter_surf = font_big.render(current_letter, True, (255,255,255))
        letter_rect = letter_surf.get_rect(center=(WIDTH//2, HEIGHT//2 - 20))
        screen.blit(letter_surf, letter_rect)

    # laikmatis (balkis)
    time_left = max(0.0, TIME_LIMIT - (now - spawn_time))
    bar_w = 300
    bar_h = 18
    bar_x = (WIDTH - bar_w)//2
    bar_y = HEIGHT//2 + 80
    # outline
    pygame.draw.rect(screen, (200,200,200), (bar_x-2, bar_y-2, bar_w+4, bar_h+4), border_radius=4)
    # background
    pygame.draw.rect(screen, (50,50,60), (bar_x, bar_y, bar_w, bar_h), border_radius=4)
    # fill proportionally
    fill_w = int((time_left / TIME_LIMIT) * bar_w)
    pygame.draw.rect(screen, (120,200,120), (bar_x, bar_y, fill_w, bar_h), border_radius=4)

    # HUD: score, streak, accuracy
    accuracy = (score / total * 100) if total > 0 else 0.0
    hud_text = f"Score: {score}   Streak: {streak}   Accuracy: {accuracy:.0f}%"
    draw_centered_text(screen, hud_text, font_med, 40)

    # instrukcija
    instr = f"Press the shown letter within {TIME_LIMIT:.2f} s (ESC to quit)"
    draw_centered_text(screen, instr, font_small, HEIGHT - 30)

    # message (hit/miss)
    if message and (now - message_timer) <= MESSAGE_DURATION:
        color = (100,255,100) if message == "Hit!" else (255,100,100)
        msg_surf = font_med.render(message, True, color)
        msg_rect = msg_surf.get_rect(center=(WIDTH//2, HEIGHT//2 + 40))
        screen.blit(msg_surf, msg_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
