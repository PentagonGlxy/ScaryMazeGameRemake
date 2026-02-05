import pygame
import sys
import os

# Initialize Pygame and the Mixer (for sound)
pygame.init()
pygame.mixer.init()

# Screen Dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Maze")

# Colors
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)      # Flash Game Cyan
RED = (255, 0, 0)         # Goal
DARK_BLUE = (0, 0, 139)   # Shadow
WHITE = (255, 255, 255)
BUTTON_COLOR = (0, 0, 0)  # Play Button Background

# Player is a Black Pixel
PLAYER_COLOR = BLACK 

# Fonts
title_font = pygame.font.SysFont("Times New Roman", 90, bold=True) 
menu_font = pygame.font.SysFont("Arial", 28, bold=True)
small_font = pygame.font.SysFont("Arial", 18, bold=True)
play_font = pygame.font.SysFont("Verdana", 30, bold=True)

# --- LOAD ASSETS (JUMPSCARE) ---
# Using raw strings (r"...") to handle Windows backslashes correctly

image_path = r"C:\Users\Mar Jose Bagasbas\Desktop\Scary Maze\do not click me!\donotclickthisphoto.jpg"
sound_path = r"C:\Users\Mar Jose Bagasbas\Desktop\Scary Maze\do not click me!\donotclickthissound.mp3"

try:
    # Load Image and scale to fit screen
    scare_img = pygame.image.load(image_path)
    scare_img = pygame.transform.scale(scare_img, (WIDTH, HEIGHT))
except Exception as e:
    print(f"Warning: Could not load image at {image_path}. Error: {e}")
    # Fallback if file not found: A blank white screen
    scare_img = pygame.Surface((WIDTH, HEIGHT))
    scare_img.fill(WHITE)

try:
    # Load Sound
    scare_sound = pygame.mixer.Sound(sound_path)
except Exception as e:
    print(f"Warning: Could not load sound at {sound_path}. Error: {e}")
    scare_sound = None

# Game State
current_level = 0 
game_state = "MENU" 

# --- Level Geometry ---

def get_level_1():
    return {
        "paths": [
            pygame.Rect(250, 100, 250, 500), # Vertical
            pygame.Rect(250, 50, 450, 150),  # Top
        ],
        "start_pos": (375, 550),           
        "goal": pygame.Rect(700, 50, 100, 150)
    }

def get_level_2():
    paths = []
    paths.append(pygame.Rect(50, 50, 750, 100))   # Top
    paths.append(pygame.Rect(50, 50, 120, 250))   # Left Drop
    paths.append(pygame.Rect(50, 200, 700, 100))  # Mid
    paths.append(pygame.Rect(630, 200, 120, 350)) # Right Drop
    paths.append(pygame.Rect(50, 450, 700, 100))  # Bot
    
    return {
        "paths": paths,
        "start_pos": (750, 100),           
        "goal": pygame.Rect(50, 450, 100, 100)
    }

def get_level_3():
    paths = []
    paths.append(pygame.Rect(50, 500, 700, 60))   # Bottom Snake
    paths.append(pygame.Rect(690, 350, 60, 150))  # Right Up
    paths.append(pygame.Rect(100, 350, 650, 60))  # Mid
    paths.append(pygame.Rect(100, 200, 60, 150))  # Left Up
    paths.append(pygame.Rect(100, 200, 330, 60))  # Top to Squeeze
    
    # The Tight Squeeze (Zig Zag)
    paths.append(pygame.Rect(400, 160, 30, 40))
    paths.append(pygame.Rect(370, 160, 60, 25))
    paths.append(pygame.Rect(370, 120, 30, 65))
    paths.append(pygame.Rect(370, 120, 60, 25))
    paths.append(pygame.Rect(400, 80, 30, 65))
    
    return {
        "paths": paths,
        "start_pos": (80, 530),            
        "goal": pygame.Rect(385, 20, 60, 60)
    }

levels = [get_level_1(), get_level_2(), get_level_3()]

# --- Helpers ---

