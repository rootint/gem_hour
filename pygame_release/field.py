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
        self.all_sprites = pygame.sprite.Group()
        self.colors = {
            0: "textures/green.png",
            1: "textures/red.png",
            2: "textures/blue.png",
            3: "textures/purple.png",
            4: "textures/yellow.png",
            5: "textures/white.png",
            -1: "textures/darkblue.png"
        }

    def load_image(self, fullname, colorkey=None):    
        """
            load_image(self, fullname, colorkey=None)
            Used to load images quickly and conveniently.
        """
        image = pygame.image.load(fullname).convert_alpha()
        return image

    def generate_field(self, width, height):
        """
            generate_field(self, width, height)
            Generates a 2 dimension list of types of gems and generates a sprite group.
        """
        self.field = [[random.randint(0, 5) for j in range(width)] for i in range(height)]
        while not self.is_move_available(self.field):
            self.field = [[random.randint(0, 5) for j in range(width)] for i in range(height)]
        for i in range(len(self.field)):
            for j in range(len(self.field[i])):
                gem = pygame.sprite.Sprite(self.all_sprites)
                gem.image = self.load_image(self.colors[self.field[i][j]])
                gem.image = pygame.transform.scale(gem.image, (self.cell_size, self.cell_size - 5))
                gem.rect = gem.image.get_rect()
                gem.rect.x = i * 55 + 5
                gem.rect.y = j * 55 + 60

    def generate_on_columns(self, columns):
        """
            generate_on_columns(self, column)
            Generates a new gem on a specified column and moves everything down.
            After that, creates a new sprite group
        """
        print(columns)
        for i in columns:
            self.field[i[0]][i[1]] = -1
        for i in range(len(self.field)):
            if -1 in self.field[i]:
                amount = self.field[i].count(-1)
                for j in range(len(self.field[i])):
                    if self.field[i][j] == -1:
                        for k in range(j, -1, -1):
                            self.field[i][k] = self.field[i][k - 1] 
                        for k in range(amount):
                            self.field[i][k] = random.randint(0, 5)
        # print(*self.field, sep='\n') # for debug purposes
        self.all_sprites = pygame.sprite.Group()
        for i in range(len(self.field)):
            for j in range(len(self.field[i])):
                gem = pygame.sprite.Sprite(self.all_sprites)
                gem.image = self.load_image(self.colors[self.field[i][j]])
                gem.image = pygame.transform.scale(gem.image, (self.cell_size, self.cell_size - 5))
                gem.rect = gem.image.get_rect()
                gem.rect.x = i * 55 + 5
                gem.rect.y = j * 55 + 60

    def is_move_available(self, field):
        """
            is_move_available(self, field): boolean
            Checks if any moves are possible on the field.
        """
        for i in range(1, len(field) - 1):
            for j in range(1, len(field[i]) - 1):
                a = []
                b = []
                a.append(field[i - 1][j - 1])
                a.append(field[i - 1][j])
                a.append(field[i - 1][j + 1])
                a.append(field[i][j - 1])
                a.append(field[i][j])                
                a.append(field[i][j + 1])
                a.append(field[i + 1][j - 1])
                a.append(field[i + 1][j])
                a.append(field[i + 1][j + 1])
                for _ in a:
                    b.append(a.count(_))
                if max(b) >= 3:
                    return True
        return False

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
        pass
