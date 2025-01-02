import pygame
import random

# 初始化 pygame
pygame.init()
pygame.mixer.init()  # 初始化音效模組

# 定義顏色
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)

# 載入音效
hit_brick_sound = pygame.mixer.Sound("C:/Users/acer/Downloads/arkanoid/hit_brick.wav")  #記得修改路徑
game_over_sound = pygame.mixer.Sound("C:/Users/acer/Downloads/arkanoid/Game_Over.mp3")  #記得修改路徑

# 設置音效音量
hit_brick_sound.set_volume(0.5)

# 設置屏幕尺寸
SCREEN_WIDTH = 850
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("乒乓球打磚塊遊戲")

# 定義遊戲對象類別
# 板子
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20)

    # 板子的移動由滑鼠操控
    def update(self):
        mouse_x = pygame.mouse.get_pos()[0]
        self.rect.centerx = mouse_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

# 球
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 15), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (7, 7), 7)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x_speed = 0    # 初始水平速度設為0，等待遊戲開始
        self.y_speed = 0    # 初始垂直速度設為0
        self.started = False

    def update(self):
        if self.started:
            self.rect.x += self.x_speed
            self.rect.y += self.y_speed

            # 撞牆反彈
            if self.rect.left <= 0:    # 撞到左邊界
                self.rect.left = 0
                self.x_speed = abs(self.x_speed)
            if self.rect.right >= SCREEN_WIDTH:    # 撞到右邊界
                self.rect.right = SCREEN_WIDTH
                self.x_speed = -abs(self.x_speed)
            if self.rect.top <= 0:     # 撞到上邊界
                self.rect.top = 0
                self.y_speed = abs(self.y_speed)

    def start_movement(self):
        self.x_speed = random.choice([3, -3])   # 設定水平速度
        self.y_speed = -3   # 設定垂直速度
        self.started = True    # 設置已開始標誌，表示遊戲已經開始，並且球可以開始移動

