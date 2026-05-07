import pygame
import sys
import collections

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

# Graph nodes positioned manually
nodes_pos = {
    'A': (100, 100),
    'B': (250, 60),
    'C': (250, 200),
    'D': (400, 100),
    'E': (500, 150),
    'F': (400, 300)
}

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}


def draw_graph(visited=set(), frontier=set(), current=None):
    screen.fill((240, 240, 240))

    # Draw edges
    for node, neighbors in graph.items():
        x1, y1 = nodes_pos[node]

        for n in neighbors:
            x2, y2 = nodes_pos[n]
            pygame.draw.line(screen, (0, 0, 0), (x1, y1), (x2, y2), 2)

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

    pygame.display.flip()


def bfs(start):
    visited = set()
    queue = collections.deque([start])

    while queue:
        current = queue.popleft()
        visited.add(current)

        draw_graph(
            visited=visited,
            frontier=set(queue),
            current=current
        )

        pygame.time.wait(700)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for neighbor in graph[current]:
            if neighbor not in visited and neighbor not in queue:
                queue.append(neighbor)


def main():
    draw_graph()
    pygame.time.wait(1000)

    bfs('A')

    pygame.time.wait(2000)
    pygame.quit()


if __name__ == "__main__":
    main()