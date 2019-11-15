import pygame

pygame.init()
window = pygame.display.set_mode((500, 500))

pygame.display.set_caption("Test Game")

x, y = 50, 50
height, width = 20, 20
velocity = 5

dead = False

while not dead:
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dead = True
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= velocity
    if keys[pygame.K_RIGHT]:
        x += velocity
    if keys[pygame.K_UP]:
        y -= velocity
    if keys[pygame.K_DOWN]:
        y += velocity 
    if keys[pygame.K_q]:
        dead = True

    window.fill((0, 0, 0))
    pygame.draw.rect(window, (0, 0, 255), (x, y, width, height))
    pygame.display.update() 

pygame.quit()
