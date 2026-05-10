import pygame
import random
import sys

pygame.init()

# ===================== SETUP =====================
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting Visualiser")

FONT = pygame.font.SysFont(None, 28)
clock = pygame.time.Clock()

ARRAY_SIZE = 50
bar_width = WIDTH // ARRAY_SIZE


def generate_array():
    return [random.randint(20, 400) for _ in range(ARRAY_SIZE)]


array = generate_array()

# Buttons
buttons = {
    "Bubble": pygame.Rect(20, 10, 120, 40),
    "Selection": pygame.Rect(160, 10, 120, 40),
    "Merge": pygame.Rect(300, 10, 120, 40),
    "Reset": pygame.Rect(440, 10, 120, 40),
}

# State
sorting = False
sort_type = None
i = j = 0
min_idx = 0

merge_stack = []


# ===================== DRAW =====================
def draw_array(arr, highlight=None):
    screen.fill((30, 30, 30))

    for idx, val in enumerate(arr):
        color = (100, 200, 250)

        if highlight:
            if idx in highlight.get("compare", []):
                color = (255, 100, 100)
            if idx in highlight.get("swap", []):
                color = (100, 255, 100)

        pygame.draw.rect(
            screen,
            color,
            (idx * bar_width, HEIGHT - val, bar_width - 2, val)
        )

    draw_buttons()
    pygame.display.flip()


def draw_buttons():
    for text, rect in buttons.items():
        pygame.draw.rect(screen, (200, 200, 200), rect)
        label = FONT.render(text, True, (0, 0, 0))
        screen.blit(label, (rect.x + 10, rect.y + 10))


# ===================== SORT STEPS =====================
def bubble_step():
    global i, j, sorting

    if i < len(array):
        if j < len(array) - i - 1:
            highlight = {"compare": [j, j + 1]}

            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                highlight = {"swap": [j, j + 1]}

            j += 1
            return highlight

        else:
            j = 0
            i += 1

    else:
        sorting = False

    return None


def selection_step():
    global i, j, min_idx, sorting

    if i < len(array):
        if j < len(array):
            highlight = {"compare": [min_idx, j]}

            if array[j] < array[min_idx]:
                min_idx = j

            j += 1
            return highlight

        else:
            array[i], array[min_idx] = array[min_idx], array[i]
            highlight = {"swap": [i, min_idx]}

            i += 1
            j = i + 1
            min_idx = i

            return highlight

    else:
        sorting = False

    return None


# Simple merge sort simulation (not full recursion for simplicity)
def merge_sort_setup():
    global merge_stack
    size = 1
    merge_stack = []

    while size < len(array):
        for left in range(0, len(array), 2 * size):
            mid = min(left + size - 1, len(array) - 1)
            right = min(left + 2 * size - 1, len(array) - 1)
            merge_stack.append((left, mid, right))
        size *= 2


def merge_step():
    global sorting

    if not merge_stack:
        sorting = False
        return None

    left, mid, right = merge_stack.pop(0)

    temp = sorted(array[left:right + 1])
    for i in range(len(temp)):
        array[left + i] = temp[i]

    return {"swap": list(range(left, right + 1))}


# ===================== MAIN =====================
def main():
    global sorting, sort_type, i, j, min_idx, array

    running = True

    while running:
        highlight = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if buttons["Bubble"].collidepoint(pos):
                    sorting = True
                    sort_type = "bubble"
                    i = j = 0

                elif buttons["Selection"].collidepoint(pos):
                    sorting = True
                    sort_type = "selection"
                    i = 0
                    j = 1
                    min_idx = 0

                elif buttons["Merge"].collidepoint(pos):
                    sorting = True
                    sort_type = "merge"
                    merge_sort_setup()

                elif buttons["Reset"].collidepoint(pos):
                    array = generate_array()
                    sorting = False

        # Run sorting step
        if sorting:
            if sort_type == "bubble":
                highlight = bubble_step()
            elif sort_type == "selection":
                highlight = selection_step()
            elif sort_type == "merge":
                highlight = merge_step()

        draw_array(array, highlight)

        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()