import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()

NODE_RADIUS = 25


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, value):
        if not self.head:
            self.head = Node(value)
            return

        current = self.head
        while current.next:
            current = current.next

        current.next = Node(value)

    def delete(self, value):
        current = self.head
        prev = None

        while current:
            if current.value == value:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return True

            prev = current
            current = current.next

        return False

    def to_list(self):
        elems = []
        current = self.head

        while current:
            elems.append(current.value)
            current = current.next

        return elems


def draw_node(x, y, value, highlight=False):
    color = (255, 100, 100) if highlight else (100, 200, 250)
    pygame.draw.circle(screen, color, (x, y), NODE_RADIUS)

    text = FONT.render(str(value), True, (0, 0, 0))
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)


def draw_arrow(start_pos, end_pos):
    pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos, 3)

    # Draw a simple arrow head
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]

    angle = pygame.math.Vector2(dx, dy).angle_to(pygame.math.Vector2(1, 0))

    arrow_head = [
        (end_pos[0] - 10, end_pos[1] - 5),
        end_pos,
        (end_pos[0] - 10, end_pos[1] + 5),
    ]

    pygame.draw.polygon(screen, (0, 0, 0), arrow_head)


def draw_linked_list(linked_list, highlight_index=None):
    screen.fill((240, 240, 240))

    nodes = []
    current = linked_list.head
    x, y = 80, HEIGHT // 2
    idx = 0

    while current:
        nodes.append((x, y, current.value, idx == highlight_index))
        x += 150
        current = current.next
        idx += 1

    for i, (x, y, val, highlight) in enumerate(nodes):
        draw_node(x, y, val, highlight)

        if i < len(nodes) - 1:
            draw_arrow((x + NODE_RADIUS, y), (x + 150 - NODE_RADIUS, y))

    pygame.display.flip()


def main():
    ll = LinkedList()

    actions = [
        ('append', 5),
        ('append', 10),
        ('append', 15),
        ('delete', 10),
        ('append', 20)
    ]

    for action, value in actions:
        if action == 'append':
            ll.append(value)
        elif action == 'delete':
            ll.delete(value)

        for i in range(len(ll.to_list())):
            draw_linked_list(ll, highlight_index=i)
            pygame.time.wait(500)

    pygame.time.wait(2000)
    pygame.quit()


if __name__ == '__main__':
    main()