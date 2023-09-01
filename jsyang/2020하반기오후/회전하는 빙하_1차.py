# 2023-08-31(목)
# 풀이 시간 : 20:50 ~ 24:20 (3시간 30분소요 / 풀이 확인함)
# 첫 제출 ms / MB
# 아니... 문제 너무 헷갈리게 해놓음 => 미궁속으로 빠져버림
# 중간에 조건 얼음 녹일 때 3이상이면 1을 안줄이는데 줄이는 걸로 잘못 체크함..
# 생각보다 오래안걸릴거같은 문제였는데 많이걸림


from collections import deque


# 레벨에 따라 회전하는 부분
def rotate_90(L):
    step = 2 ** L # 레벨 크기
    divided = 2 ** (L - 1) # 4등분 하는 크기
    temp = [[0] * length for _ in range(length)] # 회전하면서 갱신된 값들을 넣으므로 전체 격자를 0으로 초기화
    # 격자 전체에서 step 크기만큼 건너뛰면서 4등분 체크한다.
    for i in range(0, length, step):
        for j in range(0, length, step):
            # 4등분 분할정복느낌
            temp = rotate_parts(i, j, divided, 0, temp)
            temp = rotate_parts(i, j + divided, divided, 1, temp)
            temp = rotate_parts(i + divided, j, divided, 2, temp)
            temp = rotate_parts(i + divided, j + divided, divided, 3, temp)

    return temp


# L레벨안의 4등분 회전
def rotate_parts(x, y, d, direction, temp):
    # 현재 위치 x, y에서 d만큼(2^(L-1))회전해서 움직인다.
    for i in range(x, x + d):
        for j in range(y, y + d):
            # 회전 방향인 direction에 따라서 움직인다.
            nx = i + dx[direction] * d
            ny = j + dy[direction] * d
            temp[nx][ny] = board[i][j]
    return temp


# 얼음 녹이는 과정
def melt():
    melt_list = [] # 얼음을 한 번에 녹이기 때문에 좌표 값들을 저장
    for x in range(length):
        for y in range(length):
            # 얼음이 존재한다면 4방향을 살핀다.
            if board[x][y] > 0:
                cnt = 0
                for k in range(4):
                    nx = x + dx[k]
                    ny = y + dy[k]
                    if nx < 0 or nx >= length or ny < 0 or ny >= length:
                        continue
                    if board[nx][ny] > 0:
                        cnt += 1
                # 3개 미만인 경우에 1씩 줄여야 하므로 좌표 값을 넣는다
                if cnt < 3:
                    melt_list.append((x, y))

    # 얼음을 동시에 녹인다
    for x, y in melt_list:
        board[x][y] -= 1


def search_biggest():
    # BFS로 방문 표시를 통해 각 군집의 크기를 구한다.
    visited = [[False] * length for _ in range(length)]
    max_cnt = 0 # 최대 군집 크기
    for i in range(length):
        for j in range(length):
            # 해당 지역을 방문하지 않았고 빙하가 존재한다면
            if not visited[i][j] and board[i][j] > 0:
                q = deque()
                q.append((i, j))
                visited[i][j] = True
                cnt = 1 # 현재 지역을 포함하므로 1로 초기화
                while q:
                    x, y = q.popleft()
                    for k in range(4):
                        nx = x + dx[k]
                        ny = y + dy[k]
                        # 격자 범위를 벗어나가면 안된다.
                        if nx < 0 or nx >= length or ny < 0 or ny >= length:
                            continue
                        # 4방향으로 움직이면서 군집을 연결시킨다.
                        if not visited[nx][ny] and board[nx][ny] > 0:
                            visited[nx][ny] = True
                            cnt += 1
                            q.append((nx, ny))
                # 하나의 군집이 형성된다면 최대 크기와 비교해서 갱신
                max_cnt = max(max_cnt, cnt)
    return max_cnt


N, Q = map(int, input().split()) # N : 레벨 / Q : 회전 횟수
length = 2 ** N # 격자 크기
board = [list(map(int, input().split())) for _ in range(length)]
orders = list(map(int, input().split()))
# 우하좌상
dx = [0, 1, -1, 0]
dy = [1, 0, 0, -1]

# 순서대로 level
for l in orders:
    # 0이면 회전한다는 의미가 있찌만 사실상 안움직인다.
    if l:
        # 오른쪽으로 돌면서 격자판을 갱신해줌
        board = rotate_90(l)
    # 회전 이후 얼음 녹이기 과정을 거친다.
    melt()

# 회전이 모두 끝난 이후 빙하의 총 양
total = 0
for line in board:
    total += sum(line)

# 최대 군집을 구한다
max_group = search_biggest()
print(total)
# 최대 군집의 크기가 0이면 0
if max_group:
    print(max_group)
else:
    print(0)
