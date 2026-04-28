import pygame
import sys
import time

pygame.init()

WIDTH, HEIGHT = 600, 100
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

numbers = [5, 3, 9, 1, 7, 4]
cell_width = WIDTH // len(numbers)


def draw_grid(highlight_index=None):
    screen.fill((30, 30, 30))
    for i, num in enumerate(numbers):
        color = (200, 200, 200)
        if i == highlight_index:
            color = (255, 100, 100)
        rect = pygame.Rect(i * cell_width, 0, cell_width - 2, HEIGHT)
        pygame.draw.rect(screen, color, rect)
        text = FONT.render(str(num), True, (0, 0, 0))
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)


def linear_search(target):
    for i, num in enumerate(numbers):
        draw_grid(i)
        pygame.display.flip()
        if num == target:
            return i
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        time.sleep(0.5)
    return -1


def main():
    target = 1
    draw_grid()
    pygame.display.flip()
    time.sleep(1)

    idx = linear_search(target)

    draw_grid(idx)
    pygame.display.flip()
    time.sleep(2)

    pygame.quit()


if __name__ == "__main__":
    main()
