"""
Task 3.1 Challenge - Graph BFS & DFS Visualiser
- Click any node to start traversal
- Toggle BFS / DFS
- Shows traversal order on screen
- Back button
"""

import pygame
import sys
import collections

NODE_R = 25

nodes_pos = {
    'A': (120, 120), 'B': (280, 70),  'C': (280, 220),
    'D': (440, 120), 'E': (580, 180), 'F': (440, 320)
}

graph = {
    'A': ['B', 'C'], 'B': ['A', 'D', 'E'],
    'C': ['A', 'F'], 'D': ['B'],
    'E': ['B', 'F'], 'F': ['C', 'E']
}


def run(screen, font, clock, WIDTH, HEIGHT):
    small = pygame.font.SysFont(None, 24)
    traversal_order = []
    visited_nodes = set()
    frontier_nodes = set()
    current_node = None
    mode = "BFS"    # or "DFS"
    running_trav = False
    trav_steps = []   # list of (visited_snapshot, frontier, current, order_snapshot)
    step_idx = 0
    step_timer = 0

    # Layout: title at top, buttons below title, graph nodes shifted down below header
    TITLE_Y  = 14
    BTN_Y    = 56
    BFS_BTN  = pygame.Rect(20,  BTN_Y, 100, 38)
    DFS_BTN  = pygame.Rect(135, BTN_Y, 100, 38)
    BACK_BTN = pygame.Rect(WIDTH - 120, BTN_Y, 100, 38)

    # Shift all nodes down so they sit well below the header (buttons end ~y=94)
    NODE_OFFSET_Y = 120
    scaled_nodes = {
        'A': (120, NODE_OFFSET_Y + 80),
        'B': (300, NODE_OFFSET_Y + 20),
        'C': (200, NODE_OFFSET_Y + 200),
        'D': (460, NODE_OFFSET_Y + 80),
        'E': (580, NODE_OFFSET_Y + 170),
        'F': (380, NODE_OFFSET_Y + 310),
    }

    def compute_bfs(start):
        steps = []
        visited = set(); queue = collections.deque([start]); order = []
        while queue:
            cur = queue.popleft()
            if cur in visited: continue
            visited.add(cur); order.append(cur)
            steps.append((frozenset(visited), frozenset(queue), cur, list(order)))
            for nb in graph[cur]:
                if nb not in visited and nb not in queue:
                    queue.append(nb)
        return steps

    def compute_dfs(start):
        steps = []
        visited = set(); stack = [start]; order = []
        while stack:
            cur = stack.pop()
            if cur in visited: continue
            visited.add(cur); order.append(cur)
            steps.append((frozenset(visited), frozenset(stack), cur, list(order)))
            for nb in reversed(graph[cur]):
                if nb not in visited:
                    stack.append(nb)
        return steps

    def draw(vis, frontier, current, order):
        screen.fill((20, 22, 30))

        # Title
        t = font.render(f"Graph Traversal — {mode}  (click a node to start)", True, (180, 200, 255))
        screen.blit(t, (WIDTH // 2 - t.get_width() // 2, TITLE_Y))

        # Buttons
        for btn, lbl, c in [(BFS_BTN, "BFS", (60,160,100)), (DFS_BTN, "DFS", (160,80,160)), (BACK_BTN, "Back", (100,100,120))]:
            active = (lbl == mode)
            pygame.draw.rect(screen, c if not active else tuple(min(x+60,255) for x in c), btn, border_radius=8)
            bt = small.render(lbl, True, (240, 240, 240))
            screen.blit(bt, bt.get_rect(center=btn.center))

        # Edges
        drawn = set()
        for node, neighbors in graph.items():
            x1, y1 = scaled_nodes[node]
            for nb in neighbors:
                key = frozenset([node, nb])
                if key not in drawn:
                    x2, y2 = scaled_nodes[nb]
                    pygame.draw.line(screen, (80, 100, 160), (x1, y1), (x2, y2), 2)
                    drawn.add(key)

        # Nodes
        for node, (x, y) in scaled_nodes.items():
            color = (55, 70, 110)
            if node in vis:      color = (60, 190, 110)
            if node in frontier: color = (220, 180, 60)
            if node == current:  color = (220, 80, 80)
            pygame.draw.circle(screen, color, (x, y), NODE_R)
            pygame.draw.circle(screen, (150, 180, 255), (x, y), NODE_R, 2)
            nt = font.render(node, True, (240, 240, 240))
            screen.blit(nt, nt.get_rect(center=(x, y)))

        # Legend
        for col, lbl, lx in [((60,190,110),"Visited",20), ((220,180,60),"Frontier",110), ((220,80,80),"Current",220)]:
            pygame.draw.circle(screen, col, (lx, HEIGHT - 50), 8)
            lt = small.render(lbl, True, (180, 190, 210))
            screen.blit(lt, (lx + 14, HEIGHT - 58))

        # Order
        ot = small.render("Order: " + " → ".join(order), True, (200, 210, 255))
        screen.blit(ot, (20, HEIGHT - 28))

        pygame.display.flip()

    def get_clicked_node(pos):
        for node, (x, y) in scaled_nodes.items():
            if ((pos[0]-x)**2 + (pos[1]-y)**2)**0.5 <= NODE_R:
                return node
        return None

    draw(set(), set(), None, [])
    running = True
    while running:
        # Animate traversal steps
        if running_trav and step_idx < len(trav_steps):
            now = pygame.time.get_ticks()
            if now - step_timer > 700:
                step_timer = now
                vis, frontier, cur, order = trav_steps[step_idx]
                draw(vis, frontier, cur, order)
                step_idx += 1
        elif not running_trav or step_idx >= len(trav_steps):
            if trav_steps and step_idx >= len(trav_steps):
                vis, frontier, cur, order = trav_steps[-1]
                draw(vis, set(), None, order)
            elif not running_trav:
                draw(set(), set(), None, [])

        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if BFS_BTN.collidepoint(pos):
                    mode = "BFS"; trav_steps = []; running_trav = False; step_idx = 0
                elif DFS_BTN.collidepoint(pos):
                    mode = "DFS"; trav_steps = []; running_trav = False; step_idx = 0
                elif BACK_BTN.collidepoint(pos):
                    return
                else:
                    node = get_clicked_node(pos)
                    if node:
                        trav_steps = compute_bfs(node) if mode == "BFS" else compute_dfs(node)
                        step_idx = 0; running_trav = True; step_timer = pygame.time.get_ticks()