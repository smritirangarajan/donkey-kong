import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, section_width, section_height, screen):
        pygame.sprite.Sprite.__init__(self)
        self.section_width = section_width
        self.section_height = section_height
        self.screen = screen 
        self.standing = pygame.transform.scale(
            pygame.image.load('images/standing.png'),
            (int(section_width * 2), int(section_height * 2.5))
        )
        self.jumping = pygame.transform.scale(
            pygame.image.load('images/jumping.png'),
            (int(section_width * 2), int(section_height * 2.5))
        )
        self.running = pygame.transform.scale(
            pygame.image.load('images/running.png'),
            (int(section_width * 2), int(section_height * 2.5))
        )
        self.climbing1 = pygame.transform.scale(
            pygame.image.load('images/climbing1.png'),
            (int(section_width * 2), int(section_height * 2.5))
        )
        self.climbing2 = pygame.transform.scale(
            pygame.image.load('images/climbing2.png'),
            (int(section_width * 2), int(section_height * 2.5))
        )
        self.hammer_stand = pygame.transform.scale(
            pygame.image.load('images/hammer_stand.png'),
            (int(section_width * 2.5), int(section_height * 2.5))
        )
        self.hammer_jump = pygame.transform.scale(
            pygame.image.load('images/hammer_jump.png'),
            (int(section_width * 2.5), int(section_height * 2.5))
        )

        self.hammer_overhead = pygame.transform.scale(
            pygame.image.load('images/hammer_overhead.png'),
            (int(section_width * 2.5), int(section_height * 3.5))
        )
        self.y_change = 0
        self.x_speed = 6
        self.x_change = 0
        self.landed = False
        self.pos = 1
        self.dir = 1
        self.count = 0
        self.climbing = False
        self.image = self.standing
        self.hammer = False
        self.max_hammer = 450
        self.hammer_len = self.max_hammer
        self.hammer_pos = 1
        self.rect = self.image.get_rect()
        self.hitbox = self.rect
        self.hammer_box = self.rect
        self.rect.center = (x_pos, y_pos)
        self.bottom = pygame.rect.Rect(self.rect.left, self.rect.bottom-20, self.rect.width,20)

         
    
    def update(self, plats):
        self.landed = False
        for i in range(len(plats)):
            if self.bottom.colliderect(plats[i]):
                self.landed = True
                if not self.climbing:
                    self.rect.centery = plats[i].top - self.rect.height / 2 + 1


        if not self.landed and not self.climbing:
            self.y_change += 0.5
        self.rect.move_ip(self.x_change * self.x_speed, self.y_change)
        self.bottom = pygame.rect.Rect(self.rect.left, self.rect.bottom-20, self.rect.width,20)
        if self.x_change != 0 or (self.climbing and self.y_change != 0):
            if self.count < 3:
                self.count += 1
            else:
                self.count = 0
                if self.pos == 0:
                    self.pos += 1
                else:
                    self.pos = 0
        else:
            self.pos = 0
        
        if self.hammer:
            self.hammer_len -= 1
            self.hammer_pos = (self.hammer_len // 15) % 2  # Faster and consistent toggle
            if self.hammer_len <= 0:
                self.hammer = False
                self.hammer_len = self.max_hammer

        

    def draw(self):
        if not self.hammer:
            if not self.climbing and self.landed:
                if self.pos == 0:
                    self.image = self.standing
                else:
                    self.image = self.running
            if not self.landed and not self.climbing:
                self.image = self.jumping
            if self.climbing:
                if self.pos == 0:
                    self.image = self.climbing1
                else:
                    self.image = self.climbing2
        else:
            if self.hammer_pos == 0:
                self.image = self.hammer_jump
            else:
                self.image = self.hammer_overhead
        
        if self.dir == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image= self.image
    
        self.calc_hitbox()

        if self.hammer:
            self.screen.blit(self.image, (self.rect.left, self.rect.top - self.section_height))
        else:
            self.screen.blit(self.image, self.rect.topleft)
        

            

    def calc_hitbox(self):
        if not self.hammer:
            self.hitbox = pygame.rect.Rect((self.rect[0] + 15, self.rect[1] + 5),(self.rect[2] - 30, self.rect[3] - 10))
        elif self.hammer_pos  == 0:
            if self.dir == 1:
                self.hitbox = pygame.rect.Rect((self.rect[0], self.rect[1] + 5),(self.rect[2] - 30, self.rect[3] - 10))
                self.hammer_box = pygame.rect.Rect((self.hitbox[0] + self.hitbox[2], self.rect[1] + 5),(self.hitbox[2 ], self.rect[3] - 10))
            else:
                self.hitbox = pygame.rect.Rect((self.rect[0] + 40, self.rect[1] + 5),(self.rect[2] - 30, self.rect[3] - 10))
                self.hammer_box = pygame.rect.Rect((self.hitbox[0] - self.hitbox[2], self.rect[1] + 5),(self.hitbox[2], self.rect[3] - 10))
        else:
            self.hitbox = pygame.rect.Rect((self.rect[0] + 15, self.rect[1] + 5),(self.rect[2] - 30, self.rect[3] - 10))
            self.hammer_box = pygame.rect.Rect((self.hitbox[0], self.hitbox[1] - self.section_height),(self.hitbox[2], self.section_height))
