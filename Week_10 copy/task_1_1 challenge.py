import pygame
import sys
import time

pygame.init()

WIDTH, HEIGHT = 600, 150
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont(None, 36)
SMALL_FONT = pygame.font.SysFont(None, 28)
clock = pygame.time.Clock()

numbers = [5, 3, 9, 1, 7, 4]
cell_width = WIDTH // len(numbers)


def draw_grid(highlight_index=None, comparisons=0, message=""):
    screen.fill((30, 30, 30))

    # Draw number cells
    for i, num in enumerate(numbers):
        color = (200, 200, 200)
        if i == highlight_index:
            color = (255, 100, 100)

        rect = pygame.Rect(i * cell_width, 0, cell_width - 2, 80)
        pygame.draw.rect(screen, color, rect)

        text = FONT.render(str(num), True, (0, 0, 0))
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    # Draw comparison counter
    comp_text = SMALL_FONT.render(f"Comparisons: {comparisons}", True, (255, 255, 255))
    screen.blit(comp_text, (10, 90))

    # Draw message (result or prompt)
    msg_text = SMALL_FONT.render(message, True, (255, 255, 0))
    screen.blit(msg_text, (10, 120))


def linear_search(target):
    comparisons = 0
    for i, num in enumerate(numbers):
        comparisons += 1
        draw_grid(i, comparisons, f"Searching for {target}...")
        pygame.display.flip()

        # Allow quitting during animation
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        time.sleep(0.5)

        if num == target:
            return i, comparisons

    return -1, comparisons


def get_user_input():
    """Simple keyboard input inside pygame window."""
    user_text = ""
    entering = True

    while entering:
        draw_grid(message=f"Enter target: {user_text}")
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_text.isdigit():
                        return int(user_text)
                    user_text = ""  # reset invalid input

                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]

                else:
                    if event.unicode.isdigit():
                        user_text += event.unicode


def main():
    while True:
        target = get_user_input()

        index, comparisons = linear_search(target)

        if index != -1:
            msg = f"Found {target} at index {index} in {comparisons} comparisons"
        else:
            msg = f"{target} not found after {comparisons} comparisons"

        draw_grid(index if index != -1 else None, comparisons, msg)
        pygame.display.flip()
        time.sleep(2)


if __name__ == "__main__":
    main()
