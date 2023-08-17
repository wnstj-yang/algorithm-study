# 코드트리 - 2차원 테트리스 2차
# 풀이 시간 : 약 1시간 40분
# 좋은 점 : 확실히 1주 간 간격을 두니 어렴 풋이 기억나도 처음 부터 다시 짜야되므로 새로움
# 아쉬운 점 : 1주가 지나도 아직 풀이가 남아있긴 함. 다시 남아있긴 해도 그땐 넘어간 이유를 다시 알 수 있음
# 다른 방식을 적용해서 n차 시도 하는 것이 좋을 것 같다.


def move_red(t, x):
    y = 1 # 블록이 다 차있을 수 있는 상황 고려해서 인덱스상 감안하여 2번쨰부터
    # 각 1, 2type일 때를 묶고 3 type은 따로 묶는다 (범위에 따라)
    if t == 1 or t == 2:
        while True:
            # 격자를 벗어나거나 블록이 있는 경우
            if y + 1 > 5 or red[x][y + 1]:
                # 현재 위치에 블록 생성
                red[x][y] = 1
                if t == 2:
                    # type이 2라면 옆에도 놓음
                    red[x][y - 1] = 1
                break
            y += 1
    else:
        while True:
            # 다음 위치의 블록들을 살펴봤을 때 블록이 존재하거나 격자를 벗어나면
            if y + 1 > 5 or red[x][y + 1] or red[x + 1][y + 1]:
                red[x][y], red[x + 1][y] = 1, 1 # type 3에 맞는 블록을 생성
                break
            y += 1


def move_yellow(t, y):
    x = 1
    if t == 1 or t == 3:
        while True:
            if x + 1 > 5 or yellow[x + 1][y]:
                yellow[x][y] = 1
                if t == 3:
                    yellow[x - 1][y] = 1
                break
            x += 1
    else:
        while True:
            if x + 1 > 5 or yellow[x + 1][y] or yellow[x + 1][y + 1]:
                yellow[x][y], yellow[x][y + 1] = 1, 1
                break
            x += 1


def search_red():
    global ans
    # 인덱스가 2 부터 끝까지 진행해서 빨간색이면 열로 1줄이 만들어지는 지 판단
    for y in range(2, 6):
        cnt = 0
        for x in range(4):
            if red[x][y]:
                cnt += 1
            else:
                break
        # 한 개의 열 즉, 테트리스가 완성되면 블록들을 옮겨준다
        if cnt == 4:
            remove_red(y)
            ans += 1

    # 이후 연한 부분에 있어서 블록들이 존재한다면 한 칸씩 밀어준다
    for y in range(2):
        for x in range(4):
            if red[x][y]:
                remove_red(5)


def search_yellow():
    global ans

    for x in range(2, 6):
        cnt = 0
        for y in range(4):
            if yellow[x][y]:
                cnt += 1
            else:
                break

        if cnt == 4:
            remove_yellow(x)
            ans += 1
    for x in range(2):
        for y in range(4):
            if yellow[x][y]:
                remove_yellow(5)


def remove_red(idx):
    # 매개변수로 받은 idx에서부터 상위에 있는 블록들을 끌어온다
    for y in range(idx, 0, -1):
        for x in range(4):
            red[x][y] = red[x][y - 1]
    # 0번째는 0으로 모두 초기화해준다. 이미 1번째로 옮겨줬기 때문
    for x in range(4):
        red[x][0] = 0


def remove_yellow(idx):
    for x in range(idx, 0, -1):
        for y in range(4):
            yellow[x][y] = yellow[x - 1][y]

    for y in range(4):
        yellow[0][y] = 0


K = int(input())
red = [[0] * 6 for _ in range(4)]
yellow = [[0] * 4 for _ in range(6)]
ans = 0
result = 0

for _ in range(K):
    t, x, y = map(int, input().split())
    # 1. 블록 이동
    # 2. 각 행,열 지우고 한칸 씩 블록 이동 + 연한 부분 이동
    move_red(t, x)
    move_yellow(t, y)
    search_red()
    search_yellow()


for i in range(4):
    for j in range(6):
        if red[i][j]:
            result += 1

for i in range(6):
    for j in range(4):
        if yellow[i][j]:
            result += 1
print(ans)
print(result)
