import pygame
import math

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
# Added tools: 'square', 'right_tri', 'equi_tri', 'rhombus'
current_tool = 'marker' 

currX = 0
currY = 0
prevX = 0
prevY = 0

def calculate_rect(x1, y1, x2, y2):
    """Calculates the rectangle area between two points."""
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))

def draw_shape(surface, tool, color, start_pos, end_pos, thickness):
    """Handles the drawing logic for various geometric shapes."""
    x1, y1 = start_pos
    x2, y2 = end_pos
    dx = x2 - x1
    dy = y2 - y1

    if tool == 'rect':
        pygame.draw.rect(surface, color, calculate_rect(x1, y1, x2, y2), thickness)
    
    elif tool == 'circle':
        radius = int((dx**2 + dy**2)**0.5)
        pygame.draw.circle(surface, color, (x1, y1), radius, thickness)

    elif tool == 'square':
        # Side length is the maximum of the horizontal or vertical drag
        side = max(abs(dx), abs(dy))
        # Ensure it draws in the direction of the mouse
        s_x = x1 if x2 > x1 else x1 - side
        s_y = y1 if y2 > y1 else y1 - side
        pygame.draw.rect(surface, color, (s_x, s_y, side, side), thickness)

    elif tool == 'right_tri':
        # Vertices: Start point, Horizontal projection, Vertical projection
        points = [(x1, y1), (x1, y2), (x2, y2)]
        pygame.draw.polygon(surface, color, points, thickness)

    elif tool == 'equi_tri':
        # Calculates third point for an equilateral-ish triangle based on distance
        side = int((dx**2 + dy**2)**0.5)
        height = side * math.sqrt(3) / 2
        # Points based on start point as top vertex
        points = [(x1, y1), (x1 - side//2, y1 + height), (x1 + side//2, y1 + height)]
        pygame.draw.polygon(surface, color, points, thickness)

    elif tool == 'rhombus':
        # Vertices based on the bounding box of the drag
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        points = [(mid_x, y1), (x2, mid_y), (mid_x, y2), (x1, mid_y)]
        pygame.draw.polygon(surface, color, points, thickness)

running = True

print("Controls:")
print("M: Marker, R: Rect, C: Circle, E: Eraser")
print("S: Square, T: Right Triangle, Q: Equi Triangle, H: Rhombus")
print("1: Red, 2: Blue, 3: Green | +/-: Thickness")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # tool selection extension
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m: current_tool = 'marker'
            if event.key == pygame.K_r: current_tool = 'rect'
            if event.key == pygame.K_c: current_tool = 'circle'
            if event.key == pygame.K_e: current_tool = 'eraser'
            # New Keys
            if event.key == pygame.K_s: current_tool = 'square'
            if event.key == pygame.K_t: current_tool = 'right_tri'
            if event.key == pygame.K_q: current_tool = 'equi_tri'
            if event.key == pygame.K_h: current_tool = 'rhombus'
            
            if event.key == pygame.K_1: curr_color = colorRED
            if event.key == pygame.K_2: curr_color = colorBLUE
            if event.key == pygame.K_3: curr_color = colorGREEN
            
            if event.key == pygame.K_EQUALS: THICKNESS += 1
            if event.key == pygame.K_MINUS: THICKNESS = max(1, THICKNESS - 1)
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            LMBpressed = True
            prevX, prevY = event.pos
        
        if event.type == pygame.MOUSEMOTION:
            currX, currY = event.pos
            if LMBpressed:
                if current_tool == 'marker':
                    pygame.draw.line(base_layer, curr_color, (prevX, prevY), (currX, currY), THICKNESS)
                    prevX, prevY = currX, currY
                elif current_tool == 'eraser':
                    pygame.draw.circle(base_layer, colorBLACK, (currX, currY), THICKNESS * 2)
        
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            LMBpressed = False
            currX, currY = event.pos
            # Draw the final shape to the base layer
            if current_tool not in ['marker', 'eraser']:
                draw_shape(base_layer, current_tool, curr_color, (prevX, prevY), (currX, currY), THICKNESS)

    # Render base drawings
    screen.blit(base_layer, (0, 0))
    
    # Render preview (temporary visual while dragging)
    if LMBpressed and current_tool not in ['marker', 'eraser']:
        draw_shape(screen, current_tool, curr_color, (prevX, prevY), (currX, currY), THICKNESS)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
