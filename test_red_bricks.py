import pygame
import random

# 初始化pygame
pygame.init()

# 定義顏色
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)

# 設置屏幕尺寸
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("打磚塊遊戲")

# 定義遊戲對象類別
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20)

    def update(self):
        mouse_x = pygame.mouse.get_pos()[0]
        self.rect.centerx = mouse_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 15), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (7, 7), 7)
        self.rect = self.image.get_rect(center=(x, y))
        self.x_speed = random.choice([3, -3])
        self.y_speed = -3

    def update(self):
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

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((60, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color

# 初始化遊戲對象
paddle = Paddle()
ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
balls = pygame.sprite.Group(ball)

# 創建磚塊
bricks = pygame.sprite.Group()
brick_colors = [RED, BLUE]
for row in range(5):
    for col in range(10):
        color = random.choice(brick_colors)
        brick = Brick(col * 70 + 35, row * 30 + 50, color)
        bricks.add(brick)

# 所有的精靈組
all_sprites = pygame.sprite.Group()
all_sprites.add(paddle)
all_sprites.add(balls)
all_sprites.add(bricks)

# 分數與時間
score = 0
start_time = pygame.time.get_ticks()
font = pygame.font.SysFont("Arial", 20)

# 遊戲主循環
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    # 事件處理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 更新遊戲對象
    paddle.update()

    # 更新每顆球並檢查碰撞
    for ball in list(balls):  # 確保多球處理正確
        ball.update()

        # 撞擊板子
        if pygame.sprite.collide_rect(ball, paddle):
            ball.y_speed = -abs(ball.y_speed)  # 確保球向上反彈

        # 撞擊磚塊
        hit_bricks = pygame.sprite.spritecollide(ball, bricks, False)
        for brick in hit_bricks:
            score += 1  # 增加分數
            ball.y_speed = -ball.y_speed  # 磚塊碰撞後反彈
            bricks.remove(brick)
            all_sprites.remove(brick)

            # 特殊磚塊效果
            # if brick.color == ORANGE:  # 橘色磚塊分裂三顆球
            #     for _ in range(2):
            #         new_ball = Ball(ball.rect.centerx, ball.rect.centery)
            #         balls.add(new_ball)
            #         all_sprites.add(new_ball)
            if brick.color == RED:  # 紅色磚塊爆炸周圍
                for b in list(bricks):
                    if abs(b.rect.x - brick.rect.x) <= 70 and abs(b.rect.y - brick.rect.y) <= 30:
                        bricks.remove(b)
                        all_sprites.remove(b)
                        score += 1  # 炸毀的磚塊增加分數

        # 移除超出螢幕底部的球
        if ball.rect.bottom > SCREEN_HEIGHT:
            balls.remove(ball)
            all_sprites.remove(ball)

    # 增加球的速度
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # 秒
    for ball in balls:
        ball.x_speed = (3 + elapsed_time // 10) if ball.x_speed > 0 else -(3 + elapsed_time // 10)
        ball.y_speed = -(3 + elapsed_time // 10) if ball.y_speed < 0 else (3 + elapsed_time // 10)

    # 顯示分數
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # 檢查遊戲結束
    if not balls:
        running = False

    # 畫出所有遊戲對象
    all_sprites.draw(screen)

    # 更新螢幕
    pygame.display.flip()

    # 控制幀率
    clock.tick(60)

# 顯示遊戲結束訊息
game_over_text = font.render("Game Over!", True, RED)
screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2))
pygame.display.flip()

# 等待幾秒鐘後退出
pygame.time.wait(3000)

# 退出pygame
pygame.quit()
