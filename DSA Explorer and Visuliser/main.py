"""
DSA Explorer & Visualiser — Main Entry Point
Phase 1: Data Structures (Linear Search, Stack, Queue, Linked List, BST)
Phase 2: Sorting, Graphs, Heap
Phase 3: Puzzles (Pathfinding, Coin Change DP)
"""

import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 900, 620
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DSA Explorer & Visualiser")

FONT  = pygame.font.SysFont(None, 36)
SMALL = pygame.font.SysFont(None, 26)
clock = pygame.time.Clock()

#Import modules

from modules import ds_hub, sorting_visualiser, graph_visualiser, heap_visualiser, puzzle_module


# Menu

MENU_ITEMS = [
    {
        "label": "Data Structures",
        "sub":   "Stack · Queue · Linked List · BST · Search",
        "color": (80, 130, 220),
        "fn":    lambda: ds_hub.run(screen, FONT, clock, WIDTH, HEIGHT),
    },
    {
        "label": "Sorting",
        "sub":   "Bubble Sort · Selection Sort · Merge Sort",
        "color": (80, 180, 140),
        "fn":    lambda: sorting_visualiser.run(screen, FONT, clock, WIDTH, HEIGHT),
    },
    {
        "label": "Graphs",
        "sub":   "BFS · DFS · Interactive node selection",
        "color": (160, 100, 220),
        "fn":    lambda: graph_visualiser.run(screen, FONT, clock, WIDTH, HEIGHT),
    },
    {
        "label": "Heap",
        "sub":   "Min-Heap · Priority Queue · Event Simulator",
        "color": (220, 140, 60),
        "fn":    lambda: heap_visualiser.run(screen, FONT, clock, WIDTH, HEIGHT),
    },
    {
        "label": "Puzzles",
        "sub":   "A* / Dijkstra Pathfinding · Coin Change DP",
        "color": (220, 80, 120),
        "fn":    lambda: puzzle_module.run(screen, FONT, clock, WIDTH, HEIGHT),
    },
    {
        "label": "Exit",
        "sub":   "",
        "color": (100, 100, 120),
        "fn":    None,
    },
]

CARD_W, CARD_H = 380, 76
COLS_LAYOUT = 2
CARDS_PER_ROW = 2
START_Y = 180
GAP_X, GAP_Y = 30, 18

def card_rect(idx):
    col = idx % COLS_LAYOUT
    row = idx // COLS_LAYOUT
    x = WIDTH // 2 - (CARD_W * COLS_LAYOUT + GAP_X) // 2 + col * (CARD_W + GAP_X)
    y = START_Y + row * (CARD_H + GAP_Y)
    return pygame.Rect(x, y, CARD_W, CARD_H)


def draw_menu(hover_idx):
    screen.fill((16, 18, 26))

    # Subtle grid background
    for x in range(0, WIDTH, 40):
        pygame.draw.line(screen, (25, 30, 45), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, (25, 30, 45), (0, y), (WIDTH, y))

    # Title
    title = pygame.font.SysFont(None, 52).render("DSA Explorer", True, (210, 225, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

    sub = SMALL.render("Data Structures & Algorithms Visualiser — UC Software Technology 2", True, (90, 105, 145))
    screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, 92))

    # Divider
    pygame.draw.line(screen, (50, 60, 100), (80, 130), (WIDTH - 80, 130), 1)

    # Cards
    for i, item in enumerate(MENU_ITEMS):
        rect = card_rect(i)
        is_hover = (i == hover_idx)
        base_color = item["color"]
        bg = tuple(min(c + 25, 255) for c in base_color) if is_hover else (28, 34, 52)
        border = base_color

        pygame.draw.rect(screen, bg, rect, border_radius=12)
        pygame.draw.rect(screen, border, rect, 2 if not is_hover else 3, border_radius=12)

        # Accent bar
        accent_rect = pygame.Rect(rect.x + 10, rect.y + 14, 4, rect.height - 28)
        pygame.draw.rect(screen, base_color, accent_rect, border_radius=2)

        # Text
        lbl_color = (240, 245, 255) if is_hover else (190, 200, 220)
        lbl = FONT.render(item["label"], True, lbl_color)
        screen.blit(lbl, (rect.x + 24, rect.y + 14))

        if item["sub"]:
            sub_t = SMALL.render(item["sub"], True, (110, 125, 160) if not is_hover else (180, 195, 220))
            screen.blit(sub_t, (rect.x + 24, rect.y + 46))

    # Footer
    ft = SMALL.render("Click a module or use ↑↓ + ENTER", True, (60, 72, 110))
    screen.blit(ft, (WIDTH // 2 - ft.get_width() // 2, HEIGHT - 28))

    pygame.display.flip()


def main():
    selected = 0
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()
        hover_idx = None
        for i in range(len(MENU_ITEMS)):
            if card_rect(i).collidepoint(mouse_pos):
                hover_idx = i

        draw_menu(hover_idx)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(MENU_ITEMS)
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(MENU_ITEMS)
                elif event.key == pygame.K_RETURN:
                    item = MENU_ITEMS[selected]
                    if item["fn"] is None:
                        running = False
                    else:
                        item["fn"]()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, item in enumerate(MENU_ITEMS):
                    if card_rect(i).collidepoint(event.pos):
                        if item["fn"] is None:
                            running = False
                        else:
                            item["fn"]()
                        break

        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
