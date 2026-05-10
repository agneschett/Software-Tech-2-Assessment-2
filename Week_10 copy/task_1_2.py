import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont(None, 28)
clock = pygame.time.Clock()

stack = []

BLOCK_WIDTH, BLOCK_HEIGHT = 200, 40
START_X = (WIDTH - BLOCK_WIDTH) // 2
BASE_Y = HEIGHT - BLOCK_HEIGHT - 20

def draw_stack():
    screen.fill((50, 50, 50))
    for i, val in enumerate(stack):
        rect = pygame.Rect(START_X, BASE_Y - i * (BLOCK_HEIGHT + 5), BLOCK_WIDTH, BLOCK_HEIGHT)
        pygame.draw.rect(screen, (100, 150, 250), rect)
        text = FONT.render(str(val), True, (0, 0, 0))
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
    info_text = FONT.render("SPACE: Push, BACKSPACE: Pop, ESC:Quit", True, (200, 200, 200))
    screen.blit(info_text, (10, 10))
def main():
    counter = 1
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    stack.append(counter)
                    counter += 1
                elif event.key == pygame.K_BACKSPACE and stack:
                    stack.pop()
                elif event.key == pygame.K_ESCAPE:
                    running = False
        draw_stack()
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
if __name__ == "__main__":
    main()
