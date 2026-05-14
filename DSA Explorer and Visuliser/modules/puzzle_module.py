"""
Task 3.3 Challenge - Puzzle Module
Part A: Grid Pathfinding with obstacles + path reconstruction
Part B: Coin Change DP Visualiser
"""

import pygame
import sys
import heapq
import random

ROWS, COLS = 10, 10


# ─── PART A: GRID PATHFINDING ────────────────────────────────────────────────

def run_grid_puzzle(screen, font, clock, WIDTH, HEIGHT):
    CELL = min((WIDTH - 220) // COLS, (HEIGHT - 100) // ROWS)
    OFF_X = 20
    OFF_Y = 80
    small = pygame.font.SysFont(None, 22)

    grid = [[0] * COLS for _ in range(ROWS)]  # 0=open, 1=obstacle
    start = (0, 0)
    end = (ROWS - 1, COLS - 1)
    path = []
    visited_cells = set()
    mode = "obstacle"   # "obstacle", "start", "end"
    status = "Click cells to add obstacles | Right-click to remove | Run to find path"

    BTN_X = WIDTH - 195
    btns = {
        "Run A*":    pygame.Rect(BTN_X, 80,  185, 38),
        "Run Dijkstra": pygame.Rect(BTN_X, 128, 185, 38),
        "Clear Path": pygame.Rect(BTN_X, 176, 185, 38),
        "Reset Grid": pygame.Rect(BTN_X, 224, 185, 38),
        "Back":       pygame.Rect(BTN_X, 272, 185, 38),
    }

    def cell_rect(r, c):
        return pygame.Rect(OFF_X + c * CELL, OFF_Y + r * CELL, CELL - 1, CELL - 1)

    def get_cell(pos):
        x, y = pos
        c = (x - OFF_X) // CELL
        r = (y - OFF_Y) // CELL
        if 0 <= r < ROWS and 0 <= c < COLS:
            return (r, c)
        return None

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def astar():
        open_set = [(0, start)]
        came_from = {}
        g = {start: 0}
        f = {start: heuristic(start, end)}
        visited = set()
        while open_set:
            _, cur = heapq.heappop(open_set)
            if cur in visited: continue
            visited.add(cur)
            if cur == end:
                p = []
                while cur in came_from:
                    p.append(cur); cur = came_from[cur]
                p.append(start)
                return list(reversed(p)), visited
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nb = (cur[0]+dr, cur[1]+dc)
                if 0<=nb[0]<ROWS and 0<=nb[1]<COLS and grid[nb[0]][nb[1]] == 0:
                    ng = g[cur] + 1
                    if ng < g.get(nb, 9999):
                        g[nb] = ng; came_from[nb] = cur
                        heapq.heappush(open_set, (ng + heuristic(nb, end), nb))
        return [], visited

    def dijkstra():
        open_set = [(0, start)]
        came_from = {}
        dist = {start: 0}
        visited = set()
        while open_set:
            d, cur = heapq.heappop(open_set)
            if cur in visited: continue
            visited.add(cur)
            if cur == end:
                p = []
                while cur in came_from:
                    p.append(cur); cur = came_from[cur]
                p.append(start)
                return list(reversed(p)), visited
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nb = (cur[0]+dr, cur[1]+dc)
                if 0<=nb[0]<ROWS and 0<=nb[1]<COLS and grid[nb[0]][nb[1]] == 0:
                    nd = dist[cur] + 1
                    if nd < dist.get(nb, 9999):
                        dist[nb] = nd; came_from[nb] = cur
                        heapq.heappush(open_set, (nd, nb))
        return [], visited

    def draw():
        screen.fill((20, 22, 30))
        t = font.render("Pathfinding Puzzle  (A* / Dijkstra)", True, (180, 200, 255))
        screen.blit(t, (20, 10))
        st = small.render(status, True, (160, 170, 200))
        screen.blit(st, (20, 45))

        for r in range(ROWS):
            for c in range(COLS):
                rect = cell_rect(r, c)
                color = (55, 65, 95)
                if grid[r][c] == 1:  color = (180, 60, 60)
                if (r, c) in visited_cells: color = (60, 90, 160)
                if (r, c) in path:   color = (80, 220, 120)
                if (r, c) == start:  color = (60, 220, 180)
                if (r, c) == end:    color = (220, 160, 60)
                pygame.draw.rect(screen, color, rect, border_radius=3)
                pygame.draw.rect(screen, (40, 48, 70), rect, 1, border_radius=3)

        # Start/End labels
        sr = cell_rect(*start)
        er = cell_rect(*end)
        st_t = small.render("S", True, (20, 20, 30))
        en_t = small.render("E", True, (20, 20, 30))
        screen.blit(st_t, st_t.get_rect(center=sr.center))
        screen.blit(en_t, en_t.get_rect(center=er.center))

        # Side buttons
        for lbl, btn in btns.items():
            c = (60,140,200) if "Run" in lbl else (100,100,120) if lbl == "Back" else (80,80,100)
            pygame.draw.rect(screen, c, btn, border_radius=8)
            bt = small.render(lbl, True, (240,240,240))
            screen.blit(bt, bt.get_rect(center=btn.center))

        # Legend
        legend = [((60,220,180),"Start"), ((220,160,60),"End"), ((180,60,60),"Wall"),
                  ((80,220,120),"Path"), ((60,90,160),"Explored")]
        for i, (c, lbl) in enumerate(legend):
            pygame.draw.rect(screen, c, (BTN_X, 330 + i*24, 14, 14), border_radius=3)
            screen.blit(small.render(lbl, True, (180,190,210)), (BTN_X + 20, 330 + i*24))

        if path:
            pl = small.render(f"Path length: {len(path)-1} steps", True, (80, 220, 120))
            screen.blit(pl, (BTN_X, 460))

        pygame.display.flip()

    def animate_path(p, vis):
        nonlocal path, visited_cells
        visited_cells = set()
        path = []
        for cell in vis:
            visited_cells.add(cell)
            draw(); pygame.time.wait(30)
            for e in pygame.event.get():
                if e.type == pygame.QUIT: pygame.quit(); sys.exit()
        for cell in p:
            path.append(cell)
            draw(); pygame.time.wait(60)

    running = True
    while running:
        draw()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                for lbl, btn in btns.items():
                    if btn.collidepoint(pos):
                        if lbl == "Run A*":
                            p, vis = astar()
                            if p: animate_path(p, vis); status = f"A*: path found ({len(p)-1} steps)"
                            else: status = "A*: no path found!"
                        elif lbl == "Run Dijkstra":
                            p, vis = dijkstra()
                            if p: animate_path(p, vis); status = f"Dijkstra: path found ({len(p)-1} steps)"
                            else: status = "Dijkstra: no path found!"
                        elif lbl == "Clear Path":
                            path = []; visited_cells = set(); status = "Path cleared"
                        elif lbl == "Reset Grid":
                            grid[:] = [[0]*COLS for _ in range(ROWS)]
                            path = []; visited_cells = set(); status = "Grid reset"
                        elif lbl == "Back":
                            return
                        break
                else:
                    cell = get_cell(pos)
                    if cell and cell != start and cell != end:
                        if event.button == 1:
                            grid[cell[0]][cell[1]] = 1
                        elif event.button == 3:
                            grid[cell[0]][cell[1]] = 0
            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                cell = get_cell(event.pos)
                if cell and cell != start and cell != end:
                    grid[cell[0]][cell[1]] = 1


# ─── PART B: COIN CHANGE DP ──────────────────────────────────────────────────

def run_coin_change(screen, font, clock, WIDTH, HEIGHT):
    small = pygame.font.SysFont(None, 24)
    coins = [1, 3, 4, 5]
    amount = 15
    dp = None
    coin_used = None
    step = 0
    running_anim = False
    anim_timer = 0
    ANIM_DELAY = 400
    BACK_BTN = pygame.Rect(20, 10, 90, 36)
    RUN_BTN  = pygame.Rect(125, 10, 90, 36)

    CELL_W = min(50, (WIDTH - 60) // (amount + 1))
    CELL_H = 50

    def draw(highlight_i=None):
        screen.fill((20, 22, 30))
        t = font.render("Coin Change — Dynamic Programming", True, (180, 200, 255))
        screen.blit(t, (WIDTH // 2 - t.get_width() // 2, 10))

        ct = small.render(f"Coins: {coins}   |   Target amount: {amount}", True, (160, 200, 160))
        screen.blit(ct, (20, 55))

        # Column headers
        for i in range(amount + 1):
            x = 30 + i * CELL_W
            ht = small.render(str(i), True, (120, 130, 160))
            screen.blit(ht, (x + CELL_W//2 - ht.get_width()//2, 95))

        # DP row
        if dp:
            for i in range(amount + 1):
                x = 30 + i * CELL_W
                rect = pygame.Rect(x, 120, CELL_W - 2, CELL_H)
                color = (255, 180, 80) if i == highlight_i else (60, 100, 180)
                pygame.draw.rect(screen, color, rect, border_radius=6)
                pygame.draw.rect(screen, (100, 130, 220), rect, 2, border_radius=6)
                val = dp[i]
                if val < 999:
                    vt = font.render(str(val), True, (240, 240, 240))
                    screen.blit(vt, vt.get_rect(center=rect.center))
                else:
                    vt = small.render("∞", True, (200, 100, 100))
                    screen.blit(vt, vt.get_rect(center=rect.center))

        # Coin used row
        if coin_used:
            ut = small.render("Coin used:", True, (160, 200, 160))
            screen.blit(ut, (20, 185))
            for i in range(1, amount + 1):
                x = 30 + i * CELL_W
                rect = pygame.Rect(x, 200, CELL_W - 2, CELL_H - 10)
                pygame.draw.rect(screen, (50, 70, 100), rect, border_radius=6)
                if coin_used[i]:
                    ct2 = small.render(str(coin_used[i]), True, (200, 220, 100))
                    screen.blit(ct2, ct2.get_rect(center=rect.center))

        # Result
        if dp and step >= amount:
            ans = dp[amount]
            msg = f"Minimum coins for {amount}: {ans}" if ans < 999 else "No solution!"
            rt = font.render(msg, True, (80, 220, 120) if ans < 999 else (220, 80, 80))
            screen.blit(rt, (20, 270))

            # Show coin breakdown
            if ans < 999 and coin_used:
                breakdown = []
                cur = amount
                while cur > 0 and coin_used[cur]:
                    breakdown.append(coin_used[cur]); cur -= coin_used[cur]
                bt = small.render("Coins: " + " + ".join(map(str, breakdown)), True, (200, 210, 255))
                screen.blit(bt, (20, 305))

        # Buttons
        for btn, lbl, c in [(BACK_BTN,"Back",(100,100,120)), (RUN_BTN,"Run",(60,160,100))]:
            pygame.draw.rect(screen, c, btn, border_radius=8)
            btt = small.render(lbl, True, (240,240,240))
            screen.blit(btt, btt.get_rect(center=btn.center))

        inst = small.render("ESC = back to puzzles", True, (100, 110, 140))
        screen.blit(inst, (20, HEIGHT - 30))
        pygame.display.flip()

    draw()
    running = True
    while running:
        now = pygame.time.get_ticks()
        if running_anim and now - anim_timer > ANIM_DELAY:
            anim_timer = now
            if step <= amount:
                for coin in coins:
                    if step - coin >= 0 and dp[step - coin] + 1 < dp[step]:
                        dp[step] = dp[step - coin] + 1
                        coin_used[step] = coin
                draw(highlight_i=step)
                step += 1
            else:
                running_anim = False

        if not running_anim:
            draw(highlight_i=step if dp and step <= amount else None)

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
                elif RUN_BTN.collidepoint(pos):
                    dp = [999] * (amount + 1); dp[0] = 0
                    coin_used = [None] * (amount + 1)
                    step = 1; running_anim = True; anim_timer = now


# ─── PUZZLE HUB ──────────────────────────────────────────────────────────────

def run(screen, font, clock, WIDTH, HEIGHT):
    small = pygame.font.SysFont(None, 28)
    items = [
        ("Grid Pathfinding  (A* / Dijkstra)", run_grid_puzzle),
        ("Coin Change DP Visualiser",          run_coin_change),
        ("Back",                               None),
    ]
    selected = 0

    running = True
    while running:
        screen.fill((20, 22, 30))
        t = font.render("Puzzle Challenges", True, (180, 200, 255))
        screen.blit(t, (WIDTH // 2 - t.get_width() // 2, 60))

        for i, (lbl, _) in enumerate(items):
            color = (255, 200, 80) if i == selected else (160, 170, 200)
            rect = pygame.Rect(WIDTH // 2 - 220, 160 + i * 60, 440, 48)
            bg = (50, 60, 90) if i == selected else (30, 36, 55)
            pygame.draw.rect(screen, bg, rect, border_radius=10)
            pygame.draw.rect(screen, color, rect, 2, border_radius=10)
            txt = font.render(lbl, True, color)
            screen.blit(txt, txt.get_rect(center=rect.center))

        inst = small.render("↑↓ navigate   ENTER select   ESC = back", True, (100, 110, 140))
        screen.blit(inst, (WIDTH // 2 - inst.get_width() // 2, HEIGHT - 40))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(items)
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(items)
                elif event.key == pygame.K_RETURN:
                    lbl, fn = items[selected]
                    if fn is None: return
                    fn(screen, font, clock, WIDTH, HEIGHT)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, (lbl, fn) in enumerate(items):
                    rect = pygame.Rect(WIDTH // 2 - 220, 160 + i * 60, 440, 48)
                    if rect.collidepoint(event.pos):
                        if fn is None: return
                        fn(screen, font, clock, WIDTH, HEIGHT)

        clock.tick(30)
