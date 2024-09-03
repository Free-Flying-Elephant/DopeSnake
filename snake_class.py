
import pygame

class Snake:

    def __init__(self, snake_speed: int, start_coord: tuple[float, float], snake_len: int, initial_dir: tuple[int, int]) -> None:
        self.head_surf = pygame.Surface((snake_speed, snake_speed))
        self.head_surf.fill((80, 190, 0))
        self.head_rect = self.head_surf.get_rect(topleft=(start_coord[0], start_coord[1]))

        self.snake_tail = []
        for i in range(snake_len):
            snake_surf = pygame.Surface((snake_speed, snake_speed))
            snake_surf.fill((102, 204, 0))
            snake_rect = snake_surf.get_rect(topleft=(self.head_rect.topleft[0] + snake_speed * initial_dir[0] * (i), self.head_rect.topleft[1] + snake_speed * initial_dir[1] * (i)))
            self.snake_tail.append([snake_surf, snake_rect])

        if initial_dir[1] == -1:
            self.snake_dir = "down"
            self.turn = None
        else:
            self.snake_dir = "up"
            self.turn = None