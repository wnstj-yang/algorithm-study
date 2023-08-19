# 풀이시간 : 3시간 30분
# 최단거리 이후 정리하는 과정 풀이참고

from collections import deque

n, m, battery = tuple(map(int, input().split()))

board = [[0 for _ in range(n + 1)] for _ in range(n + 1)]
person = list()
m_person = [ False for _ in range(n * n)]
car_pos = (-1, -1)
queue = deque()
step = [[0 for _ in range(n + 1)] for _ in range(n + 1)]
visited = [[False for _ in range(n + 1)] for _ in range(n + 1)]
     
def bfs(start_pos):
    for i in range(1, n + 1):
        for j in range(n + 1):
            visited[i][j] = False
    
    # 시작 위치
    start_x, start_y = start_pos
    
    visited[start_x][start_y] = True
    step[start_x][start_y] = 0
    queue.append((start_x, start_y))
    
    dxs, dys = [0, 1, 0, -1], [1, 0, -1, 0]

    # BFS
    while queue:
        curr_x, curr_y = queue.popleft()
        
        for dx, dy in zip(dxs, dys):
            x, y = curr_x + dx, curr_y + dy
            
            if (1 <= x and x <= n and 1 <= y and y <= n) and not visited[x][y] and not board[x][y]:
                queue.append((x, y))
                step[x][y] = step[curr_x][curr_y] + 1
                visited[x][y] = True


# 새로운 위치
def position(b_pos, n_pos):
    if b_pos == (-1, -1):
        return True

    best_x, best_y = b_pos
    new_x, new_y = n_pos
    return (step[best_x][best_y], best_x, best_y) > (step[new_x][new_y], new_x, new_y)


# 우선순위 이동
def move():
    global car_pos, battery
    
    #최단거리
    bfs(car_pos)
    
    # 우선순위 높은 승객 위치
    b_pos, best_index = (-1, -1), -1
    for i, (start_x, start_y, end_x, end_y) in enumerate(person):
        # 처음 태우는 승객, 기름 있는 거리
        if m_person[i] or not visited[start_x][start_y] or step[start_x][start_y] > battery: 
            continue
        if position(b_pos, (start_x, start_y)):
            b_pos, best_index = (start_x, start_y), i

    if b_pos == (-1, -1):
        return False
    
    # 이동
    start_x, start_y, end_x, end_y = person[best_index]
    car_pos = (start_x, start_y)
    battery -= step[start_x][start_y]
    
    # 해당 승객 최단거리
    bfs((start_x, start_y))
    
    # 도착 가능한 체크
    if not visited[end_x][end_y] or step[end_x][end_y] > battery:
        return False
    
    # 이동
    car_pos = (end_x, end_y)
    battery -= step[end_x][end_y]
    
    # 배터리 충전
    m_person[best_index] = True
    battery += step[end_x][end_y] * 2
    
    return True


for i in range(1, n + 1):
    given_row = list(map(int, input().split()))
    for j, elem in enumerate(given_row, start=1):
        board[i][j] = elem

car_pos = tuple(map(int, input().split()))

person = [
    tuple(map(int, input().split()))
    for _ in range(m)
]

for _ in range(m):
    is_moved = move()
    if not is_moved:
        print(-1)
        exit(0)
print(battery)