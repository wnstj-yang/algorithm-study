# 2023-09-22(금) / 2023-09-23(토)
# 풀이 시간 : 21:05 ~ 22:40 / 풀이참고
# 첫 제출 : ms / 메모리 MB
# 풀다가 시간초과에 대한 처리를 어떻게해야할지 고민... -> 추후 재풀이
# Box, Belt에 대한 class를 생성(풀이참고)
# 다시 개념부터 잡고 해야할듯... 이해가 안된다.

class Box:
    def __init__(self, box_index, weight, belt):
        self.box_index = box_index
        self.weight = weight
        self.prev = None
        self.next = None
        self.belt = belt


class Belt:
    def __init__(self, head, tail, broken):
        self.head = head
        self.tail = tail
        self.broken = broken
        # head의 다음은 tail, tail의 앞은 head
        self.head.next = tail
        self.tail.prev = head
        # head의 맨 앞, tail의 맨 뒤는 None
        self.head.prev = None
        self.tail.next = None


# 벨트가 비어있는지 없는지 판단
def empty(belt_num):
    # head의 뒤, tail의 앞이 같은 박스를 바라보면 비어있다고 표시
    # 즉, Belt의 초기상태와 같음을 보여준다다
    if belts[belt_num].head.next == belts[belt_num].tail.prev:
        return True
    else:
        return False


# 어떤 벨트의 뒤에 어떤 박스를 넣을지
def add_box(belt_num, box):
    # prev와 next를 미리 설정해서 짜기
    # box list에 box 추가
    box_map[box.box_index] = box
    # 현재 벨트의 tail 앞의 박스, 현재 벨트의 tail박스를 구한다
    prev = belts[belt_num].tail.prev
    next = belts[belt_num].tail
    # 새로 넣는 박스의 앞은
    box.prev = prev
    box.next = next
    prev.next = box
    next.prev = box


def pop_front(belt_num):
    if empty(belt_num):
        return
    item = belts[belt_num].head.next
    del box_list[item.box.box_index]
    prev = belts[belt_num].head
    next = belts[belt_num].head.next.next

    prev.next = next
    next.prev = prev
    item.prev = None
    item.next = None


q = int(input())
factories = []
box_list = []
belts = []
box_map = {}
N, M = 0, 0
for _ in range(q):
    order = list(map(int, input().split()))
    number = order[0]
    if number == 100:
        N, M = order[1], order[2]
        box_list = [Box(0, 0, 0) for _ in range(N)]
        belts = [Belt(Box(0, 0, 0), Box(0, 0, 0), False) for _ in range(M)]
        info = order[3:]
        id_list = [0] * N
        weight_list = [0] * N
        for i in range(N):
            id_list[i] = info[i]
            weight_list[i] = info[N + i]
        index = 0
        for belt_num in range(M):
            for i in range(N // M):
                box_list[index] = Box(id_list[index], weight_list[index], belt_num)
                add_box(belt_num, box_list[index])
                index += 1

    elif number == 200:
        w_max = order[1]
        for i in range(M):
            if empty(i) or belts[i].broken:
                continue
            front = belts[i].head

    elif number == 300:
        pass
    elif number == 400:
        pass
    else:
        pass
print(factories)
