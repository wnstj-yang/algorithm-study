# 2023-08-29(화)
# 풀이 시간: 20:35 ~ 21:05
# 기존 스터디원분들의 풀이와 people도 같이 동작하게끔 표현
# 202ms / 35MB

from collections import deque


def move_walk():
    # 사람들도 무빙워크에서 회전하는 것처럼 stable과 같은 길이와 회전을 진행
    stable.appendleft(stable.pop())
    people.appendleft(people.pop())
    # 한 칸씩 움직인 이후 무빙워크의 끝에 사람이 존재하면 내보낸다
    if people[N - 1]:
        people[N - 1] = 0


def move_people():
    global not_stable_cnt

    # N - 2(무빙워크의 끝에서 한 칸 전)부터 무빙워크의 첫부분까지 사람 파악
    for i in range(N - 2, -1, -1):
        # 현재 위치에 사람이 있고 다음 칸에 사람이 없는 상태에서 안정성이 있다면
        # 사람을 이동시킨다.
        if people[i] == 1 and people[i + 1] == 0 and stable[i + 1] > 0:
            people[i + 1] = 1
            stable[i + 1] -= 1
            people[i] = 0
            # 이동 시킨 이후의 안정성 부분도 즉시 줄인다
            if stable[i + 1] == 0:
                not_stable_cnt += 1
    # 사람들의 이동이 끝난 이후 무빙워크의 끝에 사람이 존재한다면 내보낸다.
    if people[N - 1]:
        people[N - 1] = 0

    # 사람을 추가하는 부분. 무빙워크의 처음에 안정성이 존재한다면 사람 추가
    if stable[0] > 0:
        people[0] = 1
        stable[0] -= 1
        if stable[i] == 0:
            not_stable_cnt += 1


N, K = map(int, input().split())
stable = deque(list(map(int, input().split()))) # 안정성
people = deque([0 for _ in range(N)]) # 사람들
not_stable_cnt = 0 # 안정성이 K이상 된 수
experiment_cnt = 0 # 실험한 횟수
while True:
    move_walk()
    move_people()
    experiment_cnt += 1
    if not_stable_cnt >= K:
        break
print(experiment_cnt)
