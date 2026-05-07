import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 600, 600
ROWS, COLS = 6, 6
CELL_SIZE = WIDTH // COLS

screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()


def draw_grid(dp, highlight=None):

    screen.fill((255, 255, 255))

    for r in range(ROWS):

        for c in range(COLS):

            rect = pygame.Rect(
                c * CELL_SIZE,
                r * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            color = (200, 200, 200)

            if highlight == (r, c):
                color = (255, 180, 180)

            pygame.draw.rect(screen, color, rect)

            pygame.draw.rect(screen, (0, 0, 0), rect, 1)

            val = dp[r][c]

            if val is not None:

                text = FONT.render(str(val), True, (0, 0, 0))

                text_rect = text.get_rect(center=rect.center)

                screen.blit(text, text_rect)

    pygame.display.flip()


def count_paths():

    dp = [[None] * COLS for _ in range(ROWS)]

    for r in range(ROWS):

        for c in range(COLS):

            if r == 0 and c == 0:

                dp[r][c] = 1

            else:

                up = dp[r - 1][c] if r > 0 else 0
                left = dp[r][c - 1] if c > 0 else 0

                dp[r][c] = up + left

            draw_grid(dp, (r, c))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.time.wait(300)

    return dp[ROWS - 1][COLS - 1]


def main():

    draw_grid([[None] * COLS for _ in range(ROWS)])

    pygame.time.wait(1000)

    total_paths = count_paths()

    print(f"Total unique paths: {total_paths}")

    pygame.time.wait(3000)

    pygame.quit()


if __name__ == "__main__":
    main()