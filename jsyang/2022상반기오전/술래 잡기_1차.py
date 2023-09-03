# 2023-09-03(일)
# 풀이 시간 : 10:50 ~ 13:03 / 19:05 ~ 19:30 - 2시간 38분
# 첫 제출 : 121ms / 메모리 35MB


def move_runners():
    new_runners = {} # 새로운 도망자 목록 갱신할 딕셔너리
    for key, val in runners.items():
        # key : 좌표 / val : 방향 리스트
        x, y = key
        if abs(cx - x) + abs(cy - y) <= 3:
            for d in val:
                nx = x + dx[d]
                ny = y + dy[d]
                # 범위를 벗어났다면 반대 처리 이후 1칸 움직임
                if nx < 0 or nx >= N or ny < 0 or ny >= N:
                    d = (d + 2) % 4
                    nx = x + dx[d]
                    ny = y + dy[d]

                # 움직이려는 곳에 술래가 존재하면 가만히 있어야한다
                # 방향이 바뀌었다면 바뀐상태로 현재 위치x, y와 함께 도망자 리스트에 추가
                if nx == cx and ny == cy:
                    if (x, y) not in new_runners:
                        new_runners[(x, y)] = [d]
                    else:
                        new_runners[(x, y)].append(d)
                    continue
                #
                if (nx, ny) not in new_runners:
                    new_runners[(nx, ny)] = [d]
                else:
                    new_runners[(nx, ny)].append(d)
        # 3이하에 속하지 않는다면 그대로 다시 넣어준다
        else:
            if (x, y) not in new_runners:
                new_runners[(x, y)] = val
            else:
                new_runners[(x, y)].extend(val)

    # 새로운 도망자 목록을 반환해주어 갱신
    return new_runners


def move_catcher(k):
    # cx, cy, cd : 술래 좌표 및 방향
    # move_cnt : 움직인 횟수 / length : 움직여야 하는 거리/ times : 횟수
    # flag : True - 정중앙 -> 도착점 / False - 도착점 -> 정중앙
    # result : 총합
    global cx, cy, cd, move_cnt, length, times, flag, result

    # 술래 좌표 한 칸 옮긴다.
    cx = cx + dx[cd]
    cy = cy + dy[cd]
    move_cnt += 1
    # 한 칸씩 움직이며 length만큼 움직였다면
    # length를 몇 번 돌았는지 times를 체크해준다
    if move_cnt == length:
        move_cnt = 0
        times += 1
        # 정중앙 -> 도착점 일 시
        if flag:
            cd = (cd + 1) % 4 # 방향을 + 1로 하면서 시계방향 달팽이 진행
            if length == N - 1: # 맨 마지막은 3번을 돌아야한다.
                # 도착하면 반시계 방향을 위해 flag 및 방향처리를 진행
                if times == 3:
                    times = 0
                    flag = False
                    cd = 3
            # 이외의 경우 length를 2번돌았을 경우 길이 증가
            else:
                if times == 2:
                    length += 1
                    times = 0
        # 도착점 -> 정중앙
        else:
            cd = (cd - 1) % 4 # 반대 방향이므로 -1씩 반시계방향
            # 반시계 방향에서 3번을 모두 돌았다면 길이를 줄이도록 한다.
            if length == N - 1:
                if times == 3:
                    times = 0
                    length -= 1
            else:
                if times == 2:
                    times = 0
                    # 길이가 1이고 times가 2이면 두 번 진행한 것이므로 정중앙에 도착한 것이다
                    # flag와 방향처리를 재설정하여 다시 정중앙 -> 도착점으로 가게 변경
                    if length == 1:
                        flag = True
                        cd = 1
                    else:
                        length -= 1

    # 이동 및 방향 전한이 이루어진 이후 도망자를 3칸 살펴본다
    runners_cnt = 0
    for i in range(3):
        # 현재 위치에서부터 3칸이므로 범위가 1 ~ 4 부터가 아니라 0 ~ 3이다.
        nx = cx + dx[cd] * i
        ny = cy + dy[cd] * i
        if nx < 0 or nx >= N or ny < 0 or ny >= N or board[nx][ny]:
            continue

        if (nx, ny) in runners:
            runners_cnt += len(runners[(nx, ny)])
            del runners[(nx, ny)]
    return k * runners_cnt


N, M, H, K = map(int, input().split())
# 좌상우하 - 술래 달팽이 방향 시 +1, 반대 -1
# 도망자 방향 + 2씩 나머지 연산 처리로 반대방향 처리 가능
dx = [0, -1, 0, 1]
dy = [-1, 0, 1, 0]
board = [[0] * N for _ in range(N)] # 격자판이나 나무 파악 용도로 활용
runners = {}
cx, cy = N // 2, N // 2
cd = 1 # 술래 첫 방향
move_cnt = 0 # 이동 칸 횟수
times = 0 # 길이만큼 몇 번 진행됐는지 파악하는 변수
length = 1 # 이동하려는 길이
flag = True # True : 정중앙 -> 도착점 / False : 도착점 -> 정중앙
result = 0 # 총합
for _ in range(M):
    x, y, d = map(int, input().split())
    # d가 1이면 좌우로만 움직이고 초기 값은 오른쪽으로 설정
    if d == 1:
        runners[(x - 1, y - 1)] = [2]
    # d가 2이면 상하로만 움직이고 초기 값은 아래로 설정
    else:
        runners[(x - 1, y - 1)] = [3]

# 나무 표시는 1
for _ in range(H):
    x, y = map(int, input().split())
    board[x - 1][y - 1] = 1

# K번 동안 진행
for k in range(1, K + 1):
    runners = move_runners()
    result += move_catcher(k)

print(result)
