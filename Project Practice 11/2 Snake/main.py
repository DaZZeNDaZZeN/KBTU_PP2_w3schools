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

def draw_grid_chess(color1, color2):
    colors = [color1, color2]
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colors[(i + j) % 2], (i * CELL, j * CELL, CELL, CELL))

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        
        self.body[0].x += self.dx
        self.body[0].y += self.dy

        # Wrap around logic
        if self.body[0].x > WIDTH // CELL - 1: self.body[0].x = 0
        if self.body[0].x < 0: self.body[0].x = WIDTH // CELL - 1
        if self.body[0].y > HEIGHT // CELL - 1: self.body[0].y = 0
        if self.body[0].y < 0: self.body[0].y = HEIGHT // CELL - 1

    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_collision(self, food):
        global score
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            # Snake grows based on the food weight
            for _ in range(food.weight):
                self.body.append(Point(self.body[-1].x, self.body[-1].y))
            
            score += food.weight
            food.generate_random_pos()

class Food:
    def __init__(self, snake):
        self.snake = snake
        self.pos = Point(0, 0)
        self.weight = 1
        self.timer = 0 # Track how many frames the food has existed
        self.life_span = 40 # Food moves after 40 frames  
        self.generate_random_pos()

    def draw(self):
        # Draw different colors/sizes based on weight
        color = colorGREEN if self.weight == 1 else colorBLUE
        pygame.draw.rect(screen, color, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))
        
        # draw timer bar above food
        timer_width = (self.life_span - self.timer) * (CELL / self.life_span)
        pygame.draw.rect(screen, colorRED, (self.pos.x * CELL, self.pos.y * CELL - 5, timer_width, 5))

    def generate_random_pos(self):
        # Reset timer whenever new food is generated
        self.timer = 0
        # Random weight: 1 (common) or 2 (special)
        self.weight = random.choices([1, 2], weights=[80, 20])[0]
        
        while True:
            self.pos.x = random.randint(0, WIDTH // CELL - 1)
            self.pos.y = random.randint(0, HEIGHT // CELL - 1)
            # Ensure food doesn't spawn inside the snake
            if not any(segment == self.pos for segment in self.snake.body):
                break

    def update(self):
        # Increment timer and check if food should disappear/relocate
        self.timer += 1
        if self.timer >= self.life_span:
            self.generate_random_pos()

# Game Setup
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
            if event.key == pygame.K_RIGHT and snake.dx != -1:
                snake.dx, snake.dy = 1, 0
            elif event.key == pygame.K_LEFT and snake.dx != 1:
                snake.dx, snake.dy = -1, 0
            elif event.key == pygame.K_DOWN and snake.dy != -1:
                snake.dx, snake.dy = 0, 1
            elif event.key == pygame.K_UP and snake.dy != 1:
                snake.dx, snake.dy = 0, -1

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

    # Game Logic
    snake.move()
    food.update() # Check if food timer expired
    snake.check_collision(food)

    # Drawing
    snake.draw()
    food.draw()

    # UI
    score_text = font.render(f"Score: {score}", True, colorWHITE)
    level_text = font.render(f"Level: {level}", True, colorWHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 35))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
