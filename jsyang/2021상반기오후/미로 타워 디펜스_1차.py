# 2023-10-03(화)
# 14:20 ~ 16:04
# 157ms / 31MB
# 반복되는 부분이 있음에도 불구하고 일단 조건대로 풀고자함


# 1. 플레이어가 입력받은 방향과 공격 칸 수 만큼 공격
def attack(d, p):
    global total

    x, y = N // 2, N // 2
    for i in range(1, p + 1):
        nx = x + dx[d] * i
        ny = y + dy[d] * i
        if nx < 0 or nx >= N or ny < 0 or ny >= N:
            continue
        total += board[nx][ny] # 점수 추가
        board[nx][ny] = 0


# 2. 달팽이 방향으로 움직이면서 빈 공간 체크 후 채워나간다
def fill_monsters():
    x, y = N // 2, N // 2 # 시작 좌표(중간)
    length = 1 # 움직이려는 길이
    length_left = length # 길이의 카운팅
    cnt = 2 # 움직이려는 길이의 횟수
    monsters = [] # 몬스터들의 값
    d = 2  # 왼쪽방향
    while True:
        if x == 0 and y == 0:
            break
        nx = x + dx[d]
        ny = y + dy[d]
        # 달팽이방향으로 진행하면서 몬스터 값을 추가한다(순서대로 넣어짐)
        if board[nx][ny] > 0:
            monsters.append(board[nx][ny])
        x, y = nx, ny # 좌표 갱신
        length_left -= 1 # 움직임을 표시
        # 다 움직였다면 방향전환과 횟수를 줄인다.
        if length_left == 0:
            d = (d - 1) % 4
            cnt -= 1
            # 움직이려는 길이와 횟수를 다 지났다면
            if cnt == 0:
                length += 1 # 길이를 늘리고
                cnt = 2 # 횟수를 2로 초기화
                # 다만, N - 1의 길이를 가지면 3번 가야하므로 3으로 초기화
                if length == N - 1:
                    cnt = 3
            length_left = length # 움직이는 길이 갱신

    # ----다시 넣기----
    x, y = N // 2, N // 2
    length = 1
    length_left = length
    cnt = 2
    d = 2  # 왼쪽방향
    next_board = [[0] * N for _ in range(N)] # 새로운 격자판 초기화
    for i in range(len(monsters)):
        number = monsters[i]
        nx = x + dx[d]
        ny = y + dy[d]
        next_board[nx][ny] = number
        x, y = nx, ny
        length_left -= 1
        if length_left == 0:
            d = (d - 1) % 4
            cnt -= 1
            if cnt == 0:
                length += 1
                cnt = 2
                if length == N - 1:
                    cnt = 3
            length_left = length

    return next_board


def delete_monsters():
    global total

    x, y = N // 2, N // 2
    length = 1
    length_left = length
    cnt = 2
    d = 2  # 왼쪽방향
    num_cnt = 0
    coors = []
    number = -1
    flag = False
    while True:
        if x == 0 and y == 0:
            break
        nx = x + dx[d]
        ny = y + dy[d]
        # 같은 번호라면 개수를 증가한다.
        if board[nx][ny] == number:
            num_cnt += 1
            coors.append((nx, ny))
        else:
            # 4개 이상 같은 것이 있다면 개수와 숫자를 곱하여 점수로 넣고
            # 해당 좌표들을 0으로 초기화해준다.
            if num_cnt >= 4:
                total += (num_cnt * number)
                flag = True
                for i, j in coors:
                    board[i][j] = 0
            # 초기화 이후 number와 개수, 첫 좌표값을 초기화
            number = board[nx][ny]
            num_cnt = 1
            coors = [(nx, ny)]

        x, y = nx, ny
        length_left -= 1
        if length_left == 0:
            d = (d - 1) % 4
            cnt -= 1
            if cnt == 0:
                length += 1
                cnt = 2
                if length == N - 1:
                    cnt = 3
            length_left = length
    return flag


# 몬스터들의 새로운 짝을 만들어서 넣는다
def make_pairs():
    x, y = N // 2, N // 2
    length = 1
    length_left = length
    cnt = 2
    monsters = []
    d = 2  # 왼쪽방향
    while True:
        if x == 0 and y == 0:
            break
        nx = x + dx[d]
        ny = y + dy[d]
        if board[nx][ny] > 0:
            monsters.append(board[nx][ny])
        x, y = nx, ny
        length_left -= 1
        if length_left == 0:
            d = (d - 1) % 4
            cnt -= 1
            if cnt == 0:
                length += 1
                cnt = 2
                if length == N - 1:
                    cnt = 3
            length_left = length

    new_monsters = []
    if len(monsters) > 0:
        number = monsters[0]
        cnt = 1
        for i in range(1, len(monsters)):
            if monsters[i] == number:
                cnt += 1
            else:
                new_monsters.append(cnt) # 개수
                new_monsters.append(number) # 숫자
                number = monsters[i]
                cnt = 1
        # 마지막은 추가한다.
        new_monsters.append(cnt)
        new_monsters.append(number)

    x, y = N // 2, N // 2
    length = 1
    length_left = length
    cnt = 2
    d = 2  # 왼쪽방향
    for i in range(len(new_monsters)):
        # 범위를 벗어날 수 있으므로 좌표값으로 끝낸다.
        if x == 0 and y == 0:
            break
        nx = x + dx[d]
        ny = y + dy[d]
        board[nx][ny] = new_monsters[i]
        x, y = nx, ny
        length_left -= 1
        if length_left == 0:
            d = (d - 1) % 4
            cnt -= 1
            if cnt == 0:
                length += 1
                cnt = 2
                if length == N - 1:
                    cnt = 3
            length_left = length


N, M = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(N)]
# 우하좌상
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]
total = 0
for _ in range(M):
    d, p = map(int, input().split())
    attack(d, p)
    board = fill_monsters()
    while delete_monsters():
        board = fill_monsters()
    make_pairs()
print(total)

