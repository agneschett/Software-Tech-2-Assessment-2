import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()

NODE_RADIUS = 20


# ===================== BST NODE =====================
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

    def inorder(self):
        result = []

        def _inorder(node):
            if node:
                _inorder(node.left)
                result.append(node)
                _inorder(node.right)

        _inorder(self.root)
        return result


# ===================== DRAWING =====================
def draw_node(x, y, value, highlight=False):
    color = (255, 150, 150) if highlight else (100, 200, 250)
    pygame.draw.circle(screen, color, (x, y), NODE_RADIUS)

    text = FONT.render(str(value), True, (0, 0, 0))
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)


def draw_edge(start_pos, end_pos):
    pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos, 3)


def draw_tree(node, x, y, x_offset, nodes_pos, parent_pos=None):
    if node:
        nodes_pos[node] = (x, y)

        if parent_pos:
            draw_edge(parent_pos, (x, y))

        # Left subtree
        draw_tree(node.left, x - x_offset, y + 80, x_offset // 2, nodes_pos, (x, y))

        # Right subtree
        draw_tree(node.right, x + x_offset, y + 80, x_offset // 2, nodes_pos, (x, y))

        draw_node(x, y, node.value)


# ===================== MAIN =====================
def main():
    bst = BST()

    values = [50, 30, 70, 20, 40, 60, 80]
    for v in values:
        bst.insert(v)

    running = True
    highlight_idx = 0
    inorder_nodes = bst.inorder()

    while running:
        screen.fill((240, 240, 240))

        nodes_pos = {}
        draw_tree(bst.root, WIDTH // 2, 50, 150, nodes_pos)

        # Highlight current node in inorder traversal
        if highlight_idx < len(inorder_nodes):
            node = inorder_nodes[highlight_idx]

            # Recompute positions for highlighting
            def store_positions(node_, x, y, x_offset):
                if node_:
                    nodes_pos[node_] = (x, y)
                    store_positions(node_.left, x - x_offset, y + 80, x_offset // 2)
                    store_positions(node_.right, x + x_offset, y + 80, x_offset // 2)

            nodes_pos = {}
            store_positions(bst.root, WIDTH // 2, 50, 150)

            if node in nodes_pos:
                draw_node(*nodes_pos[node], node.value, highlight=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(1)  # Slow animation

        highlight_idx += 1
        if highlight_idx >= len(inorder_nodes):
            highlight_idx = 0

    pygame.quit()


if __name__ == "__main__":
    main()