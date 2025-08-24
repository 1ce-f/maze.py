import sys
import random
import time

# ------------------------------
# 画面クリア関数（PowerShell / CMD / Linux対応）
# ------------------------------
def clear_console():
    sys.stdout.write("\033[2J")   # 画面全体を消す
    sys.stdout.write("\033[H")    # カーソルを左上に戻す
    sys.stdout.flush()

# ------------------------------
# 迷路サイズ
# ------------------------------
W, H = 41, 21  # 奇数推奨（壁と通路をきれいに分けるため）

# ------------------------------
# 迷路初期化（全て壁）
# ------------------------------
maze = [["■" for _ in range(W)] for _ in range(H)]

# ------------------------------
# 迷路掘削（DFS再帰）
# ------------------------------
def carve(x, y):
    maze[y][x] = " "  # 壁を空白に変える
    directions = [(2,0), (-2,0), (0,2), (0,-2)]
    random.shuffle(directions)
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 < nx < W and 0 < ny < H and maze[ny][nx] == "■":
            maze[y + dy//2][x + dx//2] = " "
            carve(nx, ny)

start_x, start_y = 1, 1
carve(start_x, start_y)

goal_x, goal_y = W-2, H-2
maze[start_y][start_x] = "S"
maze[goal_y][goal_x] = "G"

# ------------------------------
# AI探索準備
# ------------------------------
ai_x, ai_y = start_x, start_y
moves = [(1,0),(0,1),(-1,0),(0,-1)]
visited = set()
path = []

# ------------------------------
# DFSでゴールまでの道筋を計算
# ------------------------------
def dfs(x, y):
    if (x, y) == (goal_x, goal_y):
        path.append((x, y))
        return True
    visited.add((x, y))
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < W and 0 <= ny < H and maze[ny][nx] != "■" and (nx, ny) not in visited:
            if dfs(nx, ny):
                path.append((x, y))
                return True
    return False

dfs(ai_x, ai_y)
path = path[::-1]  # 道筋を逆順に整理

# ------------------------------
# 迷路表示関数
# ------------------------------
def print_maze():
    for y in range(H):
        row = ""
        for x in range(W):
            if x == ai_x and y == ai_y:
                row += "A"
            else:
                row += maze[y][x]
        print(row)

# ------------------------------
# アニメーション
# ------------------------------
for px, py in path:
    ai_x, ai_y = px, py
    clear_console()
    print_maze()
    time.sleep(0.1)

print("\nゴール到達")
