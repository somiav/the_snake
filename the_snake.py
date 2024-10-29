import pygame
import random

# Настройки игры
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Константа для фона
BOARD_BACKGROUND_COLOR = BLACK

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()


class GameObject:
    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    def __init__(self):
        super().__init__(position=(GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE), body_color=GREEN)
        self.body = [self.position]
        self.length = 1
        self.direction = RIGHT

    def move(self):
        # Обновляем позицию головы
        new_head = (self.body[0][0] + self.direction[0] * GRID_SIZE,
                    self.body[0][1] + self.direction[1] * GRID_SIZE)
        # Если змея выходит за границы, появляется с другой стороны
        new_head = (new_head[0] % SCREEN_WIDTH, new_head[1] % SCREEN_HEIGHT)
        self.body.insert(0, new_head)
        if len(self.body) > self.length:
            self.body.pop()  # Удаляем последний сегмент, если длина превышает

    def update_direction(self, new_direction):
        # Изменяем направление, если оно не противоположное
        if (self.direction[0] + new_direction[0] != 0) or (self.direction[1] + new_direction[1] != 0):
            self.direction = new_direction

    def grow(self):
        self.length += 1

    def draw(self, surface):
        for segment in self.body:
            GameObject(segment, self.body_color).draw(surface)

    def check_collision(self):
        # Проверка на столкновение с самим собой
        return self.body[0] in self.body[1:]

    def get_head_position(self):
        return self.body[0]

    def reset(self):
        self.body = [self.position]
        self.length = 1
        self.direction = RIGHT

    @property
    def positions(self):  # Добавлено свойство positions
        return self.body


class Apple(GameObject):
    def __init__(self):
        super().__init__(body_color=RED)
        self.position = self.randomize_position()

    def randomize_position(self):
        return (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)


def handle_keys(snake):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        snake.update_direction(UP)
    elif keys[pygame.K_DOWN]:
        snake.update_direction(DOWN)
    elif keys[pygame.K_LEFT]:
        snake.update_direction(LEFT)
    elif keys[pygame.K_RIGHT]:
        snake.update_direction(RIGHT)


def main():
    snake = Snake()
    apple = Apple()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        handle_keys(snake)
        snake.move()

        # Проверка на столкновение с яблоком
        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.position = apple.randomize_position()

        # Проверка на столкновение с собой
        if snake.check_collision():
            print("Game Over! You collided with yourself.")
            running = False

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.flip()
        clock.tick(10)  # Ограничение FPS

    pygame.quit()


if __name__ == "__main__":
    main()
