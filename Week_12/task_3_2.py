import pygame
import sys
import random
import math

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

# Min-heap implemented as list
heap = []


def draw_heap(heap, highlight_indices=[]):
    screen.fill((255, 255, 255))

    if not heap:
        text = FONT.render("Heap is empty", True, (0, 0, 0))
        screen.blit(text, (WIDTH // 2 - 60, HEIGHT // 2))
        pygame.display.flip()
        return

    levels = int(math.log2(len(heap))) + 1
    max_nodes = 2 ** levels - 1

    node_positions = []

    for i in range(len(heap)):
        level = int(math.floor(math.log2(i + 1)))
        index_in_level = i - (2 ** level - 1)

        gap = WIDTH // (2 ** level + 1)

        x = gap * (index_in_level + 1)
        y = 60 + level * 70

        node_positions.append((x, y))

    # Draw edges
    for i in range(len(heap)):
        left = 2 * i + 1
        right = 2 * i + 2

        if left < len(heap):
            pygame.draw.line(
                screen,
                (0, 0, 0),
                node_positions[i],
                node_positions[left],
                2
            )

        if right < len(heap):
            pygame.draw.line(
                screen,
                (0, 0, 0),
                node_positions[i],
                node_positions[right],
                2
            )

    # Draw nodes
    for i, val in enumerate(heap):

        color = (100, 200, 250)

        if i in highlight_indices:
            color = (255, 100, 100)

        pygame.draw.circle(screen, color, node_positions[i], 20)

        text = FONT.render(str(val), True, (0, 0, 0))
        text_rect = text.get_rect(center=node_positions[i])

        screen.blit(text, text_rect)

    pygame.display.flip()


def heapify_up(heap, index):

    while index > 0:

        parent = (index - 1) // 2

        if heap[parent] > heap[index]:

            heap[parent], heap[index] = heap[index], heap[parent]

            draw_heap(heap, [parent, index])

            pygame.time.wait(400)

            index = parent

        else:
            break


def heapify_down(heap, index):

    n = len(heap)

    while True:

        left = 2 * index + 1
        right = 2 * index + 2

        smallest = index

        if left < n and heap[left] < heap[smallest]:
            smallest = left

        if right < n and heap[right] < heap[smallest]:
            smallest = right

        if smallest != index:

            heap[index], heap[smallest] = (
                heap[smallest],
                heap[index]
            )

            draw_heap(heap, [index, smallest])

            pygame.time.wait(400)

            index = smallest

        else:
            break


def insert(heap, val):

    heap.append(val)

    draw_heap(heap, [len(heap) - 1])

    pygame.time.wait(300)

    heapify_up(heap, len(heap) - 1)


def extract_min(heap):

    if len(heap) == 0:
        return None

    root = heap[0]

    heap[0] = heap[-1]
    heap.pop()

    draw_heap(heap, [0])

    pygame.time.wait(300)

    heapify_down(heap, 0)

    return root


def main():

    running = True

    insertions = [random.randint(1, 100) for _ in range(10)]

    idx = 0

    while running:

        screen.fill((255, 255, 255))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

        if idx < len(insertions):

            insert(heap, insertions[idx])

            idx += 1

            pygame.time.wait(600)

        else:

            pygame.time.wait(1000)

            if heap:
                extracted = extract_min(heap)
            else:
                running = False

        draw_heap(heap)

        clock.tick(30)

    pygame.time.wait(2000)

    pygame.quit()


if __name__ == "__main__":
    main()