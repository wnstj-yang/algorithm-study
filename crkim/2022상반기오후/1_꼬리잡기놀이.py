# 앞으로 한 칸 이동한다 -> 공을 던진다 -> 공을 받는다 -> 점수를 계산한다 -> 방향을 바꿔준다 -> 공을 던지는 위치를 바꿔준다 -> 앞으로 이동한다를 반복하려고 함
# 점수를 계산 하는 부분에서 공을 맞은 애가 몇 번째에 있는 애인지 계산하기 어려움
# 처음에는 공을 맞았을 때 dfs를 돌아서 위치를 계산하려고 함 혹은 처음에 값을 받을 때 위치값도 board에 같이 저장

# 지금 하려고 하는 접근은 처음 시작 시에 그룹 쪼갬(max5니까 빈 배열 5개에 각 그룹별 사람들끼리만 묶어줌)
#   -> 맞은 애가 1그룹이면, 1그룹에만 dfs 돌면서 점수 계산 및 머리꼬리 바꿔줌
# -> 다 끝나면 board 한 번 갱신하고 위치 이동.. 시간 안될 것 같음

n, m, k = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(n)]
ans = 0
visited = [[False] * (n + 1) for _ in range(n + 1)]
dxy = [(-1,0), (0,-1), (1,0), (0,1)]
cnt = 0

#몇 번째에 있는 숫자인지 확인
def dfs(x, y):
    global cnt
    visited[x][y] = True
    for dx, dy in zip(dxy):
        nx, ny = x + dx, y + dy
        if not(1 <= nx <= n and 1 <= ny <= n):
            continue
        if board[nx][ny] == 0:
            continue
        if visited[nx][ny]:
            continue
        cnt += 1
        dfs(nx, ny)

#공을 던지는 순서
direc, start = -1, -1
def throw_turn() :
    global direc, start
    start += 1
    if start % n == 0:
        direc += 1
        start = 0
        if direc > 3 :
            direc = 0
    if direc == 0 :
        return (start, 0)
    elif direc == 1:
        return (0, start)
    elif direc == 2:
        return (n-start, n)
    else:
        return (n, n-start)

#앞으로 한 칸 이동
def move():
    return True

#공을 던짐
def throw():
    global start
    a = throw_turn()
    x, y = a[0], a[1]
    #던진 공에 맞는 사람 체크
    for i in range(n):
        if direc == 0 :
            if board[x][y] == 0 or board[x][y] == 4:
                y += 1
            else :
                rotate(board[x][y])
                break
        elif direc == 1 :
            if board[x][y] == 0 or board[x][y] == 4:
                x += 1
            else :
                rotate(board[x][y])
                break
        elif direc == 2:
            if board[x][y] == 0 or board[x][y] == 4:
                y -= 1
            else :
                rotate(board[x][y])
                break
        else:
            if board[x][y] == 0 or board[x][y] == 4:
                x -= 1
            else :
                rotate(board[x][y])
                break


#공을 받음 -> 점수계산 -> 방향 전환
def rotate(x, y) :
    global ans
    dfs(x, y)


    return True

for _ in range(k):
    move()
    throw()

### --------------
m1, m2, m3, m4, m5 = [], [], [], [], []
def init() :
    for i in range(n):
        print('a')

print(ans)