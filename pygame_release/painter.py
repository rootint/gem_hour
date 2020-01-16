import pygame
import random

class Painter:
    def __init__(self, window_width, window_height, window, field, cell_size, score):
        self.window = window
        self.window_height = window_height
        self.window_width = window_width
        self.cell_size = cell_size
        self.field = field
        self.score = score
        self.score_font = pygame.font.Font("font2.ttf", 50)
        self.colors = {
            0: "textures/green.png",
            1: "textures/red.png",
            2: "textures/blue.png",
            3: "textures/purple.png",
            4: "textures/yellow.png",
            5: "textures/white.png",
            -1: "textures/darkblue.png"
        }

    def draw_gem(self, x, y, radius, color):
        # for debug purposes
        img = pygame.image.load(color)
        img = pygame.transform.scale(img, (radius, radius - 5))
        self.window.blit(img, (x, y + 2))

    def draw_field(self, field, radius):
        # for debug purposes
        for i in range(len(field)):
            for j in range(len(field[i])):
                self.draw_gem(5 + radius * j, 
                                 60 + radius * i, 
                                 radius, self.colors[field[j][i]])


    def draw_net(self, width, height, cell_size):
        # for debug purposes
        for i in range(height + 1):
            pygame.draw.line(self.window, (255, 255, 255), 
                             (0 + self.window_width // 6, i * cell_size + self.window_height // 6), 
                             (width * cell_size + self.window_width // 6, 
                              i * cell_size + self.window_height // 6))
        for i in range(width + 1):
            pygame.draw.line(self.window, (255, 255, 255), 
                             (i * cell_size + self.window_width // 6, 0 + self.window_height // 6), 
                             (i * cell_size + self.window_width // 6, 
                              height * cell_size + self.window_height // 6))

    def animate_drop(self, coords, status):
        """
            animate_drop(self, x, y, status)
            Animates gems dropping out of the screen.
        """
        for i in coords:
            print(self.field[i[0]][i[1]])
            self.draw_gem(i[0] * self.cell_size, i[1] * self.cell_size + 50 + status, 
                          self.cell_size, self.colors[self.field[i[0]][i[1]]])
        pass

    def highlight_gems(self, coords):
        """
            highlight_gems(self, coords)
            Highlights the selected gems by placing semi-transparent bubbles on top.
        """ 
        surface = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA, 32)
        for i in coords:
            x, y = i[0] + self.cell_size // 2, i[1] + self.cell_size // 2
            pygame.draw.circle(surface, (0, 0, 0, 64), (x, y), self.cell_size // 2)
        return surface

    def animate_appearance(self, coords, status):
        """
            animate_appearance(self, x, y, status)
            Animates new gems appearing from above.
        """
        pass

    def draw_main_menu(self):
        """
            draw_main_menu(self)
            Draws the main menu interface if the user is in main menu.
        """
        pass

    def draw_score(self, position, amount, tick):
        """
            draw_score(self, position, amount)
            Displays how many points are added to the score in an animated way.
        """
        current_font = pygame.font.Font("font2.ttf", 50 + tick // 2)
        score_added_text = current_font.render('+' + str(amount), 1, (255, 255, 255))
        self.window.blit(score_added_text, (200, 5))

    def draw_game_ui(self, score, time=None, moves=None):
        """
            draw_game_ui(self, score, time=None, moves=None)
            Draws the game UI while in-game.
        """
        score_text = self.score_font.render(str(score), 1, (255, 255, 255))
        self.window.blit(score_text, (15, 5)) 
