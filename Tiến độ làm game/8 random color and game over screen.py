import pygame, sys, random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 400))
    screen.blit(floor_surface, (floor_x_pos + 288, 400))
    screen.blit(floor_surface, (floor_x_pos + 576, 400))
    screen.blit(floor_surface, (floor_x_pos + 864, 400))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = IMAGES['pipe_surf'].get_rect(midtop=(600, random_pipe_pos))
    top_pipe = IMAGES['pipe_surf'].get_rect(midbottom=(600, random_pipe_pos - 150))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes
    # move every pipes(rectangle) to the left 5 pixels, return a new list of pipes (rectangle)


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:  # only the bottom pipe can reach y coordinate  512
            screen.blit(IMAGES['pipe_surf'], pipe)
        else:
            flip_pipe = pygame.transform.flip(IMAGES['pipe_surf'], False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 400:
        death_sound.play()
        return False

    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -(bird_movement * 4), 1)
    return new_bird

def rotate_falling_bird(bird_surface, bird_rect):
    global bird_movement
    if bird_rect.centery <= 400-14 :
        bird_movement += 0.05
        bird_rect.centery += int(bird_movement)

        bird_surface = pygame.transform.rotozoom(bird_surface, -(bird_movement * 15 ) ,1)
    else:
        bird_movement = 0
        bird_surface = pygame.transform.rotozoom(bird_surface, -90, 1)
    return bird_surface, bird_rect

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 30))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 30))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 390))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


# Game Variables
WIN_WIDTH = 288 * 2
WIN_HEIGHT = 512
FPS = 120
gravity = 0.15
global bird_movement
bird_movement = 0

score = 0
high_score = 0
IMAGES = {}

pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=706)
pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF', 25)
pygame.display.set_caption('Flappy Bird')

# bg_surface = pygame.image.load('assets/background-day.png').convert()


BACKGROUNDS_LIST = (
    'assets/background-day.png',
    'assets/background-night.png',
)

PIPES_Color_LIST = (
    'assets/pipe-green.png',
    'assets/pipe-red.png',
)

PLAYERS_LIST = (
    # red bird
    [
        'assets/redbird-downflap.png',
        'assets/redbird-midflap.png',
        'assets/redbird-upflap.png',
    ],
    # blue bird
    [
        'assets/bluebird-downflap.png',
        'assets/bluebird-midflap.png',
        'assets/bluebird-upflap.png',
    ],
    # yellow bird
    [
        'assets/yellowbird-downflap.png',
        'assets/yellowbird-midflap.png',
        'assets/yellowbird-upflap.png',
    ]
)

randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
randPipe = random.randint(0, len(PIPES_Color_LIST) - 1)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_x_pos = 0

# bird_downflap = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
# bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
# bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()


BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
# bird_rect = bird_surface.get_rect(center=(100, 256))

pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
IMAGES['pipe_surf'] = pygame.image.load(PIPES_Color_LIST[randPipe])

pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 900)
pipe_height = [200, 250, 300, 350, 370, 200, 250, 300, 350, 370]

welcome_surface = pygame.image.load('assets/message.png').convert_alpha()
welcome_rect = welcome_surface.get_rect(center=(288, 210))

game_over_surface = pygame.image.load('assets/gameover.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(288, 210))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
#score_sound_countdown = 133

randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)
IMAGES['player'] = [
    pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
    pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
    pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha()
]

bird_downflap = IMAGES['player'][0]
bird_midflap = IMAGES['player'][1]
bird_upflap = IMAGES['player'][2]
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 256))

game_states = {
    'game_active': False,
    'crash': False
}

def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper

def run_once_function():
    global bird_movement
    bird_movement = 0
    return bird_movement



while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_states['game_active']:
                if game_states['crash'] == True:
                    game_states['game_active'] = False
                else:
                    bird_movement = 0
                    bird_movement -= 5
                    flap_sound.play()

            if event.key == pygame.K_SPACE and game_states['game_active'] == False:
                game_states['game_active'] = True
                game_states['crash'] = False
                pipe_list.clear()
                bird_rect.center = (100, 256)
                bird_movement = -5
                score = 0
                score_sound_countdown = 0
                randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
                randPipe = random.randint(0, len(PIPES_Color_LIST) - 1)

                randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)
                IMAGES['player'] = [
                    pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
                    pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
                    pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha()
                ]

                bird_downflap = IMAGES['player'][0]
                bird_midflap = IMAGES['player'][1]
                bird_upflap = IMAGES['player'][2]
                bird_frames = [bird_downflap, bird_midflap, bird_upflap]
                bird_index = 0
                bird_surface = bird_frames[bird_index]

            if event.key == pygame.K_SPACE and  game_states['crash']:
                game_states['game_active'] = False


        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP and game_states['crash'] == False:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    # background surface

    IMAGES['bg_surface'] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()
    screen.blit(IMAGES['bg_surface'], (0, 0))
    screen.blit(IMAGES['bg_surface'], (288, 0))

    if game_states['game_active']:

        if game_states['crash'] == False:



            # Bird
            bird_movement += gravity
            bird_rect.centery += int(bird_movement)
            rotated_bird = rotate_bird(bird_surface)
            # rotated_bird = rotate_bird(IMAGES['player'][0])
            # screen.blit(bird_surface, bird_rect)
            screen.blit(rotated_bird, bird_rect)
            check_collision(pipe_list)
            game_states['crash'] = not check_collision(pipe_list)
            if game_states['crash']:
                bird_movement = 0

            # Pipes

            IMAGES['pipe_surf'] = pygame.image.load(PIPES_Color_LIST[randPipe])
            pipe_list = move_pipes(pipe_list)
            draw_pipes(pipe_list)

            # Score
            playerMidPos = 100 + bird_surface.get_width() / 2  # 34/2
            # score_sound_countdown = 0
            for pipe in pipe_list:
                pipeMidPos = pipe.centerx + pipe_surface.get_width() / 2
                print(score_sound_countdown)
                if pipeMidPos <= playerMidPos < pipeMidPos + 2:
                    score_sound_countdown += 1
                    if score_sound_countdown % 2 == 0:
                        score_sound.play()
                    score += 1
                    score -= 0.5

            score_display('main_game')

    else:
        screen.blit(welcome_surface, welcome_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')


    if game_states['crash']:



        print(bird_movement)
        print(game_states['crash'])
        # new_bird = pygame.transform.rotozoom(bird, -(bird_movement * 4), 1)
        # bird_movement = 0
        # bird_movement += 2
        # bird_rect.centery += int(bird_movement)

        # falling_bird = pygame.transform.rotozoom(bird_surface, -(bird_movement * 8), 1)

        draw_pipes(pipe_list)
        draw_floor()
        score_display('main_game')
        screen.blit(game_over_surface, game_over_rect)


        falling_bird, bird_rect = rotate_falling_bird(bird_surface, bird_rect)

        screen.blit(falling_bird, bird_rect)
    else:
        # Floor
        floor_x_pos -= 1
        draw_floor()
        if floor_x_pos <= -576:
            floor_x_pos = 0

    pygame.display.update()
    clock.tick(FPS)
