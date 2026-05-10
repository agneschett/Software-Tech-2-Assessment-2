"""
Data Structures Hub — groups:
  - Linear Search (1.1)
  - Stack Visualiser (1.2/1.3)
  - Queue Visualiser (1.2/1.3)
  - Linked List Visualiser (2.1)
  - BST Visualiser (2.2)
"""

import pygame
import sys
from modules import (
    linear_search_vis,
    ds_visualiser,
    bst_visualiser,
)


def run(screen, font, clock, WIDTH, HEIGHT):
    small = pygame.font.SysFont(None, 28)

    items = [
        ("Linear Search",        lambda: linear_search_vis.run(screen, font, clock, WIDTH, HEIGHT)),
        ("Stack Visualiser",     lambda: ds_visualiser.run_stack(screen, font, clock, WIDTH, HEIGHT)),
        ("Queue Visualiser",     lambda: ds_visualiser.run_queue(screen, font, clock, WIDTH, HEIGHT)),
        ("Linked List Visualiser", lambda: ds_visualiser.run_linked_list(screen, font, clock, WIDTH, HEIGHT)),
        ("BST Visualiser",       lambda: bst_visualiser.run(screen, font, clock, WIDTH, HEIGHT)),
        ("Back",                 None),
    ]
    selected = 0

    running = True
    while running:
        screen.fill((20, 22, 30))
        t = font.render("Data Structures", True, (180, 200, 255))
        screen.blit(t, (WIDTH // 2 - t.get_width() // 2, 50))

        sub = small.render("Explore stacks, queues, linked lists & trees", True, (100, 120, 160))
        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, 90))

        for i, (lbl, _) in enumerate(items):
            is_sel = i == selected
            color = (255, 200, 80) if is_sel else (160, 170, 200)
            rect = pygame.Rect(WIDTH // 2 - 200, 140 + i * 58, 400, 46)
            bg = (50, 60, 90) if is_sel else (30, 36, 55)
            pygame.draw.rect(screen, bg, rect, border_radius=10)
            pygame.draw.rect(screen, color, rect, 2, border_radius=10)
            txt = font.render(lbl, True, color)
            screen.blit(txt, txt.get_rect(center=rect.center))

        inst = small.render("↑↓ navigate   ENTER select   ESC = back", True, (100, 110, 140))
        screen.blit(inst, (WIDTH // 2 - inst.get_width() // 2, HEIGHT - 40))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(items)
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(items)
                elif event.key == pygame.K_RETURN:
                    lbl, fn = items[selected]
                    if fn is None: return
                    fn()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, (lbl, fn) in enumerate(items):
                    rect = pygame.Rect(WIDTH // 2 - 200, 140 + i * 58, 400, 46)
                    if rect.collidepoint(event.pos):
                        if fn is None: return
                        fn()

        clock.tick(30)
