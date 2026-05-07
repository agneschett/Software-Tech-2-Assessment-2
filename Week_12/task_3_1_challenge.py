import pygame
import sys
import collections

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BFS and DFS Visualiser")

FONT = pygame.font.SysFont(None, 28)
SMALL_FONT = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

# Graph node positions
nodes_pos = {
    'A': (100, 100),
    'B': (250, 60),
    'C': (250, 200),
    'D': (400, 100),
    'E': (550, 150),
    'F': (400, 300)
}

# Graph structure
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

# Global traversal order list
traversal_order = []


def draw_graph(visited=set(), frontier=set(), current=None):
    screen.fill((240, 240, 240))

    # Title
    title = FONT.render(
        "Click Any Node to Start DFS Traversal",
        True,
        (0, 0, 0)
    )
    screen.blit(title, (20, 20))

    # Draw edges
    for node, neighbors in graph.items():
        x1, y1 = nodes_pos[node]

        for neighbor in neighbors:
            x2, y2 = nodes_pos[neighbor]

            pygame.draw.line(
                screen,
                (0, 0, 0),
                (x1, y1),
                (x2, y2),
                2
            )

    # Draw nodes
    for node, (x, y) in nodes_pos.items():

        color = (200, 200, 200)

        if node in visited:
            color = (100, 200, 100)

        if node in frontier:
            color = (255, 200, 100)

        if node == current:
            color = (255, 100, 100)

        pygame.draw.circle(screen, color, (x, y), 25)

        text = FONT.render(node, True, (0, 0, 0))
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)

    # Display traversal order
    order_text = "Traversal Order: " + " -> ".join(traversal_order)

    traversal_surface = SMALL_FONT.render(
        order_text,
        True,
        (0, 0, 0)
    )

    screen.blit(traversal_surface, (20, 440))

    pygame.display.flip()


def dfs(start):
    visited = set()
    stack = [start]

    traversal_order.clear()

    while stack:

        current = stack.pop()

        if current not in visited:

            visited.add(current)
            traversal_order.append(current)

            draw_graph(
                visited=visited,
                frontier=set(stack),
                current=current
            )

            pygame.time.wait(700)

            # Handle quit events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Add neighbors in reverse order
            # so traversal looks cleaner
            for neighbor in reversed(graph[current]):
                if neighbor not in visited:
                    stack.append(neighbor)


def get_clicked_node(pos):
    mouse_x, mouse_y = pos

    for node, (x, y) in nodes_pos.items():

        distance = ((mouse_x - x) ** 2 + (mouse_y - y) ** 2) ** 0.5

        if distance <= 25:
            return node

    return None


def main():

    running = True

    while running:

        draw_graph()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # Mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:

                clicked_node = get_clicked_node(event.pos)

                if clicked_node:
                    dfs(clicked_node)

        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()