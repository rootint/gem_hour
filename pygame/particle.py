import pygame
import random

GRAVITY = 10
screen_rect = (0, 0, 560, 610)
all_sprites = pygame.sprite.Group()

def load_image(fullname, colorkey=None):    
    '''
        load_image(fullname, colorkey=None) -> Image
        Takes an image's path and loads it into the memory.
    '''
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Particle(pygame.sprite.Sprite):
    shard = [load_image("textures/green.png")]
    for scale in (5, 10, 20):
        shard.append(pygame.transform.scale(shard[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.shard)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = GRAVITY

    def update(self):
        '''
            update(self)
            Updates the shards position every tick.
        '''
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()
