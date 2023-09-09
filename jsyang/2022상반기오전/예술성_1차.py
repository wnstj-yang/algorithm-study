# 2023-09-09(토)
# 풀이 시간 : 18:15 ~ 18:40 / 19:07 ~ 20:57
# 첫 제출 : 320ms / 메모리 37MB

from collections import deque


# 1. 그룹들 구하기
def make_groups():
    visited = [[False] * N for _ in range(N)]
    next_groups = []
    for i in range(N):
        for j in range(N):
            if not visited[i][j]:
                visited[i][j] = True
                num = board[i][j] # 현재 구하려는 그룹의 값
                q = deque()
                q.append((i, j))
                group = [(i, j)] # 현재 그룹에 넣을 좌표들
                while q:
                    x, y = q.popleft()
                    for k in range(4):
                        nx = x + dx[k]
                        ny = y + dy[k]
                        if nx < 0 or nx >= N or ny < 0 or ny >= N:
                            continue
                        # 4방향을 돌면서 방문하지 않고 같은 그룹에 포함되는 수인지 파악
                        if not visited[nx][ny] and board[nx][ny] == num:
                            group.append((nx, ny)) # 같은 그룹이므로 좌표 추가
                            q.append((nx, ny)) # 다음 좌표로 이동
                            visited[nx][ny] = True # 방문 표시
                next_groups.append(group) # 만들어진 그룹을 추가
    return next_groups


# 2. 값들을 계산할 때 DFS 적용
def calculate(idx, cnt):
    global result

    # 그룹의 쌍이므로 2개가 정해지면 값 계산을 진행한다
    if cnt == 2:
        first, second = groups[candi[0]], groups[candi[1]]
        number = board[first[0][0]][first[0][1]]
        target = board[second[0][0]][second[0][1]]
        length = get_border(target, first, second)
        # 조건에 맞게 계산
        total = (len(first) + len(second)) * number * target * length
        result += total
        return

    # 인덱스인 idx로 현재 그룹의 개수까지 순회하면서 그룹들의 쌍을 구한다.
    # 즉, 조합
    for i in range(idx, len(groups)):
        candi[cnt] = i
        calculate(i + 1, cnt + 1)


# 3. 경계선에 있는 개수를 구한다.
def get_border(target, group, target_group):
    cnt = 0 # 개수
    for x, y in group:
        for k in range(4):
            nx = x + dx[k]
            ny = y + dy[k]
            if nx < 0 or nx >= N or ny < 0 or ny >= N:
                continue
            # target값이 여러 그룹이 있을 수 있으므로 쌍으로 만든 그룹 안에 포함되어 있는지 좌표로 확인
            if board[nx][ny] == target and (nx, ny) in target_group:
                cnt += 1
    return cnt


def rotate_groups():
    next_board = [[0] * N for _ in range(N)]
    center = N // 2
    for idx in range(N):
        next_board[center][idx] = board[idx][center]
        next_board[N - 1 - idx][center] = board[center][idx]

    # 1. 왼쪽 위
    for i in range(center):
        for j in range(center):
            next_board[j][center - 1 - i] = board[i][j]

    # 2. 오른쪽 위
    for i in range(center):
        for j in range(center + 1, N):
            next_board[j - center - 1][N - 1 - i] = board[i][j]

    # 3. 왼쪽 아래
    for i in range(center + 1, N):
        for j in range(center):
            next_board[center + 1 + j][N - i - 1] = board[i][j]

    # 4. 오른쪽 아래
    idx = 0 # 따로 인덱싱을 통해 값을 회전할 때 사용
    for i in range(center + 1, N):
        for j in range(center + 1, N):
            next_board[j][N - 1 - idx] = board[i][j]
        idx += 1

    return next_board


# 상하좌우
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]
N = int(input())
board = [list(map(int, input().split())) for _ in range(N)]
groups = []
candi = [0] * 2 # 그룹들의 쌍을 구하려는 리스트
result = 0 # 총 합
for _ in range(4):
    groups = make_groups() # 그룹들 갱신
    calculate(0, 0)
    board = rotate_groups() # 격자판 갱신(회전이후)

print(result)
