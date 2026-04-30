import pygame
import sys

pygame.init()

# ===================== SETUP =====================
WIDTH, HEIGHT = 1000, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Linked List Visualiser")

FONT = pygame.font.SysFont(None, 32)
SMALL_FONT = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

NODE_RADIUS = 25

# Input state
input_text = ""
input_mode = None
insert_value_temp = None


# ===================== NODE =====================
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


# ===================== LINKED LIST =====================
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

    def insert_at(self, pos, value):
        new_node = Node(value)

        if pos == 0:
            new_node.next = self.head
            self.head = new_node
            return True

        current = self.head
        index = 0

        while current and index < pos - 1:
            current = current.next
            index += 1

        if not current:
            return False

        new_node.next = current.next
        current.next = new_node
        return True

    def reverse_animated(self):
        prev = None
        current = self.head

        while current:
            next_node = current.next
            current.next = prev
            prev = current

            temp = LinkedList()
            temp.head = prev
            draw_linked_list(temp)
            pygame.time.wait(400)

            current = next_node

        self.head = prev


# ===================== DRAWING =====================
def draw_node(x, y, value):
    pygame.draw.circle(screen, (100, 200, 250), (x, y), NODE_RADIUS)
    text = FONT.render(str(value), True, (0, 0, 0))
    screen.blit(text, text.get_rect(center=(x, y)))


def draw_arrow(start, end):
    pygame.draw.line(screen, (0, 0, 0), start, end, 3)
    pygame.draw.polygon(screen, (0, 0, 0), [
        (end[0] - 10, end[1] - 5),
        end,
        (end[0] - 10, end[1] + 5)
    ])


def draw_instructions():
    instructions = [
        "A = Append   D = Delete   I = Insert   R = Reverse   Q = Quit"
    ]
    for i, line in enumerate(instructions):
        txt = SMALL_FONT.render(line, True, (0, 0, 0))
        screen.blit(txt, (10, 10 + i * 20))


def draw_input_box():
    if input_mode:
        prompts = {
            "append": "Enter value:",
            "delete": "Delete value:",
            "insert_value": "Insert value:",
            "insert_pos": "Insert position:"
        }
        prompt = prompts.get(input_mode, "")
        txt = FONT.render(prompt + " " + input_text, True, (0, 0, 0))
        screen.blit(txt, (10, HEIGHT - 40))


def draw_linked_list(ll):
    screen.fill((240, 240, 240))
    draw_instructions()

    current = ll.head
    x, y = 80, HEIGHT // 2

    while current:
        draw_node(x, y, current.value)

        if current.next:
            draw_arrow((x + NODE_RADIUS, y), (x + 120 - NODE_RADIUS, y))

        x += 120
        current = current.next

    draw_input_box()
    pygame.display.flip()


# ===================== MAIN =====================
def main():
    global input_text, input_mode, insert_value_temp

    ll = LinkedList()
    running = True

    while running:
        draw_linked_list(ll)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                # ================= INPUT MODE =================
                if input_mode:
                    if event.key == pygame.K_RETURN:
                        try:
                            value = int(input_text)

                            if input_mode == "append":
                                ll.append(value)

                            elif input_mode == "delete":
                                ll.delete(value)

                            elif input_mode == "insert_value":
                                insert_value_temp = value
                                input_mode = "insert_pos"
                                input_text = ""
                                continue

                            elif input_mode == "insert_pos":
                                ll.insert_at(value, insert_value_temp)

                        except:
                            print("Invalid input")

                        input_text = ""
                        input_mode = None

                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]

                    else:
                        if event.unicode.isdigit():
                            input_text += event.unicode

                # ================= NORMAL MODE =================
                else:
                    if event.key == pygame.K_a:
                        input_mode = "append"

                    elif event.key == pygame.K_d:
                        input_mode = "delete"

                    elif event.key == pygame.K_i:
                        input_mode = "insert_value"

                    elif event.key == pygame.K_r:
                        ll.reverse_animated()

                    elif event.key == pygame.K_q:
                        running = False

        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()