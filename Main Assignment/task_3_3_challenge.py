import pygame
import sys
import random

pygame.init()

# -----------------------------
# Screen Setup
# -----------------------------
WIDTH, HEIGHT = 800, 700

ROWS, COLS = 6, 6
CELL_SIZE = 80
  
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Dynamic Programming Visualiser")

FONT = pygame.font.SysFont(None, 32)
SMALL_FONT = pygame.font.SysFont(None, 24)

clock = pygame.time.Clock()

# -----------------------------
# Obstacles
# -----------------------------
obstacles = {
    (1, 2),
    (2, 2),
    (3, 1),
    (4, 4)
}

# -----------------------------
# Valid Path
# -----------------------------
valid_path = []


# -----------------------------
# Draw Grid
# -----------------------------
def draw_grid(dp, highlight=None, show_path=False):

    screen.fill((255, 255, 255))

    title = FONT.render(
        "Grid Pathfinding with Obstacles",
        True,
        (0, 0, 0)
    )

    screen.blit(title, (20, 20))

    for r in range(ROWS):

        for c in range(COLS):

            rect = pygame.Rect(
                c * CELL_SIZE + 40,
                r * CELL_SIZE + 80,
                CELL_SIZE,
                CELL_SIZE
            )

            color = (220, 220, 220)

            # Obstacles
            if (r, c) in obstacles:
                color = (50, 50, 50)

            # Highlight current cell
            if highlight == (r, c):
                color = (255, 180, 180)

            # Final path
            if show_path and (r, c) in valid_path:
                color = (100, 255, 100)

            pygame.draw.rect(screen, color, rect)

            pygame.draw.rect(screen, (0, 0, 0), rect, 2)

            # Draw DP values
            if (r, c) not in obstacles:

                val = dp[r][c]

                if val is not None:

                    text = FONT.render(
                        str(val),
                        True,
                        (0, 0, 0)
                    )

                    text_rect = text.get_rect(center=rect.center)

                    screen.blit(text, text_rect)

    pygame.display.flip()


# -----------------------------
# Count Paths using DP
# -----------------------------
def count_paths():

    dp = [[0] * COLS for _ in range(ROWS)]

    for r in range(ROWS):

        for c in range(COLS):

            # Skip obstacles
            if (r, c) in obstacles:
                dp[r][c] = 0

            elif r == 0 and c == 0:
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

            pygame.time.wait(250)

    return dp


# -----------------------------
# Reconstruct One Valid Path
# -----------------------------
def reconstruct_path(dp):

    global valid_path

    r = ROWS - 1
    c = COLS - 1

    if dp[r][c] == 0:
        return

    path = []

    while (r, c) != (0, 0):

        path.append((r, c))

        # Move upward if possible
        if r > 0 and dp[r - 1][c] > 0:
            r -= 1

        # Otherwise move left
        elif c > 0 and dp[r][c - 1] > 0:
            c -= 1

    path.append((0, 0))

    valid_path = path

    draw_grid(dp, show_path=True)


# -----------------------------
# Coin Change Visualisation
# -----------------------------
def draw_coin_table(dp, coins, amount, highlight=None):

    screen.fill((255, 255, 255))

    title = FONT.render(
        "Coin Change DP Visualisation",
        True,
        (0, 0, 0)
    )

    screen.blit(title, (20, 20))

    for i in range(amount + 1):

        rect = pygame.Rect(
            40 + i * 60,
            200,
            50,
            50
        )

        color = (220, 220, 220)

        if i == highlight:
            color = (255, 180, 180)

        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)

        text = SMALL_FONT.render(str(dp[i]), True, (0, 0, 0))
        text_rect = text.get_rect(center=rect.center)

        screen.blit(text, text_rect)

        amount_text = SMALL_FONT.render(str(i), True, (0, 0, 0))

        screen.blit(amount_text, (50 + i * 60, 260))

    coin_text = FONT.render(
        f"Coins: {coins}",
        True,
        (0, 0, 0)
    )

    screen.blit(coin_text, (20, 100))

    pygame.display.flip()


def coin_change_visualisation():

    coins = [1, 3, 4]
    amount = 10

    # Infinity placeholder
    dp = [999] * (amount + 1)

    dp[0] = 0

    for i in range(1, amount + 1):

        for coin in coins:

            if i - coin >= 0:

                dp[i] = min(dp[i], dp[i - coin] + 1)

        draw_coin_table(dp, coins, amount, i)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.time.wait(500)

    result = FONT.render(
        f"Minimum coins needed for {amount}: {dp[amount]}",
        True,
        (0, 100, 0)
    )

    screen.blit(result, (20, 350))

    pygame.display.flip()

    pygame.time.wait(3000)


# -----------------------------
# Main
# -----------------------------
def main():

    # Empty DP table initially
    empty_dp = [[None] * COLS for _ in range(ROWS)]

    draw_grid(empty_dp)

    pygame.time.wait(1000)

    # Compute paths
    dp = count_paths()

    print("Total Paths:", dp[ROWS - 1][COLS - 1])

    pygame.time.wait(1000)

    # Reconstruct valid path
    reconstruct_path(dp)

    pygame.time.wait(3000)

    # Run Coin Change visualisation
    coin_change_visualisation()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()