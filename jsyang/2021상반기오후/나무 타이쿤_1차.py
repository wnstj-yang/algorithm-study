# 2023-09-20(수)
# 풀이 시간 : 21:15 ~ 22:10
# 첫 제출 165ms / 30MB


# 영양제를 움직여준다
def move_nutrients(d, p):
    # 움직여줄 때 기존의 것은 따로 좌표값을 잡는 것보다 리스트를 초기화해서 집어넣는다.
    moved_nutrients = [[False] * N for _ in range(N)]
    for x in range(N):
        for y in range(N):
            # 존재하는 경우 움직여줌
            if nutrients[x][y]:
                # 격자들이 연결되어있기 때문에 나머지 연산으로 처리
                nx = (x + dx[d] * p) % N
                ny = (y + dy[d] * p) % N
                # 새로 움직인 곳에 영양제를 뿌린다.
                moved_nutrients[nx][ny] = True
                board[nx][ny] += 1 # 이후 리브로수를 1만큼 성장시킨다.
    return moved_nutrients


def grow_height():
    grow_list = [] # 한 번에 리브로수들의 높이를 증가시킨다.
    for x in range(N):
        for y in range(N):
            if nutrients[x][y]:
                cnt = 0
                # 1, 3, 5, 7 => 대각선인 경우
                for k in [1, 3, 5, 7]:
                    nx = x + dx[k]
                    ny = y + dy[k]
                    if nx < 0 or nx >= N or ny < 0 or ny >= N:
                        continue
                    # 현재 x, y 위치에서 대각선으로 리브로수가 존재한다면 개수 증가
                    if board[nx][ny] > 0:
                        cnt += 1
                if cnt > 0:
                    grow_list.append((x, y, cnt))
    for x, y, cnt in grow_list:
        board[x][y] += cnt


def put_nutrients():
    for x in range(N):
        for y in range(N):
            # 영양제가 없고 리브로수 높이가 2 이상인 경우 영양제를 놓고 리브로수 2만큼 잘라낸다.
            if not nutrients[x][y] and board[x][y] >= 2:
                nutrients[x][y] = True
                board[x][y] -= 2
            # 영양제가 있는경우 제외시킨다.
            else:
                nutrients[x][y] = False


N, M = map(int, input().split())
# 문제의 조건에 맞게 8방향 설정
dx = [0, -1, -1, -1, 0, 1, 1, 1]
dy = [1, 1, 0, -1, -1, -1, 0, 1]
board = [list(map(int, input().split())) for _ in range(N)]
nutrients = [[False] * N for _ in range(N)]
total = 0
# 초기 - 좌하단 4칸에 영양제 놓음
for i in range(N - 2, N, 1):
    for j in range(2):
        nutrients[i][j] = True

for _ in range(M):
    d, p = map(int, input().split())
    d -= 1 # 방향 인덱스가 0부터시작하므로 1을 줄인다.
    nutrients = move_nutrients(d, p)
    grow_height()
    put_nutrients()


for i in range(N):
    for j in range(N):
        total += board[i][j]
print(total)

