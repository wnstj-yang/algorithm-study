# 2023-08-20(일)
# 풀이 시간 : 1시간 47분
# 첫 제출 : 1565ms / 메모리 40MB
# 추후 시간 줄이는 수정 진행 예정

from collections import deque


def move_moving():
    # 1. 무빙 워크가 (시계 방향으로) 1칸 회전
    moving.rotate(1)
    # people에는 사람들이 위치한 인덱스이므로 1칸 회전이면 1 증가해준다
    for i in range(len(people)):
        people[i] += 1


def move_person(people):
    global not_stable

    temp = deque() # 새로 사람들 리스트를 저장할 공간

    while people:
        person = people.popleft() # 가장 먼저 올라간 사람부터 체크
        # 1. move_moving 함수에 이어 무빙워크로 회전 이후 N번 째에 왔다면 과정 종료
        if person == N - 1:
            continue

        # 2. 사람들의 무빙워크에서 이동 시작

        # 이동하려는 인덱스에 안정성이 0 혹은 사람이 존재한다면 제자리에 있는다
        # 주의할 점은 people 리스트가 아닌 새로 저장할 temp리스트 확인해야함
        if moving[person + 1] == 0 or person + 1 in temp:
            temp.append(person)
            continue

        # 사람의 위치 이동과 함께 안정성 1 감소
        person += 1
        moving[person] -= 1
        # 안정성이 감소해서 0이라면 0인 판의 개수 증가
        if moving[person] == 0:
            not_stable += 1

        # 이동한 곳이 N - 1(N번 째)이라면 바깥으로 나간다
        if person == N - 1:
            continue
        # 이동한 위치의 사람을 추가
        temp.append(person)
        
    # 새로운 사람 추가 진행. 첫 번째 위치가 안정성이 0이고 사람이 없을 때 증가
    if moving[0] != 0:
        temp.append(0)
        moving[0] -= 1
        # 안정성은 사람이 해당 위치에 올라간다면 즉시 감소하기에 0인 개수 판단 진행
        if moving[0] == 0:
            not_stable += 1
    return temp


N, K = map(int, input().split())
moving = deque(list(map(int, input().split()))) # 무빙워크 정보
people = deque() # 사람들을 큐에 넣어서 순서 파악
cnt = 0 # 실험 횟수
not_stable = 0 # 안정성이 0인 칸의 개수

# 실험 시작
while True:
    cnt += 1

    move_moving()
    people = move_person(people)
    # 4. 무빙워크, 사람들 회전 및 이동을 실험하면서 안정성이 0인 칸이 K 개수 이상이면 끝
    if not_stable >= K:
        break

print(cnt)
