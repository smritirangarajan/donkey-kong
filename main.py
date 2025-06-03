import os
import random
from bridge_class import Bridge
from ladder_class import Ladder
from barrel_class import Barrel
from flame_class import Flame
from player_class import Player
from hammer_class import Hammer


import pygame

os.environ['SDL_VIDEO_CENTER'] = '1'
pygame.init()
from levels_data import *



timer = pygame.time.Clock()
fps = 60

font = pygame.font.Font('freesansbold.ttf', 30)
font2 = pygame.font.Font('freesansbold.ttf', 15)

pygame.display.set_caption('Classic Donkey Kong Rebuild')

screen = pygame.display.set_mode([window_width, window_height])


counter = 0

score = 0
high_score = 0
lives = 5
bonus = 6000
reset_game = False
first_fireball_trigger = False




barrels = pygame.sprite.Group()
flames = pygame.sprite.Group()
hammers = pygame.sprite.Group()


player = Player(150, window_height-80, section_width, section_height, screen)

hammers_list = levels[active_level]['hammers']
for ham in hammers_list:
    hammers.add(Hammer(*ham, section_width, section_height, player))

barrel_spawn_time = 180
barrel_count = barrel_spawn_time / 2
barrel_time = 180

fireball_trigger = False

#function to draw platforms and ladders
def draw_screen():
    platforms = []
    climbers = []
    ladders_objs = []
    bridge_objs = []

    ladders = levels[active_level]['ladders']
    bridges = levels[active_level]['bridges']

    for ladder in ladders:
        ladders_objs.append(Ladder(*ladder, section_width, section_height, screen))
        if ladder[2] >= 3:
            climbers.append(ladders_objs[-1].body)

    for bridge in bridges:
        bridge_objs.append(Bridge(*bridge, screen, section_width, section_height))
        platforms.append(bridge_objs[-1].top)  
    
    
    
    return platforms, climbers 

def check_climb(lads):
    can_climb = False
    climb_down = False

    under = pygame.rect.Rect((player.rect[0], player.rect[1] + 2 * section_height), (player.rect[2], player.rect[3]) )

    for lad in lads:
        if player.rect.colliderect(lad) and not can_climb:
            can_climb = True
        if under.colliderect(lad):
            climb_down = True

    if (not can_climb and (not climb_down or player.y_change < 0)) or (player.landed and can_climb and player.y_change > 0 and not climb_down):
        player.climbing = False

    return can_climb, climb_down

def check_victory():
    target = levels[active_level]['target']
    target_rect = pygame.rect.Rect((target[0] * section_width, target[1]), (section_width * target[2], 1) )
    return player.bottom.colliderect(target_rect)


def draw_extras():
    #lives, levels, bonus, text
    screen.blit(font.render(f'I•{score}', True, 'white'), (3*section_width, 2*section_height))
    screen.blit(font.render(f'TOP•{high_score}', True, 'white'), (14 * section_width, 2 * section_height))
    screen.blit(font.render(f'[  ][        ][  ]', True, 'white'), (20 * section_width, 4 * section_height))
    screen.blit(font2.render(f'  M      BONUS        L ', True, 'white'), (20 * section_width + 5, 4 * section_height))
    screen.blit(font2.render(f'  {lives}          {bonus}            {active_level + 1}  ', True, 'white'),
                (20 * section_width + 5, 5 * section_height))

    #peach
    draw_peach()
    #stationary barrels
    #donkey kong
    draw_kong()
    #barrels
    draw_barrels()
    #oil_drum
    return draw_oil()

