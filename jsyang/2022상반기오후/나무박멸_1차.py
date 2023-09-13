# 2023-09-12(화)
# 풀이 시간 : 21:25 ~ 23:25/ 23:40 ~ 00:30 정도 
# 첫 제출 : 337ms / 메모리 32MB
# 왤케 못하지
# 하... 헷갈렸던 부분 -> 나무가 비어있으면 제초제를 뿌려야할 곳이 아니라고 생각함
# 위의 과정은 점수를 계산할 때 박멸할 나무를 정하는 것이고
# 그 다음으로 대각선에 나무가 비어있는 것과 관계없이 제초제를 뿌려야했다.


# 1. 나무의 성장
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
                # 근처 나무의 수 만큼 성장
                board[x][y] += cnt


# 2. 나무의 번식
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
                # 근처 빈 곳이 존재할 때 
                # 번식할 나무의 값 = 현재 나무의 값 / 빈 공간의 수
                if cnt > 0:
                    result = board[x][y] // cnt
                    spread_list.append([result, coors])

    # 한 번에 나무의 번식을 진행
    for value, coors in spread_list:
        for x, y in coors:
            board[x][y] += value


def spread_poison():
    max_trees = 0
    max_coors = []
    sx, sy = 0, 0
    for x in range(N):
        for y in range(N):
            if poisons[x][y] == 0 and board[x][y] > 0:
                cnt = board[x][y]
                for k in range(4):
                    for c in range(1, K + 1):
                        nx = x + cx[k] * c
                        ny = y + cy[k] * c
                        # 벽이거나 나무가 없는 상태면 제초제를 뿌릴 수 있겠지만,
                        # 나무의 최대 값을 구하기 때문에 조건을 벽이거나 빈 곳이라면 더 이상 갈 수없어서 멈춘다
                        if nx < 0 or nx >= N or ny < 0 or ny >= N or board[nx][ny] <= 0:
                            break
                        cnt += board[nx][ny]

                # 행, 열 작은 값부터 가기 때문에 값이 최대라면 이를 갱신해준다.
                if max_trees < cnt:
                    max_trees = cnt
                    sx, sy = x, y # 좌표 값도 초기화
    # 제초제를 뿌릴 시작점은 따로 초기화
    board[sx][sy] = 0
    poisons[sx][sy] = C
    # 아래의 대각선 방향으로 다시 하는 이유는 제초제를 뿌려야하기 때문이다.
    # 위의 과정과 동시에 하지 못하는 이유는 비어있는 곳을 건너 뛰어서 계산할 수 있기 때문이라고 생각
    for k in range(4):
        for c in range(1, K + 1):
            nx = sx + cx[k] * c
            ny = sy + cy[k] * c
            if nx < 0 or nx >= N or ny < 0 or ny >= N:
                break
            # 벽이 있거나 나무가 없는 칸이 있는 경우 해당 칸까지는 제초제가 뿌려지고,
            # 그 이후에는 전파되지 않는다.
            poisons[nx][ny] = C
            if board[nx][ny] <= 0:
                break
            board[nx][ny] = 0
    return max_trees


# 3. 제초제 매년 감소
def remove_poison():
    for x in range(N):
        for y in range(N):
            if poisons[x][y] > 0:
                poisons[x][y] -= 1


N, M, K, C = map(int, input().split()) # N : 격자 크기, M : 박멸 진행 년수, K: 제초제 확산 범위, C: 제초제 남아있는 년 수
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
    grow_trees() # 1. 나무의 성장
    spread_trees() # 2. 나무의 번식
    remove_poison() # 3. 1년이 지났으므로 제초제를 줄여준다
    total += spread_poison() # 4. 제초제 뿌림

print(total)
