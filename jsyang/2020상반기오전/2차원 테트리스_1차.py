# 코드트리 - 2차원 테트리스 1차
# 풀이 시간 : 2시간 + 다음날 1시간30분정도 = 약 3시간 30분. But... 풀이 참고
# 시간 낭비 이유 1. for문 순회 시 return 위치 파악 X 2. 문제 제대로 이해 X(연한 부분을 별개로 봄)


# 행 고정
def red_move(t, x):
    y = 1
    # type에서 범위체크 시 1과 2 그리고 3으로 묶는다
    if t == 1 or t == 2:
        while True:
            # 다음 위치가 인덱스 범위를 벗어나거나 블록이 있는 경우
            if y + 1 > 5 or red[x][y + 1]:
                red[x][y] = 1 # 현재에다 블록 추가
                # t가 2라면 옆에 블록도 추가해준다
                if t == 2:
                    red[x][y - 1] = 1
                break
            y += 1 # 열 증가
    else:
        # 애초에 파란색 범위에 맞게 type에 따라 주어지므로 x범위체크는 필요 없다.
        while True:
            # 다음 위치가 인덱스 범위를 벗어나거나 t가 3인 경우이기에 다음 위치 혹은 그 아래가 블록이 있는 경우
            if y + 1 > 5 or red[x][y + 1] or red[x + 1][y + 1]:
                # 현재까지 온 위치에서 블록들을 추가해준다
                red[x][y], red[x + 1][y] = 1, 1
                break
            y += 1


# 열 고정
def yellow_move(t, y):
    x = 1
    # type에서 범위체크 시 1과 3 그리고 2로 묶는다
    if t == 1 or t == 3:
        while True:
            # 다음 위치가 인덱스 범위를 벗어나거나 블록이 있는 경우
            if x + 1 > 5 or yellow[x + 1][y]:
                yellow[x][y] = 1
                # t가 3이라면 밑에 블록도 추가해준다
                if t == 3:
                    yellow[x - 1][y] = 1
                break
            x += 1
    else:
        while True:
            # 다음 위치가 인덱스 범위를 벗어나거나 t가 2인 경우이기에 다음 위치 혹은 그 옆에 블록이 있는 경우
            if x + 1 > 5 or yellow[x + 1][y] or yellow[x + 1][y + 1]:
                yellow[x][y], yellow[x][y + 1] = 1, 1
                break
            x += 1


# 빨간색 블록은 열이 만들어지는지 확인하고 이후에는 연한 부분에서 블록이 있는지 체크한다
def search_red():
    global ans

    for j in range(2, 6):
        cnt = 0
        for i in range(4):
            if red[i][j] == 1:
                cnt += 1
        if cnt == 4:
            remove_red(j)
            ans += 1

    for j in range(2):
        for i in range(4):
            if red[i][j] == 1:
                remove_red(5)
                break


# 노란색 블록은 행이 만들어지는지 확인하고 이후에는 연한 부분에서 블록이 있는지 체크한다
def search_yellow():
    global ans
    for i in range(2, 6):
        cnt = 0
        for j in range(4):
            if yellow[i][j] == 1:
                cnt += 1
        if cnt == 4:
            remove_yellow(i)
            ans += 1

    for i in range(2):
        for j in range(4):
            if yellow[i][j] == 1:
                remove_yellow(5)
                break


# 빨간색 박스에서의 한 칸씩 이동
def remove_red(idx):
    # 한 줄의 열이 만들어졌기 때문에 해당 열의 위치부터 위에 있는 것들을 한 칸씩 이동한다.
    for j in range(idx, 0, -1):
        for i in range(4):
            red[i][j] = red[i][j - 1]
    # 마지막으로 첫 번째(인덱스가 0인)열의 값들을 0으로 초기화(옮겼기 때문)
    for i in range(4):
        red[i][0] = 0


# 노란색 박스에서의 한 칸씩 이동
def remove_yellow(idx):
    # 한 줄의 열이 만들어졌기 때문에 해당 열의 위치부터 위에 있는 것들을 한 칸씩 이동한다.
    for i in range(idx, 0, -1):
        for j in range(4):
            yellow[i][j] = yellow[i - 1][j]
    # 마지막으로 첫 번째(인덱스가 0인)행의 값들을 0으로 초기화(옮겼기 때문)
    for j in range(4):
        yellow[0][j] = 0


K = int(input()) # 블록을 입력한 횟수
red = [[0] * 6 for _ in range(4)] # 빨간색 파트
yellow = [[0] * 4 for _ in range(6)] # 노란색 파트
ans = 0 # 빨간색이랑 노란색 테트리스 떄 행 혹은 열로 지워진 횟수
result = 0 # 테트리스 완료된 이후 타일의 개수
for _ in range(K):
    t, x, y = map(int, input().split())
    # 1. red, yellow 모두 입력받은 x, y바탕으로 블록의 위치를 구한다
    red_move(t, x)
    yellow_move(t, y)
    # 2. red, yellow에 각각 열과 행이 1자로 만들어지는지를 체크하고 연한 부분에서의 블록이 있는지 등 테트리스처럼 이동한다.
    search_red()
    search_yellow()

# 모두 이동한 이후 빨간색 테트리스에 남아있는 블록 수
for i in range(4):
    for j in range(2, 6):
        if red[i][j] == 1:
            result += 1

# 모두 이동한 이후 노란색 테트리스에 남아있는 블록 수
for i in range(2, 6):
    for j in range(4):
        if yellow[i][j] == 1:
            result += 1

print(ans) # 테트리스를 진행하며 터진 개수
print(result) # 총 남아있는 블록 수
