# set up and display
import pygame
import sys
timer = pygame.time.Clock()

from pygame.locals import *
pygame.init()

pygame.display.set_caption('game') #game title

window_size = (600,400) #game window size

screen = pygame.display.set_mode(window_size, 0, 32)

display = pygame.Surface((300, 200))

player_sprite = pygame.image.load('adventurer-idle-01.png')

grass_block = pygame.image.load('grass.png')
dirt_block = pygame.image.load('dirt.png')
tile_size = grass_block.get_width()
scrolls = [0,0] #camera width


map = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
       ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
       ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
       ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
       ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
       ['2','2','2','0','0','0','0','2','2','2','2','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2','2','2'],
       ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
       ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
       ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
       ['2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2'],
       ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
       ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
       ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
       ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
       ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
       ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']]

#player collision with tiles
def coll_test(rect, tiles):
    coll_list = []
    for tile in tiles:
       if rect.colliderect(tile):
           coll_list.append(tile)
    return coll_list

def move(rect, movement, tiles):
    coll_types = {'left': False, 'right': False, 'top': False, 'bottom': False}
    rect.x += movement[0]
    coll_list = coll_test(rect, tiles)
    for tile in coll_list:
        if movement[0] > 0:
            rect.right = tile.left
            coll_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            coll_types['left'] = True

    rect.y += movement[1]
    coll_list = coll_test(rect, tiles)
    for tile in coll_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            coll_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            coll_types['top'] = True
    return rect, coll_types

#horizontal movement 
movement_right = False
movement_left = False

#vertical movement (jump)
player_ymomentum = 0
airtime = 0

def gamemap_load(path):
    f = open(path + '.txt','r')
    content = f.read()
    f.close()
    content = content.split('\n')
    game_map = []
    for row in content:
        game_map.append(list(row))
    return game_map

player_rect = pygame.Rect(50, 50, player_sprite.get_width(), player_sprite.get_height())
coll_rect = pygame.Rect(100,100,100,50)
parallax_object = [[0.15,[100,10,50,500],[0.15,[200,20,30,500]],[0.15,[150,23,80,500]],[0.15,[130,15,70,500]],[0.15,[115,10,50,500],]]]


# game loop
while True:
    game_background = pygame.image.load("clouds.png")
    screen.blit(game_background, [0, 0])
    scrolls[0] += (player_rect.x-scroll[0]-155)/15
    scrolls[1] += (player_rect.y-scroll[1]-105)/15
    scroll = scrolls.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    pygame.draw.rect(display,(7,80,75),pygame.Rect(0,))

    display.fill((146,234,254))
    y = 0
    tile_rects = []
    for row in map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(dirt_block, (x * tile_size-scroll[0], y * tile_size-scroll[1]))
            if tile == '2':
                display.blit(grass_block, (x * tile_size-scroll[0], y * tile_size-scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))
            x += 1
        y += 1

    # player movement
    p_movement = [0, 0]
    if movement_right:
        p_movement[0] += 2
    if movement_left:
        p_movement[0] -= 2
    p_movement[1] += player_ymomentum
    player_ymomentum += 0.2
    if player_ymomentum > 3:
        player_ymomentum = 3
        
    player_rect, collisions = move(player_rect, p_movement, tile_rects)

    if collisions['bottom']:
        player_ymomentum = 0
        airtime = 0
    else:
        airtime += 1

    display.blit(player_sprite, (player_rect.x-scroll[0], player_rect.y- scroll[1])) # put one surface to another


    for event in pygame.event.get():
        if event.type == QUIT:     # check for window quitm
            pygame.quit()    # stop game
            sys.exit()
        if event.type == KEYDOWN:  # triggered anytime key in keyboard is pressed down
            if event.key == K_RIGHT:
                movement_right = True
            if event.key == K_LEFT:
                movement_left = True
            if event.key == K_UP:
                if airtime < 7:
                    player_ymomentum = -5
        if event.type == KEYUP: # triggered anytime key is released
            if event.key == K_RIGHT:
                movement_right = False
            if event.key == K_LEFT:
                movement_left = False


    surf = (pygame.transform.scale(display, window_size))
    screen.blit(surf, (0, 0))
    pygame.display.update( ) # display update
    timer.tick(60)  # frame rate 60fps







