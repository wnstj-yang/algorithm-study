# 코드트리 - 술래잡기 체스
# 소요시간 : 2시간 + 추가 30분(중간에 풀이 참고)
# 이번에도 문제의 이해와 그에 적절한 문법 사용이 부족 + 다양한 상황 해석 필요


# 1. 도둑 말들을 순서대로 이동한다
def move_theives(c_x, c_y, board_copy):
    target = 1  # 움직여야하는 순서
    # 4x4이기 때문에 1~16번까지만 이동한다
    while target <= 16:
        is_found = False  # 번호를 찾았는지 확인
        for x in range(4):
            for y in range(4):
                num, d = board_copy[x][y]
                if target == num:  # 순서에 맞는 도둑말일 때
                    is_found = True  # 찾았다는 flag 설정
                    for i in range(8):
                        nd = (d + i) % 8  # 8로 나눈 나머지를 방향 설정으로 지정
                        # 방향에 따른 다음 도둑말의 위치
                        nx = x + dx[nd]
                        ny = y + dy[nd]
                        # 격자를 벗어나거나 상어가 존재하는 경우에는 넘어간다
                        # 술래 말이 잡은 경우 0으로 설정하였지만, 0이 비어있는 경우도 될 수 있기에 좌표를 활용
                        if nx < 0 or nx >= 4 or ny < 0 or ny >= 4 or (nx == c_x and ny == c_y):
                            continue
                        # 움직일 수 있는 방향으로 초기화하고 각 도둑말들의 위치를 바꿔준다
                        board_copy[x][y][1] = nd
                        board_copy[x][y], board_copy[nx][ny] = board_copy[nx][ny], board_copy[x][y]
                        break
                # 숫자를 찾지 못한 경우에는 현재 위치에 그대로 있으며 찾은 경우 더 이상 순회하면 안된다.
                # 자리를 바꾸고 다시 순회했을 때 또 바꿀 수 있는 가능성이 존재하기 때문이다.
                if is_found:
                    break

            if is_found:
                break
        target += 1  # 순서 증가


# DFS 적용 (도둑말 이동 + 술래 말 잡기)
def dfs(x, y, result, board):
    global answer

    board_copy = [[item[:] for item in board[k]] for k in range(4)]  # 리스트 슬라이싱으로 복사
    result += board_copy[x][y][0]  # 술래말이 지나가면서 도둑 말을 잡고 난 이후의 스코어 증가
    answer = max(answer, result)  # 깊이 탐색을 하는 것이 도둑 말을 잡은 것이기에 최대 값을 지속 체크
    board_copy[x][y][0] = 0  # 술래말이 잡았음을 표현
    move_theives(x, y, board_copy)  # 도둑말 이동
    # 최대 4방향까지 이동하기 때문에 방향의 거리 상 1 ~ 5의 범위로 for문을 잡음
    for i in range(1, 5):
        # 상어의 위치 x, y
        num, d = board_copy[x][y]
        nx = x + dx[d] * i
        ny = y + dy[d] * i
        # 범위를 벗어나거나 도둑말이 없는 경우 다음 이동
        if nx < 0 or nx >= 4 or ny < 0 or ny >= 4 or board_copy[nx][ny][0] == 0:
            # return을 해서 시간이 소모됐는데 건너뛰는 경우도 존재하기 때문에 continue
            continue
        dfs(nx, ny, result, board_copy)  # 2가지 조건 진행


board = []
# 문제의 1 ~ 8 정수의 방향에 맞게 설정
dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, -1, -1, -1, 0, 1, 1, 1]
answer = 0
for _ in range(4):
    info = list(map(int, input().split()))
    state = []
    for i in range(0, len(info), 2):
        p, d = info[i], info[i + 1]
        state.append([p, d - 1])
    board.append(state)

dfs(0, 0, 0, board)
print(answer)
