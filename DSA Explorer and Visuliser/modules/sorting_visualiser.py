"""
Task 2.3 Challenge - Sorting Algorithm Visualiser
- Bubble Sort, Selection Sort, Merge Sort
- On-screen buttons to choose algorithm and reset
- Back button to return to main menu
"""

import pygame
import sys
import random

ARRAY_SIZE = 40


def run(screen, font, clock, WIDTH, HEIGHT):
    small = pygame.font.SysFont(None, 24)
    bar_width = (WIDTH - 40) // ARRAY_SIZE
    array = [random.randint(20, HEIGHT - 120) for _ in range(ARRAY_SIZE)]

    buttons = {
        "Bubble":    pygame.Rect(20,  10, 110, 38),
        "Selection": pygame.Rect(145, 10, 110, 38),
        "Merge":     pygame.Rect(270, 10, 110, 38),
        "Reset":     pygame.Rect(395, 10, 110, 38),
        "Back":      pygame.Rect(WIDTH - 130, 10, 110, 38),
    }

    sorting = False
    sort_type = None
    i = j = 0
    min_idx = 0
    merge_stack = []
    comparisons = 0
    swaps = 0
    complete = False
    highlight = None
    status_msg = "Choose an algorithm to start"

    def draw_array(hl=None):
        screen.fill((20, 22, 30))

        # Title
        t = font.render("Sorting Algorithm Visualiser", True, (180, 200, 255))
        screen.blit(t, (WIDTH // 2 - t.get_width() // 2, 58))

        # Bars
        for idx, val in enumerate(array):
            color = (60, 120, 220)
            if hl:
                if idx in hl.get("compare", []):   color = (220, 80, 80)
                if idx in hl.get("swap", []):       color = (80, 220, 120)
                if idx in hl.get("sorted", []):     color = (200, 180, 60)
            if complete:
                color = (80, 220, 120)
            x = 20 + idx * bar_width
            pygame.draw.rect(screen, color, (x, HEIGHT - val - 60, bar_width - 2, val), border_radius=2)

        # Buttons
        btn_colors = {
            "Bubble": (80, 120, 200), "Selection": (80, 160, 180),
            "Merge": (120, 80, 200), "Reset": (180, 130, 60), "Back": (100, 100, 120)
        }
        for lbl, rect in buttons.items():
            c = btn_colors[lbl]
            pygame.draw.rect(screen, c, rect, border_radius=8)
            bt = small.render(lbl, True, (240, 240, 240))
            screen.blit(bt, bt.get_rect(center=rect.center))

        # Stats
        st = small.render(f"Comparisons: {comparisons}  |  Swaps: {swaps}  |  {status_msg}", True, (160, 170, 200))
        screen.blit(st, (20, HEIGHT - 35))

        pygame.display.flip()

    def merge_sort_setup():
        size = 1
        steps = []
        while size < len(array):
            for left in range(0, len(array), 2 * size):
                mid = min(left + size - 1, len(array) - 1)
                right = min(left + 2 * size - 1, len(array) - 1)
                steps.append((left, mid, right))
            size *= 2
        return steps

    def bubble_step():
        nonlocal i, j, sorting, comparisons, swaps, complete, status_msg
        if i < len(array):
            if j < len(array) - i - 1:
                comparisons += 1
                hl = {"compare": [j, j + 1]}
                if array[j] > array[j + 1]:
                    array[j], array[j + 1] = array[j + 1], array[j]
                    hl = {"swap": [j, j + 1]}
                    swaps += 1
                j += 1
                return hl
            else:
                j = 0; i += 1
        else:
            sorting = False; complete = True; status_msg = "Sorted!"
        return None

    def selection_step():
        nonlocal i, j, min_idx, sorting, comparisons, swaps, complete, status_msg
        if i < len(array) - 1:
            if j < len(array):
                comparisons += 1
                hl = {"compare": [min_idx, j]}
                if array[j] < array[min_idx]:
                    min_idx = j
                j += 1
                return hl
            else:
                if min_idx != i:
                    array[i], array[min_idx] = array[min_idx], array[i]
                    swaps += 1
                hl = {"swap": [i, min_idx]}
                i += 1; j = i + 1; min_idx = i
                return hl
        else:
            sorting = False; complete = True; status_msg = "Sorted!"
        return None

    def merge_step():
        nonlocal sorting, swaps, complete, status_msg
        if not merge_stack:
            sorting = False; complete = True; status_msg = "Sorted!"; return None
        left, mid, right = merge_stack.pop(0)
        temp = sorted(array[left:right + 1])
        for k in range(len(temp)):
            if array[left + k] != temp[k]:
                swaps += 1
            array[left + k] = temp[k]
        return {"swap": list(range(left, right + 1))}

    running = True
    while running:
        hl = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if buttons["Bubble"].collidepoint(pos):
                    sorting = True; sort_type = "bubble"; complete = False
                    i = j = comparisons = swaps = 0; status_msg = "Bubble Sort"
                elif buttons["Selection"].collidepoint(pos):
                    sorting = True; sort_type = "selection"; complete = False
                    i = 0; j = 1; min_idx = 0; comparisons = swaps = 0; status_msg = "Selection Sort"
                elif buttons["Merge"].collidepoint(pos):
                    sorting = True; sort_type = "merge"; complete = False
                    merge_stack = merge_sort_setup(); comparisons = swaps = 0; status_msg = "Merge Sort"
                elif buttons["Reset"].collidepoint(pos):
                    array[:] = [random.randint(20, HEIGHT - 120) for _ in range(ARRAY_SIZE)]
                    sorting = False; complete = False; comparisons = swaps = 0; status_msg = "Array reset"
                elif buttons["Back"].collidepoint(pos):
                    return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        if sorting:
            if sort_type == "bubble":    hl = bubble_step()
            elif sort_type == "selection": hl = selection_step()
            elif sort_type == "merge":   hl = merge_step()

        draw_array(hl)
        clock.tick(60)