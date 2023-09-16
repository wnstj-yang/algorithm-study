# -------------------
#해설 확인 -> 어려워서 설명 들었음
n, m, k = tuple(map(int, input().split()))
board = [[0] * (n + 1)]
for _ in range(n):
    board.append([0] + list(map(int, input().split())))
v = [[] for _ in range(m + 1)]
tail = [0] * (m + 1)
visited = [[False] * (n + 1) for _ in range(n + 1)]
board_idx = [[0] * (n + 1) for _ in range(n + 1)]  # 각 팀 번호 적을 용도
ans = 0
dxs = [-1,  0, 1, 0]
dys = [ 0, -1, 0, 1]

# 초기 레일을 만들기 위해 dfs를 이용합니다.
def dfs(x, y, idx):
    visited[x][y] = True
    board_idx[x][y] = idx
    for dx, dy in zip(dxs, dys):
        nx, ny = x + dx, y + dy
        if not (1 <= nx <= n and 1 <= ny <= n):
            continue

        if board[nx][ny] == 0: #벽임
            continue
        if visited[nx][ny]: #이미 방문함
            continue

        if len(v[idx]) == 1 and board[nx][ny] != 2: #2가 있는 쪽으로 찾음
            continue

        v[idx].append((nx, ny))
        if board[nx][ny] == 3:
            tail[idx] = len(v[idx])
        dfs(nx, ny, idx)

def init():
    cnt = 1
    # 머리부터 레일저장
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if board[i][j] == 1:
                v[cnt].append((i, j))
                cnt += 1

    for i in range(1, m + 1):
        x, y = v[i][0]
        dfs(x, y, i) #완탐


def move_all():
    for i in range(1, m + 1):
        tmp = v[i][-1] #레일을 한 칸 이동해줌
        for j in range(len(v[i]) - 1, 0, -1):
            v[i][j] = v[i][j - 1]
        v[i][0] = tmp

    #board 갱신
    for i in range(1, m + 1):
        for j, (x, y) in enumerate(v[i]):
            if j == 0:
                board[x][y] = 1
            elif j < tail[i] - 1:
                board[x][y] = 2
            elif j == tail[i] - 1:
                board[x][y] = 3
            else:
                board[x][y] = 4


def get_point(x, y):
    global ans
    idx = board_idx[x][y]
    cnt = v[idx].index((x, y))
    ans += (cnt + 1) * (cnt + 1)


# 공 던짐 -> 받을 팀 번호 리턴
def throw_ball(turn):
    t = (turn - 1) % (4 * n) + 1

    if t <= n:
        for i in range(1, n + 1):
            if 1 <= board[t][i] and board[t][i] <= 3:
                get_point(t, i)
                return board_idx[t][i]
    elif t <= 2 * n:
        t -= n
        for i in range(1, n + 1):
            if 1 <= board[n + 1 - i][t] and board[n + 1 - i][t] <= 3:
                get_point(n + 1 - i, t)
                return board_idx[n + 1 - i][t]
    elif t <= 3 * n:
        t -= (2 * n)
        for i in range(1, n + 1):
            if 1 <= board[n + 1 - t][n + 1 - i] and board[n + 1 - t][n + 1 - i] <= 3:
                get_point(n + 1 - t, n + 1 - i)
                return board_idx[n + 1 - t][n + 1 - i]
    else:
        t -= (3 * n)
        for i in range(1, n + 1):
            if 1 <= board[i][n + 1 - t] and board[i][n + 1 - t] <= 3:
                get_point(i, n + 1 - t)
                return board_idx[i][n + 1 - t]

    return 0 #공 맞는 사람 없음


# 머리 순서 바꾸기 (공 맞았음)
def reverse(got_ball_idx):
    # 공 안맞음
    if got_ball_idx == 0:
        return

    idx = got_ball_idx
    new_v = []
    # 세로운 레일
    for j in range(tail[idx] - 1, -1, -1):
        new_v.append(v[idx][j])

    for j in range(len(v[idx]) - 1, tail[idx] - 1, -1):
        new_v.append(v[idx][j])

    v[idx] = new_v[:]

    # board갱신
    for j, (x, y) in enumerate(v[idx]):
        if j == 0:
            board[x][y] = 1
        elif j < tail[idx] - 1:
            board[x][y] = 2
        elif j == tail[idx] - 1:
            board[x][y] = 3
        else:
            board[x][y] = 4


init()
for i in range(1, k + 1):
    move_all()
    got_ball_idx = throw_ball(i)
    reverse(got_ball_idx)

print(ans)