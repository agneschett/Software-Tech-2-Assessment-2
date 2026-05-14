"""
Task 1.2 / 1.3 Challenge - Stack & Queue Visualiser
- Stack with SPACE/BACKSPACE
- Queue with on-screen Enqueue/Dequeue buttons + smooth animations
"""

import pygame
import sys
from modules.stack import Stack
from modules.queue_ds import Queue

BLOCK_W, BLOCK_H = 160, 40


# ─── STACK ──────────────────────────────────────────────────────────────────

def run_stack(screen, font, clock, WIDTH, HEIGHT):
    stack = Stack()
    counter = 1
    small = pygame.font.SysFont(None, 24)

    BASE_X = WIDTH // 2 - BLOCK_W // 2
    BASE_Y = HEIGHT - BLOCK_H - 60

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_SPACE:
                    stack.push(counter); counter += 1
                elif event.key == pygame.K_BACKSPACE and not stack.is_empty():
                    stack.pop()

        screen.fill((20, 22, 30))

        # Title
        t = font.render("Stack Visualiser  (LIFO)", True, (180, 200, 255))
        screen.blit(t, (WIDTH // 2 - t.get_width() // 2, 15))

        # Draw blocks
        for i, val in enumerate(stack._data):
            y = BASE_Y - i * (BLOCK_H + 6)
            rect = pygame.Rect(BASE_X, y, BLOCK_W, BLOCK_H)
            alpha = min(255, 140 + i * 15)
            color = (60 + i * 8, 100 + i * 5, 210)
            pygame.draw.rect(screen, color, rect, border_radius=8)
            pygame.draw.rect(screen, (150, 170, 255), rect, 2, border_radius=8)
            txt = font.render(str(val), True, (240, 240, 240))
            screen.blit(txt, txt.get_rect(center=rect.center))

        # TOP label
        if not stack.is_empty():
            top_y = BASE_Y - (stack.size() - 1) * (BLOCK_H + 6)
            lbl = small.render("← TOP", True, (100, 255, 180))
            screen.blit(lbl, (BASE_X + BLOCK_W + 8, top_y + 12))

        # Size
        sz = small.render(f"Size: {stack.size()}", True, (160, 170, 200))
        screen.blit(sz, (20, 60))

        inst = small.render("SPACE = Push  |  BACKSPACE = Pop  |  ESC = back", True, (100, 110, 140))
        screen.blit(inst, (WIDTH // 2 - inst.get_width() // 2, HEIGHT - 30))

        pygame.display.flip()
        clock.tick(30)


# ─── QUEUE ──────────────────────────────────────────────────────────────────

def run_queue(screen, font, clock, WIDTH, HEIGHT):
    queue_list = []   # plain list for animation simplicity
    counter = 1
    small = pygame.font.SysFont(None, 24)

    START_X = 60
    BASE_Y = HEIGHT // 2 - BLOCK_H // 2

    ENQ_BTN = pygame.Rect(WIDTH - 180, HEIGHT // 2 - 55, 140, 44)
    DEQ_BTN = pygame.Rect(WIDTH - 180, HEIGHT // 2 + 5, 140, 44)

    def draw_buttons():
        pygame.draw.rect(screen, (60, 180, 110), ENQ_BTN, border_radius=10)
        pygame.draw.rect(screen, (200, 80, 80), DEQ_BTN, border_radius=10)
        et = font.render("Enqueue", True, (240, 240, 240))
        dt = font.render("Dequeue", True, (240, 240, 240))
        screen.blit(et, et.get_rect(center=ENQ_BTN.center))
        screen.blit(dt, dt.get_rect(center=DEQ_BTN.center))

    def draw_base(highlight=None):
        screen.fill((20, 22, 30))
        t = font.render("Queue Visualiser  (FIFO)", True, (180, 200, 255))
        screen.blit(t, (WIDTH // 2 - t.get_width() // 2, 15))
        draw_buttons()

        # FRONT/REAR labels
        if queue_list:
            front_lbl = small.render("FRONT", True, (100, 255, 180))
            screen.blit(front_lbl, (START_X, BASE_Y - 22))
            rx = START_X + (len(queue_list) - 1) * (BLOCK_W + 10)
            rear_lbl = small.render("REAR", True, (255, 200, 80))
            screen.blit(rear_lbl, (rx, BASE_Y - 22))

        for i, val in enumerate(queue_list):
            x = START_X + i * (BLOCK_W + 10)
            rect = pygame.Rect(x, BASE_Y, BLOCK_W, BLOCK_H)
            color = (255, 200, 80) if i == highlight else (60, 100, 210)
            pygame.draw.rect(screen, color, rect, border_radius=8)
            pygame.draw.rect(screen, (150, 170, 255), rect, 2, border_radius=8)
            txt = font.render(str(val), True, (20, 20, 30))
            screen.blit(txt, txt.get_rect(center=rect.center))

        sz = small.render(f"Size: {len(queue_list)}", True, (160, 170, 200))
        screen.blit(sz, (20, 60))
        inst = small.render("Click buttons to Enqueue / Dequeue  |  ESC = back", True, (100, 110, 140))
        screen.blit(inst, (WIDTH // 2 - inst.get_width() // 2, HEIGHT - 30))

    def animate_enqueue(value):
        target_x = START_X + len(queue_list) * (BLOCK_W + 10)
        x = -BLOCK_W
        while x < target_x:
            draw_base()
            rect = pygame.Rect(x, BASE_Y, BLOCK_W, BLOCK_H)
            pygame.draw.rect(screen, (100, 255, 180), rect, border_radius=8)
            txt = font.render(str(value), True, (20, 20, 30))
            screen.blit(txt, txt.get_rect(center=rect.center))
            pygame.display.flip()
            x += 18; clock.tick(60)
        queue_list.append(value)

    def animate_dequeue():
        if not queue_list:
            return
        x = START_X
        while x < WIDTH + BLOCK_W:
            draw_base()
            # sliding out block
            rect = pygame.Rect(x, BASE_Y, BLOCK_W, BLOCK_H)
            pygame.draw.rect(screen, (220, 100, 80), rect, border_radius=8)
            txt = font.render(str(queue_list[0]), True, (240, 240, 240))
            screen.blit(txt, txt.get_rect(center=rect.center))
            # remaining blocks (don't draw first)
            for i, val in enumerate(queue_list[1:], 1):
                rx = START_X + (i - 1) * (BLOCK_W + 10)
                rrect = pygame.Rect(rx, BASE_Y, BLOCK_W, BLOCK_H)
                pygame.draw.rect(screen, (60, 100, 210), rrect, border_radius=8)
                t2 = font.render(str(val), True, (240, 240, 240))
                screen.blit(t2, t2.get_rect(center=rrect.center))
            pygame.display.flip()
            x += 18; clock.tick(60)
        queue_list.pop(0)

    running = True
    while running:
        draw_base()
        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ENQ_BTN.collidepoint(event.pos):
                    animate_enqueue(counter); counter += 1
                elif DEQ_BTN.collidepoint(event.pos):
                    animate_dequeue()


# ─── LINKED LIST ─────────────────────────────────────────────────────────────

class LLNode:
    def __init__(self, val):
        self.value = val
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, val):
        n = LLNode(val)
        if not self.head:
            self.head = n; return
        cur = self.head
        while cur.next: cur = cur.next
        cur.next = n

    def delete(self, val):
        cur, prev = self.head, None
        while cur:
            if cur.value == val:
                if prev: prev.next = cur.next
                else: self.head = cur.next
                return True
            prev, cur = cur, cur.next
        return False

    def insert_at(self, pos, val):
        n = LLNode(val)
        if pos == 0:
            n.next = self.head; self.head = n; return
        cur, idx = self.head, 0
        while cur and idx < pos - 1:
            cur = cur.next; idx += 1
        if not cur: return
        n.next = cur.next; cur.next = n

    def to_list(self):
        res, cur = [], self.head
        while cur: res.append(cur.value); cur = cur.next
        return res

    def reverse(self):
        prev, cur = None, self.head
        while cur:
            nxt = cur.next; cur.next = prev; prev = cur; cur = nxt
        self.head = prev


def run_linked_list(screen, font, clock, WIDTH, HEIGHT):
    ll = LinkedList()
    for v in [10, 20, 30, 40]:
        ll.append(v)

    small = pygame.font.SysFont(None, 24)
    NODE_R = 25
    input_mode = None
    input_text = ""
    insert_val_temp = None
    message = ""

    def draw_ll(highlight_val=None):
        screen.fill((20, 22, 30))
        t = font.render("Linked List Visualiser", True, (180, 200, 255))
        screen.blit(t, (WIDTH // 2 - t.get_width() // 2, 15))

        nodes = ll.to_list()
        total_w = len(nodes) * 110
        start_x = max(60, WIDTH // 2 - total_w // 2)
        y = HEIGHT // 2

        for i, val in enumerate(nodes):
            x = start_x + i * 110
            color = (255, 160, 60) if val == highlight_val else (60, 130, 220)
            pygame.draw.circle(screen, color, (x, y), NODE_R)
            pygame.draw.circle(screen, (150, 180, 255), (x, y), NODE_R, 2)
            vt = font.render(str(val), True, (240, 240, 240))
            screen.blit(vt, vt.get_rect(center=(x, y)))
            if i < len(nodes) - 1:
                ax = x + NODE_R + 2
                ex = x + 110 - NODE_R - 2
                pygame.draw.line(screen, (180, 190, 220), (ax, y), (ex, y), 2)
                pygame.draw.polygon(screen, (180, 190, 220), [
                    (ex, y - 5), (ex + 8, y), (ex, y + 5)])

        # NULL tail
        if nodes:
            tail_x = start_x + (len(nodes) - 1) * 110 + NODE_R + 8
            nt = small.render("NULL", True, (150, 80, 80))
            screen.blit(nt, (tail_x, HEIGHT // 2 - 10))

        if input_mode:
            prompts = {"append": "Append value:", "delete": "Delete value:",
                       "insert_val": "Insert value:", "insert_pos": "Insert at position:"}
            pt = font.render(prompts.get(input_mode, "") + " " + input_text + "_", True, (220, 220, 100))
            screen.blit(pt, (20, HEIGHT - 70))

        if message:
            mt = small.render(message, True, (220, 120, 80))
            screen.blit(mt, (20, HEIGHT - 95))

        inst = small.render("A=Append  D=Delete  I=Insert  R=Reverse  ESC=back", True, (100, 110, 140))
        screen.blit(inst, (20, HEIGHT - 30))
        pygame.display.flip()

    running = True
    while running:
        draw_ll()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if input_mode:
                    if event.key == pygame.K_RETURN:
                        try:
                            v = int(input_text)
                            if input_mode == "append":
                                ll.append(v); message = f"Appended {v}"
                            elif input_mode == "delete":
                                ok = ll.delete(v)
                                message = f"Deleted {v}" if ok else f"{v} not found"
                            elif input_mode == "insert_val":
                                insert_val_temp = v
                                input_mode = "insert_pos"; input_text = ""; continue
                            elif input_mode == "insert_pos":
                                ll.insert_at(v, insert_val_temp)
                                message = f"Inserted {insert_val_temp} at pos {v}"
                        except:
                            message = "Invalid input"
                        input_text = ""; input_mode = None
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.unicode.isdigit():
                        input_text += event.unicode
                else:
                    if event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_a:
                        input_mode = "append"; input_text = ""
                    elif event.key == pygame.K_d:
                        input_mode = "delete"; input_text = ""
                    elif event.key == pygame.K_i:
                        input_mode = "insert_val"; input_text = ""
                    elif event.key == pygame.K_r:
                        ll.reverse(); message = "List reversed!"
