# 2023-09-18(월)
# 풀이 시간 : 20:30 ~ 23:00 (풀이 좀 참고)
# 아예 좀 더 늦게 풀어야될 것 같다...집중이 안되고 풀이참고경향이 강했음 멘탈깨졌던 문제라그런지
# 하... for문에 쓰는 변수값으로 초기화하는 실수 발생!!!


from collections import deque


# 팀의 이동
def move(index):
    team = teams[index]
    hx, hy = team[0] # 머리의 좌표
    for i in range(4):
        nx = hx + dx[i]
        ny = hy + dy[i]
        if nx < 0 or nx >= N or ny < 0 or ny >= N:
            continue
        # 머리가 이동하는 곳에 꼬리이거나 비어있는 곳이여야한다.
        # 꼬리인 경우는 이동경로에 모두 꽉찬 경우이다.
        if board[nx][ny] == 3 or board[nx][ny] == 4:
            board[nx][ny] = 1 # 격자판의 머리
            teams[index].insert(0, [nx, ny]) # 새로운 머리를 추가해준다
            break

    tx, ty = team[-1] # 현재까지는 꼬리임
    for i in range(4):
        nx = tx + dx[i]
        ny = ty + dy[i]
        if nx < 0 or nx >= N or ny < 0 or ny >= N:
            continue
        # 꼬리의 이동은 나머지 사람으로 이동
        if board[nx][ny] == 2:
            # 머리 이동 이후의 꼬리값이 그대로라면
            if board[tx][ty] == 3:
                # 꼬리 위치의 값을 빈 값으로 처리해준다
                board[tx][ty] = 4
            # 그렇지 않다면 꼬리의 이동위치에 꼬리를 놓는다.
            board[nx][ny] = 3
            break

    # 머리는 옮겨서 새로운 좌표를 넣어주고, 꼬리는 변경이 되었기 때문에 마지막이 이제 꼬리가 아니다
    # 그래서 꼬리는 빼야한다.
    teams[index].pop()
    board[hx][hy] = 2


def throw_ball():
    global bx, by, bd, total

    fx, fy = -1, -1 # 찾은 좌표 값
    is_found = False
    for i in range(N):
        # 현재 위치에서 N 길이만큼 공을 같은 방향으로 던진다.
        nx = bx + dx[bd] * i
        ny = by + dy[bd] * i
        if nx < 0 or nx >= N or ny < 0 or ny >= N:
            continue

        # 공을 던져서 사람이 맞았다면 찾았다는 좌표 갱신
        if 0 < board[nx][ny] < 4:
            fx, fy = nx, ny
            is_found = True
            break
    # bd가 공을 던지는 회전을 의미한다면 아래의 변수 d는 공의 위치의 이동을 의미한다.
    d = (bd - 1) % 4
    # 가지고 있는 방향으로 1칸 이동
    nx = bx + dx[d]
    ny = by + dy[d]
    # 범위를 벗어나면 방향만 전환,
    if nx < 0 or nx >= N or ny < 0 or ny >= N:
        bd = (bd + 1) % 4
    else:
        bx, by = nx, ny

    # 공으로 맞춘 경우
    if is_found:
        # 몇 번째인지 파악을 하여 제곱으로 점수를 더한다.
        result = calculate(fx, fy)
        total += (result * result)
        # 이후 맞은 사람이 있는 팀을 찾아서 머리와 꼬리를 바꿔준다
        for i in range(len(teams)):
            if [fx, fy] in teams[i]:
                hx, hy = teams[i][0]
                tx, ty = teams[i][-1]
                temp = teams[i]
                teams[i] = temp[::-1]
                board[hx][hy] = 3
                board[tx][ty] = 1
                break


# 몇번째인지 파악해준다
def calculate(x, y):
    # 머리와 꼬리인 경우 각각 1번째, 팀의 길이를 반환해준다
    if board[x][y] == 1:
        return 1
    elif board[x][y] == 3:
        for i in range(len(teams)):
            if [x, y] in teams[i]:
                return len(teams[i])
    q = deque()
    q.append((x, y, 1))
    visited = [[False] * N for _ in range(N)]
    visited[x][y] = True
    while q:
        x, y, cnt = q.popleft()
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if nx < 0 or nx >= N or ny < 0 or ny >= N:
                continue
            # 머리 혹은 몸통인 부분들을 찾아나가면서 갯수를 증가해준다. 즉 몇 번째 찾는 과정
            if not visited[nx][ny] and 0 < board[nx][ny] < 3:
                q.append((nx, ny, cnt + 1))
                visited[nx][ny] = True

                if board[nx][ny] == 1:
                    return cnt + 1


N, M, K = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(N)]
teams = []
visited = [[False] * N for _ in range(N)]
# 우상좌하
dx = [0, -1, 0, 1]
dy = [1, 0, -1, 0]
bd = 0 # 현재 공의 방향
bx, by = 0, 0 # 공의 좌표
total = 0
for x in range(N):
    for y in range(N):
        if board[x][y] == 1:
            team = [[x, y]]
            q = deque()
            q.append((x, y))
            visited[x][y] = True
            tail_x, tail_y = -1, -1 # 꼬리는 따로 진행
            while q:
                i, j = q.popleft()
                for k in range(4):
                    nx = i + dx[k]
                    ny = j + dy[k]
                    if nx < 0 or nx >= N or ny < 0 or ny >= N:
                        continue
                    if not visited[nx][ny]:
                        if 0 < board[nx][ny] < 3:
                            team.append([nx, ny])
                            visited[nx][ny] = True
                            q.append((nx, ny))
                        # 꼬리에 왔으면 갱신해주고, 방문, 큐에 넣는 처리를 하지 않는다.
                        # 애초에 이동 끝이 이어져있기 때문에 꼬리에 오면 과정이 끝난다고 보면 된다.
                        elif board[nx][ny] == 3:
                            tail_x, tail_y = nx, ny
            # 마지막에 방문 처리
            visited[tail_x][tail_y] = True
            team.append([tail_x, tail_y]) # 마지막에 꼬리 추가
            teams.append(team)

for _ in range(K):
    for i in range(len(teams)):
        move(i)
    throw_ball()

print(total)
