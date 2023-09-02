#문제 이해 못했음 -> 설명 필요

from collections import deque

n, q = tuple(map(int, input().split()))
size = (1 << n)
grid = [list(map(int, input().split())) for _ in range(size)]
levels = list(map(int, input().split()))
next_grid = [[0 for _ in range(size)] for _ in range(size)]
bfs_q = deque()
visited = [[0 for _ in range(size)] for _ in range(size)]
dxs, dys = [0, 1, -1, 0], [1, 0, 0, -1]


def bfs():
    group_size = 0
    while bfs_q:
        curr_x, curr_y = bfs_q.popleft()
        group_size += 1
        for dx, dy in zip(dxs, dys):
            new_x, new_y = curr_x + dx, curr_y + dy
            if 0 <= new_x < size and 0 <= new_y < size and not visited[new_x][new_y] and grid[new_x][new_y]:
                bfs_q.append((new_x, new_y))
                visited[new_x][new_y] = True
    return group_size


def move(s_r, s_c, half, m_dir):
    for row in range(s_r, s_r + half):
        for col in range(s_c, s_c + half):
            n_r = row + dxs[m_dir] * half
            n_c = col + dys[m_dir] * half
            next_grid[n_r][n_c] = grid[row][col]

def rotate(level):
    for i in range(size):
        for j in range(size):
            next_grid[i][j] = 0

    box_size, half = (1 << level), (1 << (level - 1))

    for i in range(0, size, box_size):
        for j in range(0, size, box_size):
            move(i, j, half, 0)
            move(i, j + half, half, 1)
            move(i + half, j, half, 2)
            move(i + half, j + half, half, 3)

    for i in range(size):
        for j in range(size):
            grid[i][j] = next_grid[i][j]


def next_num(curr_x, curr_y):
    cnt = 0
    for dx, dy in zip(dxs, dys):
        new_x, new_y = curr_x + dx, curr_y + dy
        if 0 <= new_x < size and 0 <= new_y < size and grid[new_x][new_y]:
            cnt += 1
    return cnt


for level in levels:
    if level:
        rotate(level)
    for i in range(size):
        for j in range(size):
            next_grid[i][j] = 0

    for i in range(size):
        for j in range(size):
            cnt = next_num(i, j)
            if grid[i][j] and cnt < 3:
                next_grid[i][j] = grid[i][j] - 1
            else:
                next_grid[i][j] = grid[i][j]

    for i in range(size):
        for j in range(size):
            grid[i][j] = next_grid[i][j]

ans = sum([grid[i][j] for i in range(size) for j in range(size)])

max_size = 0
for i in range(size):
    for j in range(size):
        if grid[i][j] and not visited[i][j]:
            visited[i][j] = True
            bfs_q.append((i, j))
            max_size = max(max_size, bfs())
print(ans)
print(max_size)