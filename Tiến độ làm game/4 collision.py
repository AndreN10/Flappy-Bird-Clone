import pygame, sys, random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 400))
    screen.blit(floor_surface, (floor_x_pos + 288, 400))
    screen.blit(floor_surface, (floor_x_pos + 576, 400))
    screen.blit(floor_surface, (floor_x_pos + 864, 400))
    screen.blit(floor_surface, (floor_x_pos + 1152, 400))
    screen.blit(floor_surface, (floor_x_pos + 1440, 400))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(600, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(600, random_pipe_pos - 150))
    return bottom_pipe, top_pipe
    # return a tuple


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes
    # move every pipes(rectangle) to the left 5 pixels, return a new list of pipes (rectangle)


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:  # only the bottom pipe can reach y coordinate  512
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False

    # the bird get far up on the screen or hit the floor --> collision
    if bird_rect.top <= -100 or bird_rect.bottom >= 400:
        return False

    return True


# Game Variables
WIN_WIDTH = 288 * 2
WIN_HEIGHT = 512
FPS = 120
gravity = 0.15
bird_movement = 0
game_active = True

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

pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_list = []
# user event triggered by timer, an event that is going to be triggered every 1.2 seconds
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [200, 250, 300, 350]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 5
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 256)
                bird_movement = -5

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    # background surface
    screen.blit(bg_surface, (0, 0))  # put one surface on another surface
    screen.blit(bg_surface, (288, 0))

    if game_active:
        # Bird
        bird_movement += gravity
        bird_rect.centery += int(bird_movement)
        screen.blit(bird_surface, bird_rect)
        check_collision(pipe_list)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -1152:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(FPS)
