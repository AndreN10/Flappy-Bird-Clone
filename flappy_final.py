import pygame, sys, random # thêm thư viện

### Functions

# vẽ sàn
def draw_floor():
    # screen là class, blit là function (method) trong screen
    # chức năng là vẽ lên screen một surface mới, trong trường hợp này là floor surface
    # blit(source, dest)
    # source là surface mình muốn vẽ, destination là tọa độ mình muốn vẽ
    # x là hoành độ, y là tung độ
    # vẽ lên màn hình tại vị trí x= floor_x_pos đã khai báo từ đầu chương trình, y là 400
    # những dòng lệnh tiếp theo cũng tương tự
    # kích thước của màn hình là 576 x 512, kích thước của floor là 336 x 112
    # 512 - 112 = 400 --> nên ta đặt ở vị trí y = 400
    screen.blit(floor_surface, (floor_x_pos, 400))
    screen.blit(floor_surface, (floor_x_pos + 288, 400))
    screen.blit(floor_surface, (floor_x_pos + 576, 400))
    screen.blit(floor_surface, (floor_x_pos + 864, 400))

# tạo đường ống
def create_pipe():
    random_pipe_height = random.choice(pipe_height) # hàm choice cho ra ngẫu nhiên 1 giá trị nào đó có trong list pipe height
    # rồi sau đó gán vào biến random_pipe_height
    bottom_pipe = IMAGES['pipe_surf'].get_rect(midtop=(600, random_pipe_height)) # vị trí của ống dưới
    # midtop là điểm giữa trên đầu, vì ông nằm phía dưới, 600 là tọa độ x, random_pipe_height là tọa độ y
    # thực tế là chiều dài ống không thay đổi, do vị trí đặt nên ta thấy ống thay đổi độ dài
    top_pipe = IMAGES['pipe_surf'].get_rect(midbottom=(600, random_pipe_height - 150)) # vị trí của ống trên
    # random_pipe_height - 150 --> là khoảng cách giữa 2 ống trên dưới là luôn bằng 150
    # midbottom là điểm giữa phía dưới cùng, vì ông nằm phía trên
    return bottom_pipe, top_pipe # trả về bottom pipe và top pipe dưới dạng tupple

# di chuyển ống
def move_pipes(pipes): # truyền vào list pipes
    for pipe in pipes: # mỗi pipe trong pipes thì
        pipe.centerx -= 3  # di chuyển sang trái 3 pixels
        # centerx là điểm giữa của rectangle theo trục X
    return pipes # trả về list pipes mới


# vẽ ống
def draw_pipes(pipes): # truyền vào list pipes
    for pipe in pipes: # mỗi pipe trong pipes thì
        if pipe.bottom >= 512:  # nếu phía dưới của ống vượt quá 512 pixel thì, chỉ có ống phía dưới mói chạm được đến tọa độ y 512
            # Do trong assets chỉ có hình ảnh ống chỉa lên trên
            screen.blit(IMAGES['pipe_surf'], pipe) # vẽ ống lên màn hình

        else: # còn nếu ko phải ống dưới thì là ống trên
            # nếu là ống trên thì ta lật xuống phía dưới  --> ra ống phía trên chỉa xuống duói
            flip_pipe = pygame.transform.flip(IMAGES['pipe_surf'], False, True) # dùng hàm flip() trong transform
            # flip(source, flip x, flip y), flip x false, flip y true --> lật theo trục y
            screen.blit(flip_pipe, pipe) # vẽ ống lên màn hình

# kiểm tra va chạm
def check_collision(pipes): # đưa vào list pipes
    for pipe in pipes: #mỗi pipe trong pipes thì
        if bird_rect.colliderect(pipe): # dùng hàm colliderect() để phát hiện va chạm
            # check va chạm giữa chim và ống
            death_sound.play() # nếu có và chạm thì chơi âm thanh chim chết
            return False # và trả về biến bool False

    if bird_rect.bottom >= 400: # nếu chim đi quá vị trí 400, tức là sàn
        death_sound.play() # thì chơi nhạc chim chết
        return False # và trả về false
    # trả về false tức là thua, phải chơi lại

    return True # còn không vạ chạm thì trả về true, tức là tiếp tục chơi

