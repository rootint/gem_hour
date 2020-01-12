import pygame
import random

class Field:
    def __init__(self, width, height, window_width, window_height, window):
        self.width = width
        self.height = height
        self.window_width = window_width
        self.window_height = window_height
        self.window = window
        self.field = [[0] * width for i in range(height)]
        self.cell_size = 55

    def generate_field(self, width, height):
        """
            generate_field(self, width, height)
            Generates a 2 dimension list of types of gems:
            0 - Square;
            1 - Hexagon;
            2 - Triangle;
            3 - Diamond;
            4 - Octagon;
            5 - Pentagon.
        """
        self.field = [[random.randint(0, 5) for j in range(width)] for i in range(height)]
        while not self.is_move_available(self.field):
            self.field = [[random.randint(0, 5) for j in range(width)] for i in range(height)]


    def generate_on_columns(self, columns):
        """
            generate_on_columns(self, column)
            Generates a new gem on a specified column and moves everything down.
        """
        for i in columns:
            self.field[i[0]][i[1]] = -1
        for i in range(len(self.field)):
            if -1 in self.field[i]:
                amount = self.field[i].count(-1)
                for j in range(len(self.field[i])):
                    if self.field[i][j] == -1:
                        for k in range(j, -1, -1):
                            self.field[i][k] = self.field[i][k - 1] 
                        for k in range(amount - 2):
                            self.field[i][k] = random.randint(0, 5)
        print(*self.field, sep='\n')

    def is_move_available(self, field):
        """
            is_move_available(self, field): boolean
            Checks if any moves are possible on the field.
        """
        return True

    def draw_cells(self):
        """
            draw_cells(self)
            Draws all the visible gems.
        """
        pass

    def remove_cell(self, x, y):
        """
            remove_cell(self, x, y)
            Removes the gem from a specified position,
            moves top ones and draws the animation.
        """
        pass

    def draw_all(self):
        """
            draw_all(self)
            Draws all the visible field.
        """
        # pygame.draw.rect(self.window, (94, 94, 94), 
        #                  (self.window_width // 6, self.window_height // 6,
        #                   self.window_width - 2 * self.window_width // 6, 
        #                   self.window_height - 2 * self.window_width // 6))
        self.draw_cells()
