import pygame, sys  # thêm thư viện pygame và sys vào sử dụng


# hàm có chức năng vẽ sàn lên screen đã tạo
def draw_floor():
    # screen là class, blit là function (method) trong screen
    # chức năng là vẽ lên screen một surface mới, trong trường hợp này là floor surface
    # blit(source, dest)
    # source là surface mình muốn vẽ, destination là tọa độ mình muốn vẽ
    # x là hoành độ, y là tung độ
    # vẽ lên màn hình tại vị trí x= floor_x_pos đã khai báo từ đầu chương trình, y là 400
    # những dòng lệnh tiếp theo cũng tương tự
    screen.blit(floor_surface, (floor_x_pos, 400))
    screen.blit(floor_surface, (floor_x_pos + 288, 400))
    screen.blit(floor_surface, (floor_x_pos + 576, 400))
    screen.blit(floor_surface, (floor_x_pos + 864, 400))


# khai báo độ rộng của screen
# ở đây hình nền có sẵn có độ phân giải 288 x 512
# do em muốn chiều ngang rộng hơn để phù hợp hơn khi chơi trên máy tính nên em đã làm nó rộng gấp đôi
WIN_WIDTH = 288 * 2
# khai báo chiều cao của screen
WIN_HEIGHT = 512
# khai báo tần số quét
FPS = 120

# khởi tạo tất cả các mô-đun pygame, giống như trên STM32
pygame.init()
# khởi tạo màn hình cho game, độ phân giải
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
# tạo một đối tượng clock để giúp theo dõi thời gian, em dùng cái này để thiết lập FPS
clock = pygame.time.Clock()

# sử dụng method load để load hình có sẵn trong máy rồi lưu vào bg_surface.
# bg_surface là hình ảnh background trong game
# hàm convert() không cần thiết, không có nó game vẫn chạy
# khi blit ảnh ra màn hình thì pygame blit từng pixel ảnh trong hình --> chậm --> FPS không cao
# khi sử dụng hàm convert() thì format của các pixel trong ảnh bị thay đổi làm cho hàm blit dễ xử lý hơn
# làm tăng hiệu năng của game
# tóm lại là chức năng của convert() là thay đổi pixel format của ảnh làm tăng hiệu năng của game
bg_surface = pygame.image.load('assets/background-day.png').convert()
'''convert isn't strictly necessary, but what it does is it converts the image into a type of file that is easier to 
work with for pygame, basically makes it easier for pygame to run our game --> allows us to run the game at a faster
pace'''

# tương tự như trên, load hình của sàn rồi lưu vào biến floor_surface, convert dể chạy mượt hơn
floor_surface = pygame.image.load('assets/base.png').convert()
# floor_x_pos là vị trí của sàn
# khởi tạo giá trị ban đầu là 0
floor_x_pos = 0

while True:  # đây là vòng lặp chính trong game
    # pygame.event.get() lấy sự kiện từ hàng đợi
    for event in pygame.event.get():  # for mỗi event trong hàng đợi thì xử lý
        if event.type == pygame.QUIT:  # nếu bấm nút X trên màn hình game thì
            pygame.quit()  # hủy khởi tạo tất cả các mô-đun pygame --> tắt game
            sys.exit()  # thêm câu lệnh này để code exit với code 0 --> không báo lỗi
                        # không có game vẫn chạy bình thường

    # vẽ lên màn hình game background image
    # do mỗi hình chỉ có độ phân giải 288 x 512, mà màn hình game em muốn là 576 x 512
    # nên phải vẽ 2 hình mới đủ màn hình
    # một hình tại x=0 và một hình tại x = 288 vậy là đủ 576 pixels chiều rộng
    screen.blit(bg_surface, (0, 0))  # put one surface on another surface
    screen.blit(bg_surface, (288, 0))

    # Floor
    # mỗi lần chạy vòng lặp while thì ví trí hoành độ của sàn bị trừ 2 pixels
    # nghĩa là di chuyển về phía bên trái 2 pixels
    floor_x_pos -= 2
    # sau đó thì gọi hàm draw_floor chức năng là vẽ sàn lên màn hình
    draw_floor()
    # nếu ví trí của floor_x_pos nhỏ hơn hoặc bằng âm 576 thì giá trị của nó bị reset
    # vậy sẽ tạo ra sàn di chuyển về bên trái mãi mãi không bị mất đi
    # nếu không có điều kiện if này thì sàn sẽ di chuyển được 1 thời gian ngắn và biến
    # mất khỏi màn hình
    if floor_x_pos <= -576:
        floor_x_pos = 0

    # khi ta vẽ lên screen sử dụng method blit mà không gọi medthod update thì màn hình sẽ
    # không hiển thị những thay đổi trước đó
    # không có dòng lệnh này thì game sẽ không được hiển thị --> không chạy được
    pygame.display.update()

    # thiết lập FPS cho game
    # truyền tham số FPS vào
    # Bằng cách gọi clock.tick (FPS) một lần cho mỗi khung hình,
    # chương trình sẽ không bao giờ chạy với tốc độ hơn FPS khung hình mỗi giây
    # nghĩa là 1 giây vòng lặp while chạy FPS lần
    # không có dòng lệnh thì game vẫn chạy bình thường nhưng tốc độ game phụ thuộc vào cấu hình
    # máy --> FPS không ổn định --> trải nghiệm game không tốt
    clock.tick(FPS)