def draw_oil():

    flames_img = pygame.transform.scale(
            pygame.image.load('images/fire.png'),
            (int(section_width * 2.5), int(section_height))
        )
    
    # Increase size and move higher
    x = 4 * section_width
    y = window_height - 5 * section_height  # moved higher

    barrel_width = 2.4 * section_width
    barrel_height = 2.7 * section_height  # made taller

    # Draw main barrel
    oil = pygame.draw.rect(screen, 'blue', [x, y, barrel_width, barrel_height])

    # Lips on top and bottom
    lip_height = 0.15 * section_height
    pygame.draw.rect(screen, 'blue', [x - 0.05 * section_width, y - lip_height, barrel_width + 0.1 * section_width, lip_height])
    pygame.draw.rect(screen, 'blue', [x - 0.05 * section_width, y + barrel_height, barrel_width + 0.1 * section_width, lip_height])

    # Light blue vertical bar
    pipe_w = 0.12 * section_width
    pygame.draw.rect(screen, 'light blue', [x + 0.1 * section_width, y + 0.2 * section_height, pipe_w, 2.3 * section_height])
    # Smaller text, slightly shifted down
    font_size = int(0.9 * section_height)
    oil_font = pygame.font.SysFont("Arial", font_size, bold=True)
    text_surface = oil_font.render("OIL", True, "light blue")
    text_rect = text_surface.get_rect(center=(x + barrel_width / 2, y + barrel_height / 2 + 0.05 * section_height))
    screen.blit(text_surface, text_rect)

    # Flame dots positioned just above the bottom
    flame_y = y + barrel_height - 0.3 * section_height
    for i in range(4):
        cx = x + 0.4 * section_width + i * 0.4 * section_width
        pygame.draw.circle(screen, 'red', (int(cx), int(flame_y)), 3)

    if counter < 15 or 30 < counter < 45:
         screen.blit(flames_img, (x, y - section_height))
    else: 
         screen.blit(pygame.transform.flip(flames_img, True, False),  (x, y-section_height))

    return oil


def draw_barrels():
    barrel_side = pygame.transform.scale(
            pygame.image.load('images/barrel2.png'),
            (int(section_width * 2), int(section_height * 2.5))
    )
    screen.blit(pygame.transform.rotate(barrel_side, 90), (section_width * 1.2, 5.4 * section_height))
    screen.blit(pygame.transform.rotate(barrel_side, 90), (section_width * 2.5, 5.4 * section_height))
    screen.blit(pygame.transform.rotate(barrel_side, 90), (section_width * 1.2, 7.7 * section_height))
    screen.blit(pygame.transform.rotate(barrel_side, 90), (section_width * 2.5, 7.7 * section_height))

def draw_peach():
    peach1 = pygame.transform.scale(
            pygame.image.load('images/peach1.png'),
            (int(section_width * 2), int(section_height * 3)))
    peach2 = pygame.transform.scale(
            pygame.image.load('images/peach2.png'),
            (int(section_width * 2), int(section_height * 3)))
    if(barrel_count > barrel_spawn_time /2):
        screen.blit(peach1, (10*section_width, row6_y - 6*section_height))
    else:
        screen.blit(peach2, (10*section_width, row6_y - 6*section_height))

def draw_kong():
    dk1 = pygame.transform.scale(
            pygame.image.load('images/dk1.png'),
            (int(section_width * 5), int(section_height * 5)))
    dk2 = pygame.transform.scale(
            pygame.image.load('images/dk2.png'),
            (int(section_width * 5), int(section_height * 5)))
    dk3 = pygame.transform.scale(
            pygame.image.load('images/dk3.png'),
            (int(section_width * 5), int(section_height * 5)))
    
    barrel_img = pygame.transform.scale(
            pygame.image.load('images/barrel.png'),
            (int(section_width * 2), int(2.7 * section_height))
        )
    phase_time = barrel_time // 4
    if barrel_spawn_time - barrel_count > 3 * phase_time:
        dk_img = dk2
    elif barrel_spawn_time - barrel_count > 2 * phase_time:
        dk_img = dk1
    elif barrel_spawn_time - barrel_count > phase_time:
        dk_img = dk3
    else:
        dk_img = pygame.transform.flip(dk1, True, False)
        screen.blit(barrel_img, (180,140))
    
    screen.blit(dk_img, (3.5* section_width, row6_y - 5.5 * section_height))

