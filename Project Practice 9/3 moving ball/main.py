import pygame as pg

pg.init()
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()

# variables
velocity = pg.Vector2(0, 0)
player_pos = pg.Vector2(screen.get_width() / 2, screen.get_height() / 2) 
acceleration = 100
friction = 50
max_speed = 20
running = True
player_size = 25 # radius
FPS = 60
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

    delta = clock.tick(FPS) / 1000.0


    pressed_keys = pg.key.get_pressed()
    
    # acceleration
    # delta time is used to get consistent movement     
    # that doesn't depend on FPS
    if pressed_keys[pg.K_UP]:
        velocity.y -= acceleration * delta
    if pressed_keys[pg.K_DOWN]:
        velocity.y += acceleration * delta
    if pressed_keys[pg.K_RIGHT]:
        velocity.x += acceleration * delta
    if pressed_keys[pg.K_LEFT]:
        velocity.x -= acceleration * delta

    # friction
    if velocity.x > friction * delta:
        velocity.x -= friction * delta
    elif velocity.x < -friction * delta:
        velocity.x += friction * delta
    else:
        velocity.x = 0

    if velocity.y > friction * delta:
        velocity.y -= friction * delta
    elif velocity.y < -friction * delta:
        velocity.y += friction * delta
    else:
        velocity.y = 0

    # capping the speed
    if velocity.x > max_speed:
        velocity.x = max_speed
    elif velocity.x < -max_speed:
        velocity.x = -max_speed
    
    # moving player
    player_pos += velocity

    # screen boundary check
    if player_pos.x < player_size:
        player_pos.x = player_size
        velocity.x = 0
    elif player_pos.x > screen.get_width() - player_size:
        player_pos.x = screen.get_width() - player_size
        velocity.x = 0
    if player_pos.y < player_size:
        player_pos.y = player_size
        velocity.y = 0
    elif player_pos.y > screen.get_height() - player_size:
        player_pos.y = screen.get_height() - player_size
        velocity.y = 0

    # white bg
    screen.fill("#FFFFFF")
    # player
    pg.draw.circle(screen, "red", player_pos, player_size)

    pg.display.flip()


pg.quit()

