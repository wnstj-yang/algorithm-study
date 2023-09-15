# 2023-09-15(금)
# 풀이 시간 : 20:50 ~ 23:55 / 24:10 ~ 25:00
# 첫 제출 ms / MB

# 기본기가 부족한느낌...? 조건 1번을 어떻게해야될지 고민하는 과정에서 시간 80프로쓴듯
# 문제 왜이렇게 못읽지... 행이 가장크고 열도 가장 큰것으로 봤다...
# 문제 좀 덜 풀린다 싶으면 처음부터 다시 읽기 + 점검 필요
# 돌고 돌아 결국엔 문제 이해...

from collections import deque


def search_bombs(x, y):
    q = deque()
    q.append((x, y))
    visited[x][y] = True
    color = board[x][y] # 같은 색상 파악 위함 
    cnt = 1 # 현재 위치에 대해서 갯수 증가
    red_cnt = 0 # 따로 빨간색 폭탄 개수 처리
    coors = [(x, y)] # 하나의 폭발 묶음의 좌표들
    red_coors = [] # 방문처리를 위한 빨간색 폭탄의 좌표
    while q:
        x, y = q.popleft()
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if nx < 0 or nx >= N or ny < 0 or ny >= N:
                continue
            
            # 방문하지 않고 같은 색 혹은 빨간색 폭탄이라면
            if not visited[nx][ny] and (board[nx][ny] == color or board[nx][ny] == 0):
                q.append((nx, ny)) # 큐에 추가
                visited[nx][ny] = True
                cnt += 1
                # 빨간색 폭탄인지, 같은 색인지에 따라 개수, 좌표값 처리
                if board[nx][ny] == 0:
                    red_cnt += 1
                    red_coors.append((nx, ny))
                else:
                    coors.append((nx, ny))
    # 방문했던 빨간색 폭탄은 다시 방문하지 않은 것으로 처리해야한다.
    # 그렇지 않은 로직이 있다면 무한 루프 발생 -> 메모리 초과
    for x, y in red_coors:
        visited[x][y] = False
        
    length = len(coors) + len(red_coors) # 빨간색, 같은색 폭탄들의 개수
    # 2개 이상이고 모두 빨간색이면 안된다.
    if length >= 2 and cnt - red_cnt != 0:
        # 행은 가장 커야하고 열은 가장 작아야한다.
        # coors에는 빨간 폭탄이 없기에 기준점이 된다.
        coors.sort(key=lambda x:(-x[0], x[1]))
        x, y = coors[0][0], coors[0][1]
        coors.extend(red_coors) # 빨간색 폭탄 좌표 추가
        # [전체 개수, 빨간 폭탄 개수, x, y좌표, 모든 좌표]
        bomb_list.append([cnt, red_cnt, x, y, coors])


# 폭발시키면서 빈 공간 표시인 -2로 초기화 진행 및 점수 반환
def explode(coor_list):
    cnt = len(coor_list)
    for x, y in coor_list:
        board[x][y] = -2
    return cnt * cnt


def gravity():
    # 열 순서대로 행의 밑에서부터 올라온다.
    for j in range(N):
        cnt = 0
        for i in range(N - 1, -1, -1):
            # 빈 공간이라면 옮길 수 있기에 자리 수 증가
            if board[i][j] == -2:
                cnt += 1
            # -1이라면 더이상 가지 못하므로 0으로 초기화
            elif board[i][j] == -1:
                cnt = 0
            # 그 외에 색깔이 존재한다면 옮긴다.
            else:
                # 움직일 수 있는 경우에만 옮긴다.
                if cnt > 0:
                    board[i + cnt][j] = board[i][j]
                    board[i][j] = -2


# 반시계 방향 90도
def rotate():
    temp = [item[:] for item in board]
    for i in range(N):
        for j in range(N):
            temp[N - 1 - j][i] = board[i][j]
    return temp


# 상하좌우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]
N, M = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(N)]
total = 0
bomb_list = [] # 폭탄묶음의 리스트
while True:
    bomb_list = []
    visited = [[False] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if not visited[i][j] and board[i][j] > 0:
                search_bombs(i, j)
    # 폭탄 묶음이 없으면 끝
    if len(bomb_list) == 0:
        break
    
    # 폭탄 묶음의 총 개수는 크고, 빨간 폭탄 수는 적어야 한다.
    # 이어서 기준점인 행은 가장 크고 열은 가장 작아야한다.
    bomb_list.sort(key=lambda x:(-x[0], x[1], -x[2], x[3]))
    total += explode(bomb_list[0][4]) # 기준점의 좌표들
    gravity() # 중력작용
    board = rotate() # 90도 반시계 회전
    gravity() # 중력작용

print(total)
