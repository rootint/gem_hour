import pygame
import random
# import numpy

class Painter:
    def __init__(self, window_width, window_height, window):
        self.window = window
        self.window_height = window_height
        self.window_width = window_width
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
        img = pygame.image.load(color)
        img = pygame.transform.scale(img, (radius, radius - 5))
        self.window.blit(img, (x, y + 2))
        # pygame.draw.circle(self.window, color, (x, y), radius // 2 - 2)

    def draw_field(self, field, radius):
        # print(*field, sep='\n1s')
        for i in range(len(field)):
            for j in range(len(field[i])):
                self.draw_gem(5 + radius * j, 
                                 60 + radius * i, 
                                 radius, self.colors[field[j][i]])


    def draw_net(self, width, height, cell_size):
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
        pass

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

    def draw_game_ui(self, score, time=None, moves=None):
        """
            draw_game_ui(self, score, time=None, moves=None)
            Draws the game UI while in-game.
        """
        pygame.draw.rect(self.window, (94, 94, 94), 
                         (0, 0, self.window_width, 60))


class Game:
    def __init__(self, window_width, window_height):
        self.window = pygame.display.set_mode((window_width, window_height))
        self.field = Field(10, 10, window_width, window_height, self.window)
        self.painter = Painter(window_width, window_height, self.window)
        self.dead = False
        self.is_ui_updated = True
        self.is_field_updated = True
        pygame.display.set_caption("Gem Hour")

    def launch(self):
        """
            launch(self)
            Called only once on a level start.
            Initializes the field and launches the tick() function.
        """
        self.field.generate_field(10, 10)
        self.window.fill((47, 47, 47))
        self.tick()

    def tick(self):
        """
            tick(self)
            Contains the main game loop.
        """
        clicked_pos = []
        while not self.dead:
            pygame.time.delay(1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.dead = True
            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pressed()
            if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
                self.dead = True
            if True:  # register mouse movement only on the field itself
                if mouse[0] == 1:
                    clicked_pos.append(pygame.mouse.get_pos())
                else:
                    if len(clicked_pos) > 3:
                        if (self.is_selection_removable(self.analyze_mouse_movement(clicked_pos))):
                            self.field.generate_on_columns(self.analyze_mouse_movement(clicked_pos))
                            self.painter.animate_drop(self.analyze_mouse_movement(clicked_pos), 0)
                            print('success')    
                        else:
                            print('succ')
                    clicked_pos = []

            if True:
                self.draw_all("game") # optimize draw_all feature
                pygame.display.flip()
                self.is_ui_updated = self.is_field_updated = False
            if not self.field.is_move_available(self.field.field):
                self.dead = True

    def draw_all(self, status):
        """
            draw_all(self, status)
            Draws everything that a user sees (eg. UI and Field).
            The window contains different info, depending on its status,
            whether it's a main menu or a game level.
        """
        if status == "game":
            self.painter.draw_game_ui(10)
            self.field.draw_all()
            # self.painter.draw_net(10, 10, self.field.cell_size)
            self.painter.draw_field(self.field.field, self.field.cell_size)

    def analyze_mouse_movement(self, position_list):
        """
            analyze_mouse_movement(self, position_list): list
            Converts coordinates of mouse movement into cell coordinates and returns it.
        """
        top_y = 60 # fix it!
        top_x = 5
        coordinates = set()
        for i in position_list:
            x = i[0] - top_x
            y = i[1] - top_y
            coordinates.add((x // self.field.cell_size, y // self.field.cell_size))
        return list(coordinates)

    def is_selection_removable(self, coordinates):
        """
            is_selection_removable(self, coordinates): boolean
            Returns a boolean value which tells whether all the coordinates
            have the same cell color.
        """
        print(coordinates)
        if len(coordinates) < 3:
            return False
        main_color = self.field.field[coordinates[0][0]][coordinates[0][1]]
        for i in coordinates:
            if self.field.field[i[0]][i[1]] != main_color:
                return False
        return True


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


def main():
    """
        main()
        Called on a program start, launches the game itself.
    """
    game = Game(560, 610)
    game.launch()
    pygame.quit()

if __name__ == "__main__":
    main()
