import pygame
import random
from field import Field
from painter import Painter

class Game:
    def __init__(self, window_width, window_height):
        self.window = pygame.display.set_mode((window_width, window_height))
        self.field = Field(10, 10, window_width, window_height, self.window)
        self.dead = False
        self.is_ui_updated = True
        self.is_field_updated = True
        self.window_width = window_width
        self.window_height = window_height
        self.score = 0
        self.time_elapsed = 0
        self.background_image = self.field.load_image("textures/bg.jpg")
        pygame.display.set_caption("Gem Hour: Also Try Bejeweled!")
        from emitter import Emitter
        self.emitter = Emitter()
        self.bubble_surface = pygame.Surface((window_width, window_height), pygame.SRCALPHA, 32)

    def start_screen(self):
        """
            start_screen(self)
            Called in the very beginning, creates the pre-game intro.
            On click in opens the game itself.
        """
        start = False
        clock = pygame.time.Clock()
        intro_text = ["Gem  Hour", "",
                      "You have to join groups of gems",
                      "(more than three) to eliminate them.",
                      "The more you do - the higher your score is"]

        background = self.field.load_image('textures/bg.jpg')
        self.window.blit(background, (0, 0))
        font = pygame.font.Font("Treamd.ttf", 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.window.blit(string_rendered, intro_rect)

        while not self.dead and not start:
            for event in pygame.event.get():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.dead = True
                keys = pygame.key.get_pressed()
                mouse = pygame.mouse.get_pressed()
                if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
                    self.dead = True
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    start = True
            pygame.display.flip()
            clock.tick(60)
        if start:
            self.tick()

    def launch(self):
        """
            launch(self)
            Called only once on a game start.
            Initializes the field and launches the start_screen() function.
        """
        self.field.generate_field(10, 10)
        # self.window.fill((47, 47, 47))
        self.painter = Painter(self.window_width, self.window_height, 
                               self.window, self.field.field, self.field.cell_size, self.score)
        self.start_screen()

    def tick(self):
        """
            tick(self)
            Contains the main game loop.
        """
        # not used
        fall_velocity = 1.5 # velocity of falling gems
        clicked_pos = []
        is_dropping = False # boolean that checks if anything is falling out of the field
        dropping_gems = [] # a list of gems to be dropped
        drop_y = 0 # calculates coordinates of dropping gems
        drop_time = 0

        fps = 90
        draw_score_tick = 0
        clock = pygame.time.Clock()
        while not self.dead:
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.on_game_end()
                    self.dead = True
            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pressed()
            if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
                self.on_game_end()
                self.dead = True
            if (pygame.mouse.get_pos()[1] in range(60, self.window_height) and 
                pygame.mouse.get_pos()[0] in range(5, self.window_width - 5)):
                if mouse[0] == 1:
                    clicked_pos.append(pygame.mouse.get_pos())
                    self.emitter.create_particles(pygame.mouse.get_pos())
                    selection = self.analyze_mouse_movement(clicked_pos)
                    self.bubble_surface = self.painter.highlight_gems(self.get_removed_coordinates(selection))
                else:
                    if len(clicked_pos) > 3:
                        self.bubble_surface = self.painter.highlight_gems([])
                        if self.is_selection_removable(selection):
                            draw_score_tick = 1
                            self.painter.draw_score(self.get_removed_coordinates(selection)[0],
                                                    len(dropping_gems) * 20, draw_score_tick)
                            dropping_gems = selection
                            self.field.generate_on_columns(selection)
                            self.painter.animate_appearance(selection, 0)
                            is_dropping = True  
                            self.score += len(dropping_gems) * 20
                    clicked_pos = []
            if not self.field.is_move_available(self.field.field):
                self.dead = True
                self.on_game_end()
            # pygame.display.set_caption('FPS ' + str(clock.get_fps())) # for debug purposes
            self.window.blit(self.background_image, [0, 0])
            self.draw_all("game") # optimize draw_all feature
            self.window.blit(self.bubble_surface, [0, 0])
            if draw_score_tick in range(1, 20):
                self.painter.draw_score(self.get_removed_coordinates(selection)[0],
                                        len(dropping_gems) * 20, draw_score_tick)
                draw_score_tick += 1
            else:
                draw_score_tick = 0
            pygame.display.flip()

    def draw_all(self, status):
        """
            draw_all(self, status)
            Draws everything that a user sees (eg. UI and Field).
            The window contains different info, depending on its status,
            whether it's a main menu or a game level.
        """
        if status == "game":
            self.painter.draw_game_ui(self.score, self.time_elapsed)
            self.field.all_sprites.draw(self.window)

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

    def get_removed_coordinates(self, coords):
        """
           get_removed_coordinates(self, coords): list
           Returns a list with the top-left coordinates of each selected gem. 
        """
        coordinates = []
        for i in coords:
            x, y = i[0], i[1]
            coordinates.append((5 + x * self.field.cell_size, 60 + y * self.field.cell_size))
        return coordinates

    def is_selection_removable(self, coordinates):
        """
            is_selection_removable(self, coordinates): boolean
            Returns a boolean value which tells whether all the coordinates
            have the same cell color.
        """
        # print(coordinates)
        if len(coordinates) < 3:
            return False
        main_color = self.field.field[coordinates[0][0]][coordinates[0][1]]
        for i in coordinates:
            if self.field.field[i[0]][i[1]] != main_color:
                return False
                # return True
        return True

    def on_game_end(self):
        """
            on_game_end(self)
            Called after the game, shows the outro screen.
            Also saves the highest score to scores.txt
        """
        start = False
        clock = pygame.time.Clock()
        intro_text = ["Good Job!", "",
                      f"Your final score is {self.score}",
                      "See you again later!"]

        with open('scores.txt') as file:
            data = file.read().split()
        if int(data[-1]) < self.score:
            clear = open('scores.txt', 'w').close()    
            output = open('scores.txt', 'w')
            output.write(f"Your best score: {self.score}" + '\n')
            output.close()

        background = self.field.load_image('textures/bg.jpg')
        self.window.blit(background, (0, 0))
        font = pygame.font.Font("Treamd.ttf", 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.window.blit(string_rendered, intro_rect)

        while not self.dead and not start:
            for event in pygame.event.get():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.dead = True
                keys = pygame.key.get_pressed()
                mouse = pygame.mouse.get_pressed()
                if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
                    self.dead = True
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return
            pygame.display.flip()
            clock.tick(60)
