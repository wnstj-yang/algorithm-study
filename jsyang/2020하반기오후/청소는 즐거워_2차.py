# 2023-10-04(수)
# 21:15 ~ 22:47
# 242ms / 32MB


def move_dust():
    global total, x, y

    cx = x + dx[d]
    cy = y + dy[d]
    curr = board[cx][cy]
    board[cx][cy] = 0
    total_dust = 0
    for key, value in directions[d].items():
        nx = cx + key[0]
        ny = cy + key[1]
        total_dust += int(curr * value)
        if nx < 0 or nx >= N or ny < 0 or ny >= N:
            total += int(curr * value)
            continue

        board[nx][ny] = int(board[nx][ny] + curr * value)
    nx = cx + dx[d]
    ny = cy + dy[d]
    if nx < 0 or nx >= N or ny < 0 or ny >= N:
        total += (curr - total_dust)
    else:
        board[nx][ny] = board[nx][ny] + (curr - total_dust)
    return cx, cy


# 좌하우상
dx = [0, 1, 0, -1]
dy = [-1, 0, 1, 0]
d = 0
N = int(input())
board = [list(map(int, input().split())) for _ in range(N)]
directions = {
    0:
        {
            (-2, 0): 0.02, (-1, -1): 0.1, (-1, 0): 0.07, (-1, 1): 0.01, (0, -2): 0.05,
            (1, -1): 0.1, (1, 0): 0.07, (1, 1): 0.01, (2, 0): 0.02
        }
    ,
    1:
        {
            (0, -2): 0.02, (1, -1): 0.1, (0, -1): 0.07, (-1, -1): 0.01, (2, 0): 0.05,
            (1, 1): 0.1, (0, 1): 0.07, (-1, 1): 0.01, (0, 2): 0.02
        }
    ,
    2:
        {
            (-2, 0): 0.02, (-1, 1): 0.1, (-1, 0): 0.07, (-1, -1): 0.01, (0, 2): 0.05,
            (1, 1): 0.1, (1, 0): 0.07, (1, -1): 0.01, (2, 0): 0.02
        }
    ,
    3:
        {
            (0, -2): 0.02, (-1, -1): 0.1, (0, -1): 0.07, (1, -1): 0.01, (-2, 0): 0.05,
            (-1, 1): 0.1, (0, 1): 0.07, (1, 1): 0.01, (0, 2): 0.02
        }
    ,
}

cnt = 2
length = 1
length_left = length
total = 0
x, y = N // 2, N // 2
while True:
    if x == 0 and y == 0:
        break

    x, y = move_dust()
    length_left -= 1

    if length_left == 0:
        cnt -= 1
        d = (d + 1) % 4
        if cnt == 0:
            cnt = 2
            length += 1
            if length == N - 1:
                cnt = 3
        length_left = length
print(total)
