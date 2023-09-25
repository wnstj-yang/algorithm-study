# 2023-09-25(월)
# 풀이 시간: 21:10 ~ 21:55
# 470ms / 42MB


def move_atomics():
    next_board = [[[] for _ in range(N)] for _ in range(N)]
    for x in range(N):
        for y in range(N):
            if board[x][y]:
                for m, s, d in board[x][y]:
                    nx = (x + dx[d] * s) % N
                    ny = (y + dy[d] * s) % N
                    next_board[nx][ny].append((m, s, d))
    return next_board


def divide():
    for x in range(N):
        for y in range(N):
            if len(board[x][y]) >= 2:
                total_mass = 0
                total_speed = 0
                is_odd = False
                is_even = False
                for m, s, d in board[x][y]:
                    total_mass += m
                    total_speed += s
                    # 0을 포함한 짝수인 경우 상하좌우, 그 외의 경우(나머지 연산해서 1) 홀수면 대각선
                    if d % 2 == 0:
                      is_even = True
                    else:
                        is_odd = True
                total_mass = total_mass // 5
                total_speed = total_speed // len(board[x][y])
                board[x][y] = [] # 해당 값 초기화
                if total_mass == 0:
                    continue
                # 홀수(대각선), 짝수(상하좌우)가 모두 있으면 대각선 4방향
                if is_odd and is_even:
                    for i in [1, 3, 5, 7]:
                        board[x][y].append((total_mass, total_speed, i))
                else:
                    for i in [0, 2, 4, 6]:
                        board[x][y].append((total_mass, total_speed, i))


dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, 1, 1, 1, 0, -1, -1, -1]
N, M, K = map(int, input().split()) # N : 격자판 크기, M : 원자의 수, K : 실험 시간
board = [[[] for _ in range(N)] for _ in range(N)]

for _ in range(M):
    x, y, m, s, d = map(int, input().split()) # 1 <= x, y <= N 좌표, m : 질량, s: 속력, d: 방향
    board[x - 1][y - 1].append((m, s, d))

for _ in range(K):
    board = move_atomics()
    divide()

total = 0
for i in range(N):
    for j in range(N):
        if board[i][j]:
            for m, s, d in board[i][j]:
                total += m
print(total)
