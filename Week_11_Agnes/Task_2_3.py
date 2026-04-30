import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

ARRAY_SIZE = 30
array = [random.randint(10, 350) for _ in range(ARRAY_SIZE)]
bar_width = WIDTH // ARRAY_SIZE


def draw_array(array, color_positions=None):
    screen.fill((30, 30, 30))

    for i, val in enumerate(array):
        color = (100, 200, 250)

        if color_positions and i in color_positions.get('compare', []):
            color = (255, 100, 100)

        if color_positions and i in color_positions.get('swap', []):
            color = (100, 255, 100)

        pygame.draw.rect(
            screen,
            color,
            (i * bar_width, HEIGHT - val, bar_width - 2, val)
        )

    pygame.display.flip()


def bubble_sort_visualize(array):
    n = len(array)

    for i in range(n):
        for j in range(0, n - i - 1):

            draw_array(array, {
                'compare': [j, j + 1],
                'swap': []
            })
            pygame.time.wait(50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]

                draw_array(array, {
                    'compare': [],
                    'swap': [j, j + 1]
                })
                pygame.time.wait(50)

    draw_array(array)


def main():
    draw_array(array)
    pygame.time.wait(1000)

    bubble_sort_visualize(array)

    pygame.time.wait(2000)
    pygame.quit()


if __name__ == "__main__":
    main()