# 2023-08-13(일) / 10:50 ~ 12:50
# 풀이 시간 :  1시간 40분 / 2시간(소요시간/기준)
# 첫 제출 : 929ms / 메모리 46MB => 다른 사람들에 비해 느림. 최적화 필요


# 1. 플레이어들의 이동
def move_players():
    # 현재 플레이어 수(정보 포함), 움직이는 turns 상태를 지속 업데이트로 전역 변수로 선언
    global players, players_turns

    next_turns = [[item[:] for item in players_turns[k]] for k in range(N)] # 다음 턴들을 초기화하기 위해 리스트 슬라이싱 복사
    next_players = [] # 턴을 진행하면서 플레이어 수들을 초기화
    berfore_take = {} # 점유를 하기 전
    for p, x, y, d in players:
        '''
        남아있는 현재 각 플레이어들의 정보 
        p : player 번호
        x, y : player 좌표
        d : 방향
        '''
        taken = False # 점유 할 수 있는지 확인하는 flag
        for i in pritority_directions[p][d]:
            dx, dy = directions[i] # 우선순위에 따른 이동 정보
            # 이동했을 때의 좌표
            nx = x + dx
            ny = y + dy
            # 격자판 범위를 벗어나는지 체크
            if nx < 0 or nx >= N or ny < 0 or ny >= N:
                continue

            # 빈 공간인 경우 우선순위에 따라 움직였으므로 점유 가능성 체크
            if len(next_turns[nx][ny]) == 0:
                taken = True
                # 현재 위치에 다른 player들도 점유할 수 있기 때문에 임시로 정보 저장 / p : player번호, i : 방향
                if (nx, ny) not in berfore_take:
                    berfore_take[(nx, ny)] = [(p, i)]
                else:
                    berfore_take[(nx, ny)].append((p, i))
                break

        # 점유하지 못했다면 근처에 자신이 점유한 곳으로 이동
        if not taken:
            for i in pritority_directions[p][d]:
                dx, dy = directions[i]
                nx = x + dx
                ny = y + dy
                if nx < 0 or nx >= N or ny < 0 or ny >= N:
                    continue
                # 기존에 자신의 점유한 공간으로 이동(우선순위에 따라 이동하므로 따로 check불필요)
                if next_turns[nx][ny][0] == p:
                    if (nx, ny) not in berfore_take:
                        berfore_take[(nx, ny)] = [(p, i)]
                    else:
                        berfore_take[(nx, ny)].append((p, i))
                    break

    # 모두 이동한 다음 점유하기 전의 정보들을 바탕으로 실제로 움직이기 시작
    for key, value in berfore_take.items():
        x, y = key # x, y 좌표
        p, i = value[0] # player 번호, 방향
        # 길이가 1보다 큰 경우에는 같은 좌표에 여러명이 존재하기 때문에 정렬시켜서 가장 작은 번호만 살린다
        if len(value) > 1:
            value.sort()
            p, i = value[0]

        next_players.append([p, x, y, i])
        next_turns[x][y] = [p, K]
    # 복사했던 turn정보들, 다음 턴을 진행할 플레이어들의 정보들을 갱신 시킨다
    players = next_players
    players_turns = next_turns


# 2. turn 수들을 지워준다
def delete_turns():
    for i in range(N):
        for j in range(N):
            # 턴 수들의 정보에서 길이가 0이 아닌 경우 점유상태임을 표현
            if len(players_turns[i][j]) != 0:
                is_in = False
                # 각 플레이어들의 좌표와 현재 순회하고있는 점유 상태의 좌표가 같은 경우
                # 처음으로 이동한 플레이어들의 턴수를 줄이지 않으므로 내비둔다
                for p, x, y, d in players:
                    if i == x and j == y:
                        is_in = True
                        break
                # 반면 이미 점유한 상태의 경우 턴수를 하나씩 줄이고 0이 된다면 빈 칸으로 만든다
                if not is_in:
                    players_turns[i][j][1] -= 1
                    if players_turns[i][j][1] == 0:
                        players_turns[i][j] = []


# 상하좌우
directions = {
    1: [-1, 0],
    2: [1, 0],
    3: [0, -1],
    4: [0, 1]
}


N, M, K = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(N)] # 격자판
players_turns = [[[] for _ in range(N)] for _ in range(N)] # 추후 넣을 player들의 turn 수 상태
players = [] # 플레이어들의 정보
pritority_directions = {} # 각 플레이어마다 진행하는 방향에 따른 우선순위 방향들 저장
answer = 1 # 턴의 수
first_directions = list(map(int, input().split())) # 첫 방향
for i in range(N):
    for j in range(N):
        # 격자판에 플레이어가 존재하는 경우
        # players : [플레이어 번호, x좌표, y좌표, 방향]
        if board[i][j] != 0:
            player = board[i][j]
            players.append([player, i, j, first_directions[player - 1]])
            pritority_directions[player] = {}
            players_turns[i][j] = [player, K] # 초기 플레이어들의 턴 수


# 각 플레이어들의 방향에 따른 우선순위들을 저장해준다
for i in range(1, M + 1):
    for j in range(1, 5):
        pritority_directions[i][j] = list(map(int, input().split()))


while answer <= 1000:
    move_players()
    delete_turns()
    # 1개 남았을 떄 이게 1번이라면 끝
    if len(players) == 1 and players[0][0] == 1:
        break
    answer += 1

# 1000보다 큰 경우 -1 반환
if answer == 1001:
    print(-1)
else:
    print(answer)
