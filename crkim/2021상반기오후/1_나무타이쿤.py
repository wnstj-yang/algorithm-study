n, m = map(int, input().split())
graph = [list(map(int, input().split())) for _ in range(n)]
movelist = [tuple(map(int, input().split())) for _ in range(m)]
direction = [(0,0), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1), (1,0), (1,1)] #1부터 시작
nutrients = [(n-2, 0), (n-2, 1), (n-1, 0), (n-1, 1)] #초기 특수 영양제 위치

def grow(nutrients, move):
    growlist = [(-1,-1),(-1,1),(1,1),(1,-1)]  # 대각선

    for i in range(len(nutrients)):
        x, y = nutrients[i]
        nx, ny = (x + direction[move[0]][0] * move[1]) % n, (y + direction[move[0]][1] * move[1]) % n #위치 값 확인
        nutrients[i] = (nx,ny)

        # 성장
        graph[nx][ny] += 1

    # 성장 2 - 주변 개수 확인
    for (nx, ny) in nutrients:
        for grow in growlist:
            gx, gy = nx + grow[0], ny + grow[1]
            if 0 <= gx < n and 0 <= gy < n and graph[gx][gy] > 0:
                graph[nx][ny] += 1

    return nutrients

# 2 이상인 나무 자르기
def cut():
    newnutrients = []
    for x in range(n):
        for y in range(n):
            if (x,y) not in nutrients and graph[x][y]>1:
                graph[x][y] -= 2
                newnutrients.append((x,y))
    return newnutrients


#좌표 업데이트
for i in range(m):
    nutrients = grow(nutrients, movelist[i])
    nutrients = cut()

answer = 0
for x in range(n):
    for y in range(n):
        answer += graph[x][y]
print(answer)