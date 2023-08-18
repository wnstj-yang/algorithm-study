# 2023-08-19(금) / 22:00 ~ 00:25
# 풀이 시간 :  약 2시간 30분 
# 첫 제출 : 204ms / 메모리 40MB 
# 추가적인 주석 작성 예정 + 코드 정리 필요


from collections import deque


def search_passenger(cx, cy):
    q = deque()
    visited = [[False] * N for _ in range(N)]
    visited[cx][cy] = True
    q.append((0, C, cx, cy))
    for num in board[cx][cy]:
        # 최단 거리의 승객을 찾았다면 나머지는 목적지로 봐도 무방하다
        if num >= 2:
            return (cx, cy, C)
    next_list = []
    found_dist = 987654321
    found_num = 987654321
    while q:
        dist, C_left, x, y = q.popleft()  # 움직이는 횟수, 배터리 상태, 전기차 좌표x, y
        # 전기차 배터리가 없으면 멈춤 / 돌아다니면서 후보가 될 수 있는 곳의 거리보다 크거나 같다면 후보로 보지 않는다.
        if C_left == 0 or dist >= found_dist:
            continue

        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if nx < 0 or nx >= N or ny < 0 or ny >= N or (len(board[nx][ny]) == 1 and board[nx][ny][0] == 1):
                continue

            if not visited[nx][ny]:
                visited[nx][ny] = True
                if len(board[nx][ny]) > 0:
                    for num in board[nx][ny]:
                        # 최단 거리의 승객을 찾았다면 나머지는 목적지로 봐도 무방하다
                        if num >= 2:
                            next_list.append((dist + 1, nx, ny, C_left - 1))
                            found_dist = dist + 1
                            found_num = num
                            break

                q.append((dist + 1, C_left - 1, nx, ny))

    if len(next_list) == 0:
        return (-1, -1, -1)

    next_list.sort(key=lambda x: (x[0], x[1], x[2]))
    dist, x, y, C_left = next_list[0]
    return (x, y, C_left)


def search_destination(cx, cy, target):
    q = deque()
    visited = [[False] * N for _ in range(N)]
    visited[cx][cy] = True
    q.append((0, C, cx, cy))
    next_list = []
    found_dist = 987654321
    found_target = False
    while q:
        dist, C_left, x, y = q.popleft()
        if C_left == 0:
            continue

        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if nx < 0 or nx >= N or ny < 0 or ny >= N or (len(board[nx][ny]) == 1 and board[nx][ny][0] == 1):
                continue

            if not visited[nx][ny]:
                visited[nx][ny] = True
                if len(board[nx][ny]) > 0:
                    for num in board[nx][ny]:
                        if num == target:
                            found_target = True
                            board[nx][ny].remove(num)
                            return (nx, ny, C_left - 1 + (dist + 1) * 2)

                q.append((dist + 1, C_left - 1, nx, ny))
    return (-1, -1, -1)


N, M, C = map(int, input().split())  # 격자 크키, 승객 수, 배터리 충전량
board = [[[] for _ in range(N)] for _ in range(N)]
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]
for i in range(N):
    state = list(map(int, input().split()))
    for j in range(N):
        if state[j]:
            board[i][j].append(state[j])

cx, cy = map(int, input().split())
cx -= 1
cy -= 1
num = 2
for _ in range(M):
    xs, ys, xe, ye = map(int, input().split())
    xs -= 1
    ys -= 1
    xe -= 1
    ye -= 1
    board[xs][ys].append(num)
    board[xe][ye].append(-num)
    num += 1
result = 0
ans = -1


while M > 0:
    target = -1
    # 찾았는데 0인 경우에는 끝임
    cx, cy, C = search_passenger(cx, cy)
    if cx == -1 and cy == -1:
        break
    # 현재 전기차 위치에는 출발지가 무조건 1명이다. 그래서 1(벽)보다 큰 승객을 찾으면 제거해준다
    for n in board[cx][cy]:
        if n > 1:
            target = -n
            board[cx][cy].remove(n)
            break

    cx, cy, C = search_destination(cx, cy, target)
    if cx == -1 and cy == -1:
        break
    else:
        M -= 1

print(C)