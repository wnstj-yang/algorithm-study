# 2023-09-15(금)
# 풀이 시간 : 20:50 ~ 23:55
# 첫 제출 ms / MB
# 기본기가 부족한느낌...? 조건 1번을 어떻게해야될지 고민하는 과정에서 시간 80프로쓴듯
# 문제 왜이렇게 못읽지... 행이 가장크고 열도 가장 큰것으로 봤다...
# 문제 좀 덜 풀린다 싶으면 처음부터 다시 읽기 + 점검 필요


from collections import deque


def search_bombs(x, y):
    q = deque()
    q.append((x, y))
    visited[x][y] = True
    color = board[x][y]
    cnt = 1
    red_cnt = 0
    coors = [(x, y)]
    red_coors = []
    while q:
        x, y = q.popleft()
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if nx < 0 or nx >= N or ny < 0 or ny >= N:
                continue
            if not visited[nx][ny] and (board[nx][ny] == color or board[nx][ny] == 0):
                q.append((nx, ny))
                # coors.append((nx, ny))
                cnt += 1
                if board[nx][ny] == 0:
                    red_cnt += 1
                    red_coors.append((nx, ny))
                else:
                    visited[nx][ny] = True
                    coors.append((nx, ny))
    # 2개 이상이고 모두 빨간색이면 안된다.
    if len(coors) >= 2 and cnt - red_cnt != 0:
        coors.sort(key=lambda x:(-x[0], x[1]))
        coors.extend(red_coors)
        if (cnt, red_cnt) not in bomb_list:
            bomb_list[(cnt, red_cnt)] = [coors]
        else:
            bomb_list[(cnt, red_cnt)].append(coors)


def explode(coor_list):
    cnt = 0
    for x, y in coor_list:
        board[x][y] = -2
        cnt += 1
    return cnt * cnt



def gravity():
    # 열 순서대로 행의 밑에서부터 올라온다.
    for j in range(N):
        cnt = 0
        for i in range(N - 1, -1, -1):
            if board[i][j] == -2:
                cnt += 1
            elif board[i][j] == -1:
                cnt = 0
            else:
                if cnt > 0:
                    board[i + cnt][j] = board[i][j]
                    board[i][j] = -2



# 반시계 방향 90도
def rotate():
    temp = [item[:] for item in board]
    for i in range(N):
        for j in range(N):
            temp[N - 1 - j][i] = board[i][j]


# 상하좌우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]
N, M = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(N)]
total = 0
bomb_list = {}
while True:
    isBomb = False
    visited = [[False] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if not visited[i][j] and board[i][j] > 0:
                search_bombs(i, j)
                isBomb = True
    if not isBomb:
        break
    # 조건에 따라 크기가 크고, 빨간색 개수가 적은 순으로 정렬을 진행한다.
    # 이전에 폭탄묶음 안의 폭탄의 좌표들을 모두 행, 열 순으로 가장 큰 수로 정렬한 상태이다
    sorted_bomb_list = sorted(bomb_list.items(), reverse=True)
    if len(sorted_bomb_list) > 0:
        key = sorted_bomb_list[0][0]
        standards = sorted_bomb_list[0][1]
        print(key)
        print(standards)
        if len(standards) == 1:
            explode(standards[0])
        else:
            for standard in standards:
                standard.sort()


        # for coors in values:
        #     for x, y in coors:
        #         if board[x][y] > 0:
        #             coors.remove((x, y))
        #             coors.insert(0, (x, y))
        #             # coors.sort(key=lambda x: (-x[0], -x[1]))
        #             if x not in standards:
        #                 standards[x] = [coors]
        #             else:
        #                 standards[x].append(coors)
        #             break
        # # standards = sorted(standards.items(), reverse=True)
        # key, values = standards[0][0], standards[0][1]
        # if len(values) > 0:

    break



print(total)

