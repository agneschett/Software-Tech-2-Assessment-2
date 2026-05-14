"""
Task 3.2 Challenge - Heap & Priority Queue Event Simulator
- Insert events with priority (time)
- Visualize heap tree
- Extract-min animates heap restructuring
- Show event descriptions panel
"""

import pygame
import sys
import math
import random


SAMPLE_EVENTS = [
    (15, "Bus Arrival"),
    (3,  "Emergency Alert"),
    (20, "Meeting Starts"),
    (8,  "Traffic Change"),
    (12, "Train Arrival"),
    (1,  "System Boot"),
    (18, "Maintenance"),
    (5,  "Door Opens"),
]


def run(screen, font, clock, WIDTH, HEIGHT):
    small = pygame.font.SysFont(None, 22)
    heap = []          # min-heap of (priority, description)
    current_event = "None yet"
    events_to_insert = list(SAMPLE_EVENTS)
    random.shuffle(events_to_insert)
    insert_idx = 0
    auto_mode = True   # auto-insert then auto-extract
    auto_timer = 0
    AUTO_DELAY = 900   # ms between auto steps

    PANEL_X = WIDTH - 220
    BACK_BTN  = pygame.Rect(20, 10, 90, 36)
    RESET_BTN = pygame.Rect(125, 10, 90, 36)
    EXTRACT_BTN = pygame.Rect(225, 10, 110, 36)

    def node_positions():
        pos = []
        for i in range(len(heap)):
            level = int(math.floor(math.log2(i + 1)))
            idx_in_level = i - (2 ** level - 1)
            usable_w = PANEL_X - 20
            gap = usable_w // (2 ** level + 1)
            x = gap * (idx_in_level + 1) + 10
            y = 120 + level * 80
            pos.append((x, y))
        return pos

    def heapify_up(idx):
        while idx > 0:
            parent = (idx - 1) // 2
            if heap[parent][0] > heap[idx][0]:
                heap[parent], heap[idx] = heap[idx], heap[parent]
                draw(highlight=[parent, idx]); pygame.time.wait(400)
                idx = parent
            else:
                break

    def heapify_down(idx):
        n = len(heap)
        while True:
            left, right, smallest = 2*idx+1, 2*idx+2, idx
            if left  < n and heap[left][0]    < heap[smallest][0]: smallest = left
            if right < n and heap[right][0]   < heap[smallest][0]: smallest = right
            if smallest != idx:
                heap[idx], heap[smallest] = heap[smallest], heap[idx]
                draw(highlight=[idx, smallest]); pygame.time.wait(400)
                idx = smallest
            else:
                break

    def insert_event(ev):
        heap.append(ev)
        draw(highlight=[len(heap)-1]); pygame.time.wait(300)
        heapify_up(len(heap)-1)

    def extract_min():
        nonlocal current_event
        if not heap: return
        root = heap[0]
        current_event = f"[{root[0]}] {root[1]}"
        if len(heap) == 1:
            heap.pop()
        else:
            heap[0] = heap.pop()
            draw(highlight=[0]); pygame.time.wait(300)
            heapify_down(0)

    def draw(highlight=None):
        screen.fill((20, 22, 30))

        # Title
        t = font.render("Priority Queue — Heap Visualiser", True, (180, 200, 255))
        screen.blit(t, (20, 55))

        # Buttons
        for btn, lbl, c in [(BACK_BTN,"Back",(100,100,120)), (RESET_BTN,"Reset",(160,100,60)), (EXTRACT_BTN,"Extract Min",(180,80,80))]:
            pygame.draw.rect(screen, c, btn, border_radius=8)
            bt = small.render(lbl, True, (240,240,240))
            screen.blit(bt, bt.get_rect(center=btn.center))

        # Current event
        ce = small.render(f"Processing: {current_event}", True, (220, 100, 100))
        screen.blit(ce, (20, HEIGHT - 30))

        # Side panel — upcoming
        pygame.draw.rect(screen, (30, 35, 50), (PANEL_X, 60, 220, HEIGHT - 70), border_radius=10)
        uh = small.render("Upcoming Events:", True, (180, 200, 255))
        screen.blit(uh, (PANEL_X + 10, 70))
        for i, (pri, desc) in enumerate(sorted(heap)[:10]):
            color = (100, 220, 140) if i == 0 else (160, 170, 200)
            et = small.render(f"{pri:2d}  {desc}", True, color)
            screen.blit(et, (PANEL_X + 10, 95 + i * 26))

        if not heap:
            et = font.render("Heap is empty", True, (160, 170, 200))
            screen.blit(et, (PANEL_X // 2 - et.get_width() // 2, HEIGHT // 2))
            pygame.display.flip(); return

        pos = node_positions()

        # Edges
        for i in range(len(heap)):
            for child in [2*i+1, 2*i+2]:
                if child < len(heap):
                    pygame.draw.line(screen, (80, 100, 160), pos[i], pos[child], 2)

        # Nodes
        for i, (pri, desc) in enumerate(heap):
            color = (220, 80, 80) if highlight and i in highlight else (60, 120, 220)
            pygame.draw.circle(screen, color, pos[i], 26)
            pygame.draw.circle(screen, (150, 180, 255), pos[i], 26, 2)
            pt = small.render(str(pri), True, (240, 240, 240))
            screen.blit(pt, pt.get_rect(center=pos[i]))

        pygame.display.flip()

    draw()
    running = True
    while running:
        now = pygame.time.get_ticks()

        # Auto mode
        if auto_mode and now - auto_timer > AUTO_DELAY:
            auto_timer = now
            if insert_idx < len(events_to_insert):
                insert_event(events_to_insert[insert_idx]); insert_idx += 1
            elif heap:
                extract_min()
            else:
                auto_mode = False

        draw()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if BACK_BTN.collidepoint(pos):
                    return
                elif RESET_BTN.collidepoint(pos):
                    heap.clear(); insert_idx = 0; current_event = "None yet"
                    events_to_insert = list(SAMPLE_EVENTS); random.shuffle(events_to_insert)
                    auto_mode = True; auto_timer = now
                elif EXTRACT_BTN.collidepoint(pos):
                    auto_mode = False; extract_min()
