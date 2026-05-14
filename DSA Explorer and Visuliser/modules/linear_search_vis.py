"""
Task 1.1 Challenge - Linear Search Visualiser
- Multi-target search with comparison counter
- Keyboard input for target value
"""

import pygame
import sys
import time

NUMBERS = [5, 3, 9, 1, 7, 4, 8, 2]


def run(screen, font, clock, WIDTH, HEIGHT):
    cell_width = WIDTH // len(NUMBERS)
    cell_height = 80
    small_font = pygame.font.SysFont(None, 28)

    BACK_BTN = pygame.Rect(20, 15, 90, 36)

    def draw_grid(highlight_index=None, comparisons=0, message="", found_indices=None):
        screen.fill((20, 22, 30))

        # Back button
        pygame.draw.rect(screen, (100, 100, 120), BACK_BTN, border_radius=8)
        bt = small_font.render("Back", True, (240, 240, 240))
        screen.blit(bt, bt.get_rect(center=BACK_BTN.center))

        # Title
        title = font.render("Linear Search Visualiser", True, (180, 200, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 18))

        # Cells — pushed down to give title and Back btn room
        y_offset = 70
        for i, num in enumerate(NUMBERS):
            color = (55, 65, 95)
            if found_indices and i in found_indices:
                color = (60, 200, 120)
            if i == highlight_index:
                color = (220, 80, 80)

            rect = pygame.Rect(i * cell_width + 4, y_offset, cell_width - 8, cell_height)
            pygame.draw.rect(screen, color, rect, border_radius=8)
            pygame.draw.rect(screen, (100, 120, 180), rect, 2, border_radius=8)

            text = font.render(str(num), True, (240, 240, 240))
            screen.blit(text, text.get_rect(center=rect.center))

        # Index labels
        for i in range(len(NUMBERS)):
            idx_text = small_font.render(f"[{i}]", True, (120, 130, 160))
            screen.blit(idx_text, (i * cell_width + cell_width // 2 - 10, y_offset + cell_height + 8))

        # Stats — well below the grid
        comp_text = small_font.render(f"Comparisons: {comparisons}", True, (200, 200, 100))
        screen.blit(comp_text, (20, y_offset + cell_height + 40))

        msg_color = (80, 220, 120) if "Found" in message else (220, 100, 80) if "not found" in message else (200, 210, 255)
        msg_text = small_font.render(message, True, msg_color)
        screen.blit(msg_text, (20, y_offset + cell_height + 68))

        # Instructions
        inst = small_font.render("Type a number + ENTER to search | ESC = back", True, (100, 110, 140))
        screen.blit(inst, (20, HEIGHT - 40))

    def get_user_input(current_text, prompt_msg):
        draw_grid(message=f"{prompt_msg}: {current_text}_")
        pygame.display.flip()

    def linear_search(target, found_indices):
        comparisons = 0
        for i, num in enumerate(NUMBERS):
            comparisons += 1
            draw_grid(i, comparisons, f"Searching for {target}...", found_indices)
            pygame.display.flip()
            pygame.time.wait(400)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

            if num == target:
                return i, comparisons
        return -1, comparisons

    user_text = ""
    found_indices = set()
    message = "Type a number and press ENTER"
    comparisons = 0

    running = True
    while running:
        draw_grid(message=message + (f"  |  Input: {user_text}_" if user_text is not None else ""), comparisons=comparisons, found_indices=found_indices)
        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BTN.collidepoint(event.pos):
                    return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_RETURN:
                    if user_text.lstrip('-').isdigit():
                        target = int(user_text)
                        user_text = ""
                        idx, comparisons = linear_search(target, found_indices)
                        if idx != -1:
                            found_indices.add(idx)
                            message = f"Found {target} at index {idx} in {comparisons} comparisons!"
                        else:
                            message = f"{target} not found after {comparisons} comparisons"
                    else:
                        user_text = ""
                        message = "Invalid input — enter a number"
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    if event.unicode.isdigit() or (event.unicode == '-' and user_text == ""):
                        user_text += event.unicode