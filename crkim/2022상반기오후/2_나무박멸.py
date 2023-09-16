# 피지컬 문제로 구현하다가 막히는 부분이 많아서 결국 해설 참고... -> 구현해야 하는 부분과 고려해야하는 부분이 많을 수록 놓치는 부분이 많음
# 제초제 뿌리는 과정은 max값 갱신을 차근차근 구현하면 되는데, 엄한 부분만 생각했음
# simulation 문제 해결과정에서 입력받은 배열 안에서 모든 걸 해결해야 한다고 생각하는 순간 꼬이는 것 같음
# 정보 업데이트를 위한 새로운 배열들을 많이 만들어보는 연습을 할 것

n, m, k, c = map(int, input().split())
tree = [[0] * (n + 1)]
for _ in range(n):
    tree.append([0] + list(map(int, input().split())))

add_tree = [[0] * (n + 1) for _ in range(n + 1)]
herb = [[0] * (n + 1) for _ in range(n + 1)]
ans = 0


# 나무 성장
def grow():
    dxy = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if tree[i][j] <= 0:
                continue
            cnt = 0
            for dx, dy in dxy:
                nx, ny = i + dx, j + dy
                if not (1 <= nx <= n and 1 <= ny <= n):
                    continue
                if tree[nx][ny] > 0:
                    cnt += 1  # 인접한 것 세기
            tree[i][j] += cnt


# 번식
def spread():
    dxy = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # 중복체크를 위해 배열 2개
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            add_tree[i][j] = 0  # 초기화

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if tree[i][j] <= 0:
                continue
            cnt = 0
            for dx, dy in dxy:
                nx, ny = i + dx, j + dy
                if not (1 <= nx <= n and 1 <= ny <= n):
                    continue
                if herb[nx][ny]:
                    continue
                if tree[nx][ny] == 0:
                    cnt += 1

            # 인접한 경우 인접 개수만큼 나눠서 더해줌
            for dx, dy in dxy:
                nx, ny = i + dx, j + dy
                if not (1 <= nx <= n and 1 <= ny <= n):
                    continue
                if herb[nx][ny]:
                    continue
                if tree[nx][ny] == 0:
                    add_tree[nx][ny] += tree[i][j] // cnt

    # 누적된 것 한 번에 업데이트
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            tree[i][j] += add_tree[i][j]


# 제초제 뿌리기
def spray():
    global ans

    dxy = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    max_del, max_x, max_y = 0, 1, 1
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if tree[i][j] <= 0:
                continue

            cnt = tree[i][j]
            for dx, dy in dxy:
                nx, ny = i, j
                for _ in range(k):
                    nx, ny = nx + dx, ny + dy
                    if not (1 <= nx <= n and 1 <= ny <= n):
                        break
                    if tree[nx][ny] <= 0:
                        break
                    cnt += tree[nx][ny]

            if max_del < cnt:  # 최댓값 갱신
                max_del = cnt
                max_x = i
                max_y = j

    ans += max_del
    # 맥스값 찾았을 때 제초제 뿌림
    if tree[max_x][max_y] > 0:
        tree[max_x][max_y] = 0
        herb[max_x][max_y] = c

        for dx, dy in dxy:
            nx, ny = max_x, max_y
            for _ in range(k):
                nx, ny = nx + dx, ny + dy
                if not (1 <= nx <= n and 1 <= ny <= n):
                    break
                if tree[nx][ny] < 0:
                    break
                if tree[nx][ny] == 0:
                    herb[nx][ny] = c
                    break

                tree[nx][ny] = 0
                herb[nx][ny] = c


# 제초제 유통기한 감소
def delete_herb():
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if herb[i][j] > 0:
                herb[i][j] -= 1


for _ in range(m):
    grow()
    spread()
    delete_herb()
    spray()

print(ans)