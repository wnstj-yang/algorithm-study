# 2023-09-17(일)
# 풀이 시간 : 10:55 ~ 12:55 / 18:00 ~ 18:40
# 첫 제출 : 135ms / 메모리 31MB
# 진 사람 움직일 때 한 칸 움직이고 또 4칸을 방향설정하다보니 틀어진듯

def move(num):
    # current x, y, d, s, g
    cx, cy, cd, cs, cg = players[num]
    is_player = False
    # 플레이어가 가진 방향으로 한 칸 이동
    nx = cx + dx[cd]
    ny = cy + dy[cd]
    # 격자를 벗어나면 정반대방향으로 돌린 후 한 칸 잉동
    if nx < 0 or nx >= N or ny < 0 or ny >= N:
        cd = (cd + 2) % 4
        nx = cx + dx[cd]
        ny = cy + dy[cd]
    # 이동된 좌표값으로 갱신
    cx, cy = nx, ny
    players[num][0], players[num][1], players[num][2] = nx, ny, cd

    # 자신을 제외하고 현재 위치에 다른 사람들이 있는지 파악
    for i in range(M):
        if i != num:
            # target x, y, d, s, g
            tx, ty = players[i][0], players[i][1]

            if cx == tx and cy == ty:
                is_player = True
                break

    # 플레이어가 있는 경우
    if is_player:
        fight(num)

    # 플레이어가 없는 경우
    else:
        get_guns(num)


def get_guns(num):
    # 플레이어를 번호를 파라미터로 받아서 각 x, y좌표와 총의 공격력을 가져온다
    x, y, g = players[num][0], players[num][1], players[num][4]

    if len(board[x][y]) > 0:
        max_gun = max(board[x][y]) # 현재 위치에서 가장 높은 공격력을 가진 총

        # 현재 플레이어가 가지고 있는 총 공격력값이 작다면 갱신시켜준다
        if g < max_gun:
            players[num][4] = max_gun # 플레이어가 가장 높은 공격력을 가진 총을 가져간다.
            board[x][y].remove(max_gun)  # 플레이어가 가져갔기에 없앤다.
            if g != 0:
                board[x][y].append(g) # 기존의 가지고 있던 총을 내려놓는다.


def fight(num):
    # 현재 좌표에 있는 player들과의 싸움 진행
    cx, cy, cd, cs, cg = players[num]
    current_total = cs + cg
    # 이긴 플레이어의 인덱스를 현재 플레이어로 놓고, 진 플레이어는 -1로 초기화
    win_index, lose_index = num, -1

    for i in range(M):
        tx, ty, td, ts, tg = players[i]
        if i != num and cx == tx and cy == ty:
            # target x, y, d, s, g
            target_total = ts + tg

            # 현재 플레이어의 총 합과 타겟 플레이어의 총합이 같을 때
            if current_total == target_total:
                if cs > ts:
                    # 현재 플레이어가 이김
                    total[num] += (current_total - target_total)
                    lose_index = i
                else:
                    # 타겟 플레이어가 이김
                    total[i] += (target_total - current_total)
                    win_index = i
                    lose_index = num
            # 현재 플레이어가 이긴 경우
            elif current_total > target_total:
                total[num] += (current_total - target_total)
                lose_index = i
            # 타겟 플레이어가 이긴 경우
            else:
                total[i] += (target_total - current_total)
                win_index = i
                lose_index = num
            break

    loser_process(lose_index)
    get_guns(win_index)


def loser_process(num):
    # 진 사람은 총을 내려 놓는다
    x, y, d, s, g = players[num]
    players[num][4] = 0

    if g != 0:
        board[x][y].append(g)

    for i in range(4):
        is_player = False
        nx = x + dx[d]
        ny = y + dy[d]

        # 격자를 벗어나면 정반대방향으로 돌린 후 한 칸 이동
        if nx < 0 or nx >= N or ny < 0 or ny >= N:
            d = (d + 1) % 4
            continue

        # 자신을 제외하고 현재 위치에 다른 사람들이 있는지 파악
        for t in range(M):
            tx, ty = players[t][0], players[t][1]
            if nx == tx and ny == ty:
                is_player = True
                break

        if not is_player:
            players[num] = [nx, ny, d, s, 0]
            break
        else:
            d = (d + 1) % 4
    get_guns(num)


N, M, K = map(int, input().split())
board = [[[] for _ in range(N)] for _ in range(N)]
gun_info = [list(map(int, input().split())) for _ in range(N)]
# 상우하좌
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
players = []
total = [0] * M
for i in range(N):
    for j in range(N):
        # 비어있는 표시는 0이 [0]이 아닌 []로 표시
        if gun_info[i][j] > 0:
            board[i][j].append(gun_info[i][j])

for _ in range(M):
    x, y, d, s = map(int, input().split())
    # x좌표, y좌표, 방향, 초기능력치, 총의 공격력
    players.append([x - 1, y - 1, d, s, 0])

for _ in range(K):
    # 첫 번째 플레이어부터 이동
    for i in range(M):
        move(i)
print(*total)
