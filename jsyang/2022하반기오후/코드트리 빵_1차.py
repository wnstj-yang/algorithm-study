# 2023-09-24(일)
# 풀이 시간 : 13:10 ~ 15:10 / 22:00 ~ 22:50
# 첫 제출 : 151ms / 메모리 33MB
# 이게... 뭔가 좀 최적화가 필요해보인다. 아니면 단계를 나누던가 해야할듯

from collections import deque


# 격자 내의 사람들 원하는 편의점으로 1칸 이동 - 최단거리로
def move():
    global finished # 몇명이 이동을 끝냈는지 확인하는 변수

    next_people = [] # 횟수를 진행하면서 남아있는 사람들 추가 (num : 사람 번호, x : 행, y : 열)
    arrived = [] # 사람 번호가 편의점까지 도착했다면 모든 사람들이 움직인 이후에 가지 못하는 것으로 처리해주기 위해 따로 리스트 생성
    for i, j, num in people:
        ax, ay = -1, -1 # 최단 거리로 갈 수 있는 다음 좌표
        min_dist = 987654321 # 최단 거리의 값
        # 4개 방향(우선순위 설정된 상태)으로 최단 거리로의 다음 좌표를 구한다.
        for k in range(4):
            nx = i + dx[k]
            ny = j + dy[k]
            # 못움직이는 칸이나 격자 벗어나면 continue
            if nx < 0 or nx >= N or ny < 0 or ny >= N or board[nx][ny] == -1:
                continue
            # 조건에 맞다면 다음 방향에서 BFS 시작
            q = deque()
            q.append((1, nx, ny)) # 다음 칸부터 BFS를 하기 때문에 한 칸 움직인 상태로 본다.
            visited = [[False] * N for _ in range(N)]
            visited[i][j] = True # 현재 위치
            visited[nx][ny] = True # 다음에 움직일 위치를 방문 처리
            while q:
                cnt, r, c = q.popleft()
                # 편의점 찾음
                if board[r][c] == num:
                    # 편의점까지 도착했다면 거리와 최단거리가 되는 좌표값을 갱신시켜준다
                    if cnt < min_dist:
                        ax = nx
                        ay = ny
                        min_dist = cnt
                    break

                for z in range(4):
                    nr = r + dx[z]
                    nc = c + dy[z]
                    if nr < 0 or nr >= N or nc < 0 or nc >= N:
                        continue

                    # 다음 위치를 방문하지 않고 움직일 수 있는 공간이라면
                    if not visited[nr][nc] and board[nr][nc] != -1:
                        visited[nr][nc] = True
                        q.append((cnt + 1, nr, nc))

        # 편의점 이동 하는데 편의점이 아니라면 1칸 이동, 아니면 도착했으므로 arrived에 추가해준다.
        if board[ax][ay] == num:
            arrived.append((ax, ay))
        else:
            next_people.append((ax, ay, num))

    # 모든 사람들이 이동한 이후 끝이 난 사람들은 해당 위치를 통과하지 못하도록 만든다.
    if arrived:
        for x, y in arrived:
            board[x][y] = -1 # 해당 위치로 움직이지 못한다.
            finished += 1 # 끝난 사람의 수
    return next_people


# 사람 번호가 처음으로 편의점 위치에서부터 최단 거리의 베이스캠프로 이동한다.
def move_first(x, y):
    q = deque()
    q.append((x, y))
    visited = [[False] * N for _ in range(N)]
    visited[x][y] = True
    while q:
        x, y = q.popleft()
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if nx < 0 or nx >= N or ny < 0 or ny >= N or board[nx][ny] == -1:
                continue

            if not visited[nx][ny]:
                # 최단 거리의 베이스캠프까지 왔다면 해당 위치를 움직이지 못하는 값인 -1로 초기화를 진행하고 위치를 반환한다.
                if board[nx][ny] == 1:
                    board[nx][ny] = -1
                    return nx, ny
                # 움직일 수 있다면 옮긴다.(사람이 존재할 수도 있고 빈 공간일 수도 편의점일 수도 있다.)
                else:
                    visited[nx][ny] = True
                    q.append((nx, ny))


# 상좌우하 - 우선순위
dx = [-1, 0, 0, 1]
dy = [0, -1, 1, 0]
N, M = map(int, input().split())
people = [] # 매 time마다 사람들의 수와 정보를 저장하는 리스트
q = deque() # 임시로 저장할 사람들의 정보 큐
board = [list(map(int, input().split())) for _ in range(N)]
finished = 0 # 끝난 사람들의 수
for i in range(2, M + 2):
    x, y = map(int, input().split())
    # 사람 번호, x - 1, y - 1은 현재 사람의 좌표
    q.append([i, x - 1, y - 1])
    # 편의점
    board[x - 1][y - 1] = i

time = 1
while True:
    people = move() # 1. 사람들을 움직인다.
    # 순회를 하면서 사람들의 수가 없고 끝난 사람들의 수가 M이면 끝
    # finished를 따로하는 이유는 첫 사람이 들어가고 움직이려할 때 people만 조건으로 하면 끝이나서 정상작동이 되지 않기 때문
    if len(people) == 0 and finished == M:
        print(time)
        break

    # 새로운 사람들을 넣는다.
    if 1 <= time <= M:
        num, x, y = q.popleft()
        nx, ny = move_first(x, y)
        people.append((nx, ny, num))

    time += 1 # 시간 증가
