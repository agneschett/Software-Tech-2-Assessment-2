"""
Task 2.2 Challenge - BST Visualiser
- Insert, Delete, Search with path highlight
- In/Pre/Post-order traversal animations
"""

import pygame
import sys

NODE_R = 22


class BSTNode:
    def __init__(self, v):
        self.value = v
        self.left = self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, v):
        def _ins(node, v):
            if not node: return BSTNode(v)
            if v < node.value: node.left = _ins(node.left, v)
            elif v > node.value: node.right = _ins(node.right, v)
            return node
        self.root = _ins(self.root, v)

    def delete(self, v):
        def _min(node):
            while node.left: node = node.left
            return node
        def _del(node, v):
            if not node: return None
            if v < node.value: node.left = _del(node.left, v)
            elif v > node.value: node.right = _del(node.right, v)
            else:
                if not node.left: return node.right
                if not node.right: return node.left
                s = _min(node.right)
                node.value = s.value
                node.right = _del(node.right, s.value)
            return node
        self.root = _del(self.root, v)

    def search_path(self, v):
        path, cur = [], self.root
        while cur:
            path.append(cur)
            if v == cur.value: return path, True
            cur = cur.left if v < cur.value else cur.right
        return path, False

    def inorder(self):
        res = []
        def _in(n):
            if n: _in(n.left); res.append(n); _in(n.right)
        _in(self.root); return res

    def preorder(self):
        res = []
        def _pre(n):
            if n: res.append(n); _pre(n.left); _pre(n.right)
        _pre(self.root); return res

    def postorder(self):
        res = []
        def _post(n):
            if n: _post(n.left); _post(n.right); res.append(n)
        _post(self.root); return res


def _positions(node, x, y, offset, pos=None):
    if pos is None: pos = {}
    if node:
        pos[node] = (x, y)
        _positions(node.left, x - offset, y + 70, max(offset // 2, 20), pos)
        _positions(node.right, x + offset, y + 70, max(offset // 2, 20), pos)
    return pos


def run(screen, font, clock, WIDTH, HEIGHT):
    bst = BST()
    for v in [50, 30, 70, 20, 40, 60, 80]:
        bst.insert(v)

    small = pygame.font.SysFont(None, 24)
    input_mode = None
    input_text = ""
    highlight_nodes = set()
    message = ""
    trav_list = []
    trav_idx = 0
    trav_timer = 0
    trav_name = ""

    BACK_BTN = pygame.Rect(20, 15, 90, 36)

    def draw(pos):
        screen.fill((20, 22, 30))

        # Back button
        pygame.draw.rect(screen, (100, 100, 120), BACK_BTN, border_radius=8)
        bt = small.render("Back", True, (240, 240, 240))
        screen.blit(bt, bt.get_rect(center=BACK_BTN.center))

        t = font.render("BST Visualiser", True, (180, 200, 255))
        screen.blit(t, (WIDTH // 2 - t.get_width() // 2, 18))

        # Edges
        for node, (x, y) in pos.items():
            for child in [node.left, node.right]:
                if child and child in pos:
                    pygame.draw.line(screen, (80, 100, 160), (x, y), pos[child], 2)

        # Nodes
        for node, (x, y) in pos.items():
            hl = node in highlight_nodes
            color = (220, 100, 80) if hl else (60, 120, 220)
            pygame.draw.circle(screen, color, (x, y), NODE_R)
            pygame.draw.circle(screen, (150, 180, 255), (x, y), NODE_R, 2)
            vt = font.render(str(node.value), True, (240, 240, 240))
            screen.blit(vt, vt.get_rect(center=(x, y)))

        # Traversal label
        if trav_name:
            tl = small.render(f"Traversal: {trav_name}", True, (200, 200, 100))
            screen.blit(tl, (20, 55))

        if message:
            mt = small.render(message, True, (200, 150, 80))
            screen.blit(mt, (20, 75))

        if input_mode:
            prompts = {"insert": "Insert:", "delete": "Delete:", "search": "Search:"}
            pt = font.render(prompts.get(input_mode, "") + " " + input_text + "_", True, (220, 220, 100))
            screen.blit(pt, (20, HEIGHT - 65))

        inst = small.render("I=Insert  D=Delete  S=Search  1=Inorder  2=Preorder  3=Postorder  ESC=back", True, (100, 110, 140))
        screen.blit(inst, (20, HEIGHT - 30))

    running = True
    while running:
        pos = _positions(bst.root, WIDTH // 2, 70, 180)
        draw(pos)

        # Step traversal animation
        if trav_list:
            now = pygame.time.get_ticks()
            if now - trav_timer > 500:
                trav_timer = now
                if trav_idx < len(trav_list):
                    highlight_nodes = {trav_list[trav_idx]}
                    trav_idx += 1
                else:
                    trav_list = []
                    highlight_nodes = set()

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if input_mode:
                    if event.key == pygame.K_RETURN:
                        try:
                            v = int(input_text)
                            if input_mode == "insert":
                                bst.insert(v); message = f"Inserted {v}"
                            elif input_mode == "delete":
                                bst.delete(v); message = f"Deleted {v}"; highlight_nodes = set()
                            elif input_mode == "search":
                                path, found = bst.search_path(v)
                                highlight_nodes = set(path)
                                message = f"Found {v}!" if found else f"{v} not found (path shown)"
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
                    elif event.key == pygame.K_i:
                        input_mode = "insert"; input_text = ""; highlight_nodes = set()
                    elif event.key == pygame.K_d:
                        input_mode = "delete"; input_text = ""
                    elif event.key == pygame.K_s:
                        input_mode = "search"; input_text = ""
                    elif event.key == pygame.K_1:
                        trav_list = bst.inorder(); trav_idx = 0; trav_timer = pygame.time.get_ticks(); trav_name = "In-order"
                    elif event.key == pygame.K_2:
                        trav_list = bst.preorder(); trav_idx = 0; trav_timer = pygame.time.get_ticks(); trav_name = "Pre-order"
                    elif event.key == pygame.K_3:
                        trav_list = bst.postorder(); trav_idx = 0; trav_timer = pygame.time.get_ticks(); trav_name = "Post-order"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not input_mode and BACK_BTN.collidepoint(event.pos):
                    return