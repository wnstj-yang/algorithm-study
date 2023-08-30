n = int(input())
board = [list(map(int, input().split())) for _ in range(n)]

n_x, n_y = n // 2, n // 2
dx, dy = [0, 1, 0, -1], [-1, 0, 1, 0]

# 방향, 이동할 개수
direction, c_move = 0, 1
cnt = 0

d_ratio = [[0, 0, 2, 0, 0], [0, 10, 7, 1, 0], [5, 0, 0, 0, 0], [0, 10, 7, 1, 0], [0, 0, 2, 0, 0]]


# 청소 진행
def move():
    global n_x, n_y, cnt
    # 위치 계산
    n_x, n_y = n_x + dx[direction], n_y + dy[direction]
    temp = 0

    for i in range(5):
        for j in range(5):
            dust = (board[n_x][n_y] * d_ratio[i][j]) // 100
            x, y = (n_x + i - 2), (n_y + j - 2)
            if 0 <= x < n and 0 <= y < n:
                board[x][y] += dust
            else:
                cnt += dust

            temp += dust  # a 값 체크하려고

    # a 값 넣어주기
    x, y = n_x + dx[direction], n_y + dy[direction]
    dust = board[n_x][n_y] - temp
    if 0 <= x < n and 0 <= y < n:
        board[x][y] += dust
    else:
        cnt += dust


while True:
    # 이동할 개수만큼
    for _ in range(c_move):
        move()
        if (n_x, n_y) == (0, 0):
            break

    direction = (direction + 1) % 4
    d_ratio = list(map(list, zip(*d_ratio)))

    # 이동 개수가 증가해야 하는 타이밍 : 방향이 오른쪽이거나 왼쪽 일 때
    if direction == 2 or direction == 0:
        c_move += 1

    if (n_x, n_y) == (0, 0):
        move()
        break

print(cnt)