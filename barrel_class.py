import pygame
import random

class Barrel(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, screen, screen_height, section_width, section_height):
        super().__init__()
        self.section_width = section_width
        self.section_height = section_height
        self.screen_height = screen_height
        self.image = pygame.Surface((50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, y_pos)
        self.y_change = 0
        self.x_change = 1
        self.pos = 0
        self.count = 0
        self.oil_collision = False
        self.falling = False
        self.check_lad = False
        self.bottom = self.rect
        self.edge_probe = pygame.Rect(self.rect.left, self.rect.bottom + 2, 6, 5)
        self.screen = screen
        self.rolling_off_edge = False  # for platform falling (not ladder-based)


    def draw(self):
        barrel_img = pygame.transform.scale(
            pygame.image.load('images/barrel.png'),
            (int(self.section_width * 2), int(2.7 * self.section_height))
        )
        self.screen.blit(pygame.transform.rotate(barrel_img, 90 * self.pos), self.rect.topleft)
    
    def update(self, plats, oil_drum, fire_trig, row5_top, row4_top, row3_top, row2_top, row1_top):
                # Gravity
        if self.y_change < 8 and not self.rolling_off_edge:
            self.y_change += 2

        # Check platform collision
        on_ground = False
        for plat in plats:
            if self.bottom.colliderect(plat) and abs(self.rect.bottom - plat.top) < self.section_height:
                self.y_change = 0
                self.rolling_off_edge = False
                on_ground = True
                break

        # Determine direction based on row
        if not self.rolling_off_edge:
            if row5_top >= self.rect.bottom:
                self.x_change = 5
            elif row3_top >= self.rect.bottom >= row4_top:
                self.x_change = 5
            elif row1_top >= self.rect.bottom >= row2_top:
                self.x_change = 5
            else:
                self.x_change = -5

        # Edge probe for platform detection
        probe_width = 6
        probe_offset = self.rect.width // 3  # Small offset behind front edge

        if self.x_change > 0:
            # moving right → probe slightly behind the right edge
            edge_x = self.rect.right - probe_offset
        else:
            # moving left → probe slightly behind the left edge
            edge_x = self.rect.left + probe_offset - probe_width

        self.edge_probe = pygame.Rect(edge_x, self.rect.bottom + 1, probe_width, 6)

        # Trigger falling if platform ends
        if not self.rolling_off_edge:
            supported = any(self.edge_probe.colliderect(plat) for plat in plats)
            if not supported:
                self.rolling_off_edge = True
                self.y_change = 4
                self.x_change = 0  # stop horizontal while dropping

        # Move
        self.rect.move_ip(self.x_change, self.y_change)

        # Death below screen
        if self.rect.top > self.screen_height:
            self.kill()
         # Fireball trigger
        if self.rect.colliderect(oil_drum) and not self.oil_collision:
            self.oil_collision = True
            if random.randint(0, 4) == 4:
                fire_trig = True

        # Animation frame update
        if self.count < 6:
            self.count += 1
        else:
            self.count = 0
            if self.x_change > 0:
                self.pos = (self.pos + 1) % 4
            else:
                self.pos = (self.pos - 1) % 4

        return fire_trig

    def check_fall(self, lads):
        already_collided = False
        below = pygame.Rect((self.rect.left, self.rect.top + self.section_height), (self.rect.width, 3))

        for lad in lads:
            if below.colliderect(lad) and not self.falling and not self.check_lad:
                self.check_lad = True
                already_collided = True

                if random.randint(0, 60) == 60:
                    self.falling = True
                    self.y_change = 4

        if not already_collided:
            self.check_lad = False
