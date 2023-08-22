# 2023-08-22(화)
# 풀이 시간: 21:15 ~ 22:30
# 아쉬운 점: 집중력이 좀 덜 됐다. 1주를 간격으로 두었지만 음... 일단 좀 더 집중해서 푸는게 좋을 것 같다
# 아쉬운 점 2: 풀이가 좀 단순해진 것 같다. 기존 풀이와 다른 방법은 없는지 고민하는 과정, x, y축 변경해서 푸는 적용도 필요

# 도둑말의 이동
def move_runners(cx, cy, copy_board):
    # 1 ~ 16번 순으로 움직여야 한다.
    for target in range(1, 17):
        found = False # 번호를 찾았다면 더이상 순회 X. 오히려 중복 발생
        for x in range(4):
            for y in range(4):
                if copy_board[x][y][0] == target:
                    d = copy_board[x][y][1] # 기존 방향
                    for k in range(8):
                        nd = (d + k) % 8 # 45도 반시계 회전을 8방향으로 돌기에 나머지연산으로 범위 내 이동 표현
                        nx = x + dx[nd]
                        ny = y + dy[nd]
                        # 격자를 벗어나거나 술래 말이 있다면 이동 X
                        if nx < 0 or nx >= 4 or ny < 0 or ny >= 4 or (nx == cx and ny == cy):
                            continue
                        # 변경된 방향을 넣고 서로의 위치를 바꾼다.
                        copy_board[x][y][1] = nd
                        copy_board[x][y], copy_board[nx][ny] = copy_board[nx][ny], copy_board[x][y]
                        found = True
                        break
                if found:
                    break
            if found:
                break


# 최대값을 위해 깊이 우선 탐색으로 찾아나선다
def dfs(cx, cy, result, board):
    global ans
    # DFS 시 기존의 정보의 변경 보다 리스트 슬라이싱을 활용하여 리스트 복사를 진행해 탐색
    copy_board = [[item[:] for item in board[i]] for i in range(4)]
    result += copy_board[cx][cy][0] # 술래말이 잡았기 때문에 결과 값을 더해준다
    ans = max(result, ans) # 최대 값 판단
    d = copy_board[cx][cy][1] # 술래말이 잡았던 도둑말의 이동방향 저장
    copy_board[cx][cy] = [0, 0] # 빈 값으로 변경
    move_runners(cx, cy, copy_board)

    # 최대 4칸 이동 가능하므로 해당 방향으로 4칸이동가능한지 파악 후 이동 진행
    for i in range(1, 5):
        nx = cx + dx[d] * i
        ny = cy + dy[d] * i
        if nx < 0 or nx >= 4 or ny < 0 or ny >= 4:
            continue
        if copy_board[nx][ny][0] != 0:
            dfs(nx, ny, result, copy_board)


# 주어진 8방향
dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, -1, -1, -1, 0, 1, 1, 1]

board = []
ans = 0
for i in range(4):
    info = list(map(int, input().split()))
    temp = []
    for j in range(0, 8, 2):
        temp.append([info[j], info[j+1] - 1])
    board.append(temp)
dfs(0, 0, 0, board)
print(ans)
