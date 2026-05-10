import pygame
import sys
pygame.init()

from modules import data_structures_visualiser

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Algorithm Explorer")

FONT = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()


def draw_text(text, pos):
    txt_surface = FONT.render(text, True, (0, 0, 0))
    screen.blit(txt_surface, pos)


def main_menu():
    screen.fill((200, 200, 250))
    draw_text("Algorithm Explorer", (WIDTH // 3, 50))

    buttons = {
        'Data Structures': pygame.Rect(300, 150, 200, 50),
        'Sorting': pygame.Rect(300, 230, 200, 50),
        'Graphs': pygame.Rect(300, 310, 200, 50),
        'Exit': pygame.Rect(300, 390, 200, 50),
    }

    for text, rect in buttons.items():
        pygame.draw.rect(screen, (150, 150, 200), rect)
        draw_text(text, (rect.x + 20, rect.y + 10))

    pygame.display.flip()
    return buttons


def main():
    running = True
    current_module = None

    while running:
        if current_module is None:
            buttons = main_menu()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos

                    for name, rect in buttons.items():
                        if rect.collidepoint(pos):

                            if name == "Exit":
                                running = False

                            elif name == "Data Structures":
                                current_module = name

                            else:
                                # Future modules here
                                pass

        else:
            try:
                if current_module == "Data Structures":
                    data_structures_visualiser.run(screen)
                    # Add other modules here as needed

            except SystemExit:
                running = False
                break

            finally:
                current_module = None

        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()