import pygame
import time
import random

pygame.init()
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("贪吃蛇")

# 1. 初始化变量
snake_x = 300
snake_y = 300
x_change = 0
y_change = 0

snake_List = []
Length_of_snake = 1 

# 生成第一个食物（确保食物初始位置不会生成在蛇头上）
food_x = round(random.randrange(0, screen_width - 20) / 20.0) * 20.0
food_y = round(random.randrange(0, screen_height - 20) / 20.0) * 20.0

running = True
clock = pygame.time.Clock()

# 用于显示文字的字体
font_style = pygame.font.SysFont("bahnschrift", 25)

while running:
    # 2. 监听事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -20
                y_change = 0
            elif event.key == pygame.K_RIGHT:
                x_change = 20
                y_change = 0
            elif event.key == pygame.K_UP:
                x_change = 0
                y_change = -20
            elif event.key == pygame.K_DOWN:
                x_change = 0
                y_change = 20

    # 3. 撞墙判定（修复了撞墙后直接退出的问题）
    if snake_x >= screen_width or snake_x < 0 or snake_y >= screen_height or snake_y < 0:
        running = False
        # 这里我们只是退出 while 循环，不立刻关窗口，这样能看到红方块和结束提示

    # 4. 更新蛇头坐标
    snake_x += x_change
    snake_y += y_change

    # 5. 填充背景
    screen.fill((0, 0, 0))
    
    # 6. 画食物
    pygame.draw.rect(screen, (255, 0, 0), [food_x, food_y, 20, 20])

    # 7. 身体逻辑
    snake_Head = []
    snake_Head.append(snake_x)
    snake_Head.append(snake_y)
    snake_List.append(snake_Head)
    
    if len(snake_List) > Length_of_snake:
        del snake_List[0]

    # 画出蛇的所有身体方块
    for x in snake_List:
        pygame.draw.rect(screen, (0, 255, 0), [x[0], x[1], 20, 20])

    # 8. 吃到食物判定（这里加上了坐标绝对值判定，防止“跨过”食物）
    if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
        food_x = round(random.randrange(0, screen_width - 20) / 20.0) * 20.0
        food_y = round(random.randrange(0, screen_height - 20) / 20.0) * 20.0
        Length_of_snake += 1 

    # 9. 刷新屏幕
    pygame.display.update()
    clock.tick(10) 

# --- 撞墙后的停留页面 ---
# 这部分代码在 while 循环外面，所以游戏结束后会执行到这里，让画面停顿
dis_width = screen_width
dis_height = screen_height
mesg = font_style.render("Game Over! Press X to exit.", True, (255, 0, 0))
screen.blit(mesg, [dis_width / 6, dis_height / 3])
pygame.display.update()

# 给玩家 2 秒钟的反应时间看结果，然后才真正关闭
time.sleep(2)
pygame.quit()