# 磚塊
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((60, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color

# 磚塊出現機率
def generate_row(y_position):
    new_row = pygame.sprite.Group()
    for col in range(12):
        rand = random.random()
        if rand < 0.05:    # 紅色磚塊5%的機率
            color = RED
        elif rand < 0.15:   # 橘色磚塊10%的機率
            color = ORANGE
        else:   # 藍色磚塊剩餘的機率
            color = BLUE
        brick = Brick(col * 70 + 10, y_position, color)
        new_row.add(brick)
    return new_row

# 重設遊戲函數
def reset_game():

    # 初始化板子
    paddle = Paddle()

    # 初始化球
    balls = pygame.sprite.Group()
    initial_ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40)
    balls.add(initial_ball)

    # 初始化磚塊
    bricks = pygame.sprite.Group()
    for row in range(5):
        for col in range(12):
            brick = Brick(col * 70 + 10, row * 30, BLUE)
            bricks.add(brick)

    # 更新所有遊戲物件
    all_sprites = pygame.sprite.Group()
    all_sprites.add(paddle, balls, bricks)

    return paddle, balls, bricks, all_sprites, 0, False, False

# 初始化遊戲
font = pygame.font.SysFont("Arial", 20)
game_over_font = pygame.font.SysFont("Arial", 40)
clock = pygame.time.Clock()

# 遊戲主循環
running = True
while running:
    # 初始化遊戲設定
    paddle, balls, bricks, all_sprites, score, game_started, game_over = reset_game()
    start_time = pygame.time.get_ticks()
    scroll_speed = 0.05    # 磚塊下降速度
    scroll_accumulator = 0     # 用於累積時間以實現平滑下降

    # 單局遊戲迴圈
    in_game = True
    while in_game:
        screen.fill(BLACK)

        # 事件處理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                in_game = False
            if game_over and event.type == pygame.KEYDOWN:
                # 遊戲結束時，按下enter鍵重複執行遊戲
                if event.key == pygame.K_RETURN:
                    in_game = False
                # 遊戲結束時，按下esc鍵退出遊戲
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    in_game = False
            # 滑鼠左鍵點擊開始遊戲
            if not game_started and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for ball in balls:
                    ball.start_movement()
                game_started = True    # 遊戲開始

        if not game_over and game_started:
            # 更新遊戲對象
            paddle.update()

            # 累積時間並移動磚塊
            scroll_accumulator += scroll_speed
            if scroll_accumulator >= 1:
                for brick in bricks:
                    brick.rect.y += 1
                scroll_accumulator -= 1

            # 設定新生成的磚塊
            if all(brick.rect.top >= 0 for brick in bricks):
                if not bricks:
                    new_row_y = SCREEN_HEIGHT // 5  # 設置新行出現的初始位置
                    new_row = generate_row(new_row_y)
                    bricks.add(new_row)
                    all_sprites.add(new_row)
                else:
                    highest_brick_y = min(brick.rect.top for brick in bricks)
                    new_row_y = highest_brick_y - 30
                    new_row = generate_row(new_row_y)
                    bricks.add(new_row)
                    all_sprites.add(new_row)

            # 更新每顆球並檢查碰撞
            for ball in balls:
                ball.update()

                # 撞擊板子
                if pygame.sprite.collide_rect(ball, paddle):
                    ball.y_speed = -abs(ball.y_speed)

                # 撞擊磚塊
                hit_bricks = pygame.sprite.spritecollide(ball, bricks, True)
                for brick in hit_bricks:
                    score += 1
                    ball.y_speed = -ball.y_speed
                    bricks.remove(brick)
                    all_sprites.remove(brick)
                    hit_brick_sound.play()  # 播放撞擊磚塊的音效

                    # 特殊磚塊效果
                    if brick.color == ORANGE:   # 橘色磚塊
                        # 分裂出兩顆新球
                        for _ in range(2):  
                            new_ball = Ball(ball.rect.centerx, ball.rect.centery)
                            # 確保分裂球開始運動，並設置隨機方向
                            new_ball.x_speed = random.choice([3, -3])
                            new_ball.y_speed = -3  # 可以調整速度方向
                            new_ball.started = True
                            balls.add(new_ball)
                            all_sprites.add(new_ball)
                    elif brick.color == RED:    # 紅色磚塊
                        for b in list(bricks):
                            if abs(b.rect.x - brick.rect.x) <= 70 and abs(b.rect.y - brick.rect.y) <= 30:
                                bricks.remove(b)    # 四周的磚塊爆炸
                                all_sprites.remove(b)
                                score += 1

                # 移除超出螢幕底部的球
                for ball in list(balls):
                    if ball.rect.bottom > SCREEN_HEIGHT:
                        balls.remove(ball)
                        all_sprites.remove(ball)

             # 增加球的速度
            if not game_over and game_started:
                elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
                for ball in balls:
                    if ball.started:  # 確保只有開始移動的球才會加速
                        ball.x_speed = (3 + elapsed_time // 10) if ball.x_speed > 0 else -(3 + elapsed_time // 10)
                        ball.y_speed = -(3 + elapsed_time // 10) if ball.y_speed < 0 else (3 + elapsed_time // 10)

            # 檢查遊戲結束
            if not balls:
                game_over = True
                game_over_sound.play()  # 播放遊戲結束音效


        # 繪製遊戲物件
        all_sprites.draw(screen)

        # 顯示分數
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # 遊戲結束畫面
        if game_over:
            game_over_text = game_over_font.render(f"Game Over! Final Score: {score}", True, RED)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 20))
            continue_text = font.render("Press ENTER to restart or ESC to exit", True, WHITE)
            screen.blit(continue_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 20))

        # 更新螢幕
        pygame.display.flip()

        # 控制幀率
        clock.tick(60)

pygame.quit()

