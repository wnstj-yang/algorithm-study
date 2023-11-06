# 2023-11-06(월)
# 22:06 ~ 23:51
# 다시 화이팅


def rotate(x, y, divide, d, temp):
    for i in range(x, x + divide):
        for j in range(y, y + divide):
            nx = i + dx[d] * divide
            ny = j + dy[d] * divide
            temp[nx][ny] = board[i][j]


def search(l):
    temp = [[0] * length for _ in range(length)]
    level = 2 ** l
    divide = 2 ** (l - 1)
    for i in range(0, length, level):
        for j in range(0, length, level):
            rotate(i, j, divide, 0, temp)
            rotate(i, j + divide, divide, 1, temp)
            rotate(i + divide, j + divide, divide, 2, temp)
            rotate(i + divide, j, divide, 3, temp)
    return temp


def melt():
    melt_list = []
    for i in range(length):
        for j in range(length):
            if board[i][j]:
                cnt = 0
                for k in range(4):
                    nx = i + dx[k]
                    ny = j + dy[k]
                    if nx < 0 or nx >= length or ny < 0 or ny >= length:
                        continue
                    if board[nx][ny]:
                        cnt += 1
                if cnt < 3:
                    melt_list.append((i, j))
    for x, y in melt_list:
        board[x][y] -= 1


N, Q = map(int, input().split())
length = 2 ** N
board = [list(map(int, input().split())) for _ in range(length)]
levels = list(map(int, input().split()))
# 우하좌상
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]
for l in levels:
    if l:
        board = search(l)
    melt()

q = []
visited = [[False] * length for _ in range(length)]
max_cnt = 0
total = 0

for i in range(length):
    for j in range(length):
        if not visited[i][j] and board[i][j]:
            total += board[i][j]
            visited[i][j] = True
            q = [(i, j)]
            cnt = 1
            while q:
                x, y = q.pop()
                for k in range(4):
                    nx = x + dx[k]
                    ny = y + dy[k]
                    if nx < 0 or nx >= length or ny < 0 or ny >= length:
                        continue
                    if not visited[nx][ny] and board[nx][ny]:
                        cnt += 1
                        total += board[nx][ny]
                        visited[nx][ny] = True
                        q.append((nx, ny))
            max_cnt = max(max_cnt, cnt)
print(total)
print(max_cnt)
