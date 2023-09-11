# 2023-09-10(일) / 2023-09-11(월)
# 풀이 시간 : 10:40 ~ 12:50 / 17:55 ~ 18:45 / 19:20 ~ 20:05
# 풀이 시간2 : 21:35 ~ 23:00 - 풀이 참고 중
# 첫 제출 : ms / 메모리 MB
# 재풀이 예정

### 다 삭제하고 다시 풀 예정


# from collections import deque
# 
# 
# def move_team(team):
#     # moved_team = [item[:] for item in team]
#     # next_board까지해서 다시 해보기
#     x, y = team[0]
#     print(team)
# 
#     for k in range(4):
#         nx = x + dx[k]
#         ny = y + dy[k]
#         if nx < 0 or nx >= N or ny < 0 or ny >= N:
#             continue
# 
#         if board[nx][ny] == 4 or board[nx][ny] == 3:
#             board[nx][ny] = 1
#             team.insert(0, [nx, ny])
# 
#     tail_x, tail_y = team.pop()
#     for k in range(4):
#         nx = tail_x + dx[k]
#         ny = tail_y + dy[k]
#         if nx < 0 or nx >= N or ny < 0 or ny >= N:
#             continue
#         # 다음 위치가 2인 경우
#         if board[nx][ny] == 2:
#             # 현재 꼬리 값이 3이라면 빈 공간 처리를 해주고 꼬리를 변경해야한다
#             if board[tail_x][tail_y] == 3:
#                 board[tail_x][tail_y] = 4
#             # 다른 2개의 경우에서는 꼬리 변경해준다
#             board[nx][ny] = 3
# 
#     return team
# 
# 
# def throw_ball():
#     global result, rx, ry, d, rounds
# 
#     isFound = False
#     for k in range(N):
#         nx = rx + dx[d] * k
#         ny = ry + dy[d] * k
#         if 0 < board[nx][ny] < 4:
#             for i in range(len(teams)):
#                 team = teams[i]
#                 for t in range(len(team)):
#                     x, y = team[t]
#                     if x == nx and y == ny:
#                         num = 0
#                         if board[nx][ny] == 1:
#                             num = 1
#                         elif board[nx][ny] == 3:
#                             num = len(team[t])
#                         else:
#                             q = deque()
#                             q.append((x, y, 1))
#                             visited = [[False] * N for _ in range(N)]
#                             visited[x][y] = True
#                             while q:
#                                 qx, qy, cnt = q.popleft()
#                                 for j in range(4):
#                                     nqx = qx + dx[j]
#                                     nqy = qy + dy[j]
#                                     if nqx < 0 or nqx >= N or nqy < 0 or nqy >= N:
#                                         continue
#                                     if not visited[nqx][nqy] and 0 < board[nqx][nqy] < 3:
#                                         if board[nqx][nqy] == 1:
#                                             num = cnt + 1
#                                             break
#                                         visited[nqx][nqy] = True
#                                         q.append((nqx, nqy, cnt + 1))
# 
#                         result += ((num + 1) * (num + 1))
#                         isFound = True
#                         before_head_r, before_head_c = team[0]
#                         before_tail_r, before_tail_c = team[-1]
#                         teams[i] = team[::-1]
#                         board[before_head_r][before_head_c] = 3
#                         board[before_tail_r][before_tail_c] = 1
#                         break
# 
#                 if isFound:
#                     break
#         if isFound:
#             break
# 
#     tx = rx + rdx[d]
#     ty = ry + rdy[d]
#     if tx < 0 or tx >= N or ty < 0 or ty >= N:
#         d = (d + 1) % 4
#     else:
#         rx, ry = tx, ty
#     print(rx, ry, d)
#     # rounds += 1
#     # if rounds % N == 0:
#     #     d = (d + 1) % 4
#     #     if rx == N:
#     #         rx = N - 1
#     #     if ry == N:
#     #         ry = N - 1
# 
# 
# N, M, K = map(int, input().split())
# board = [list(map(int, input().split())) for _ in range(N)]
# # 우상좌하
# dx = [0, -1, 0, 1]
# dy = [1, 0, -1, 0]
# # 하우상좌
# rdx = [1, 0, -1, 0]
# rdy = [0, 1, 0, -1]
# result = 0 # 총합
# rounds = 0 # 라운드 수
# rx, ry = 0, 0 # 라운드 수에 따른 공이 시작하는 위치
# d = 0 # 방향
# teams = []
# visited = [[False] * N for _ in range(N)]
# for i in range(N):
#     for j in range(N):
#         if not visited[i][j] and board[i][j] == 1:
#             visited[i][j] = True
#             team = [[i, j]]
#             q = deque()
#             q.append((i, j))
#             tail_x, tail_y = -1, -1
#             while q:
#                 x, y = q.popleft()
#                 for k in range(4):
#                     nx = x + dx[k]
#                     ny = y + dy[k]
#                     if nx < 0 or nx >= N or ny < 0 or ny >= N:
#                         continue
# 
#                     if not visited[nx][ny]:
#                         if 0 < board[nx][ny] < 3:
#                             team.append([nx, ny])
#                             q.append((nx, ny))
#                             # visited[nx][ny] = True
#                         elif board[nx][ny] == 3:
#                             tail_x, tail_y = nx, ny
#                         visited[nx][ny] = True
#             team.append([tail_x, tail_y])
# 
#             # team의 첫번째는 방향.
#             teams.append(team)
# 
# for r in range(K):
#     next_teams = []
#     for team in teams:
#         coors = team
# 
#         next_team = move_team(coors)
# 
#         next_teams.append(next_team)
# 
#     teams = next_teams
#     throw_ball()
# 
# print(result)