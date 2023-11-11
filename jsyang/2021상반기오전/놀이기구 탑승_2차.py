# 2023-11-11(토)
# 16:00 ~ 16:35


def search(s, likes):
    candidates = []
    for x in range(N):
        for y in range(N):
            if board[x][y] == 0:
                like = 0
                blank = 0
                for k in range(4):
                    nx = x + dx[k]
                    ny = y + dy[k]
                    if nx < 0 or nx >= N or ny < 0 or ny >= N:
                        continue

                    if board[nx][ny] == 0:
                        blank += 1
                    elif board[nx][ny] in likes:
                        like += 1
                candidates.append([like, blank, x, y])
    candidates.sort(key=lambda x:(-x[0], -x[1], x[2], x[3]))
    x, y = candidates[0][2], candidates[0][3]
    board[x][y] = s


N = int(input())
board = [[0] * N for _ in range(N)]
students = {}
score = {
    0: 0,
    1: 1,
    2: 10,
    3: 100,
    4: 1000
}
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]
total = 0
for _ in range(N * N):
    n0, n1, n2, n3, n4 = map(int, input().split())
    students[n0] = [n1, n2, n3, n4]

for student, likes in students.items():
    search(student, likes)

cnt = 0
for x in range(N):
    for y in range(N):
        cnt = 0
        student = board[x][y]
        for k in range(4):
            nx = x + dx[k]
            ny = y + dy[k]
            if nx < 0 or nx >= N or ny < 0 or ny >= N:
                continue
            if board[nx][ny] in students[student]:
                cnt += 1
        total += score[cnt]
print(total)
