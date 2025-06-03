import pygame

class Bridge:
    def __init__(self, x_pos, y_pos, length, screen, section_width, section_height):
        self.x_pos = x_pos * section_width
        self.y_pos = y_pos
        self.length = length
        
        self.screen = screen
        self.section_width = section_width
        self.section_height = section_height
        self.top = self.draw()
    
    def draw(self):
        line_width = 7
        platform_color = (225, 51, 129)

        for i in range(self.length):
            bot_coord  = self.y_pos + self.section_height
            left_coord = self.x_pos + (self.section_width * i)
            mid_coord = left_coord + (self.section_width * 0.5)
            right_coord = left_coord + self.section_width
            top_coord = self.y_pos

            #drawing the lines for the bridges (have a diagonal pattern)
            pygame.draw.line(self.screen, platform_color, (left_coord, top_coord), (right_coord, top_coord), line_width)
            pygame.draw.line(self.screen, platform_color, (left_coord, bot_coord), (right_coord, bot_coord), line_width)
            pygame.draw.line(self.screen, platform_color, (left_coord, bot_coord), (right_coord, bot_coord), line_width)
            pygame.draw.line(self.screen, platform_color, (left_coord, bot_coord), (mid_coord, top_coord), line_width)
            pygame.draw.line(self.screen, platform_color, (mid_coord, top_coord), (right_coord, bot_coord), line_width)

        #get the top platform surface
        top_line = pygame.rect.Rect((self.x_pos, self.y_pos),(self.length*self.section_width, 10))

        return top_line
