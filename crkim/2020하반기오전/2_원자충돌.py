# 변수 선언 및 입력:

n, m, k = tuple(map(int, input().split()))

grid = [
    [[] for _ in range(n)]
    for _ in range(n)
]

next_grid = [
    [[] for _ in range(n)]
    for _ in range(n)
]


def in_range(x, y):
    return 0 <= x and x < n and 0 <= y and y < n


def next_pos(x, y, v, move_dir):
    dxs = [-1, -1, 0, 1, 1, 1, 0, -1]
    dys = [0, 1, 1, 1, 0, -1, -1, -1]

    # 움직인 이후 값이 음수가 되는 경우, 이를 양수로 쉽게 만들기 위해서는
    # n의 배수이며 더했을 때 값을 항상 양수로 만들어 주는 수인 nv를 더해주면 됩니다.
    nx = (x + dxs[move_dir] * v + n * v) % n
    ny = (y + dys[move_dir] * v + n * v) % n

    return (nx, ny)


def move_all():
    for x in range(n):
        for y in range(n):
            for w, v, move_dir in grid[x][y]:
                next_x, next_y = next_pos(x, y, v, move_dir)
                next_grid[next_x][next_y].append(
                    (w, v, move_dir)
                )


def split(x, y):
    sum_of_mass, sum_of_velocity = 0, 0
    num_of_dir_type = [0, 0]

    for w, v, move_dir in next_grid[x][y]:
        sum_of_mass += w
        sum_of_velocity += v
        num_of_dir_type[move_dir % 2] += 1

    start_dir = -1
    # 전부 상하좌우 방향이거나, 전부 대각선 방향으로만 이루어져 있다면
    # 각각 상하좌우 방향을 갖습니다.
    if not num_of_dir_type[0] or not num_of_dir_type[1]:
        start_dir = 0
    # 그렇지 않다면, 각각 대각선 방향을 갖습니다.
    else:
        start_dir = 1

    atom_cnt = len(next_grid[x][y])

    # 각 방향 갖는 원자를 추가해줍니다.
    for move_dir in range(start_dir, 8, 2):
        # 질량이 0보다 큰 경우에만 추가합니다.
        if sum_of_mass // 5 > 0:
            grid[x][y].append(
                (sum_of_mass // 5,
                 sum_of_velocity // atom_cnt,
                 move_dir)
            )


def compound():
    # Step1. grid값을 초기화합니다.
    for i in range(n):
        for j in range(n):
            grid[i][j] = list()

    # Step2. 합성을 진행합니다.
    for i in range(n):
        for j in range(n):
            atom_cnt = len(next_grid[i][j])
            if atom_cnt == 1:
                grid[i][j].append(next_grid[i][j][0])
            # 2개 이상인 경우에는 분열됩니다.
            elif atom_cnt > 1:
                split(i, j)


def simulate():
    # Step1. next_grid를 초기화합니다.
    for i in range(n):
        for j in range(n):
            next_grid[i][j] = list()

    # Step2. 원자들을 전부 움직입니다.
    move_all()

    # Step3. 합성이 일어나고, 그 결과를 grid에 저장합니다.
    compound()


for _ in range(m):
    x, y, m, s, d = tuple(map(int, input().split()))
    grid[x - 1][y - 1].append((m, s, d))

# k초에 걸쳐 시뮬레이션을 반복합니다.
for _ in range(k):
    simulate()

ans = sum([
    weight
    for i in range(n)
    for j in range(n)
    for weight, _, _ in grid[i][j]
])

print(ans)