# xoay chim
def rotate_bird(bird): # đưa vào surface bird
    new_bird = pygame.transform.rotozoom(bird, -(bird_movement * 4), 1)
    # rotozoom(Surface, angle, scale): surface: bird , angle: -(bird_movement * 4), scale: 1
    # xoay surface của chim, góc xoay dựa vào tốc độ của chim, thêm dấu - để chim xoay đúng chiều
    # tại tốc độ di chuyển nhỏ nên góc xoay không lớn nên phải * 4 để thấy rõ, scale không sử dụng mặc định là 1
    return new_bird # trả về surface chim mới

# tạo hiệu ứng chim rớt khi va chạm
def rotate_falling_bird(bird_surface, bird_rect): # đưa vào surface và rectangle của chim
    # surface để xoay, rectangle để di chuyển tọa độ
    global bird_movement, bird_falling_angle # làm biến bird_movement, bird_falling_angle thành biến toàn cục
    # mở rộng scope, giá trị 2 biến trên được lấy từ đầu chương trình lúc khai báo biến
    #if 400 <= bird_rect.centery or bird_rect.centery <= 400 - 24:
    if bird_rect.centery <= 400 - 24: # nếu chim còn ở phía trên của sàn thì
        bird_movement += 0.25 # tăng tốc độ di chuyển của chim
        bird_rect.centery += int(bird_movement) # vị trí của chim theo trục y được cộng vào từ tốc độ di chuyển của chim
        bird_falling_angle += 2.5 # tăng góc rơi của chim
        if bird_falling_angle >= 90: # nếu góc rơi quá 90 độ thì
            bird_falling_angle = 90  # reset lại 90, không cho rơi quá 90 độ
        bird_surface = pygame.transform.rotozoom(bird_surface, - (bird_falling_angle), 1) # xoay chim với những thông số đã tạo
    else: # nếu không thì, tức là đang ở sàn
        bird_movement = 0 # cho chim ngừng di chuyển
        bird_surface = pygame.transform.rotozoom(bird_surface, - (bird_falling_angle), 1) # giữ nguyên góc rơi của chim
    return bird_surface, bird_rect # trả về surface (chim đã xoay) và rectangle (tọa độ hay vị trí của chim)

# tạo hiệu ứng vỗ cánh cho chim
def bird_animation():
    new_bird = bird_frames[bird_index] # list bird_frames lưu sẵn 3 hình của chim
    # bird index là chỉ số được tạo sẵn, bird index sẽ tăng dần mỗi 200ms và được reset về 0 khi vượt quá 2
    # vậy là mỗi 0.2s thì sẽ load một ảnh trong list, liên tục như vậy sẽ tạo ra hiệu ứng chim vỗ cánh
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    # center là điểm chính giữa của rectangle
    # tọa độ x của chim không đổi
    # tọa độ y thay đổi theo biến, nghĩa là lấy tọa độ của chim trước đó
    return new_bird, new_bird_rect # trả về surface mới và rectangle mới

# hiển thị điểm số
def score_display(game_state): # đưa vào biến game state, tùy trạng thái mà hiển thị điểm
    # lúc đang chơi thì hiển thì score thôi
    if game_state == 'main_game': # nếu như truyền vào chuỗi "main_game" thì
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255)) # hiển thị điểm hiện tại
        # chuyển điểm thành int rồi thành string, true: khử răng cưa, RGB = 255, 255, 255 là màu trắng
        score_rect = score_surface.get_rect(center=(288, 30)) # vị trí hiển thị điểm
        screen.blit(score_surface, score_rect) # vẽ điểm lên màn hình

    # khi mới bắt đầu game thì hiển thị điểm với high score
    if game_state == 'start': # nếu như truyền vào chuỗi "game_over" thì
        # giống phía trên
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        # f' là string format, hỗ trợ hiển thị chuỗi và giá trị của biến
        # hiển thị string Score lên kèm theo đó là điểm số score
        score_rect = score_surface.get_rect(center=(288, 30))
        screen.blit(score_surface, score_rect)
        # bổ sung thêm high_score
        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 390))
        screen.blit(high_score_surface, high_score_rect)

