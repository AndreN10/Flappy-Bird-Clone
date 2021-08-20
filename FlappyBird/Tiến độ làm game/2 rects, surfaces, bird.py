import pygame, sys


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 400))
    screen.blit(floor_surface, (floor_x_pos + 288, 400))
    screen.blit(floor_surface, (floor_x_pos + 576, 400))
    screen.blit(floor_surface, (floor_x_pos + 864, 400))


# Game Variables
WIN_WIDTH = 288 * 2
WIN_HEIGHT = 512
FPS = 120
gravity = 0.25
bird_movement = 0

pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

bg_surface = pygame.image.load('assets/background-day.png').convert()
'''convert isn't strictly necessary, but what it does is it converts the image into a type of file that is easier to 
work with for pygame, basically makes it easier for pygame to run our game --> allows us to run the game at a faster
pace'''

floor_surface = pygame.image.load('assets/base.png').convert()
floor_x_pos = 0

bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert()
# It takes a surface and puts a rectangle around it (exact same dimension of the surface)
bird_rect = bird_surface.get_rect(center=(100, 256))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 8

    # background surface
    screen.blit(bg_surface, (0, 0))  # put one surface on another surface
    screen.blit(bg_surface, (288, 0))

    # bird
    bird_movement += gravity
    bird_rect.centery += int(bird_movement)
    screen.blit(bird_surface, bird_rect)

    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(FPS)
