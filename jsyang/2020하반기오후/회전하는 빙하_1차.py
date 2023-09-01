# 2023-08-31(목)
# 풀이 시간 : 20:50 ~ 24:20 (3시간 30분소요 / 풀이 확인함)
# 첫 제출 ms / MB
# 아니... 문제 너무 헷갈리게 해놓음 => 미궁속으로 빠져버림
# 중간에 조건 얼음 녹일 때 3이상이면 1을 안줄이는데 줄이는 걸로 잘못 체크함..
# 생각보다 오래안걸릴거같은 문제였는데 많이걸림


from collections import deque


# 레벨에 따라 회전하는 부분
def rotate_90(L):
    step = 2 ** L
    divided = 2 ** (L - 1)

    temp = [[0] * length for _ in range(length)]
    for i in range(0, length, step):
        for j in range(0, length, step):
            # 4등분
            temp = rotate_parts(i, j, divided, 0, temp)
            temp = rotate_parts(i, j + divided, divided, 1, temp)
            temp = rotate_parts(i + divided, j, divided, 2, temp)
            temp = rotate_parts(i + divided, j + divided, divided, 3, temp)

    return temp


# L레벨안의 4등분 회전
def rotate_parts(x, y, d, direction, temp):
    for i in range(x, x + d):
        for j in range(y, y + d):
            nx = i + dx[direction] * d
            ny = j + dy[direction] * d
            temp[nx][ny] = board[i][j]
    return temp


def melt():
    melt_list = []
    for x in range(length):
        for y in range(length):
            if board[x][y] > 0:
                cnt = 0
                for k in range(4):
                    nx = x + dx[k]
                    ny = y + dy[k]
                    if nx < 0 or nx >= length or ny < 0 or ny >= length:
                        continue
                    if board[nx][ny] > 0:
                        cnt += 1
                if cnt < 3:
                    melt_list.append((x, y))

    # 얼음을 동시에 녹인다
    for x, y in melt_list:
        board[x][y] -= 1


def search_biggest():
    visited = [[False] * length for _ in range(length)]
    max_cnt = 0
    for i in range(length):
        for j in range(length):
            if not visited[i][j] and board[i][j] > 0:
                q = deque()
                q.append((i, j))
                visited[i][j] = True
                cnt = 1
                while q:
                    x, y = q.popleft()
                    for k in range(4):
                        nx = x + dx[k]
                        ny = y + dy[k]
                        if nx < 0 or nx >= length or ny < 0 or ny >= length:
                            continue
                        if not visited[nx][ny] and board[nx][ny] > 0:
                            visited[nx][ny] = True
                            cnt += 1
                            q.append((nx, ny))
                max_cnt = max(max_cnt, cnt)
    return max_cnt



# 얼음 녹이기

N, Q = map(int, input().split())
length = 2 ** N
board = [list(map(int, input().split())) for _ in range(length)]
orders = list(map(int, input().split()))
# 우하좌상
dx = [0, 1, -1, 0]
dy = [1, 0, 0, -1]

for l in orders:
    if l:
        board = rotate_90(l)
    melt()

total = 0
for line in board:

    total += sum(line)
max_group = search_biggest()
print(total)
if max_group:
    print(max_group)
else:
    print(0)
