import pygame
class Ladder:
    def __init__(self, x_pos, y_pos, length, section_width, section_height, screen):
        self.screen = screen
        self.section_width = section_width
        self.section_height = section_height
        self.x_pos = x_pos * self.section_width
        self.y_pos = y_pos
        self.length =length
        self.body = self.draw()
    
    def draw(self):
        line_width = 3
        ladder_color = 'light blue'
        lad_height = 0.6
        for i in range(self.length):
            top_coord = self.y_pos + lad_height*self.section_height * i
            bot_coord= top_coord + lad_height*self.section_height
            mid_coord = (bot_coord - top_coord)/2 + top_coord
            left_coord = self.x_pos
            right_coord = left_coord + self.section_width
            pygame.draw.line(self.screen, ladder_color, (left_coord, top_coord), (left_coord, bot_coord), line_width)
            pygame.draw.line(self.screen, ladder_color, (right_coord, top_coord), (right_coord, bot_coord), line_width)
            pygame.draw.line(self.screen, ladder_color, (left_coord, mid_coord), (right_coord, mid_coord), line_width)
        body = pygame.rect.Rect((self.x_pos, self.y_pos -self.section_height), (self.section_width, lad_height * self.length * self. section_height + self.section_height))
        return body




