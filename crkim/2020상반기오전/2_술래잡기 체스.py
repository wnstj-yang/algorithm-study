# 풀이시간 : 마찬가지로 문제가 너무 어려워서 몇차례 시도후에 해설을 확인했습니다. -> 2시간 / 다음날 2시간
# 맨 처음에는 무조건 완전탐색으로 문제를 풀어야 한다고 생각했는데, 당연히 시간초과가 날 수 밖에 없고 -> 그럼 백트래킹 가지치기로 접근해야 한다는 것까지 생각했습니다.
# 해설을 다시 적어보면서 문제를 이해했습니다.

TAGGER = (-2, -2)
BLANK = (-1, -1)

n = 4
board = [[(0, 0) for _ in range(n)] for _ in range(n)]
# 상, 좌상, 좌, 좌하, 하, 우하, 우, 우상
dxs = [-1, -1,  0,  1, 1, 1, 0, -1]
dys = [ 0, -1, -1, -1, 0, 1, 1,  1]
max_score = 0


def in_range(x, y):
    return 0 <= x and x < n and 0 <= y and y < n

# 도둑말이 이동할 수 있는 곳인지 확인
def thief_can_go(x, y):
    return in_range(x, y) and board[x][y] != TAGGER


# 술래가 이동할 수 있는 곳인지 확인
def tagger_can_go(x, y):
    return in_range(x, y) and board[x][y] != BLANK


def done(x, y, d):
    # 갈 수 있는 모든 경우의 수 확인
    for dist in range(1, n + 1):
        nx, ny = x + dxs[d] * dist, y + dys[d] * dist
        if tagger_can_go(nx, ny):
            return False
    
    return True


def get_next(x, y, move_dir):
    # 45'씩 8번 회전 가능한지
    for rotate_num in range(8):
        adjusted_dir = (move_dir + rotate_num) % 8
        next_x, next_y = x + dxs[adjusted_dir], y + dys[adjusted_dir]
        if thief_can_go(next_x, next_y):
            return (next_x, next_y, adjusted_dir)
    return (x, y, move_dir)


def swap(x, y, nx, ny):
    board[x][y], board[nx][ny] = board[nx][ny], board[x][y]

#도둑말 하나가 움직이는 과정
def move(target_num):
    for x in range(n):
        for y in range(n):
            piece_num, move_dir = board[x][y]
            if piece_num == target_num:
                # 이동해야할 위치와 바라보게 될 방향
                next_x, next_y, next_dir = get_next(x, y, move_dir)
                # 현재 말의 방향을 바꿔준 뒤, 두 말의 위치를 교환
                board[x][y] = (piece_num, next_dir)
                swap(x, y, next_x, next_y)
                return


# 모든 도둑말 움직임
def move_all():
    for i in range(1, n * n + 1):
        move(i)


# 술래말 탐색 x, y, d = 위치, 방향
def search_max_score(x, y, d, score):
    global max_score
    
    #움직일 곳이 없을 때, max 값 갱신
    if done(x, y, d):
        max_score = max(max_score, score)
        return
    
    # 현재 턴에 움직일 수 있는 곳
    for dist in range(1, n + 1):
        nx, ny = x + dxs[d] * dist, y + dys[d] * dist
        # 이동불가능한 위치면 패스
        if not tagger_can_go(nx, ny):
            continue
        
        # 현재 상태 저장(초기화 할 거기 때문에)
        temp = [[board[i][j] for j in range(n)] for i in range(n)]
        
        # 도둑말 잡기
        extra_score, next_dir = board[nx][ny]
        board[nx][ny], board[x][y] = TAGGER, BLANK
        
        # 도둑말 루프 돌기
        move_all()

        # 또 다시 탐색
        search_max_score(nx, ny, next_dir, score + extra_score)
    
        # 초기화
        for i in range(n):
            for j in range(n):
                board[i][j] = temp[i][j]


for i in range(n):
    given_row = list(map(int, input().split()))
    for j in range(n):
        p, d = given_row[j * 2], given_row[j * 2 + 1]
        board[i][j] = (p, d - 1)

    
# 처음 셋팅
init_score, init_dir = board[0][0]
board[0][0] = TAGGER
#한바퀴 돌고 시작
move_all()

#탐색 시작
search_max_score(0, 0, init_dir, init_score)
print(max_score)