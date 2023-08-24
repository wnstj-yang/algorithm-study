# 2023-08-24(목)
# 풀이 시간 : 21:20 ~ 22: 30
# 첫 제출 : 292ms / 메모리 43MB


# 원자들의 이동
def move_atomics(arr):
    temp = [[[] for _ in range(N)] for _ in range(N)] # 새로운 움직임을 넣을 격자
    for x in range(N):
        for y in range(N):
            if len(arr[x][y]) > 0: # 원자가 1개 이상인 위치라면 움직여준다
                for atomic in arr[x][y]:
                    m, s, d = atomic
                    # 각 방향에서 속력만큼 이동하고 격자가 연결되어있다는 가정 하에 N으로 나머지연산을 진행하여 움직인다.
                    nx = (x + dx[d] * s) % N
                    ny = (y + dy[d] * s) % N
                    temp[nx][ny].append((m, s, d))
    return temp


# 원자들의 합성 진행
def synthesis(board):
    for x in range(N):
        for y in range(N):
            if len(board[x][y]) >= 2: # 원자 2개이상일 경우
                mass_sum = 0 # 질량들의 합
                speed_sum = 0 # 속력들의 합
                atomics_cnt = len(board[x][y]) # 기존 원자들의 개수
                """
                상하좌우 값 : 0, 2, 4, 6 / 대각선 : 1, 3, 5, 7
                위의 값을 2로 나누었을 때 나머지가 0이면 상하좌우, 1이면 대각선
                둘 다면 대각선을 가진다 / 상하좌우로만 아니면 대각선만이면 상하좌우
                """
                is_odd, is_even = False, False # is_odd : 상하좌우 / is_even : 대각선
                for atomic in board[x][y]:
                    m, s, d = atomic
                    mass_sum += m
                    speed_sum += s
                    # 각 원자들의 방향판단
                    if d % 2 == 0:
                        is_odd = True
                    else:
                        is_even = True
                m = mass_sum // 5 # 총 질량을 5로 나눈다
                # 0이라면 소멸
                if m == 0:
                    board[x][y] = []
                else:
                    s = speed_sum // atomics_cnt # 총 속력을 기존 원자 개수로 나눈다
                    directions = [0, 2, 4, 6] # 방향을 모두 가지면 대각선인 경우를 제외하면 상하좌우
                    if is_odd and is_even:
                        directions = [1, 3, 5, 7]
                    board[x][y] = []
                    # 새로운 원자들 4개를 넣기 위해 위에 초기화를 진행하고 넣어준다
                    for d in directions:
                        board[x][y].append((m, s, d))


N, M, K = map(int, input().split())
board = [[[] for _ in range(N)] for _ in range(N)]
# 방향에 따른 8방향설정
dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, 1, 1, 1, 0, -1, -1, -1]
result = 0
for _ in range(M):
    x, y, m, s, d = map(int, input().split())
    board[x - 1][y - 1].append((m, s, d))

while K:
    # 1. 모든 원자의 이동
    board = move_atomics(board)
    # 2. 원자의 합성
    synthesis(board)
    K -= 1 # 초 감소

# 남아있는 모든 원자들의 질량의 합을 구한다
for x in range(N):
    for y in range(N):
        if len(board[x][y]) > 0:
            for m, s, d in board[x][y]:
                result += m
print(result)