# cập nhật điểm số
def update_score(score, high_score): # truyền vào 2 biến
    if score > high_score: # nếu điểm hiện tại lớn hơn high score thì
        high_score = score # high score = điểm hiện tại
    return high_score # trả về high_score

# xuất FPS
def show_fps():
    fps = str(int(clock.get_fps())) # lấy FPS từ class clock sau đó ép kiểu int, rồi ép tiếp thành string rồi gán vào biến FPS
    fps_surface = game_font.render(fps, 1, pygame.Color('red')) # viết text lên surface
    #text cần vẽ là fps, khử răng cưa là true, màu của text là đỏ
    fps_rect = fps_surface.get_rect(center=(20, 20)) # tọa độ cần đặt
    screen.blit(fps_surface, fps_rect) # vẽ lên màn hình


### Game Variables

# khai báo độ rộng của screen
# ở đây hình nền có sẵn có độ phân giải 288 x 512
# do em muốn chiều ngang rộng hơn để phù hợp hơn khi chơi trên máy tính nên em đã làm nó rộng gấp đôi
WIN_WIDTH = 288 * 2
WIN_HEIGHT = 512
FPS = 60 # khai báo khung hình trên giây
gravity = 0.3 # trọng lực để chim rơi xuống
global bird_movement, bird_falling_angle # khai báo biến toàn cục, tốc độ di chuyển của chim và góc rơi
bird_movement = 0 # ban đầu tốc độ = 0
bird_falling_angle = 0 # ban đầu góc rơi = 0

bird_hover = 0 # chim lướt đầu màn hình
bird_direction = 1 # hướng lướt

score_sound_countdown = 0 # biến đếm để chơi âm thanh ghi điểm
score = 0 # điểm số
high_score = 0 # điểm cao nhất
IMAGES = {} # tuple ảnh rỗng

pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=706) # đặt trước các đối số init của mixer
# tần số, bits per sample, kênh, bitrate
pygame.init() # khởi tạo tất cả các mô-đun pygame, giống như trên STM32
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT)) # khởi tạo màn hình cho game, độ phân giải

# tạo một đối tượng clock để giúp theo dõi thời gian, em dùng cái này để thiết lập FPS
clock = pygame.time.Clock()

# load font trong asset, size 25
game_font = pygame.font.Font('04B_19.TTF', 25)
pygame.display.set_caption('Flappy Bird') # set tựa đề trên caption game

# bg_surface = pygame.image.load('assets/background-day.png').convert()

# tuple hình nền
BACKGROUNDS_LIST = (
    'assets/background-day.png',
    'assets/background-night.png',
)
# tuple ống
PIPES_Color_LIST = (
    'assets/pipe-green.png',
    'assets/pipe-red.png',
)
# tuple bao gồm 3 lists chim gồm 3 phần tử
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
# tạo biến ranBg và randPipe để load random hình nền và ống trong list
# randint(x, y) cho ra số nguyên ngẫu nhiên từ khoảng x đến y
randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
randPipe = random.randint(0, len(PIPES_Color_LIST) - 1)

floor_surface = pygame.image.load('assets/base.png').convert() # load ảnh sàn
# convert() dùng để chuyển đổi format pixel --> giúp game dễ blit ra màn hình theo khuyến cáo của nhà sản xuất
# không dùng game vẫn chạy bình thường nhưng FPS tối đa không cao
floor_x_pos = 0 # vị trí x của sàn

# bird_downflap = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
# bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
# bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()

# tạo user event, cứ mỗi 200ms trigger một lần, không cần tác động từ người dùng
# dùng để tạo hiệu ứng vỗ cánh cho chim
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
# bird_rect = bird_surface.get_rect(center=(100, 256))
#pipe_surface = pygame.image.load('assets/pipe-green.png').convert()

# load hình ảnh random trong list pipe
# thêm vào tuple IMAGES một giá trị pipe_surf chứa hình ảnh được load
IMAGES['pipe_surf'] = pygame.image.load(PIPES_Color_LIST[randPipe]).convert()

