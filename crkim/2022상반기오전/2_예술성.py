#구현력이 부족해서 시도해보다가 해설 참고

n = int(input())
arr = [list(map(int, input().split())) for _ in range(n)]
next_arr = [[0] * n for _ in range(n)]
group_n = 0
group = [[0] * n for _ in range(n)]
group_cnt = [0] * (n * n + 1) 
visited = [[False] * n for _ in range(n)]

dxy = [(1,0), (-1,0), (0,1), (0,-1)]
# (x, y) 위치에서 DFS를 진행
def dfs(x, y):
    for dx, dy in dxy:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and arr[nx][ny] == arr[x][y]:
            visited[nx][ny] = True
            group[nx][ny] = group_n
            group_cnt[group_n] += 1
            dfs(nx, ny)

def rotate_square(sx, sy, square_n):
    # 시계 방향 90도 회전
    for x in range(sx, sx + square_n):
        for y in range(sy, sy + square_n):
            ox, oy = x - sx, y - sy
            rx, ry = oy, square_n - ox - 1 #좌표갱신
            next_arr[rx + sx][ry + sy] = arr[x][y] 

#점수 더하기
ans = 0
for _ in range(4):
    group_n = 0
    # visited 초기화
    for i in range(n):
        for j in range(n):
            visited[i][j] = False
    # 그룹묶기
    for i in range(n):
        for j in range(n):
            if not visited[i][j]:
                group_n += 1
                visited[i][j] = True
                group[i][j] = group_n
                group_cnt[group_n] = 1
                dfs(i, j)

    # 점수계산
    art_score = 0
    # 특정 변을 사이에 두고 두 칸의 그룹이 다른 경우 점수 더함
    for i in range(n):
        for j in range(n):
            for dx, dy in dxy:
                nx, ny = i + dx, j + dy
                if 0 <= nx < n and 0 <= ny < n and arr[i][j] != arr[nx][ny]:
                    g1, g2 = group[i][j], group[nx][ny]
                    num1, num2 = arr[i][j], arr[nx][ny]
                    cnt1, cnt2 = group_cnt[g1], group_cnt[g2]
                    art_score += (cnt1 + cnt2) * num1 * num2
    
    ans += (art_score // 2) #중복 제거

    # 회전
    for i in range(n):
        for j in range(n):
            next_arr[i][j] = 0 #초기화
    
    for i in range(n):
        for j in range(n):
            if j == n // 2: #세로
                next_arr[j][i] = arr[i][j]
            elif i == n // 2: #가로
                next_arr[n - j - 1][i] = arr[i][j]

    # 정사각형 4개 회전
    sqaure_n = n // 2
    rotate_square(0, 0, sqaure_n)
    rotate_square(0, sqaure_n + 1, sqaure_n)
    rotate_square(sqaure_n + 1, 0, sqaure_n)
    rotate_square(sqaure_n + 1, sqaure_n + 1, sqaure_n)
    
    # 값 갱신
    for i in range(n):
        for j in range(n):
            arr[i][j] = next_arr[i][j]

print(ans)