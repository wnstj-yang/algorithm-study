#생각한 방법

#1. 초기값 설정
#2. 우선순위에 따른 이동
#3. 1턴 = 모든 플레이어가 다 움직여야 함
#3-0 빈칸이 있으면 빈칸으로, 빈칸이 없으면 독점 위치로 이동함
#3-1 n_player에 이동하고자 하는 값을 넣어둠
#3-2 n_player 중 x,y 값이 겹치는 곳은 플레이어 넘버가 낮은 애한테 줌
#3-3 삭제된 n_player -> 재탐색 (독식한 위치로)
#4. 이동 완료시 n_player 다 지움
#5. 1만 남거나 1000이 될 때까지 while 
#but. K값은 어떻게 처리할까?

# 다시 생각하는 과정
# 모든 움직임 시에 k개의 값도 함께 카운트 해줘야 함
# 현재 위치 기준으로 이동할 수 있는 4방향 탐색, 

n, m ,k = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(n)]
start = map(int, input().split())
p_dir= [list(map(int, input().split())) for _ in range(m*4)]

player = [[(1000, 1000) for _ in range(n)] for _ in range(n)]
n_player = [[(1000, 1000) for _ in range(n)] for _ in range(n)]

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

time = 0
alive = [i for i in range(1, m+1)]

def range_check(x, y, target):
    if not (0 <= x and x < n and 0 <= y and y < n):
        return False
    if n_player[x][y] == (1000, 1000):
        n_player[x][y] = target
    else :
        pass
    return True

def occupy(target):
    return True

def dir_check(target) :
    return True

def one_term():
    for player in range(4):
        if occupy(player) == False :
            dir_check(player)
        else :
            range_check(player)

    for i in range(n):
        pass
    return True

while True :
    if time >= 1000 :
        time = -1
        break
    elif len(alive) == 1 and sum(alive) == 1:
        break
    else :
        one_term()
        time += 1
print(time)

