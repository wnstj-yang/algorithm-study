# 2023-10-12(목)
# 풀이 시간 : 21:18 ~ 23:31
# 첫 제출 : 226ms / 메모리 26MB


def move_players():
    global total

    moved = [[[] for _ in range(N)] for _ in range(N)]
    for r in range(N):
        for c in range(N):
            if len(players[r][c]) > 0:
                dist = abs(r - ex) + abs(c - ey) # 최단거리
                for p in players[r][c]:
                    isMoved = False
                    for k in range(4):
                        nr = r + dx[k]
                        nc = c + dy[k]
                        if nr < 0 or nr >= N or nc < 0 or nc >= N:
                            continue

                        check_dist = abs(nr - ex) + abs(nc - ey)
                        if check_dist == 0: # 도착함
                            total += 1 # 이동 거리 증가
                            isMoved = True # 탈출한 것이므로 움직였다는 표시
                            break

                        # 참가자가 움직일 수 있고 상하좌우 우선순위에 따라서 움직였을 때의 최단거리가 더 작다면 이동한다
                        if board[nr][nc] == 0 and check_dist < dist:
                            moved[nr][nc].append(p + 1) # 이동
                            total += 1 # 이동 거리 증가
                            isMoved = True
                            break

                    if not isMoved:
                        moved[r][c].append(p)
    return moved


# 최소 정사각형을 행, 열이 작은 순서로 진행하기 때문에 크기와 조건에 맞게 구했다면 빠져나간다.
def get_square():
    for l in range(2, N + 1):
        for x in range(N - l + 1):
            for y in range(N - l + 1):
                isExit = False
                isPlayer = False
                for i in range(x, x + l):
                    for j in range(y, y + l):
                        if len(players[i][j]) > 0:
                            isPlayer = True
                        if i == ex and j == ey:
                            isExit = True
                        if isPlayer and isExit:
                            return x, y, l

    return 0, 0, 0 # 없으면 0, 0, 0


def rotate():
    global ex, ey
    sx, sy, length = get_square()
    if sx == 0 and sy == 0 and length == 0:
        return
    temp1 = [[0] * length for _ in range(length)] # 격자판 회전
    temp2 = [[[] for _ in range(length)] for _ in range(length)] # 참가자 회전
    rotated1 = [[0] * length for _ in range(length)] # 격자판 회전
    rotated2 = [[[] for _ in range(length)] for _ in range(length)] # 참가자 회전

    # 1. 각각 받은 중간의 정사각형 좌표와 크기를 0,0부터 시작해서 값을 넣는다.
    for i in range(sx, sx + length):
        for j in range(sy, sy + length):
            temp1[i - sx][j - sy] = board[i][j]
            temp2[i - sx][j - sy] = players[i][j]

    # 2. 만들어진 temp리스트들에다가 90도 시계방향 회전 진행
    for i in range(length):
        for j in range(length):
            rotated1[j][length - 1 - i] = temp1[i][j]
            rotated2[j][length - 1 - i] = temp2[i][j]

    # 3. 회전된 것을 격자판, 참가들의 배열에 초기화시킨다.
    for i in range(sx, sx + length):
        for j in range(sy, sy + length):
            board[i][j] = rotated1[i - sx][j - sy]
            players[i][j] = rotated2[i - sx][j - sy]
            # 10은 탈출구를 뜻하며 내구도를 깎지 않고 좌표를 갱신시켜준다.
            if board[i][j] == 10:
                ex, ey = i, j
                continue
            board[i][j] -= 1
            if board[i][j] < 0:
                board[i][j] = 0


N, M, K = map(int, input().split())
ex, ey = -1, -1
# 상하좌우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]
board = [list(map(int, input().split())) for _ in range(N)]
players = [[[] for _ in range(N)] for _ in range(N)]
total = 0
for i in range(1, M + 1):
    x, y = map(int, input().split())
    # 번호와 이동거리
    players[x - 1][y - 1].append(0)
ex, ey = map(int, input().split())
ex -= 1
ey -= 1
board[ex][ey] = 10 # 탈출구

for _ in range(K):
    players = move_players()
    rotate()

print(total)
print(ex + 1, ey + 1)
