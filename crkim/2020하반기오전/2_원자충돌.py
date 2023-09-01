#문제 풀이시간 : 3시간 => 풀이 완성 못했음 / 가로세로대각선 dxdy 퍼지는 부분에서 막힘
#해설 참고 -> 해설 최적화

n, m, k = tuple(map(int, input().split()))
board = [[[] for _ in range(n)] for _ in range(n)]
next = [[[] for _ in range(n)] for _ in range(n)]
dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, 1, 1, 1, 0, -1, -1, -1]

for _ in range(m):
    x, y, m, s, d = tuple(map(int, input().split()))
    board[x - 1][y - 1].append((m, s, d))

for _ in range(k):
    for i in range(n):
        for j in range(n):
            next[i][j] = list()

    for x in range(n):
        for y in range(n):
            for w, v, m_dir in board[x][y]:
                n_x, n_y = (x + dx[m_dir] * v + n * v) % n, (y + dy[m_dir] * v + n * v) % n
                next[n_x][n_y].append((w, v, m_dir))

    for i in range(n):
        for j in range(n):
            board[i][j] = list()

    for i in range(n):
        for j in range(n):
            n_cnt = len(next[i][j])
            if n_cnt == 1:
                board[i][j].append(next[i][j][0])
            elif n_cnt > 1:
                mass, velo = 0, 0
                d_type = [0, 0]

                for w, v, m_dir in next[i][j]:
                    mass += w
                    velo += v
                    d_type[m_dir % 2] += 1

                s_dir = -1
                if not d_type[0] or not d_type[1]:
                    s_dir = 0
                else:
                    s_dir = 1

                n_cnt = len(next[i][j])

                for m_dir in range(s_dir, 8, 2):
                    if mass // 5 > 0:
                        board[i][j].append((mass // 5, velo // n_cnt, m_dir))


ans = sum([weight for i in range(n) for j in range(n) for weight, _, _ in board[i][j]])

print(ans)