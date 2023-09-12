# 2023-09-12(화)
# 풀이 시간 : 21:25 ~ 23:25/ 23:40 ~ 풀이 중
# 첫 제출 : ms / 메모리 MB


from collections import deque


def grow_trees():
    for x in range(N):
        for y in range(N):
            # 제초제가 없고 나무가 존재할 때
            if poisons[x][y] == 0 and board[x][y] > 0:
                cnt = 0
                for k in range(4):
                    nx = x + dx[k]
                    ny = y + dy[k]
                    if nx < 0 or nx >= N or ny < 0 or ny >= N:
                        continue
                    if poisons[nx][ny] == 0 and board[nx][ny] > 0:
                        cnt += 1
                board[x][y] += cnt


def spread_trees():
    spread_list = []
    for x in range(N):
        for y in range(N):
            # 제초제가 없고 나무가 존재할 때
            if poisons[x][y] == 0 and board[x][y] > 0:
                cnt = 0
                coors = []
                for k in range(4):
                    nx = x + dx[k]
                    ny = y + dy[k]
                    if nx < 0 or nx >= N or ny < 0 or ny >= N:
                        continue
                    # 제초제가 없고 나무가 없는 빈 공간일 때
                    if poisons[nx][ny] == 0 and board[nx][ny] == 0:
                        cnt += 1
                        coors.append((nx, ny))
                if cnt > 0:
                    result = board[x][y] // cnt
                    spread_list.append([result, coors])
    print(spread_list)
    for value, coors in spread_list:
        for x, y in coors:
            board[x][y] += value


def spread_poison():
    max_trees = 0
    max_coors = []
    for x in range(N):
        for y in range(N):
            if poisons[x][y] == 0 and board[x][y] > 0:
                cnt = board[x][y]
                coors = [(x, y)]
                for k in range(4):
                    for c in range(1, K + 1):
                        nx = x + cx[k] * c
                        ny = y + cy[k] * c
                        if nx < 0 or nx >= N or ny < 0 or ny >= N:
                            break
                        if board[nx][ny] == -1 or poisons[nx][ny] != 0:
                            break
                        if board[nx][ny] > 0:
                            cnt += board[nx][ny]
                            coors.append((nx, ny))

                if max_trees < cnt:
                    max_trees = cnt
                    max_coors = coors
    print(max_trees, max_coors)
    for x, y in max_coors:
        poisons[x][y] = C + 1
        if board[x][y] <= 0:
            continue
        board[x][y] = 0

    return max_trees


def remove_poison():
    for x in range(N):
        for y in range(N):
            if poisons[x][y] > 0:
                poisons[x][y] -= 1



N, M, K, C = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(N)]
poisons = [[0] * N for _ in range(N)]
# 상하좌우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]
# 대각선 4방향 왼쪽위부터 시계방향
cx = [-1, -1, 1, 1]
cy = [-1, 1, 1, -1]
total = 0
for _ in range(M):
    grow_trees()
    spread_trees()
    # remove_poison()
    total += spread_poison()
    remove_poison()
    for i in board:
        print(i)
    print('----------')
    for i in poisons:
        print(i)
    print('---------------')

print(total)
