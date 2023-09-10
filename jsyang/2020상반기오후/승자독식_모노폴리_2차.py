# 2023-09-08(금) / 2023-09-09(토)
# 풀이 시간: 22:00 ~ 22:45 / 16:20 ~ 17:35
# 기존 풀이보다 조금 더 시간복잡도는 줄이고 표현이 간결해짐


def move_players():
    next_board = [item[:] for item in board] # 격자판 갱신하기 위한 것
    before_move = {} # 움직이기 이전의 players정보
    next_players = {} # 다음 플레이어들의 정보
    for key, value in players.items():
        isMoved = False # 인접 4방향에 대해서 움직였는지 아닌지 파악
        x, y = key # 좌표
        number, d = value # player의 번호 및 방향
        # 우선순위에 따른 방향
        for nd in player_direction_orders[number][d]:
            nx = x + dx[nd]
            ny = y + dy[nd]
            # 격자판을 벗어나면 안된다.
            if nx < 0 or nx >= N or ny < 0 or ny >= N:
                continue
            # 비어있는 곳이라면 움직일 수 있다.
            if len(board[nx][ny]) == 0:
                isMoved = True
                # 움직일 수 있는 좌표에 다른 플레이어들도 있다면 추가 아니면 본인 추가
                if (nx, ny) not in before_move:
                    before_move[(nx, ny)] = [(number, nd)]
                else:
                    before_move[(nx, ny)].append((number, nd))
                break
        # 움직일 수 없다면 인접4방향 중 자신의 우선순위 방향에 따라 점유한 곳으로 이동
        if not isMoved:
            for nd in player_direction_orders[number][d]:
                nx = x + dx[nd]
                ny = y + dy[nd]
                if nx < 0 or nx >= N or ny < 0 or ny >= N:
                    continue
                # 점유중이고 해당 점유 공간이 자신이 한 곳일 때 추가
                if len(board[nx][ny]) > 0 and board[nx][ny][0] == number:
                    before_move[(nx, ny)] = [(number, nd)]
                    break

    # 움직이기 전에 같은 공간에 여러 명이 있는 경우를 처리한다.
    for key, value in before_move.items():
        x, y = key
        # 여러 명이라면 정렬 진행
        if len(value) > 1:
            value.sort()
        # 가장 작은 번호이므로 첫 번째 플레이어를 추가한다.
        number, d = value[0][0], value[0][1]
        next_players[(x, y)] = [number, d]
        next_board[x][y] = [number, d, K]
    # 갱신된 players과 격자판을 반환
    return next_players, next_board


def remove_occupy():
    for x in range(N):
        for y in range(N):
            # 현재 자신의 위치가 아니고 점유된 곳이라면 턴 수를 뺀다.
            if board[x][y] and (x, y) not in players:
                board[x][y][2] -= 1
                # 0이라면 비워준다
                if board[x][y][2] == 0:
                    board[x][y] = []


N, M, K = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(N)]
players = {}
player_direction_orders = {}
# 상하좌우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

first_directions = list(map(int, input().split()))
# 방향이 1 ~ 4로 주어지기 때문에 이를 1씩 빼주어 인덱스 설정 진행
for k in range(len(first_directions)):
    first_directions[k] -= 1

for i in range(1, M + 1):
    player_direction_orders[i] = {}
    for j in range(4):
        direcs = list(map(int, input().split()))
        # 방향이 1 ~ 4로 주어지기 때문에 이를 1씩 빼주어 인덱스 설정 진행
        for k in range(4):
            direcs[k] -= 1
        player_direction_orders[i][j] = direcs

for i in range(N):
    for j in range(N):
        if board[i][j]:
            d = first_directions[board[i][j] - 1]
            players[(i, j)] = [board[i][j], d]
            board[i][j] = [board[i][j], d, K]
        else:
            board[i][j] = []

cnt = 1 # 첫 번째로 점유했기 때문에 초기화를 1로 진행
while cnt <= 1000:
    players, board = move_players()
    remove_occupy()
    # players의 길이가 1이고 
    if len(players) == 1:
        key = list(players.keys())
        x, y = key[0][0], key[0][1]
        # 번호가 1인 플레이어만 남는다면 끝
        if players[(x, y)][0] == 1:
            break
    cnt += 1
if cnt == 1001:
    print(-1)
else:
    print(cnt)
