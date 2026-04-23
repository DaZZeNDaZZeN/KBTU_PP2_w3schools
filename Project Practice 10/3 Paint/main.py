
import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
# base_layer stores saved drawings
base_layer = pygame.Surface((WIDTH, HEIGHT))
base_layer.fill((0, 0, 0)) # black background

colorRED = (255, 0, 0)
colorBLUE = (0, 0, 255)
colorGREEN = (0, 255, 0)
colorWHITE = (255, 255, 255)
colorBLACK = (0, 0, 0)

clock = pygame.time.Clock()

# internal variables
LMBpressed = False
THICKNESS = 5
curr_color = colorRED
current_tool = 'marker' # 'marker', 'rect', 'circle', 'eraser'

currX = 0
currY = 0
prevX = 0
prevY = 0

def calculate_rect(x1, y1, x2, y2):
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))

running = True

print("Controls: M: Marker, R: Rect, C: Circle, E: Eraser | 1: Red, 2: Blue, 3: Green")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # tool selection
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m: current_tool = 'marker'
            if event.key == pygame.K_r: current_tool = 'rect'
            if event.key == pygame.K_c: current_tool = 'circle'
            if event.key == pygame.K_e: current_tool = 'eraser'
            
            if event.key == pygame.K_1: curr_color = colorRED
            if event.key == pygame.K_2: curr_color = colorBLUE
            if event.key == pygame.K_3: curr_color = colorGREEN
            
            if event.key == pygame.K_EQUALS: THICKNESS += 1
            if event.key == pygame.K_MINUS: THICKNESS = max(1, THICKNESS - 1)
        
        # mouse logic
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            LMBpressed = True
            prevX, prevY = event.pos
        
        # logic for marker and eraser
        if event.type == pygame.MOUSEMOTION:
            currX, currY = event.pos
            if LMBpressed:
                if current_tool == 'marker':
                    # drawing directly to base_layer for marker to keep the trail
                    pygame.draw.line(base_layer, curr_color, (prevX, prevY), (currX, currY), THICKNESS)
                    prevX, prevY = currX, currY
                elif current_tool == 'eraser':
                    pygame.draw.circle(base_layer, colorBLACK, (currX, currY), THICKNESS * 2)
        
        # logic for saving shapes onto base_layer
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            LMBpressed = False
            currX, currY = event.pos
            
            # save shapes onto the base_layer
            if current_tool == 'rect':
                pygame.draw.rect(base_layer, curr_color, calculate_rect(prevX, prevY, currX, currY), THICKNESS)
            elif current_tool == 'circle':
                radius = int(((currX - prevX)**2 + (currY - prevY)**2)**0.5)
                pygame.draw.circle(base_layer, curr_color, (prevX, prevY), radius, THICKNESS)

    # draw the "saved" drawings
    screen.blit(base_layer, (0, 0))
    
    # draw "preview" shapes while dragging (only for shapes, not marker and eraser)
    if LMBpressed:
        if current_tool == 'rect':
            pygame.draw.rect(screen, curr_color, calculate_rect(prevX, prevY, currX, currY), THICKNESS)
        elif current_tool == 'circle':
            radius = int(((currX - prevX)**2 + (currY - prevY)**2)**0.5)
            pygame.draw.circle(screen, curr_color, (prevX, prevY), radius, THICKNESS)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
