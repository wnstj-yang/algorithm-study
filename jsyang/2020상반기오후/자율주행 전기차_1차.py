# 2023-08-19(금) / 22:00 ~ 00:25
# 풀이 시간 :  약 2시간 30분 
# 첫 제출 : 204ms / 메모리 40MB 


from collections import deque


# BFS 적용
def search_passenger(cx, cy):
    q = deque()
    visited = [[False] * N for _ in range(N)]
    visited[cx][cy] = True
    q.append((0, C, cx, cy)) # 거리, 배터리 양, 전기차 x, y좌표
    # 전기차의 위치에 승객이 존재하는 경우 
    for num in board[cx][cy]:
        # 최단 거리의 승객을 찾았다면 나머지는 목적지로 봐도 무방하다
        if num >= 2:
            return cx, cy, C
        
    next_list = [] # 최단 거리에 있는 승객들의 정보
    found_dist = 987654321 # 최단 거리인 승객을 찾았을 때 그 이상으로 탐색 안하기 위해 거리 저장

    while q:
        dist, C_left, x, y = q.popleft()  # 움직이는 횟수, 배터리 상태, 전기차 좌표x, y
        # 전기차 배터리가 없으면 멈춤 / 돌아다니면서 후보가 될 수 있는 곳의 거리보다 크거나 같다면 후보로 보지 않는다.
        if C_left == 0 or dist >= found_dist:
            continue

        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            # 격자를 벗어나거나 벽인 경우 넘어간다
            if nx < 0 or nx >= N or ny < 0 or ny >= N or (len(board[nx][ny]) == 1 and board[nx][ny][0] == 1):
                continue

            # 전기차가 방문하지 않은 곳이라면
            if not visited[nx][ny]:
                visited[nx][ny] = True # 방문 체크
                # 출발지나 도착지가 최소 1개 이상인 경우
                if len(board[nx][ny]) > 0:
                    for num in board[nx][ny]:
                        # 최단 거리의 승객을 찾았다면 나머지는 목적지로 봐도 무방하다
                        if num >= 2:
                            # 현재 거리 + 1(다음), 다음 이동 좌표, 배터리 양 1 감소
                            next_list.append((dist + 1, nx, ny, C_left - 1))
                            found_dist = dist + 1
                            break

                q.append((dist + 1, C_left - 1, nx, ny))
    
    # 다음으로 갈 곳이 없다면 끝 - 배터리 0
    if len(next_list) == 0:
        return -1, -1, -1

    # 거리, 상단, 열은 왼쪽 순으로 정렬
    next_list.sort(key=lambda x: (x[0], x[1], x[2]))
    dist, x, y, C_left = next_list[0]

    return x, y, C_left


def search_destination(cx, cy, target):
    q = deque()
    visited = [[False] * N for _ in range(N)]
    visited[cx][cy] = True
    q.append((0, C, cx, cy))
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
                        # 승객의 도착지점을 찾았다면 충전량을 이동 거리의 2배하고 더한 값을 반환
                        if num == target:
                            board[nx][ny].remove(num)
                            return nx, ny, C_left - 1 + (dist + 1) * 2

                q.append((dist + 1, C_left - 1, nx, ny))
    return -1, -1, -1


N, M, C = map(int, input().split())  # 격자 크키, 승객 수, 배터리 충전량
board = [[[] for _ in range(N)] for _ in range(N)] # N x N의 격자판 내 출발지와 도착지가 여러 개 존재할 수 있다.
# 상하좌우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]
# 입력받은 것을 추가해준다
for i in range(N):
    state = list(map(int, input().split()))
    for j in range(N):
        if state[j]:
            board[i][j].append(state[j])

cx, cy = map(int, input().split()) # 전기차 위치
# 인덱스에 맞게 1씩 줄인다
cx -= 1
cy -= 1
num = 2 # 승객의 번호를 2번으로 해놓고 M의 수만큼 증가하면서 추가
for _ in range(M):
    # 승객 출발 x, y좌표 / 승객 도착 x, y 좌표 + 인덱스에 맞게 1씩 줄임
    xs, ys, xe, ye = map(int, input().split())
    xs -= 1
    ys -= 1
    xe -= 1
    ye -= 1
    board[xs][ys].append(num) # 출발 지점 추가
    board[xe][ye].append(-num) # 도착 지점을 음수로 표현
    num += 1


# 승객들을 모두 찾을때 까지 진행한다
while M > 0:
    target = -1
    # 최단 거리로 승객을 찾아 나선다
    cx, cy, C = search_passenger(cx, cy)
    # 배터리가 없어서 멈춘 경우 끝
    if cx == -1 and cy == -1:
        break
    # 현재 전기차 위치에는 출발지가 무조건 1명이다. 그래서 1(벽)보다 큰 승객을 찾으면 제거해준다
    for n in board[cx][cy]:
        if n > 1:
            target = -n # 승객을 도착지점으로 보낼 곳을 저장
            board[cx][cy].remove(n) # 승객을 태웠으니 격자에서 제거
            break

    cx, cy, C = search_destination(cx, cy, target)
    # 도착 지점을 찾지 못하면 C도 -1로 반환 받기 때문에 끝 아니라면 승객 수 1 줄임
    if cx == -1 and cy == -1:
        break
    else:
        M -= 1

print(C)
