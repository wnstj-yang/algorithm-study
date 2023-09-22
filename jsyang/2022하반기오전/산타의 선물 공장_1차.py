# 2023-09-22(금)
# 풀이 시간 : 21:05 ~ 22:40
# 첫 제출 : ms / 메모리 MB
# 풀다가 시간초과에 대한 처리를 어떻게해야할지 고민... -> 추후 재풀이


from collections import deque


def drop_stuff(w_max):
    result = 0
    for i in range(len(factories)):
        id, w = factories[i][0]
        if w <= w_max:
            factories[i].append(factories[i].pop())
        else:
            result += w
    print(result)


def remove_stuff(r_id):
    pass
    # for i in range(len(factories)):   ``  ``
    #     factories[i].
    # print(result)




q = int(input())
factories = []
for _ in range(q):
    order = list(map(int, input().split()))
    number = order[0]
    if number == 100:
        N, M = order[1], order[2]
        info = order[3:]
        cnt = 0
        box_list = deque()
        for i in range(0, len(info), 2):
            if cnt == N // M:
                cnt = 0
                factories.append(box_list)
                box_list = deque()
            box_list.append((info[i], info[i + 1]))
            cnt += 1
        factories.append(box_list)

    elif number == 200:
        pass
    elif number == 300:
        pass
    elif number == 400:
        pass
    else:
        pass
print(factories)
