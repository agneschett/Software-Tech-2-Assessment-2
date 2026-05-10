import pygame
import sys
import time

pygame.init()

WIDTH, HEIGHT = 700, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont(None, 28)
clock = pygame.time.Clock()

queue = []

BLOCK_WIDTH, BLOCK_HEIGHT = 80, 40
START_X = 50
BASE_Y = HEIGHT // 2

# Button settings
BUTTON_WIDTH, BUTTON_HEIGHT = 120, 40
ENQ_BUTTON = pygame.Rect(500, 50, BUTTON_WIDTH, BUTTON_HEIGHT)
DEQ_BUTTON = pygame.Rect(500, 120, BUTTON_WIDTH, BUTTON_HEIGHT)


def draw_buttons():
    pygame.draw.rect(screen, (100, 200, 100), ENQ_BUTTON)
    pygame.draw.rect(screen, (200, 100, 100), DEQ_BUTTON)

    enq_text = FONT.render("Enqueue", True, (0, 0, 0))
    deq_text = FONT.render("Dequeue", True, (0, 0, 0))

    screen.blit(enq_text, enq_text.get_rect(center=ENQ_BUTTON.center))
    screen.blit(deq_text, deq_text.get_rect(center=DEQ_BUTTON.center))


def draw_queue(highlight_index=None):
    screen.fill((40, 40, 40))
    draw_buttons()

    for i, val in enumerate(queue):
        x = START_X + i * (BLOCK_WIDTH + 10)
        rect = pygame.Rect(x, BASE_Y, BLOCK_WIDTH, BLOCK_HEIGHT)

        color = (100, 150, 250)
        if i == highlight_index:
            color = (255, 180, 100)

        pygame.draw.rect(screen, color, rect)
        text = FONT.render(str(val), True, (0, 0, 0))
        screen.blit(text, text.get_rect(center=rect.center))


def animate_enqueue(value):
    """Slide a new block from the left into position."""
    target_index = len(queue)
    target_x = START_X + target_index * (BLOCK_WIDTH + 10)

    x = -BLOCK_WIDTH
    while x < target_x:
        screen.fill((40, 40, 40))
        draw_buttons()

        # Draw existing queue
        for i, val in enumerate(queue):
            rect = pygame.Rect(START_X + i * (BLOCK_WIDTH + 10), BASE_Y, BLOCK_WIDTH, BLOCK_HEIGHT)
            pygame.draw.rect(screen, (100, 150, 250), rect)
            text = FONT.render(str(val), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center=rect.center))

        # Draw sliding new block
        rect = pygame.Rect(x, BASE_Y, BLOCK_WIDTH, BLOCK_HEIGHT)
        pygame.draw.rect(screen, (255, 255, 100), rect)
        text = FONT.render(str(value), True, (0, 0, 0))
        screen.blit(text, text.get_rect(center=rect.center))

        pygame.display.flip()
        x += 10
        clock.tick(60)

    queue.append(value)


def animate_dequeue():
    """Slide the first block out to the right, then shift others left."""
    if not queue:
        return

    # Animate first block sliding out
    x = START_X
    while x < WIDTH:
        screen.fill((40, 40, 40))
        draw_buttons()

        # Draw sliding-out block
        rect = pygame.Rect(x, BASE_Y, BLOCK_WIDTH, BLOCK_HEIGHT)
        pygame.draw.rect(screen, (255, 180, 100), rect)
        text = FONT.render(str(queue[0]), True, (0, 0, 0))
        screen.blit(text, text.get_rect(center=rect.center))

        # Draw remaining queue
        for i, val in enumerate(queue[1:], start=1):
            rx = START_X + (i - 1) * (BLOCK_WIDTH + 10)
            rect = pygame.Rect(rx, BASE_Y, BLOCK_WIDTH, BLOCK_HEIGHT)
            pygame.draw.rect(screen, (100, 150, 250), rect)
            text = FONT.render(str(val), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center=rect.center))

        pygame.display.flip()
        x += 12
        clock.tick(60)

    # Remove first element
    queue.pop(0)

    # Shift remaining blocks left smoothly
    shift_distance = BLOCK_WIDTH + 10
    shift = 0
    while shift < shift_distance:
        screen.fill((40, 40, 40))
        draw_buttons()

        for i, val in enumerate(queue):
            rx = START_X + i * (BLOCK_WIDTH + 10) + (shift_distance - shift)
            rect = pygame.Rect(rx, BASE_Y, BLOCK_WIDTH, BLOCK_HEIGHT)
            pygame.draw.rect(screen, (100, 150, 250), rect)
            text = FONT.render(str(val), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center=rect.center))

        pygame.display.flip()
        shift += 10
        clock.tick(60)


def main():
    counter = 1
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                if ENQ_BUTTON.collidepoint(mx, my):
                    animate_enqueue(counter)
                    counter += 1

                elif DEQ_BUTTON.collidepoint(mx, my):
                    animate_dequeue()

        draw_queue()
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()