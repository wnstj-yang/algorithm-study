# 2023-10-03(화)
# 17:40 ~ 17:50 / 18:20 ~ 19:48
# 128ms / 33MB


from collections import deque


# 주사위를 펼쳤을 때 6개의 자리에서 방향에따라 자리 변환
def roll_dice():
    if d == 0:
        dice[0], dice[3], dice[4], dice[1] = dice[1], dice[0], dice[3], dice[4]
    elif d == 1:
        dice[0], dice[2], dice[4], dice[5] = dice[2], dice[4], dice[5], dice[0]
    elif d == 2:
        dice[0], dice[3], dice[4], dice[1] = dice[3], dice[4], dice[1], dice[0]
    else:
        dice[0], dice[2], dice[4], dice[5] = dice[5], dice[0], dice[2], dice[4]


def calculate():
    q = deque()
    q.append((cx, cy))
    visited = [[False] * N for _ in range(N)]
    number = board[cx][cy]
    visited[cx][cy] = True
    cnt = 1
    while q:
        x, y = q.popleft()
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if nx < 0 or nx >= N or ny < 0 or ny >= N:
                continue

            if not visited[nx][ny] and board[nx][ny] == number:
                cnt += 1
                q.append((nx, ny))
                visited[nx][ny] = True

    return cnt * number


def check_direction():
    global d, cx, cy, total

    nx = cx + dx[d]
    ny = cy + dy[d]
    # 주사위의 좌표를 움직이기 전에 격자를 벗어났으면 반대 방향으로 전환
    if nx < 0 or nx >= N or ny < 0 or ny >= N:
        d = (d + 2) % 4
        nx = cx + dx[d]
        ny = cy + dy[d]
    roll_dice() # 주사위를 굴리고
    cx, cy = nx, ny # 주사위의 위치 좌표값 갱신
    total += calculate() # 점수 계산

    # 주사위의 아랫면 > 해당 칸에 있는 숫자 - 시계 90도 회전
    if dice[4] > board[cx][cy]:
        d = (d + 1) % 4
    # 주사위의 아랫면 < 해당 칸에 있는 숫자 - 반시계 90도 회전
    elif dice[4] < board[cx][cy]:
        d = (d - 1) % 4


dice = [1, 4, 5, 3, 6, 2] # 주사위 펼쳤을 때
# 우하좌상
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]
d = 0 # 방향
N, M = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(N)]
cx, cy = 0, 0 # dice의 위치
total = 0
for _ in range(M):
    check_direction()
print(total)
