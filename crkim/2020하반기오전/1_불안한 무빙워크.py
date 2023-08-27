# 틀린 코드
m ,k = map(int, input().split())
arr = list(map(int, input().split()))
people = list(0 for _ in range(len(arr) // 2))
cnt, ans = 0, 0

# 무빙워크가 움직임, 사람도 움직임
def move_walk() :
    arr.insert(0, arr[-1])
    arr.pop()
    people.insert(0, 0)
    people.pop()

#사람들 앞으로 한 칸 이동
def move_people() :
    global arr
    arr1 = arr[:len(arr)//2]
    for i in range(1, len(people)):
        if people[-i] > 0 and arr[-(i+1)] > 0:
            people[-i] -= 1
            people[-(i+1)] += 1
            arr1[-(i+1)] -= 1

    if people[0] != 0:
        people[1] += 1
        people[0] = 0
        arr1[1] -= 1
    arr = arr1 + arr[len(arr)//2:]

# 새로운 사람을 0번 자리에 추가
def add() :
    if people[0] == 0 and arr[0] > 0:
        people[0] = 1
        arr[0] -= 1
    if people[-1] == 1 :
        people[-1] = 0

while True:
    if cnt >= k:
        break
    else :
        move_walk()
        move_people()
        add()
        for i in arr:
            if i == 0:
                cnt += 1
        ans += 1

print(ans)