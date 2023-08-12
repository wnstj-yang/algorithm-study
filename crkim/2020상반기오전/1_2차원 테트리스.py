# 풀이시간 : 문제 읽고 이해, 테스트만 3시간 걸렸습니다. -> 해설 참고
# 해설 확인 후 최적화 하는 방법으로 문제 풀이를 이해했습니다.

# (0-빈 배열) 1타입, 2타입, 3타입 지정
shapes = [[], [[1, 0],[0, 0]], [[1, 1], [0, 0]], [[1, 0],[1, 0]]]
n, m, k = 6, 4, int(input())
# 보드 생성
board = [[[0 for _ in range(m)] for _ in range(n)] for _ in range(2)]
score = 0

def can_go(b_num, tile_type, x, y):
    # 바닥에 부딪히거나, 벽돌이 존재하는 경우 진행불가 (범위 제한 체크) 
    for dx in range(2):
        for dy in range(2):
            if shapes[tile_type][dx][dy]:
                nx, ny = x + dx, y + dy
                if not (0 <= nx and nx < n and 0 <= ny and ny < m) or board[b_num][nx][ny]:
                    return False
    return True

# 보드에 특정 타입의 타일 놓기
def put(b_num, tile_type, x, y):
    for dx in range(2):
        for dy in range(2):
            if shapes[tile_type][dx][dy]:
                nx, ny = x + dx, y + dy
                board[b_num][nx][ny] = 1
            

def down_one_line(b_num, end_row):
    for row in range(end_row, 0, -1):
        for col in range(m):
            board[b_num][row][col] = board[b_num][row - 1][col]
            board[b_num][row - 1][col] = 0

def all_filled(b_num, row):
    for col in range(m):
        if board[b_num][row][col] != 1:
            return False
    return True

#어두운 부분 : 아래 -> 위 가득 채워져 있으면 +1 / 당겨줌
def process_dark(b_num):
    global score
    row = n - 1
    while(row >= 2):
        if all_filled(b_num, row):
            score += 1
            down_one_line(b_num, row)
        else:
            row -= 1
    
#색칠하기전에 블록이 존재하는지 체크
def block_exist(b_num, row):
    return any([
        board[b_num][row][col] == 1
        for col in range(m)
    ])

#연한 부분
def process_light(b_num):
    # 1. 2 줄 중에 하나라도 타일이 놓여 있는지 체크
    drop_cnt = 0
    if block_exist(b_num, 0):
        drop_cnt += 1
    if block_exist(b_num, 1):
        drop_cnt += 1
    
    # 2. 체크한 수만큼 타일 내려줌
    for _ in range(drop_cnt):
        down_one_line(b_num, n - 1)


def drop(b_num, tile_type, col):
    # 1. 블록 떨어뜨림
    for row in range(n):
        # 다음 행에 블록이 있다면, 지금 위치에 놓기
        if not can_go(b_num, tile_type, row + 1, col):
            put(b_num, tile_type, row, col)
            break
    
    #2. 진한 부분
    process_dark(b_num)
    
    #3. 연한부분
    process_light(b_num)


def simulate(t, x, y):
    # 1. 노란색 영역
    drop(0, t, y)
    
    # 2. 빨간색 영역 -> 90도 회전
    if t == 1:
        drop(1, 1, m - 1 - x)
    elif t == 2:
        drop(1, 3, m - 1 - x)
    else:
        drop(1, 2, m - 1 - (x + 1))

for _ in range(k):
    t, x, y = tuple(map(int, input().split()))
    simulate(t, x, y)

print(score)

cnt  = 0
for l in range(2):
    for i in range(n):
        for j in range(m):
            cnt += board[l][i][j]
print(cnt)