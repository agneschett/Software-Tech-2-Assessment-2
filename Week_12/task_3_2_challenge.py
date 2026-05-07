import pygame
import sys
import random
import math

pygame.init()

# Screen setup
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Priority Queue Event Simulator")

FONT = pygame.font.SysFont(None, 28)
SMALL_FONT = pygame.font.SysFont(None, 22)

clock = pygame.time.Clock()

# Priority Queue (Min Heap)
heap = []

# Current processed event
current_event = "No event processed yet"


# -----------------------------
# Heap Drawing Function
# -----------------------------
def draw_heap(heap, highlight_indices=[]):

    screen.fill((245, 245, 245))

    # Title
    title = FONT.render(
        "Priority Queue Event Simulator",
        True,
        (0, 0, 0)
    )
    screen.blit(title, (20, 20))

    # Current Event Display
    current_text = FONT.render(
        f"Processing: {current_event}",
        True,
        (180, 0, 0)
    )
    screen.blit(current_text, (20, 60))

    # Upcoming Events
    upcoming_title = FONT.render(
        "Upcoming Events:",
        True,
        (0, 0, 0)
    )
    screen.blit(upcoming_title, (650, 100))

    sorted_events = sorted(heap)

    for i, event in enumerate(sorted_events[:8]):

        event_text = SMALL_FONT.render(
            f"{event[0]} - {event[1]}",
            True,
            (0, 0, 0)
        )

        screen.blit(event_text, (650, 140 + i * 30))

    # If heap empty
    if not heap:

        empty_text = FONT.render(
            "Heap is empty",
            True,
            (0, 0, 0)
        )

        screen.blit(empty_text, (300, 300))

        pygame.display.flip()
        return

    # Node positions
    node_positions = []

    for i in range(len(heap)):

        level = int(math.floor(math.log2(i + 1)))

        index_in_level = i - (2 ** level - 1)

        gap = WIDTH // (2 ** level + 1)

        x = gap * (index_in_level + 1)
        y = 150 + level * 90

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
    for i, event in enumerate(heap):

        color = (100, 180, 255)

        if i in highlight_indices:
            color = (255, 120, 120)

        pygame.draw.circle(
            screen,
            color,
            node_positions[i],
            30
        )

        # Only display time inside node
        text = SMALL_FONT.render(
            str(event[0]),
            True,
            (0, 0, 0)
        )

        text_rect = text.get_rect(center=node_positions[i])

        screen.blit(text, text_rect)

    pygame.display.flip()


# -----------------------------
# Heapify Up
# -----------------------------
def heapify_up(heap, index):

    while index > 0:

        parent = (index - 1) // 2

        if heap[parent][0] > heap[index][0]:

            heap[parent], heap[index] = (
                heap[index],
                heap[parent]
            )

            draw_heap(heap, [parent, index])

            pygame.time.wait(500)

            index = parent

        else:
            break


# -----------------------------
# Heapify Down
# -----------------------------
def heapify_down(heap, index):

    n = len(heap)

    while True:

        left = 2 * index + 1
        right = 2 * index + 2

        smallest = index

        if left < n and heap[left][0] < heap[smallest][0]:
            smallest = left

        if right < n and heap[right][0] < heap[smallest][0]:
            smallest = right

        if smallest != index:

            heap[index], heap[smallest] = (
                heap[smallest],
                heap[index]
            )

            draw_heap(heap, [index, smallest])

            pygame.time.wait(500)

            index = smallest

        else:
            break


# -----------------------------
# Insert Event
# -----------------------------
def insert_event(heap, event):

    heap.append(event)

    draw_heap(heap, [len(heap) - 1])

    pygame.time.wait(400)

    heapify_up(heap, len(heap) - 1)


# -----------------------------
# Extract Earliest Event
# -----------------------------
def extract_min(heap):

    global current_event

    if len(heap) == 0:
        return None

    root = heap[0]

    current_event = f"{root[0]} - {root[1]}"

    heap[0] = heap[-1]

    heap.pop()

    if heap:
        heapify_down(heap, 0)

    draw_heap(heap, [0])

    pygame.time.wait(1000)

    return root


# -----------------------------
# Main Function
# -----------------------------
def main():

    running = True

    # Sample events
    events = [
        (15, "Bus Arrival"),
        (3, "Emergency Alert"),
        (20, "Meeting Starts"),
        (8, "Traffic Light Change"),
        (12, "Train Arrival"),
        (1, "System Boot"),
        (18, "Maintenance Check"),
        (5, "Door Opens")
    ]

    # Shuffle insert order
    random.shuffle(events)

    insert_index = 0

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

        # Insert events first
        if insert_index < len(events):

            insert_event(heap, events[insert_index])

            insert_index += 1

            pygame.time.wait(800)

        # Then process events
        elif heap:

            extract_min(heap)

            pygame.time.wait(1200)

        else:

            draw_heap(heap)

            done_text = FONT.render(
                "All events processed!",
                True,
                (0, 120, 0)
            )

            screen.blit(done_text, (320, 520))

            pygame.display.flip()

            pygame.time.wait(3000)

            running = False

        draw_heap(heap)

        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()