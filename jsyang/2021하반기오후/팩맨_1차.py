# 2023-10-13(금) / 2023-10-14(토)
# 21:20 ~ 25:35 / 추가 풀이...(참고함)
# ms / MB


# 2. 몬스터 이동 - 알은 그대로, 몬스터만 이동
def move_monsters():
    next_board = [[[] for _ in range(4)] for _ in range(4)]
    for x in range(4):
        for y in range(4):
            is_moved = False
            for d in board[x][y]:
                for k in range(8):
                    nd = (d + k) % 8
                    nx = x + dx[nd]
                    ny = y + dy[nd]
                    if nx < 0 or nx >= 4 or ny < 0 or ny >= 4:
                        continue
                    if nx == r and ny == c:
                        continue
                    if dead[nx][ny] > 0:
                        continue

                    next_board[nx][ny].append(nd)
                    is_moved = True
                    break

                if not is_moved:
                    next_board[x][y].append(d)
    return next_board


# 3. 팩맨 이동
def move_packman():
    global r, c, dead_list

    max_cnt = -1
    path = []
    for i in range(len(orders)):
        x, y = r, c
        cnt = 0
        visited = []
        out = False
        for k in range(len(orders[i])):
            d = orders[i][k]
            nx = x + px[d]
            ny = y + py[d]
            if nx < 0 or nx >= 4 or ny < 0 or ny >= 4:
                out = True
                break

            if [nx, ny] not in visited:
                cnt += len(board[nx][ny])
            visited.append([nx, ny])
            x, y = nx, ny

        if not out and cnt > max_cnt:
            max_cnt = cnt
            path = visited

    r, c = path[-1]
    clean_dead()

    for nx, ny in path:
        if board[nx][ny]:
            dead[nx][ny] = 2
            board[nx][ny] = []


# 4. 시체 소멸 및 추가
def clean_dead():
    for i in range(4):
        for j in range(4):
            if dead[i][j] > 0:
                dead[i][j] -= 1


# 5. 몬스터 복제 완성
def born_eggs():
    for i in range(4):
        for j in range(4):
            board[i][j].extend(eggs[i][j])


def get_packman_orders(k):
    if k == 3:
        orders.append(list(candi))
        return

    for i in range(4):
        candi[k] = i
        get_packman_orders(k + 1)


orders = []
candi = [0] * 3
get_packman_orders(0)
board = [[[] for _ in range(4)] for _ in range(4)]
eggs = [[[] for _ in range(4)] for _ in range(4)]
dead = [[0] * 4 for _ in range(4)]
dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, -1, -1, -1, 0, 1, 1, 1]
# 상좌하우
px = [-1, 0, 1, 0]
py = [0, -1, 0, 1]

M, T = map(int, input().split())
r, c = map(int, input().split())
r -= 1
c -= 1
dead_list = []
for _ in range(M):
    x, y, d = map(int, input().split())
    board[x - 1][y - 1].append(d - 1)


for t in range(T):
    # 1. 몬스터 복제 시도
    eggs = [[item[:] for item in board[i]] for i in range(4)]
    board = move_monsters()
    move_packman()
    born_eggs()

total = 0
for i in range(4):
    for j in range(4):
        total += len(board[i][j])
print(total)
