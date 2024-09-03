
import pygame
import numpy as np
from sys import exit
import os
from random import randint
import time

import snake_class as snake
import func as fc


def collision(idx, snakes) -> None:
    for snake_memb in snakes:
        for surf, rect in snake_memb.snake_tail[1:]:
            screen.blit(surf, rect)
    for snake_memb in snakes:
        screen.blit(snake_memb.head_surf, snake_memb.head_rect)
    end_surface = end_font.render(f"THE END: snake {idx} lost", False, "Black")
    end_rect = end_surface.get_rect(center = (screen_width/2, 50))
    screen.blit(end_surface, end_rect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


if __name__ == "__main__":

    print(fc.temp_path())

    pygame.init()
    screen_width = 1000
    screen_height = 780
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Dope Snake")
    clock = pygame.time.Clock() # clock object

    backgound_surface = pygame.image.load(os.path.join(fc.temp_path(), f"graphics{os.sep}dope_snake.png")).convert_alpha()
    score_font = pygame.font.Font(os.path.join(fc.temp_path(), f"fonts{os.sep}Silkscreen{os.sep}slkscr.ttf"), 50) # font object
    end_font = pygame.font.Font(os.path.join(fc.temp_path(), f"fonts{os.sep}Silkscreen{os.sep}slkscr.ttf"), 50)

    yum_lst = []
    yum_count = 0
    # score_surface = score_font.render(f"score: {yum_count}", False, "Black")
    # score_rect = score_surface.get_rect(center = (screen_width/2, 50))

    fps = 4 * 2
    spawn_time = 3
    loop_count = 999999
    true_loop_count = 0
    speedup = 0
    snake_dir = "up"
    countdown = 5
    turn = None
    turn_hist = []

    snake_speed = 20
    snake_len = 4

    snakes = []
    snakes.append(snake.Snake(snake_speed, (screen_width/2, 120), snake_len, (0, -1)))
    snakes.append(snake.Snake(snake_speed, (screen_width/2, screen_height-120), snake_len, (0, 1)))

    while True:

        while countdown > 0:
            screen.blit(backgound_surface, (-300, -100))
            end_surface = end_font.render(f"{countdown}", False, "Black")
            end_rect = end_surface.get_rect(center = (screen_width/2, 50))
            screen.blit(end_surface, end_rect)
            pygame.display.update()
            clock.tick(3)
            countdown -= 1

        loop_count += 1
        true_loop_count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if snakes[0].snake_dir != "down": snakes[0].snake_dir = "up"
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if snakes[0].snake_dir != "up": snakes[0].snake_dir = "down"
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if snakes[0].snake_dir != "left": snakes[0].snake_dir = "right"
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if snakes[0].snake_dir != "right": snakes[0].snake_dir = "left"

        snakes[1].turn = fc.snake_ai([x[1].topleft for x in yum_lst], snakes[1].head_rect.topleft, snakes[1].snake_dir, [x[1].topleft for x in snakes[1].snake_tail] + [x[1].topleft for x in snakes[0].snake_tail], turn_hist, snake_speed)
        if snakes[1].turn != None: snakes[1].snake_dir = snakes[1].turn

        screen.blit(backgound_surface, (-300, -100))

        if loop_count >= fps * spawn_time:
            yum_surf = pygame.Surface((20, 20))
            yum_surf.fill((160, 160, 160))
            col = True
            yum_coll = 0
            while col:
                yum_loc = ((randint(0, screen_width - snake_speed) // snake_speed * snake_speed), randint(0, screen_height - snake_speed) // snake_speed * snake_speed)
                for snake_memb in snakes:
                    snake_tail = snake_memb.snake_tail
                    for tail_memb in snake_tail:
                        if tail_memb[1].topleft == yum_loc:
                            yum_coll = 1
                            break
                    if yum_coll == 1:
                        yum_coll = 0
                        break
                else:
                    col = False
            yum_rect = yum_surf.get_rect(topleft=yum_loc)
            yum_lst.append([yum_surf, yum_rect])
            loop_count = 0

        for i, snake_memb in enumerate(snakes):

            if snakes[i].snake_dir == "left": snakes[i].head_rect.left -= snake_speed
            if snakes[i].snake_dir == "right": snakes[i].head_rect.right += snake_speed
            if snakes[i].snake_dir == "up": snakes[i].head_rect.top -= snake_speed
            if snakes[i].snake_dir == "down": snakes[i].head_rect.bottom += snake_speed

            if snakes[i].head_rect.left >= screen_width: snakes[i].head_rect.left = 0
            if snakes[i].head_rect.right <= 0: snakes[i].head_rect.right = screen_width
            if snakes[i].head_rect.top >= screen_height: snakes[i].head_rect.top = 0
            if snakes[i].head_rect.bottom <= 0: snakes[i].head_rect.bottom = screen_height

            snake_surf = pygame.Surface((20, 20))
            snake_surf.fill((102, 204, 0))
            snake_rect = snake_surf.get_rect(topleft=snakes[i].head_rect.topleft)
            snakes[i].snake_tail.insert(0, [snake_surf, snake_rect])

        for surf, rect in yum_lst:
            screen.blit(surf, rect)

        for i, snake_memb in enumerate(snakes):        
            for surf, rect in yum_lst:    
                if snakes[i].head_rect.colliderect(rect) == 1:
                    yum_lst.pop(yum_lst.index([surf, rect]))
                    yum_count += 1
                    break
            else:
                snakes[i].snake_tail.pop(-1)
            screen.blit(snakes[i].head_surf, snakes[i].head_rect)

            for surf, rect in snakes[i].snake_tail[1:]:
                screen.blit(surf, rect)
                
            for surf, rect in snakes[i].snake_tail[1:]:
                for k in range(2):
                    if snakes[k].head_rect.colliderect(rect) == 1:
                        print("collision")
                        collision(k, snakes)    
        
        if len(yum_lst) < 1: loop_count = 9999999
        if true_loop_count > 10 * (speedup * 2 + 2):
            fps += 2
            speedup += 1
            true_loop_count = 0

        # snakes[1].turn = fc.snake_ai([x[1].topleft for x in yum_lst], snakes[1].head_rect.topleft, snakes[1].snake_dir, [x[1].topleft for x in snakes[1].snake_tail] + [x[1].topleft for x in snakes[0].snake_tail], turn_hist, snake_speed)

        pygame.display.update()
        clock.tick(fps) # FPS ceiling