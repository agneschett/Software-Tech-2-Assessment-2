import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 900, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BST Visualiser")

FONT = pygame.font.SysFont(None, 28)
clock = pygame.time.Clock()

NODE_RADIUS = 20

input_text = ""
input_mode = None
message = ""


# ===================== NODE =====================
class BSTNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


# ===================== BST =====================
class BST:
    def __init__(self):
        self.root = None

    def insert(self, value):
        def _insert(node, value):
            if not node:
                return BSTNode(value)
            if value < node.value:
                node.left = _insert(node.left, value)
            elif value > node.value:
                node.right = _insert(node.right, value)
            return node

        self.root = _insert(self.root, value)

    # -------- Traversals --------
    def inorder(self):
        result = []

        def _in(node):
            if node:
                _in(node.left)
                result.append(node)
                _in(node.right)

        _in(self.root)
        return result

    def preorder(self):
        result = []

        def _pre(node):
            if node:
                result.append(node)
                _pre(node.left)
                _pre(node.right)

        _pre(self.root)
        return result

    def postorder(self):
        result = []

        def _post(node):
            if node:
                _post(node.left)
                _post(node.right)
                result.append(node)

        _post(self.root)
        return result

    # -------- Search Path --------
    def search_path(self, value):
        path = []
        current = self.root

        while current:
            path.append(current)

            if value == current.value:
                return path
            elif value < current.value:
                current = current.left
            else:
                current = current.right

        return path  # not found, still return path

    # -------- Delete --------
    def delete(self, value):
        def _delete(node, value):
            if not node:
                return None

            if value < node.value:
                node.left = _delete(node.left, value)
            elif value > node.value:
                node.right = _delete(node.right, value)
            else:
                # Case 1: No child
                if not node.left and not node.right:
                    return None

                # Case 2: One child
                if not node.left:
                    return node.right
                if not node.right:
                    return node.left

                # Case 3: Two children
                successor = self.get_min(node.right)
                node.value = successor.value
                node.right = _delete(node.right, successor.value)

            return node

        self.root = _delete(self.root, value)

    def get_min(self, node):
        while node.left:
            node = node.left
        return node


# ===================== DRAW =====================
def draw_node(x, y, value, highlight=False):
    color = (255, 120, 120) if highlight else (100, 200, 250)
    pygame.draw.circle(screen, color, (x, y), NODE_RADIUS)

    text = FONT.render(str(value), True, (0, 0, 0))
    screen.blit(text, text.get_rect(center=(x, y)))


def draw_edge(start, end):
    pygame.draw.line(screen, (0, 0, 0), start, end, 2)


def draw_tree(node, x, y, offset, positions, parent=None):
    if node:
        positions[node] = (x, y)

        if parent:
            draw_edge(parent, (x, y))

        draw_tree(node.left, x - offset, y + 70, offset // 2, positions, (x, y))
        draw_tree(node.right, x + offset, y + 70, offset // 2, positions, (x, y))

        draw_node(x, y, node.value)


def draw_ui():
    instructions = [
        "I=Insert  D=Delete  S=Search",
        "1=Inorder  2=Preorder  3=Postorder"
    ]
    for i, txt in enumerate(instructions):
        screen.blit(FONT.render(txt, True, (0, 0, 0)), (10, 10 + i * 20))

    if input_mode:
        screen.blit(FONT.render("Enter value: " + input_text, True, (0, 0, 0)), (10, HEIGHT - 40))

    if message:
        screen.blit(FONT.render(message, True, (200, 0, 0)), (10, HEIGHT - 70))


# ===================== MAIN =====================
def main():
    global input_text, input_mode, message

    bst = BST()
    for v in [50, 30, 70, 20, 40, 60, 80]:
        bst.insert(v)

    highlight_nodes = []
    traversal_list = []
    index = 0

    running = True

    while running:
        screen.fill((240, 240, 240))

        positions = {}
        draw_tree(bst.root, WIDTH // 2, 60, 150, positions)

        # Highlight nodes
        for node in highlight_nodes:
            if node in positions:
                draw_node(*positions[node], node.value, highlight=True)

        draw_ui()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                # INPUT MODE
                if input_mode:
                    if event.key == pygame.K_RETURN:
                        val = int(input_text)

                        if input_mode == "insert":
                            bst.insert(val)

                        elif input_mode == "delete":
                            bst.delete(val)

                        elif input_mode == "search":
                            highlight_nodes = bst.search_path(val)
                            message = "Found!" if highlight_nodes and highlight_nodes[-1].value == val else "Not Found"

                        input_text = ""
                        input_mode = None

                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]

                    else:
                        if event.unicode.isdigit():
                            input_text += event.unicode

                # NORMAL MODE
                else:
                    if event.key == pygame.K_i:
                        input_mode = "insert"
                    elif event.key == pygame.K_d:
                        input_mode = "delete"
                    elif event.key == pygame.K_s:
                        input_mode = "search"

                    elif event.key == pygame.K_1:
                        traversal_list = bst.inorder()
                        index = 0
                    elif event.key == pygame.K_2:
                        traversal_list = bst.preorder()
                        index = 0
                    elif event.key == pygame.K_3:
                        traversal_list = bst.postorder()
                        index = 0

        # Animate traversal
        if traversal_list:
            highlight_nodes = [traversal_list[index]]
            pygame.time.wait(400)
            index += 1
            if index >= len(traversal_list):
                traversal_list = []

        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
    