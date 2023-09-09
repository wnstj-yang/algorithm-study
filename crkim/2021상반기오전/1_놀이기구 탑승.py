n = int(input())
board = [[0 for _ in range(n)] for _ in range(n)]
dx = [1, -1, 0, 0]
dy = [0, 0, -1, 1]
students = [[] for _ in range(n*n + 1)]
arr = []

for _ in range(n*n):
    temp = list(map(int, input().split()))
    like = temp[1:]
    students[temp[0]].append(like) #좋아하는 학생 새 배열로 정리
    arr.append(temp[0]) #순서대로 진행할 학생 배열

for people in arr :
    # 가장 우선순위가 낮은 값
    prev_case = (0, 0, -(n-1), -(n-1))
    my_x, my_y = n-1, n-1 #현재 위치
    # 우선순위 비교, 저장
    for i in range(n) :
        for j in range(n) :
            if board[i][j] != 0 : continue
            like_friend, empty_space = 0, 0
            for k in range(4) :
                nx = i + dx[k]
                ny = j + dy[k]
                if 0 <= nx < n and 0 <= ny < n :
                    if board[nx][ny] == 0 :
                        empty_space += 1 #빈공간임
                    elif board[nx][ny] in students[st][0]:
                        like_friend += 1 #좋아하는 친구 수

            list_tuple = (like_friend, empty_space, i, j)
            if list_tuple > prev_case :
                # tuple 비교로 가장 큰 우선순위 값 저장
                my_x, my_y = list_tuple[2], list_tuple[3]
                prev_case = list_tuple
            else :
                my_x, my_y = prev_case[2], prev_case[3]

    # 비교 끝 -> 배치
    board[my_x][my_y] = people

answer = 0
for i in range(n) :
    for j in range(n) :
        now = board[i][j]
        cnt = 0
        for k in range(4) :
            nx = i + dx[k]
            ny = j + dy[k]
            if 0 <= nx < n and 0 <= ny < n :
                if board[nx][ny] in students[now][0]:
                    cnt += 1
        if cnt != 0 :
            answer += 10**(cnt-1)

print(answer)