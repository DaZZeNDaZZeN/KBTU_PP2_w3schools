import pygame
import random

# colors
colorWHITE = (255, 255, 255)
colorGRAY = (200, 200, 200)
colorBLACK = (0, 0, 0)
colorRED = (255, 0, 0)
colorGREEN = (0, 255, 0)
colorBLUE = (0, 0, 255)
colorYELLOW = (255, 255, 0)

pygame.init()

WIDTH = 600
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))

font = pygame.font.SysFont("Verdana", 20)

# size of the cell
CELL = 40

def draw_grid():
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colorGRAY, (i * CELL, j * CELL, CELL, CELL), 1)

def draw_grid_chess(color1, color2):
    colors = [color1, color2]

    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colors[(i + j) % 2], (i * CELL, j * CELL, CELL, CELL))

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x}, {self.y}"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        # direction to move
        self.dx = 1
        self.dy = 0

    def move(self):
        # moves everything towards head
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        
        # moves head
        self.body[0].x += self.dx
        self.body[0].y += self.dy

        # checks the right border
        if self.body[0].x > WIDTH // CELL - 1:
            self.body[0].x = 0
        # checks the left border
        if self.body[0].x < 0:
            self.body[0].x = WIDTH // CELL - 1
        # checks the bottom border
        if self.body[0].y > HEIGHT // CELL - 1:
            self.body[0].y = 0
        # checks the top border
        if self.body[0].y < 0:
            self.body[0].y = HEIGHT // CELL - 1


    def draw(self):
        # draws head in different color than the rest of the body
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_collision(self, food):
        global score
        # checks collision with food and creates new body segment if eaten
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            print("Got food!")
            self.body.append(Point(head.x, head.y))
            food.generate_random_pos()
            score += 1

class Food:
    def __init__(self, snake):
        self.pos = Point(9, 9)
        self.snake = snake

    def draw(self):
        pygame.draw.rect(screen, colorGREEN, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def generate_random_pos(self):
        # food will not overlap the body of the snake
        self.pos.x = random.randint(0, WIDTH // CELL - 1)
        self.pos.y = random.randint(0, HEIGHT // CELL - 1)
        while True:
            for i in self.snake.body:
                if self.pos == i:
                    self.pos.x = random.randint(0, WIDTH // CELL - 1)
                    self.pos.y = random.randint(0, HEIGHT // CELL - 1)
                    break
            else:
                break


FPS = 5
level = 0
score = 0
clock = pygame.time.Clock()

snake = Snake()
food = Food(snake)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # movement
            if event.key == pygame.K_RIGHT:
                snake.dx = 1
                snake.dy = 0
            elif event.key == pygame.K_LEFT:
                snake.dx = -1
                snake.dy = 0
            elif event.key == pygame.K_DOWN:
                snake.dx = 0
                snake.dy = 1
            elif event.key == pygame.K_UP:
                snake.dx = 0
                snake.dy = -1

    # changing level depending on score
    if score == 3 and level == 0:
        level += 1
    elif score == 6 and level == 1:
        level += 1
    elif score == 9 and level == 2:
        level += 1
    elif score == 12 and level == 3:
        level += 1

    screen.fill(colorBLACK)
    
    # drawing different background for each level
    # and increase speed through fps
    if level == 0:
        draw_grid_chess(colorBLACK, colorBLACK)
        FPS = 5
    elif level == 1:
        draw_grid_chess(colorBLACK, colorWHITE)
        FPS = 6
    elif level == 2:
        draw_grid_chess("#FF00FF", "#C04000") # purple and orange
        FPS = 8
    elif level == 3:
        draw_grid_chess("#00FFFF", "#3333EE") # cyan and blue
        FPS = 10
    elif level == 4:
        draw_grid_chess("#4E0707", "#BC544B") # dark red and pink
        FPS = 15

    snake.move()
    snake.check_collision(food)

    snake.draw()
    food.draw()

    # drawing score and level to the screen
    score_text = font.render(f"score:{score}", True, "#FFFFFF")
    level_text = font.render(f"lvl:{level}", True, "#FFFFFF")
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 30))


    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
