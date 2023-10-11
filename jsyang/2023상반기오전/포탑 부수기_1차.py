# 2023-10-11(수)
# 풀이 시간 : 21:10 ~ 23:50
# 첫 제출 : 366ms / 메모리 34MB

from collections import deque

INF = 987654321


# 가장 약한 포탑
def select_attacker():
    global min_attack

    candi = []
    min_attack = INF
    # 1. 격자판 돌면서 가장 약한 값 찾기
    for i in range(N):
        for j in range(M):
            if board[i][j] > 0:
                min_attack = min(min_attack, board[i][j])
    # 2. 개수 찾기
    for i in range(N):
        for j in range(M):
            if board[i][j] == min_attack:
                candi.append((history[i][j], i + j, i, j)) # 공격 상태에 대한 이력, 행 + 열, 행, 열

    # 정렬 시 공격한지 가장 최근의 경우 큰 값이 필요하므로 내림차순 정렬
    if len(candi) > 1:
        candi.sort(key=lambda x:(-x[0], -x[1], -x[3]))

    x, y = candi[0][2], candi[0][3]
    board[x][y] += (N + M)
    attack_status[x][y] = True # 공격 관련 표시;
    return x, y


def select_received():
    global max_attack

    candi = []
    max_attack = 0
    # 1. 가장 높은 포탑 선정
    for i in range(N):
        for j in range(M):
            if ax == i and ay == j:
                continue
            if board[i][j] != 0:
                max_attack = max(max_attack, board[i][j])
    # 2. 후보 찾기
    for i in range(N):
        for j in range(M):
            if ax == i and ay == j:
                continue
            if board[i][j] == max_attack:
                candi.append((history[i][j], i + j, i, j)) # 공격 상태에 대한 이력, 행 + 열, 행, 열

    # 정렬 시 공격한지 가장 오래된 경우 작은 값이 필요하므로 오름차순 정렬
    if len(candi) > 1:
        candi.sort(key=lambda x:(x[0], x[1], x[3]))

    x, y = candi[0][2], candi[0][3]
    attack_status[x][y] = True # 공격 관련 표시;
    return x, y


def attack():
    # 1. 레이저 공격
    q = deque()
    q.append((ax, ay, [])) # 경로파악을 위한 리스트 !
    visited = [[False] * M for _ in range(N)]
    visited[ax][ay] = True
    attack_value = board[ax][ay] # 공격자의 값
    laser = False # 레이저 flag 판단

    while q:
        x, y, path = q.popleft()
        # 공격받는 포탑의 위치까지 온 경우 최단거리
        if x == rx and y == ry:
            laser = True
            # 구해온 경로에 대해서 공격받는 값으로 공격
            for x, y in path:
                if x == rx and y == ry:
                    board[x][y] -= attack_value
                else:
                    board[x][y] -= (attack_value // 2)
                attack_status[x][y] = True # 공격 관련 표시
            break

        for i in range(4):
            # 격자판은 범위를 벗어나도 반대편으로 연결되기 때문에 나머지연산으로 처리
            nx = (x + dx[i]) % N
            ny = (y + dy[i]) % M

            # 부서진 포탑이 아니고 방문처리가 되지 않은 경우 큐와 해당하는 경로를 추가
            if board[nx][ny] != 0 and not visited[nx][ny]:
                visited[nx][ny] = True
                q.append((nx, ny, path + [(nx, ny)]))

    # 2. 포탄 공격
    if not laser:
        board[rx][ry] -= attack_value
        x, y = rx, ry
        # 공격 받는 자의 8방향 처리
        for i in range(8):
            nx = (x + dx2[i]) % N
            ny = (y + dy2[i]) % M
            if nx == ax and ny == ay:
                continue

            if board[nx][ny] != 0:
                board[nx][ny] -= (attack_value // 2)
                attack_status[nx][ny] = True


# 공격처리가 된 이후 0보다 작은 경우 부서진 포함으로 처리
def make_destroyed():
    for i in range(N):
        for j in range(M):
            if board[i][j] < 0:
                board[i][j] = 0


# 공격 관련된 포탑이 아니고 부서지지 않은 경우 공격력 1을 증가해준다
def repair():
    for i in range(N):
        for j in range(M):
            if board[i][j] > 0 and not attack_status[i][j]:
                board[i][j] += 1


# 부서지지 않은 포탑이 1개인지 파악하여 중지할지 판단하는 함수
def check_destroyed():
    cnt = 0
    for i in range(N):
        for j in range(M):
            if board[i][j] != 0:
                cnt += 1
    if cnt == 1:
        return True
    return False


N, M, K = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(N)] # 공격 격자판
history = [[0] * M for _ in range(N)] # 최근 혹은 공격한지 오래된 포탑
attack_status = [[False] * M for _ in range(N)] # 공격 관련 판단 상태
ax, ay = -1, -1
rx, ry = -1, -1
# 우하좌상
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]
# 우하좌상 + 대각선 4방향
dx2 = [0, -1, 0, 1, -1, -1, 1, 1]
dy2 = [1, 0, -1, 0, -1, 1, 1, -1]
min_attack = INF
max_attack = 0
result = 0 # 마지막 결과값
for time in range(1, K + 1):
    attack_status = [[False] * M for _ in range(N)] # 공격 상태 초기화
    ax, ay = select_attacker() # 공격하는 포탑의 좌표 - 공격자 선정
    history[ax][ay] = time # 공격했으므로 현재 시간으로 초기화
    rx, ry = select_received() # 공격 받는 포탑의 좌표 - 공격자의 공격
    attack() # 공격자의 공격 - (레이저, 포탄)
    make_destroyed() # 포탑 부서짐
    repair() # 포탑 정비
    # 포탑 파악
    if check_destroyed():
        break

# 가장 강한 포탑 구하기
for i in board:
    result = max(result, max(i))
print(result)
