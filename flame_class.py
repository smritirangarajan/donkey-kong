import pygame
import random

class Flame(pygame.sprite.Sprite):
    def __init__(self,x_pos, y_pos, section_width, section_height, screen_height):
        pygame.sprite.Sprite.__init__(self)
        self.fireball = pygame.transform.scale(
            pygame.image.load('images/fireball.png'),
            (int(section_width * 1.5), int(section_height * 2))
        )
        self.fireball2  = pygame.transform.scale(
            pygame.image.load('images/fireball2.png'),
            (int(section_width * 1.5), int(section_height * 2))
        )
        self.image = self.fireball
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, y_pos)
        self.pos = 1
        self.count = 0
        self.x_count = 0
        self.x_change = 2
        self.x_max = 4
        self.y_change = 0
        self.row = 1
        self.check_lad = False
        self.climbing = False
        self.section_width = section_width
        self.section_height = section_height
        self.screen_height = screen_height
    
    def update(self, plats):
        if(self.y_change < 3 and not self.climbing):
            self.y_change += 0.25
        for i in range(len(plats)):
            if self.rect.colliderect(plats[i]):
                self.climbing = False
                self.y_change = -4
        if self.count < 15:
            self.count += 1
        else:
            self.count = 0
            self.pos *= -1

            if self.x_count  < self.x_max:
                self.x_count += 1
            else:
                self.x_count = 0
                if self.x_change > 0:
                    if self.row in [1,3,5]:
                        self.x_max = random.randint(3,6)
                    else:
                        self.x_max = random.randint(6,10)
                else:
                    if self.row in [1,3,5]:
                        self.x_max = random.randint(6,10)
                    else:
                        self.x_max = random.randint(3,6)
                self.x_change *= -1
        if self.pos == 1:
            if(self.x_change > 0):
                self.image = self.fireball
            else:
                self.image = pygame.transform.flip(self.fireball, True, False)
        else:
            if(self.x_change > 0):
                self.image = self.fireball2
            else:
                self.image = pygame.transform.flip(self.fireball2, True, False)
        self.rect.move_ip(self.x_change, self.y_change)

        if self.rect.top > self.screen_height or self.rect.top < 0:
            self.kill()

        
    def check_climb(self, lads, row6_y, row5_y, row4_y, row3_y, row2_y):
        already_collided = False

        for lad in lads:
            if self.rect.colliderect(lad) and not self.climbing and not self.check_lad:
                self.check_lad = True
                already_collided = True
                if random.randint(0,120) == 120:
                    self.climbing = True
                    self.y_change = -4
        
        if not already_collided:
            self.check_lad = False
        
        if self.rect.bottom < row6_y:
            self.row = 6
        
        elif self.rect.bottom < row5_y:
            self.row = 5
        elif self.rect.bottom < row4_y:
            self.row = 4
        elif self.rect.bottom < row3_y:
            self.row = 3
        elif self.rect.bottom < row2_y:
            self.row = 2
        else:
            self.row = 1
    

