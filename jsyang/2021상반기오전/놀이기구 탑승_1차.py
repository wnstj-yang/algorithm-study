# 2023-09-06(수)
# 풀이 시간 : 20:50 ~ 21:45
# 첫 제출 100ms / 33MB


# 인접한 곳들을 체크
def check(student, likes):
    candidates = [] # 자기가 좋아하는 학생, 비어있는 곳, 좌표 정보 저장
    for x in range(N):
        for y in range(N):
            # 비어 있는 곳이라면 인접한 곳을 탐색한다
            if board[x][y] == 0:
                like = 0 # 현재 학생이 좋아하는 학생 수
                empty = 0 # 비어 있는 곳을 카운트
                for k in range(4):
                    nx = x + dx[k]
                    ny = y + dy[k]
                    # 격자 판을 벗어난 경우 제외
                    if nx < 0 or nx >= N or ny < 0 or ny >= N:
                        continue
                    # 좋아하는 학생이 있다면 카운트
                    if board[nx][ny] in likes:
                        like += 1
                    # 비어 있는 곳이라면 해당 부분 카운트
                    elif board[nx][ny] == 0:
                        empty += 1
                # 구한 정보들을 현재 학생에 넣을 수 있는 후보로 저장한다.
                candidates.append((like, empty, x, y))
    if candidates:
        # 좋아하는 학생 수, 비어 있는 곳의 개수 순으로 내림차순 정렬을 진행한다.
        # 위의 부분이 문제의 1, 2 조건에 해당하며 3, 4번은 x, y(행열)을 오름차순으로 정렬
        candidates.sort(key=lambda x: (-x[0], -x[1], x[2], x[3]))
        # 정렬된 곳에서 모든 조건에 충족하는 부분이 첫 번째이므로 해당 좌표를 구한다.
        x, y = candidates[0][2], candidates[0][3]
        board[x][y] = student # 현재 위치에 학생 저장


# 문제에서 저장된 좋아하는 학생 수에 따른 점수 계산
def calculate():
    total = 0 # 총 합
    # 학생들이 모두 지정된 이후 점수 계산
    for x in range(N):
        for y in range(N):
            student = board[x][y]
            cnt = 0 # 좋아하는 학생 수
            for k in range(4):
                nx = x + dx[k]
                ny = y + dy[k]
                if nx < 0 or nx >= N or ny < 0 or ny >= N:
                    continue
                # 인접한 학생이 현재 학생이 좋아하는지 체크해서 명 수 카운팅
                if board[nx][ny] in students[student]:
                    cnt += 1
            # 좋아하는 명 수에 따른 점수 계산을 더해준다
            total += scores[cnt]
    return total


# 상하좌우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]
N = int(input())
board = [[0] * N for _ in range(N)]
students = {}
scores = {
    0: 0,
    1: 1,
    2: 10,
    3: 100,
    4: 1000,
}

for _ in range(N * N):
    n0, n1, n2, n3, n4 = map(int, input().split())
    students[n0] = [n1, n2, n3, n4]
    check(n0, [n1, n2, n3, n4])

print(calculate())