pipe_list = [] # tạo pipe list trống dùng để tạo chướng ngại vật
# tạo user event trigger mỗi 900ms, dùng để tạo đường ống
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 900)
pipe_height = [200, 250, 300, 350, 370, 200, 250, 300, 350, 370] # tạo pipe height list với độ cao khác nhau

# start screen
welcome_surface = pygame.image.load('assets/message.png').convert_alpha()
# convert alpha khác với convert ở chỗ là những pixels trống trong ảnh sẽ bị làm transparent
# nếu không sử dụng alpha thì ảnh sẽ không khả dụng, thầy có thể tự test
welcome_rect = welcome_surface.get_rect(center=(288, 210)) # vị trí của hình ảnh

# tương tự như trên đây là game over screen
game_over_surface = pygame.image.load('assets/gameover.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(288, 210))

# tạo âm thanh trong game
# load file từ assets đã có sẵn
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav') # tiếng vỗ cánh
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav') # tiếng chim chết
score_sound = pygame.mixer.Sound('sound/sfx_point.wav') # tiếng ghi điểm khi vượt qua mỗi cặp trụ

# tạo biến random để thay đổi chim mỗi lần chơi khác nhau
randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)
# tạo list player vào tuple images
# màu chim được lấy theo player list
# thứ tự chim vỗ lấy theo 0 1 2 trong IMAGES['player']
# do mình tăng biến bird_index theo 0 1 2
IMAGES['player'] = [
    pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
    pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
    pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha()
]

# tạo frame cho chim, dùng để tạo hiệu ứng vỗ cánh
bird_downflap = IMAGES['player'][0] # thứ tự trong list 0
bird_midflap = IMAGES['player'][1] # 1
bird_upflap = IMAGES['player'][2]  # 2
bird_frames = [bird_downflap, bird_midflap, bird_upflap] # bird_frames = [0, 1, 2]
bird_index = 0 # dùng bird index để thao túng bird frames
bird_surface = bird_frames[bird_index] # surface được vẽ ra screen lấy từ bird frames
bird_rect = bird_surface.get_rect(center=(100, 256)) # tọa độ của chim lúc bắt đầu

# tạo dictionary trạng thái game
# ban đầu thì set False
game_states = {
    'game_active': False, # game chưa bắt đầu
    'crash': False # cũng chưa bị va chạm
}



