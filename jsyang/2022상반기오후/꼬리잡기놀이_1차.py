# 2023-09-10(일)
# 풀이 시간 : 10:40 ~ 12:50 / 17:55 ~ 18:45 / 19:20 ~ 20:05
# 첫 제출 : ms / 메모리 MB
# 재풀이 예정


from collections import deque


def move_team(team):
    moved_team = []
    # next_board까지해서 다시 해보기

    for number, x, y in team[:1]:
        for k in range(4):
            nx = x + dx[k]
            ny = y + dy[k]
            if nx < 0 or nx >= N or ny < 0 or ny >= N:
                continue

            if board[nx][ny] == 4:
                board[nx][ny] = number
                moved_team.append([number, nx, ny])
                board[x][y] = 4
                break

    for i in range(1, len(team)):
        go_number, go_x, go_y = team[i]
        to_number, to_x, to_y = team[i - 1]
        if i == len(team) - 1:
            moved_team.append([3, to_x, to_y])
            board[to_x][to_y] = 3
        else:
            moved_team.append([2, to_x, to_y])
            board[to_x][to_y] = 2
    board[team[-1][1]][team[-1][2]] = 4
    return moved_team


def throw_ball():
    global result, rx, ry, d, rounds

    isFound = False
    for k in range(N):
        nx = rx + dx[d] * k
        ny = ry + dy[d] * k
        if 0 < board[nx][ny] < 4:
            for i in range(len(teams)):
                team = teams[i]
                for t in range(len(team)):
                    n, x, y = team[t]
                    if x == nx and y == ny:
                        result += ((t + 1) * (t + 1))
                        isFound = True
                        sn, sx, sy = team[0]
                        en, ex, ey = team[-1]
                        teams[i][0][0] = en
                        teams[i][-1][0] = sn
                        teams[i].sort()
                        board[sx][sy], board[ex][ey] = board[ex][ey], board[sx][sy]
                        break

                if isFound:
                    break
        if isFound:
            break

    rx = rx + rdx[d]
    ry = ry + rdy[d]
    rounds += 1
    if rounds % N == 0:
        d = (d + 1) % 4
        if rx == N:
            rx = N - 1
        if ry == N:
            ry = N - 1


N, M, K = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(N)]
# 상하좌우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]
# 하우상좌
rdx = [1, 0, -1, 0]
rdy = [0, 1, 0, -1]
result = 0 # 총합
rounds = 0 # 라운드 수
rx, ry = 0, 0 # 라운드 수에 따른 공이 시작하는 위치
d = 0 # 방향
teams = []
visited = [[False] * N for _ in range(N)]
for i in range(N):
    for j in range(N):
        if not visited[i][j] and board[i][j] == 1:
            visited[i][j] = True
            team = [[i, j]]
            q = deque()
            q.append((i, j))
            tail_x, tail_y = -1, -1
            while q:
                x, y = q.popleft()
                for k in range(4):
                    nx = x + dx[k]
                    ny = y + dy[k]
                    if nx < 0 or nx >= N or ny < 0 or ny >= N:
                        continue

                    if not visited[nx][ny]:
                        if 0 < board[nx][ny] < 3:
                            team.append([nx, ny])
                            q.append((nx, ny))
                        elif board[nx][ny] == 3:
                            tail_x, tail_y = nx, ny
                        visited[nx][ny] = True
            team.append([tail_x, tail_y])

            # team의 첫번째는 방향.
            teams.append(team)

for r in range(K):
    next_teams = []
    for team in teams:
        coors = team

        next_team = move_team(coors)

        next_teams.append(next_team)

    teams = next_teams
    throw_ball()