run = True

def barrel_collide(reset):
    for brl in barrels:
        if brl.rect.colliderect(player.hitbox):
            reset = True

    return reset
def reset():
    global player, barrel, flames, hammers, first_fireball_trigger, victory, lives, bonus

    pygame.time.delay(1000)

    # Clear all sprite groups
    barrels.empty()
    flames.empty()
    hammers.empty()

    # Reduce life and reset bonus
    lives -= 1
    bonus = 6000

    # Recreate player FIRST
    player.kill()
    player = Player(150, window_height - 80, section_width, section_height, screen)

    # Now recreate hammers with new player reference
    for h in hammers_list:
        hammers.add(Hammer(*h, section_width, section_height, player))

    # Reset flags
    first_fireball_trigger = False
    victory = False


while run:
    screen.fill('black')
    timer.tick(fps)
    if(counter < 60):
        counter += 1
    else:
        counter = 0
        if bonus > 0:
            bonus -= 100

    #draw platforms and ladders on the screen
    plats, lads = draw_screen()
    
    oil_drum = draw_extras()

    if barrel_count < barrel_spawn_time: 
        barrel_count += 1
    else:
        barrel_count = random.randint(0,120)
        barrel_time = barrel_spawn_time - barrel_count
        barrel = Barrel(200, 140, screen, screen_height, section_width, section_height)
        barrels.add(barrel)

        if not first_fireball_trigger:
           flame = Flame(5*section_width, window_height - 4*section_height, section_width, section_height, screen_height)
           flames.add(flame)
           fireball_trigger = False
    
    for barrel in barrels:
        barrel.draw()
        barrel.check_fall(lads)
        fireball_trigger = barrel.update(plats, oil_drum, fireball_trigger,row5_top, row4_top, row3_top, row2_top, row1_top)

        if(barrel.rect.colliderect(player.hammer_box) and player.hammer):
            barrel.kill()
            score += 500
    
    if fireball_trigger:
        flame = Flame(5*section_width, window_height - 4*section_height, section_width, section_height, screen_height)
        flames.add(flame)
        fireball_trigger = False

    for flame in flames:
        flame.check_climb(lads, row6_y, row5_y, row4_y, row3_y, row2_y)
        if flame.rect.colliderect(player.hitbox):
            reset_game = True

    flames.draw(screen)
    flames.update(plats)
    player.update(plats)
    player.draw()
    for ham in hammers:
        ham.draw(screen)

    reset_game = barrel_collide(reset_game )

    if(reset_game):
        if(lives > 0):
            reset()
            reset_game = False
        else:
            run = False

    victory = check_victory()
    climb, down = check_climb(lads)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and not player.climbing:
                player.x_change = 1
                player.dir = 1
            if event.key == pygame.K_LEFT and not player.climbing:
                player.x_change = -1
                player.dir = -1
            if event.key == pygame.K_SPACE and player.landed:
                player.landed = False
                player.y_change = -3
            if event.key == pygame.K_UP:
                if climb:
                    player.y_change = -2
                    player.x_change = 0
                    player.climbing = True
            if event.key == pygame.K_DOWN:
                if down:
                    player.y_change = 2
                    player.x_change = 0
                    player.climbing = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and not player.climbing:
                player.x_change = 0
            if event.key == pygame.K_LEFT and not player.climbing:
                player.x_change = 0
            if event.key == pygame.K_UP:
                if climb:
                    player.y_change = 0
                if player.climbing and player.landed:
                    player.climbing = False
            if event.key == pygame.K_DOWN:
                if down:
                    player.y_change = 0
                if player.climbing and player.landed:
                    player.climbing = False
                    

    if victory:
        screen.blit(font.render('VICTORY!', True, 'white'), (window_width/2, width_height/2))
        reset_game = True
        lives += 1

        score += bonus

        if score > high_score:
            high_score = score

    score = 0
    pygame.display.flip()

pygame.quit()