while True: # vòng lặp chính trong game

    # pygame.event.get() lấy sự kiện từ hàng đợi
    for event in pygame.event.get():  # for mỗi event trong hàng đợi thì xử lý
        if event.type == pygame.QUIT:  # nếu bấm nút X trên màn hình game thì
            pygame.quit()  # hủy khởi tạo tất cả các mô-đun pygame --> tắt game
            sys.exit()  # thêm câu lệnh này để code exit với code 0 --> không báo lỗi
            # không có game vẫn chạy bình thường

        if event.type == pygame.KEYDOWN: # nếu có nhấn phím
            if event.key == pygame.K_SPACE and game_states['game_active']: # nếu nhấn phím space và game_active == true
                # if game_states['crash'] == True:
                #     game_states['game_active'] = False
                if bird_rect.top >= -50 and bird_rect.bottom <= 390: # nếu chim nằm ở trong khoảng từ -50 đến 390 thì
                    # xử lý vỗ cánh
                    bird_movement = 0 # chịu tác động bởi gravity nên bird_movement khác 0
                    # muốn bay lên thì phải reset bird_movement
                    bird_movement -= 6 # sau đó trừ 6 để bay lên, +6 thì chim bay xuống
                    #trục y của game ngược với trục oy trong toán
                    flap_sound.play() # chơi tiếng vỗ cánh

            if event.key == pygame.K_SPACE and game_states['game_active'] == False: # nếu nhấn phím space và game_active == false
                game_states['game_active'] = True # reset lại game active

                # reset lại giá trị các biến khi bắt đầu lại game
                pipe_list.clear() # xóa pipe trong pipe list
                # bird_rect.center = (100, 256)
                bird_movement = -6
                score = 0
                score_sound_countdown = 0
                bird_falling_angle = 0

            if event.key == pygame.K_SPACE and game_states['crash']: # nếu nhấn phím space và crash == true
                # bị va chạm thì reset lại game active và crash thành false
                game_states['game_active'] = False
                game_states['crash'] = False

                bird_rect.center = (100, 256)  # reset lại vị trí chim

                #reset lại biến random cho background, pipe và chim

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

        # chỉ tạo pipe khi trigger user event spawnpipe và game_states['game_active'] == True và game_states['crash'] == False
        # khi crash = true thì không cần tạo pipe hoặc game active = false cũng vậy
        if event.type == SPAWNPIPE and game_states['game_active'] == True and game_states['crash'] == False:
            pipe_list.extend(create_pipe()) # extend pipe được tạo từ hàm create pipe vào pipe list

        # khi user event birflap trigger và crash = false
        # nếu crash = true thì chim không cần vỗ cánh, tại nó chết rồi không vỗ được.
        if event.type == BIRDFLAP and game_states['crash'] == False:
            if bird_index < 2: # nếu bird index < 2 thì
                bird_index += 1 # cộng 1 vào bird index, tương đương bird_index = bird_index + 1
            else: # không thì
                bird_index = 0 # reset lại 0
            # như vậy thì giá trị của bird index sẽ giao động trong khoảng 0 1 2 0 1 2 .....

            # tạo hiệu ứng vỗ cánh cho chim
            bird_surface, bird_rect = bird_animation() # bird surface và bird rect sẽ lưu giá trị trả về từ hàm bird_animation
            # hình ảnh chim xoay là của bird_surface


    # background surface
    IMAGES['bg_surface'] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert() # load hình background random

    # vẽ lên màn hình game bg_surface
    # do mỗi hình chỉ có độ phân giải 288 x 512, mà màn hình game em muốn là 576 x 512
    # nên phải vẽ 2 hình mới đủ màn hình
    # một hình tại x=0 và một hình tại x = 288 vậy là đủ 576 pixels chiều rộng
    screen.blit(IMAGES['bg_surface'], (0, 0))
    screen.blit(IMAGES['bg_surface'], (288, 0))

    # Trạng thái game
    if game_states['game_active']: # nếu game active, nghĩa là bắt đầu chơi game

        if game_states['crash'] == False: # nếu chim chưa bị va chạm

            # Bird
            bird_movement += gravity # chim sẽ bị rơi xuống do trọng lực, cộng vào biến bird_movement
            bird_rect.centery += int(bird_movement) # tọa độ theo trục y của chim sẽ cộng theo biến bird_movement
            rotated_bird = rotate_bird(bird_surface) # xoay xoay rồi sau đó lưu surface mới vào rotated bird

            screen.blit(rotated_bird, bird_rect) # vẽ chim đã xoay ra màn hình
            check_collision(pipe_list) # kiểm tra va chạm
            game_states['crash'] = not check_collision(pipe_list) # lưu giá trị bool trả về từ hàm check va chạm vào crash
            # dùng để chuyển state
            # print(game_states['crash'])

            if game_states['crash']: # nếu bị va chạm rồi thì crash == true
                bird_movement = 0 # reset lại tốc độ chim để hàm rotate falling bird xử lý



            # Pipes
            IMAGES['pipe_surf'] = pygame.image.load(PIPES_Color_LIST[randPipe]).convert_alpha() # load ảnh ống màu ngẫu nhiên
            pipe_list = move_pipes(pipe_list) # di chuyển ống
            draw_pipes(pipe_list) # vẽ ống ra màn hình
            if len(pipe_list) >= 10: # nếu số lượng ống trong list nhiều hơn hoặc bằng 10 thì
                pipe_list.pop(0) # xóa bỏ ống ở vị trí thứ 0 trong list tức là ống đầu tiên



            # Score
            playerMidPos = bird_rect.centerx # vị trí giữa trục x của chim
            for pipe in pipe_list: # với mỗi pipe trong pipe list
                pipeMidPos = pipe.centerx # vị trí giữa theo trục x của ống
                if pipeMidPos <= playerMidPos < pipeMidPos + 2: # nghĩa là nếu chim qua 1 cặp ống
                    # playerMidPos nằm GIỮA vị trí của pipeMidPos và pipeMidPos + 2 pixels
                    # do hàm check collision do thư viện pygame cấp có độ chính xác chưa cao
                    # với lệnh if trên thì mỗi lần chim vượt qua 1 cặp ống thì if đúng 2 lần
                    # mà ta muốn khi qua cặp ống thì chỉ tăng 1 điểm và chơi nhạc score sound 1 lần
                    score_sound_countdown += 1
                    if score_sound_countdown % 2 == 0: # 2 4 6 8 ... chia hết cho 2  --> chỉ chạy 1 lần
                        score_sound.play() # chơi nhạc ghi điểm
                    score += 1 # 2 4 6 8 ... cộng lên
                    score -= 0.5 # 1 2 3 4 ... trừ bù
                    # mỗi lần qua cặp ống tăng đúng 1 điểm và chơi 1 lần nhạc

            score_display('main_game') # hiển thị điểm số


    else: # nếu game không active
        # chim nhấp nhô lên xuống tại start screen
        if abs(bird_hover) == 3: # abs là trị tuyệt đối, bird hover = 3 nghĩa là khoảng nhấp nhô là 3 đơn vị
            # khi đạt đủ 3 thì
            bird_direction *= -1 # hướng đi lên thì nhân cho âm 1 sẽ hướng xuống
        if bird_direction == 1: # khi hướng = 1
            # cộng 0.25 vào biến bird_hover để di chuyển, giống biến bird_movement
            bird_hover += 0.25 # chim hướng xuống
        else: # hướng = -1
            bird_hover -= 0.25 # chim hướng lên

        bird_rect.centery += int(bird_hover) # vị trị của bird thì phụ thuộc vào biến bird hover
        screen.blit(bird_surface, bird_rect) # vẽ chim lên màn hình

        screen.blit(welcome_surface, welcome_rect) # vẽ welcome screen
        high_score = update_score(score, high_score) # update high score
        score_display('start') # hiển thị điểm ra màn hình

    if game_states['crash']: # Nếu chim bị va chạm

        draw_pipes(pipe_list) # vẽ ống nhưng không di chuyển ống
        score_display('main_game') # hiện thị điểm số
        screen.blit(game_over_surface, game_over_rect) # vẽ lên màn hình game over

        falling_bird, bird_rect = rotate_falling_bird(bird_surface, bird_rect) # tạo hiệu ứng chim rớt xuống dưới sàn
        screen.blit(falling_bird, bird_rect) # vẽ chim trước
        draw_floor() # vẽ sàn
        # vẽ chim trước vẽ sàn sẽ tạo hiệu ứng chim cắm mỏ xuống sàn
    else: # nếu không bị va chạm
        # Floor
        floor_x_pos -= 2 # di chuyển sàn về bên trái 2 pixels
        draw_floor() # vẽ sàn

        # reset lại vị trí sàn để tạo hiệu ứng chuyển động liên tục của sàn
        if floor_x_pos <= -576:
            floor_x_pos = 0

    show_fps() # hiện thị FPS trong game
    pygame.display.update() # update màn hình, không có dòng lệnh này thì game sẽ không chạy đuọc
    clock.tick_busy_loop(FPS)
    # thiết lập FPS cho game
    # truyền tham số FPS vào
    # Bằng cách gọi clock.tick (FPS) một lần cho mỗi khung hình,
    # chương trình sẽ không bao giờ chạy với tốc độ hơn FPS khung hình mỗi giây
    # nghĩa là 1 giây vòng lặp while chạy FPS lần
    # không có dòng lệnh thì game vẫn chạy bình thường nhưng tốc độ game phụ thuộc vào cấu hình
    # máy --> FPS không ổn định --> trải nghiệm game không tốt
    # còn có một hàm tương tự là clock.tick(FPS), nhưng FPS cho ra không ổn định bằng nhưng chiếm ít CPU hơn