def draw_menu():
    screen.fill(CYAN)
    
    # Title & Shadow
    shadow_surf = title_font.render("The Maze", True, DARK_BLUE)
    screen.blit(shadow_surf, (WIDTH//2 - shadow_surf.get_width()//2 + 5, 65))
    
    title_surf = title_font.render("The Maze", True, (0, 0, 100)) 
    screen.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 60))
    
    # Version
    ver = small_font.render("v 1.1", True, BLACK)
    screen.blit(ver, (WIDTH//2 + 180, 130))
    
    # Instructions
    lines = [
        "Test your skills!",
        "Try to reach the goal without touching the walls",
        "How steady is your hand?",
        "Let's find out! Try and beat all four levels!",
    ]
    y_start = 200
    for line in lines:
        txt = menu_font.render(line, True, BLACK)
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, y_start))
        y_start += 45

    # Note
    note = small_font.render("sound effects will help", True, BLACK)
    screen.blit(note, (WIDTH//2 - note.get_width()//2, 400))

    # Play Button
    button_rect = pygame.Rect(WIDTH//2 - 90, 460, 180, 60)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    play_txt = play_font.render("PLAY", True, WHITE)
    screen.blit(play_txt, (WIDTH//2 - play_txt.get_width()//2, 472))
    
    return button_rect

def draw_level(lvl_idx):
    lvl_data = levels[lvl_idx]
    for rect in lvl_data["paths"]:
        pygame.draw.rect(screen, CYAN, rect)
    pygame.draw.rect(screen, RED, lvl_data["goal"])
    lbl = menu_font.render(f"Level {lvl_idx + 1}", True, WHITE)
    screen.blit(lbl, (WIDTH - 120, HEIGHT - 50))

def check_collision(player_rect, lvl_idx):
    lvl_data = levels[lvl_idx]
    is_safe = False
    
    for rect in lvl_data["paths"]:
        if rect.colliderect(player_rect):
            is_safe = True
            break
            
    if lvl_data["goal"].colliderect(player_rect):
        return "GOAL"
        
    if not is_safe:
        return "WALL"
        
    return "SAFE"

# --- Main Loop ---
running = True
clock = pygame.time.Clock()

while running:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if game_state == "MENU":
            pygame.mouse.set_visible(True)
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_rect = pygame.Rect(WIDTH//2 - 90, 460, 180, 60)
                if button_rect.collidepoint(mouse_pos):
                    game_state = "PLAYING"
                    current_level = 1
                    start_pos = levels[0]["start_pos"]
                    pygame.mouse.set_pos(start_pos)
                    pygame.mouse.set_visible(False) 

    # --- Drawing ---
    
    if game_state == "MENU":
        draw_menu()
        
    elif game_state == "WIN":
        # --- JUMPSCARE STATE ---
        pygame.mouse.set_visible(False)
        
        # Display the Scary Image
        screen.blit(scare_img, (0, 0))
        
        # Allow exiting with ESC key (optional)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    elif game_state == "PLAYING":
        screen.fill(BLACK)
        
        if current_level <= len(levels):
            lvl_idx = current_level - 1
            draw_level(lvl_idx)
            
            player_rect = pygame.Rect(mouse_pos[0]-2, mouse_pos[1]-2, 5, 5)
            pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
            
            status = check_collision(player_rect, lvl_idx)
            
            if status == "WALL":
                # Teleport to current level start
                start_pos = levels[lvl_idx]["start_pos"]
                pygame.mouse.set_pos(start_pos)
                
            elif status == "GOAL":
                if current_level == 3:
                    # LEVEL 3 FINISHED - TRIGGER JUMPSCARE
                    game_state = "WIN"
                    
                    # Play sound immediately
                    if scare_sound:
                        scare_sound.play()
                        
                    # Cursor remains hidden (set_visible(False) is already active)
                else:
                    current_level += 1
                    next_pos = levels[current_level-1]["start_pos"]
                    pygame.mouse.set_pos(next_pos)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()