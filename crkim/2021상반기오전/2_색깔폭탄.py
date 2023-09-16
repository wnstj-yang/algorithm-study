# new = list(map(list, zip(*arr)))[::-1] #반시계방향 회전 알고리즘 좀 외우기
# 존재하는 해설이 너무 상세해서 접근 방식에 대한 아이디어를 얻으려고 동일한 문제인 '백준 상어중학교' 확인함
# 접근 방법이나 풀이 형식은 이해하나, 구현 자체에 대해 어려움이 있음
# 다시 한 번 풀어보고 이해해봐야 할 것 같음

from collections import deque

RED = 0
ROCK = -1
EMPTY = -2
EMPTY_BUNDLE = (-1, -1, -1, -1)

# 변수 선언 및 입력:
n, m = tuple(map(int, input().split()))
grid = [list(map(int, input().split())) for _ in range(n)]
temp = [[EMPTY for _ in range(n)] for _ in range(n)]
bfs_q = deque()
visited = [[False for _ in range(n)] for _ in range(n)]
ans = 0


def can_go(x, y, color):
    return 0 <= x < n and 0 <= y < n and not visited[x][y] and (
            grid[x][y] == color or grid[x][y] == RED)


def bfs(x, y, color):
    for i in range(n):
        for j in range(n):
            visited[i][j] = False
    visited[x][y] = True
    bfs_q.append((x, y))
    dxs, dys = [0, 1, 0, -1], [1, 0, -1, 0]
    while bfs_q:
        curr_x, curr_y = bfs_q.popleft()

        for dx, dy in zip(dxs, dys):
            new_x, new_y = curr_x + dx, curr_y + dy

            if can_go(new_x, new_y, color):
                bfs_q.append((new_x, new_y))
                visited[new_x][new_y] = True


def get_bundle(x, y):
    bfs(x, y, grid[x][y])
    bomb_cnt, red_cnt = 0, 0
    standard = (-1, -1)

    for i in range(n):
        for j in range(n):
            if not visited[i][j]:
                continue

            bomb_cnt += 1

            if grid[i][j] == RED:
                red_cnt += 1
            elif (i, -j) > standard:
                standard = (i, -j)

    std_x, std_y = standard
    return (bomb_cnt, -red_cnt, std_x, std_y)


def find_best_bundle():
    best_bundle = EMPTY_BUNDLE
    for i in range(n):
        for j in range(n):
            if grid[i][j] >= 1:
                bundle = get_bundle(i, j)
                if bundle > best_bundle:
                    best_bundle = bundle

    return best_bundle


def remove():
    for i in range(n):
        for j in range(n):
            if visited[i][j]:
                grid[i][j] = EMPTY


def gravity():
    for i in range(n):
        for j in range(n):
            temp[i][j] = EMPTY

    for j in range(n):
        last_idx = n - 1
        for i in range(n - 1, -1, -1):
            if grid[i][j] == EMPTY:
                continue
            if grid[i][j] == ROCK:
                last_idx = i
            temp[last_idx][j] = grid[i][j]
            last_idx -= 1

    for i in range(n):
        for j in range(n):
            grid[i][j] = temp[i][j]


def rotate():
    for i in range(n):
        for j in range(n):
            temp[i][j] = EMPTY
    for j in range(n - 1, -1, -1):
        for i in range(n):
            temp[n - 1 - j][i] = grid[i][j]
    for i in range(n):
        for j in range(n):
            grid[i][j] = temp[i][j]


def clean(x, y):
    bfs(x, y, grid[x][y])
    remove()
    gravity()


def simulate():
    global ans
    best_bundle = find_best_bundle()
    bomb_cnt, _, x, y = best_bundle

    if best_bundle == EMPTY_BUNDLE or bomb_cnt <= 1:
        return False
    ans += bomb_cnt * bomb_cnt
    clean(x, -y)
    rotate()
    gravity()
    return True


while True:
    keep_going = simulate()
    if not keep_going:
        break

print(ans)