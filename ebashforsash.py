import pygame

clock =pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((566,200)) # , flags=pygame.NOFRAME
pygame.display.set_caption('Pygame itProger Game')
icon = pygame.image.load('images/icon1.png').convert_alpha()
pygame.display.set_icon(icon)
# player
bg = pygame.image.load('images/bg.jpg').convert_alpha()
walk_left = [
    pygame.image.load('images/player_left/player_left1.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left2.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left3.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left4.png').convert_alpha()
]
walk_right = [
    pygame.image.load('images/player_right/player_right1.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right2.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right3.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right4.png').convert_alpha()
]

ghost = pygame.image.load('images/ghost.png').convert_alpha()
# ghost_x=620
ghost_list_in_game = []

player_anim_count = 0
bg_x=0
player_speed = 5
player_x = 150
player_y = 125
is_jump = False
jump_count = 8

bg_sound = pygame.mixer.Sound('sounds/123.mp3')
bg_sound.play()
ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer,2500)

label = pygame.font.Font( 'fonts/NotoSansHK-Black.ttf', 40)
lose_label = label.render('Вы проебали!', False, ('pink'))
restart_label = label.render('Играть заного!', False, ('yellow'))
restart_label_rect = restart_label.get_rect(topleft=(180,100))

bullets_left = 5
bullet = pygame.image.load('images/bullet.png').convert_alpha()
bullets = []


gameplay = True

running=True
while running:

    screen.blit(bg,(bg_x,0))
    screen.blit(bg, (bg_x+566, 0))

    if gameplay:

        player_rect = walk_left[0].get_rect(topleft=(player_x,player_y))
        if ghost_list_in_game:
             for (i, el) in enumerate(ghost_list_in_game):
                    screen.blit(ghost,el)
                    el.x -= 10
                    if el.x < -10:
                        ghost_list_in_game.pop(i)
                    if player_rect.colliderect(el):
                        gameplay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x>1:
            player_x -=player_speed
        elif keys[pygame.K_RIGHT] and player_x<530:
            player_x += player_speed
        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump= True
        else:
            if jump_count>= -8:
                if jump_count > 0:
                    player_y -=(jump_count**2)/2
                else:
                    player_y+=(jump_count**2)/2
                jump_count -= 1
            else:
                is_jump=False
                jump_count=8
        if player_anim_count ==3:
            player_anim_count = 0
        else:
            player_anim_count+=1
        bg_x -=2
        if bg_x==-566:
            bg_x=0
        # if keys[pygame.K_b]:
        #     bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))

        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 4
                if el.x > 560:
                    bullets.pop(i)
                if ghost_list_in_game:
                    for (index, ghost_el) in enumerate(ghost_list_in_game):
                        if el.colliderect(ghost_el):
                            ghost_list_in_game.pop(index)
                            bullets.pop(i)
    else:
        screen.fill('black')
        screen.blit(lose_label,(180, 50))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            ghost_list_in_game.clear()
            bullets.clear()

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(620,125)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_b and bullets_left > 0 :
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))
            bullets_left -= 1
    clock.tick(10)

