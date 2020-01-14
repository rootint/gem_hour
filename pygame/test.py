import pygame
import random
import math
import os

colors = {
    0: "textures/green.png",
    1: "textures/red.png",
    2: "textures/blue.png",
    3: "textures/purple.png",
    4: "textures/yellow.png",
    5: "textures/white.png",
    -1: "textures/darkblue.png"
}

def load_image(fullname, colorkey=None):    
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def generate_field(width, height):
    all_sprites = pygame.sprite.Group()
    field = [[random.randint(0, 5) for j in range(width)] for i in range(height)]
    print(*field, sep="\n")
    for i in range(len(field)):
        for j in range(len(field[i])):
            sprite = pygame.sprite.Sprite(all_sprites)
            sprite.image = load_image(colors[field[i][j]])
            sprite.image = pygame.transform.scale(sprite.image, (50, 50))
            sprite.rect = sprite.image.get_rect()
            sprite.rect.x = i * 50
            sprite.rect.y = j * 50
    return field, all_sprites



pygame.init()
window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("test")
clock = pygame.time.Clock()

field, all_sprites = generate_field(10, 10)

dead = False
while not dead:
    clock.tick(90)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dead = True
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
            dead = True
        all_sprites.draw(window)
        pygame.display.flip()
        pygame.display.set_caption("FPS " + str(clock.get_fps()))

pygame.quit()
