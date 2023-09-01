# 2023-08-20(일)
# 풀이 시간 : 10:40 ~ 12:31
# 첫 제출 : 232ms / 메모리 36MB


def move_dust(x, y, d):
    global total

    # current 좌표
    cx = x + dust_a_list[d][0]
    cy = y + dust_a_list[d][1]
    curr = board[cx][cy] # 빗자루가 이동한 위치의 먼지
    board[cx][cy] = 0 # 모두 없어진다.
    total_dust = 0 # 각 방향마다 움직이는 비율들의 먼지 총합
    # 각 방향마다 사전형으로 좌표 : 비율 식으로 저장함
    # key : 좌표, value : 비율 / Ex. (-1, 0): 0.02
    for key, value in directions[d].items():
        dx, dy = key # current좌표에서의 각 비율에 대한 위치
        nx = cx + dx
        ny = cy + dy
        total_dust += int(curr * value) # a%에서 curr 먼지 총합 - total_dust식이므로 저장
        # 격자를 벗어났다면 움직이면서 격자를 벗어나느
        if nx < 0 or nx >= N or ny < 0 or ny >= N:
            total += int(curr * value)
            continue
        # 비율에 따라 기존 값과 더해준다
        board[nx][ny] = int(board[nx][ny] + curr * value)
    # a%에 대해 범위에 따라 안에 있으면 현재 값과 비율들을 더한 값을 빼준다
    nx = cx + dust_a_list[d][0]
    ny = cy + dust_a_list[d][1]
    if 0 <= nx < N and 0 <= ny < N:
        board[nx][ny] = board[nx][ny] + (curr - total_dust)
    else:
        total += (curr - total_dust)
    return cx, cy


N = int(input())
board = [list(map(int, input().split())) for _ in range(N)]
# 좌하우상 방향에 따른 먼지 이동 비율(a%는 따로)
directions = {
    0: {
        (0, -2): 0.05,
        (-1, -1): 0.1,
        (1, -1): 0.1,
        (-2, 0): 0.02,
        (-1, 0): 0.07,
        (1, 0): 0.07,
        (2, 0): 0.02,
        (-1, 1): 0.01,
        (1, 1): 0.01
    },
    1: {
        (2, 0): 0.05,
        (1, -1): 0.1,
        (1, 1): 0.1,
        (0, -2): 0.02,
        (0, -1): 0.07,
        (0, 1): 0.07,
        (0, 2): 0.02,
        (-1, -1): 0.01,
        (-1, 1): 0.01
    },
    2: {
        (0, 2): 0.05,
        (-1, 1): 0.1,
        (1, 1): 0.1,
        (-2, 0): 0.02,
        (-1, 0): 0.07,
        (1, 0): 0.07,
        (2, 0): 0.02,
        (-1, -1): 0.01,
        (1, -1): 0.01
    },
    3: {
        (-2, 0): 0.05,
        (-1, -1): 0.1,
        (-1, 1): 0.1,
        (0, -2): 0.02,
        (0, -1): 0.07,
        (0, 1): 0.07,
        (0, 2): 0.02,
        (1, -1): 0.01,
        (1, 1): 0.01
    }
}
# 좌하우상 a%
dust_a_list = {
    0: (0, -1),
    1: (1, 0),
    2: (0, 1),
    3: (-1, 0)
}
length = 1
total = 0 # 격자밖으로 나간 먼지들 총합
sx, sy = N // 2, N // 2 # 중앙 시작점이자 움직임때마다의 시작점
nd = 0 # 방향(다음 위치의 방향 등)
move_cnt = 0 # 각 길이마다 움직인 횟수 측정
cnt = 2 # 모든 길이는 마지막 길이를 제외하고 2번 진행한다
while length < N:
    # 각 길이만큼 같은 방향으로 움직인다.
    for _ in range(length):
        # 먼지의 이동을 진행하며 좌표 갱신
        sx, sy = move_dust(sx, sy, nd)

    move_cnt += 1 # length만큼 움직인 횟수
    nd = (nd + 1) % 4 # 해당 길이만큼 움직였으므로 방향 회전 진행
    # 길이만큼 움직인 횟수가 cnt라면 길이를 늘려서 움직인다.
    if move_cnt == cnt:
        length += 1
        move_cnt = 0
        # 이 때 격자의 좌측상단(도착점)으로 가기 위한 마지막 길이라면
        # length만큼 3번 움직여야 도착한다.
        if length == N - 1:
            cnt = 3
print(total)
