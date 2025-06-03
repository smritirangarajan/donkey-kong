import pygame
class Hammer(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, section_width, section_height, player):
        pygame.sprite.Sprite.__init__(self)
        
       
        self.section_width = section_width
        self.section_height = section_height
        hammer = pygame.transform.scale(
            pygame.image.load('images/hammer.png'),
            (int(self.section_width * 2), int(2 * self.section_height))
        )
        self.image = hammer
        self.rect = self.image.get_rect()
        self.rect.top = y_pos
        
        self.rect.left = x_pos * self.section_width
        self.player = player
        self.used = False

    def draw(self, screen):
        if not self.used:
            screen.blit(self.image, (self.rect[0], self.rect[1]))
            if self.rect.colliderect(self. player.hitbox):
                self.kill()
                self.player.hammer = True
                self.player.hammer_len = self.player.max_hammer
                self.used = True
