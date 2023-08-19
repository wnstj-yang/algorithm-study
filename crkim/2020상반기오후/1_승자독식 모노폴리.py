#생각한 방법

#1. 초기값 설정
#2. 우선순위에 따른 이동
#3. 1턴 = 모든 플레이어가 다 움직여야 함
#3-0 빈칸이 있으면 빈칸으로, 빈칸이 없으면 독점 위치로 이동함
#3-1 n_player에 이동하고자 하는 값을 넣어둠
#3-2 n_player 중 x,y 값이 겹치는 곳은 플레이어 넘버가 낮은 애한테 줌
#3-3 삭제된 n_player -> 재탐색 (독식한 위치로)
#4. 이동 완료시 n_player 다 지움
#5. 1만 남거나 1000이 될 때까지 while 
#but. K값은 어떻게 처리할까?

# 다시 생각하는 과정
# 모든 움직임 시에 k개의 값도 함께 카운트 해줘야 함
# 현재 위치 기준으로 이동할 수 있는 4방향 탐색 

# 해설 참조

DIR_NUM = 4
EMPTY = (401, 401)
EMPTY_NUM = 401

n, m, k = tuple(map(int, input().split()))
given_map = [list(map(int, input().split())) for _ in range(n)]
next_dir = [[[0 for _ in range(DIR_NUM)] for _ in range(DIR_NUM)] for _ in range(m + 1)]
player = [[EMPTY for _ in range(n)] for _ in range(n)]
next_player = [[EMPTY for _ in range(n)] for _ in range(n)]
contract = [[EMPTY for _ in range(n)] for _ in range(n)]
elapsed_time = 0

def in_range(x, y):
    return 0 <= x and x < n and 0 <= y and y < n

def can_go(x, y, target_num):
    if not in_range(x, y):
        return False
    contract_num, _ = contract[x][y]
    return contract_num == target_num


def next_pos(x, y, curr_dir):
    dxs, dys = [-1, 1, 0, 0], [0, 0, -1, 1]
    num, _ = player[x][y]
    for move_dir in next_dir[num][curr_dir]:
        nx, ny = x + dxs[move_dir], y + dys[move_dir]
        if can_go(nx, ny, EMPTY_NUM):
            return (nx, ny, move_dir)
    for move_dir in next_dir[num][curr_dir]:
        nx, ny = x + dxs[move_dir], y + dys[move_dir]
        
        if can_go(nx, ny, num):
            return (nx, ny, move_dir)

def update(x, y, new_player):
    if next_player[x][y] > new_player:
        next_player[x][y] = new_player


def move(x, y):
    num, curr_dir = player[x][y]
    nx, ny, move_dir = next_pos(x, y, curr_dir)
    update(nx, ny, (num, move_dir))

def dec_contract(x, y):
    num, remaining_period = contract[x][y]
    if remaining_period == 1:
        contract[x][y] = EMPTY
    else:
        contract[x][y] = (num, remaining_period - 1)


def add_contract(x, y):
    num, _ = player[x][y]
    contract[x][y] = (num, k)


def simulate():
    for i in range(n):
        for j in range(n):
            next_player[i][j] = EMPTY

    for i in range(n):
        for j in range(n):
            if player[i][j] != EMPTY:
                move(i, j)

    for i in range(n):
        for j in range(n):
            player[i][j] = next_player[i][j]

    for i in range(n):
        for j in range(n):
            if contract[i][j] != EMPTY:
                dec_contract(i, j)

    for i in range(n):
        for j in range(n):
            if player[i][j] != EMPTY:
                add_contract(i, j)


def end():
    if elapsed_time >= 1000:
        return True
    for i in range(n):
        for j in range(n):
            if player[i][j] == EMPTY:
                continue
            num, _ = player[i][j]
            if num != 1:
                return False
    
    return True

init_dirs = list(map(int, input().split()))
for num, move_dir in enumerate(init_dirs, start=1):
    for i in range(n):
        for j in range(n):
            if given_map[i][j] == num:
                player[i][j] = (num, move_dir - 1)
                contract[i][j] = (num, k)

for num in range(1, m + 1):
    for curr_dir in range(DIR_NUM):
        dirs = list(map(int, input().split()))
        for i, move_dir in enumerate(dirs):
            next_dir[num][curr_dir][i] = move_dir - 1

while not end():
    simulate()
    elapsed_time += 1

if elapsed_time >= 1000:
    elapsed_time = -1

print(elapsed_time)