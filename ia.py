import pygame
import random
import math
import time

# ---------- CONFIGURAÇÃO ----------
GRID_COLS = 13
GRID_ROWS = 11
TILE = 48
SCREEN_W = GRID_COLS * TILE
SCREEN_H = GRID_ROWS * TILE + 120
FPS = 60
PROB_BLOCK = 0.6
BOMB_FUSE = 2.0
EXPLOSION_DURATION = 0.6

# Cores
C_FLOOR = (200, 200, 200)
C_WALL = (80, 80, 80)
C_BLOCK = (150, 100, 60)
C_PLAYER = (30, 144, 255)
C_ENEMY = (255, 0, 0)
C_BOMB = (0, 0, 0)
C_EXPLOSION = (255, 140, 0)
C_UI = (40, 40, 40)
C_BTN = (220, 220, 220)
C_TEXT = (10, 10, 10)

# Tipos de célula
EMPTY, WALL, BLOCK = 0, 1, 2

pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Bomberman IA - Pydroid")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)

# ---------- FUNÇÕES DE MAPA ----------
def gerar_mapa(cols, rows, prob_block=0.6):
    grid = [[EMPTY for _ in range(cols)] for __ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if r == 0 or c == 0 or r == rows - 1 or c == cols - 1:
                grid[r][c] = WALL
    for r in range(2, rows - 1, 2):
        for c in range(2, cols - 1, 2):
            grid[r][c] = WALL
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if grid[r][c] == EMPTY:
                if (r, c) in [(1,1),(1,2),(2,1),(rows-2,cols-2),(rows-3,cols-2),(rows-2,cols-3)]:
                    continue
                if random.random() < prob_block:
                    grid[r][c] = BLOCK
    return grid

grid = gerar_mapa(GRID_COLS, GRID_ROWS, PROB_BLOCK)

# ---------- PLAYER E INIMIGO ----------
player = {"r": 1, "c": 1, "cooldown": 0.12, "last_move": 0}

enemy = {
    "r": GRID_ROWS - 2,
    "c": GRID_COLS - 2,
    "last_move": 0,
    "cooldown": 0.4,
    "last_bomb": 0,
    "bomb_cooldown": 3.0,
    "spawn_time": time.time(),
    "last_pos": (GRID_ROWS - 2, GRID_COLS - 2),
    "stuck_counter": 0,
    "last_dir": (0, 0)
}

# ---------- BOMBAS E EXPLOSÕES ----------
bombs = []
explosions = []

def place_bomb(r, c):
    for b in bombs:
        if b["r"] == r and b["c"] == c:
            return
    bombs.append({"r": r, "c": c, "placed_at": time.time()})

def explode_bomb(bomb):
    r, c = bomb["r"], bomb["c"]
    explosions.append({"r": r, "c": c, "started_at": time.time()})
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < GRID_ROWS and 0 <= nc < GRID_COLS and grid[nr][nc] != WALL:
            explosions.append({"r": nr, "c": nc, "started_at": time.time()})
            if grid[nr][nc] == BLOCK:
                grid[nr][nc] = EMPTY

def cleanup_bombs_and_explosions():
    now = time.time()
    to_explode = [b for b in bombs if now - b["placed_at"] >= BOMB_FUSE]
    for b in to_explode:
        explode_bomb(b)
        bombs.remove(b)
    for e in explosions[:]:
        if now - e["started_at"] >= EXPLOSION_DURATION:
            explosions.remove(e)

def is_cell_walkable(r, c):
    if not (0 <= r < GRID_ROWS and 0 <= c < GRID_COLS):
        return False
    if grid[r][c] in (WALL, BLOCK):
        return False
    for b in bombs:
        if b["r"] == r and b["c"] == c:
            return False
    return True

# checa se local (r,c) está "seguro" de bombas/ explosões próximas
def local_seguro(r, c):
    for e in explosions:
        if abs(e["r"] - r) + abs(e["c"] - c) <= 1:
            return False
    for b in bombs:
        if abs(b["r"] - r) + abs(b["c"] - c) <= 1:
            return False
    return True

# ---------- CLASSES DE ÁRVORE DE DECISÃO ----------
class Node:
    def evaluate(self, state):
        raise NotImplementedError

class DecisionNode(Node):
    def __init__(self, condition, true_branch, false_branch):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch
    def evaluate(self, state):
        try:
            if self.condition(state):
                return self.true_branch.evaluate(state)
            return self.false_branch.evaluate(state)
        except Exception as e:
            print("Erro em DecisionNode.condition:", e)
            return (0,0)

class ActionNode(Node):
    def __init__(self, action):
        self.action = action
    def evaluate(self, state):
        try:
            res = self.action(state)
            if res is None:
                return (0,0)
            return res
        except Exception as e:
            print("Erro em ActionNode:", e)
            return (0,0)

class SequenceNode(Node):
    def __init__(self, nodes):
        self.nodes = nodes

    def evaluate(self, state):
        last = (0, 0)
        for node in self.nodes:
            try:
                res = node.evaluate(state)
            except Exception as e:
                print("Erro em SequenceNode:", e)
                res = (0, 0)
            if res is None:
                res = (0, 0)
            if isinstance(res, (int, float)):
                res = (int(res), 0)
            try:
                dr, dc = res
                last = (dr, dc)
            except Exception:
                last = (0, 0)
        return last

# ---------- CONDIÇÕES E AÇÕES ----------

def cond_explosao_perto(state):
    r, c = state["r"], state["c"]
    for e in state["explosions"]:
        if abs(e["r"] - r) + abs(e["c"] - c) <= 1:
            return True
    return False

def cond_recem_spawn(state):
    now = time.time()
    enemy_data = state["enemy_data"]
    return now - enemy_data["spawn_time"] < 3.0

def cond_jogador_perto(state):
    r, c = state["r"], state["c"]
    pr, pc = state["player_r"], state["player_c"]
    return abs(pr - r) + abs(pc - c) <= 3

def cond_jogador_muito_perto(state):
    r, c = state["r"], state["c"]
    pr, pc = state["player_r"], state["player_c"]
    return abs(pr - r) + abs(pc - c) <= 2

def cond_quase_bloqueado(state):
    """Considera bloqueado se tiver 0 ou 1 saídas walkable."""
    r, c = state["r"], state["c"]
    livres = 0
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r + dr, c + dc
        if is_cell_walkable(nr, nc):
            livres += 1
    return livres <= 1

# ---------- AÇÕES ----------

def fugir(state):
    """Move o inimigo para longe da explosão uma direção."""
    r, c = state["r"], state["c"]
    if not state["explosions"]:
        return (0,0)
    # escolhe explosão mais próxima
    closest = min(state["explosions"], key=lambda e: abs(e["r"]-r)+abs(e["c"]-c))
    e = closest
    dr = 1 if r < e["r"] else -1 if r > e["r"] else 0
    dc = 1 if c < e["c"] else -1 if c > e["c"] else 0
    # tenta ir na direção oposta, se não for andar, tenta outra direção segura
    cand_dirs = []
    if dr != 0:
        cand_dirs.append((dr,0))
    if dc != 0:
        cand_dirs.append((0,dc))
    cand_dirs += [(1,0),(-1,0),(0,1),(0,-1)]
    for d in cand_dirs:
        nr, nc = r + d[0], c + d[1]
        if is_cell_walkable(nr, nc) and local_seguro(nr, nc):
            return d
    return (0,0)

def ir_ate_jogador(state):
    pr, pc = state["player_r"], state["player_c"]
    r, c = state["r"], state["c"]
    dr = 1 if pr > r else -1 if pr < r else 0
    dc = 1 if pc > c else -1 if pc < c else 0
    # prioriza movimento que seja walkable
    if dr != 0:
        if is_cell_walkable(r+dr, c):
            return (dr, 0)
    if dc != 0:
        if is_cell_walkable(r, c+dc):
            return (0, dc)
    # fallback: escolha aleatória válida
    for d in [(1,0),(-1,0),(0,1),(0,-1)]:
        nr, nc = r + d[0], c + d[1]
        if is_cell_walkable(nr, nc):
            return d
    return (0,0)

def encontrar_muro_entre_inimigo_e_jogador(state):
    r, c = state["r"], state["c"]
    pr, pc = state["player_r"], state["player_c"]

    # mesma linha
    if r == pr:
        step = 1 if pc > c else -1
        for cc in range(c + step, pc, step):
            if grid[r][cc] == WALL:
                return None
            if grid[r][cc] == BLOCK:
                return (r, cc)
    # mesma coluna
    if c == pc:
        step = 1 if pr > r else -1
        for rr in range(r + step, pr, step):
            if grid[rr][c] == WALL:
                return None
            if grid[rr][c] == BLOCK:
                return (rr, c)
    return None

def ir_ate_muro(state):
    """Mover até a célula ADJACENTE ao bloco destrutível."""
    alvo = encontrar_muro_entre_inimigo_e_jogador(state)
    if not alvo:
        return andar_aleatorio(state)
    mr, mc = alvo
    r, c = state["r"], state["c"]
    # se for na mesma linha, move horizontalmente até a célula antes do bloco
    if mr == r:
        if mc > c:
            target_c = mc - 1
        else:
            target_c = mc + 1
        if target_c == c:
            return (0, 0)  
        dc = 1 if target_c > c else -1
        if is_cell_walkable(r, c+dc):
            return (0, dc)
        # tenta caminho vertical se bloqueado
        for d in [(1,0),(-1,0)]:
            if is_cell_walkable(r + d[0], c):
                return d
        return (0,0)
    # se for na mesma coluna, move verticalmente até célula antes do bloco
    if mc == c:
        if mr > r:
            target_r = mr - 1
        else:
            target_r = mr + 1
        if target_r == r:
            return (0, 0)
        dr = 1 if target_r > r else -1
        if is_cell_walkable(r+dr, c):
            return (dr, 0)
        for d in [(0,1),(0,-1)]:
            if is_cell_walkable(r, c + d[1]):
                return d
        return (0,0)
    return andar_aleatorio(state)

def colocar_bomba_e_fugir(state):
    """Coloca bomba e foge para uma célula segura. Sempre retorna (dr,dc)."""
    now = time.time()
    enemy_data = state["enemy_data"]
    r, c = state["r"], state["c"]

    # bloqueio inicial
    if now - enemy_data.get("spawn_time", now) < 2.0:
        return (0, 0)

    # antes de plantar, verificar se existe pelo menos uma célula walkable e segura
    possiveis = []
    for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
        nr, nc = r + dr, c + dc
        if is_cell_walkable(nr, nc) and local_seguro(nr, nc):
            possiveis.append((dr, dc))
    if not possiveis:
        # sem rota de fuga segura, evita plantar
        return (0, 0)

    # planta bomba se cooldown permitir
    if now - enemy_data.get("last_bomb", 0) > enemy_data.get("bomb_cooldown", 3.0):
        place_bomb(r, c)
        enemy_data["last_bomb"] = now

    # escolhido um destino seguro para fugir
    return random.choice(possiveis)

def colocar_bomba(state):
    now = time.time()
    enemy_data = state["enemy_data"]
    if now - enemy_data.get("last_bomb", 0) > enemy_data.get("bomb_cooldown", 3.0):
        place_bomb(state["r"], state["c"])
        enemy_data["last_bomb"] = now
    return (0, 0)

def andar_aleatorio(state):
    """Evita imediatamente voltar na direção oposta."""
    enemy_data = state["enemy_data"]
    opostos = {(1,0):(-1,0), (-1,0):(1,0), (0,1):(0,-1), (0,-1):(0,1)}
    direcoes = [(1,0),(-1,0),(0,1),(0,-1)]
    last = enemy_data.get("last_dir", (0,0))
    # remove o oposto da última direção se possível
    to_try = [d for d in direcoes if d != opostos.get(last)]
    random.shuffle(to_try)
    for d in to_try:
        nr, nc = state["r"] + d[0], state["c"] + d[1]
        if is_cell_walkable(nr, nc):
            enemy_data["last_dir"] = d
            return d
    # fallback: tenta qualquer direção válida
    for d in direcoes:
        nr, nc = state["r"] + d[0], state["c"] + d[1]
        if is_cell_walkable(nr, nc):
            enemy_data["last_dir"] = d
            return d
    return (0,0)

# ---------- ÁRVORE DE DECISÃO ----------
ai_tree = DecisionNode(
    cond_recem_spawn,
    ActionNode(andar_aleatorio),  # nos primeiros segundos, só explora
    DecisionNode(
        cond_explosao_perto,
        ActionNode(fugir),
        DecisionNode(cond_quase_bloqueado,
            SequenceNode([
                ActionNode(ir_ate_muro),
                ActionNode(colocar_bomba_e_fugir),
                ActionNode(fugir)
            ]),
            DecisionNode(cond_jogador_muito_perto,
                ActionNode(colocar_bomba_e_fugir),
                DecisionNode(cond_jogador_perto,
                    ActionNode(ir_ate_jogador),
                    ActionNode(andar_aleatorio)
                )
            )
        )
    )
  ) 


# ---------- INTERFACE ----------
btn_size = 64
pad_margin = 12
pad_x = pad_margin + btn_size
pad_y = SCREEN_H - 60
btn_up = pygame.Rect(pad_x - btn_size//2, pad_y - btn_size - 6, btn_size, btn_size)
btn_left = pygame.Rect(pad_x - btn_size - 6, pad_y, btn_size, btn_size)
btn_down = pygame.Rect(pad_x - btn_size//2, pad_y + btn_size + 6, btn_size, btn_size)
btn_right = pygame.Rect(pad_x + btn_size + 6 - btn_size//2, pad_y, btn_size, btn_size)
btn_bomb = pygame.Rect(SCREEN_W - pad_margin - btn_size, pad_y - btn_size//2, btn_size, btn_size)

def draw_text(txt, x, y):
    screen.blit(font.render(txt, True, C_TEXT), (x, y))

def try_move_player(dr, dc):
    now = time.time()
    if now - player["last_move"] < player["cooldown"]:
        return
    nr, nc = player["r"] + dr, player["c"] + dc
    if is_cell_walkable(nr, nc):
        player["r"], player["c"] = nr, nc
        player["last_move"] = now

# ---------- LOOP PRINCIPAL ----------
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if btn_up.collidepoint(mx,my): try_move_player(-1, 0)
            elif btn_down.collidepoint(mx,my): try_move_player(1, 0)
            elif btn_left.collidepoint(mx,my): try_move_player(0, -1)
            elif btn_right.collidepoint(mx,my): try_move_player(0, 1)
            elif btn_bomb.collidepoint(mx,my): place_bomb(player["r"], player["c"])
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: try_move_player(-1, 0)
            elif event.key == pygame.K_DOWN: try_move_player(1, 0)
            elif event.key == pygame.K_LEFT: try_move_player(0, -1)
            elif event.key == pygame.K_RIGHT: try_move_player(0, 1)
            elif event.key == pygame.K_SPACE: place_bomb(player["r"], player["c"])

    cleanup_bombs_and_explosions()

    # IA inimigo
    state = {
        "r": enemy["r"],
        "c": enemy["c"],
        "player_r": player["r"],
        "player_c": player["c"],
        "explosions": explosions,
        "enemy_data": enemy
    }

    # chamada segura da IA (previne retorno None)
    try:
        result = ai_tree.evaluate(state)
        if result is None:
            result = (0, 0)
        if isinstance(result, (int, float)):
            result = (int(result), 0)
        dr, dc = result
    except Exception as e:
        print("Erro avaliando ai_tree:", e)
        dr, dc = (0, 0)

    now = time.time()
    if now - enemy["last_move"] > enemy["cooldown"]:
        nr, nc = enemy["r"] + dr, enemy["c"] + dc
        if is_cell_walkable(nr, nc):
            enemy["r"], enemy["c"] = nr, nc
            enemy["last_move"] = now

    # anti-stuck: se não progrediu, aumenta contador; se travado, força passo aleatório válido
    if (enemy["r"], enemy["c"]) == enemy.get("last_pos", (-1,-1)):
        enemy["stuck_counter"] = enemy.get("stuck_counter", 0) + 1
    else:
        enemy["stuck_counter"] = 0
    enemy["last_pos"] = (enemy["r"], enemy["c"])

    if enemy["stuck_counter"] > 8:
        moved = False
        for _ in range(8):
            drx, dcx = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
            nr, nc = enemy["r"] + drx, enemy["c"] + dcx
            if is_cell_walkable(nr, nc):
                enemy["r"], enemy["c"] = nr, nc
                enemy["stuck_counter"] = 0
                enemy["last_dir"] = (drx, dcx)
                moved = True
                break
        if not moved:
            enemy["stuck_counter"] = 0

    # colisão jogador-explosão
    for e in explosions:
        if e["r"] == player["r"] and e["c"] == player["c"]:
            player["r"], player["c"] = 1, 1

    # desenhar mapa
    screen.fill((0,0,0))
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            x, y = c*TILE, r*TILE
            cell = grid[r][c]
            if cell == EMPTY:
                pygame.draw.rect(screen, C_FLOOR, (x, y, TILE, TILE))
            elif cell == WALL:
                pygame.draw.rect(screen, C_WALL, (x, y, TILE, TILE))
            elif cell == BLOCK:
                pygame.draw.rect(screen, C_FLOOR, (x, y, TILE, TILE))
                pygame.draw.rect(screen, C_BLOCK, (x+6, y+6, TILE-12, TILE-12))
            pygame.draw.rect(screen, (160,160,160), (x,y,TILE,TILE), 1)

    # bombas
    for b in bombs:
        bx, by = b["c"]*TILE + TILE//2, b["r"]*TILE + TILE//2
        pygame.draw.circle(screen, C_BOMB, (bx, by), 12)
    # explosões
    for e in explosions:
        ex, ey = e["c"]*TILE, e["r"]*TILE
        pygame.draw.rect(screen, C_EXPLOSION, (ex, ey, TILE, TILE))

    # jogador
    px, py = player["c"]*TILE + TILE//2, player["r"]*TILE + TILE//2
    pygame.draw.circle(screen, C_PLAYER, (px, py), TILE//3)
    # inimigo
    ex, ey = enemy["c"]*TILE + TILE//2, enemy["r"]*TILE + TILE//2
    pygame.draw.circle(screen, C_ENEMY, (ex, ey), TILE//3)

    # UI
    pygame.draw.rect(screen, C_UI, (0, SCREEN_H - 120, SCREEN_W, 120))
    for btn, label in [(btn_up,"↑"),(btn_left,"←"),(btn_down,"↓"),(btn_right,"→")]:
        pygame.draw.rect(screen, C_BTN, btn)
        draw_text(label, btn.centerx-6, btn.centery-8)
    pygame.draw.rect(screen, C_BTN, btn_bomb)
    draw_text("BOMBA", btn_bomb.left+6, btn_bomb.centery-8)
    draw_text("IA: foge, destrói blocos quando útil, explora", 10, SCREEN_H - 110)

    pygame.display.flip()

pygame.quit()