#include <iostream>
#include <deque>

using namespace std;

struct MovingWalk {
    bool isHuman;
    int safe;
    MovingWalk(bool isHuman, int safe) : isHuman(isHuman), safe(safe) {}
};

int n, k, up, down, step;
deque<MovingWalk> movingWalk;

void init() {
    step = 0;
    movingWalk.clear();
}

void input() {
    scanf("%d %d", &n, &k);
    // up�� down�� �׻� ����
    up = 0;
    down = n - 1;
    int input;
    for (int i = 0; i < 2 * n; i++) {
        scanf("%d", &input);
        movingWalk.push_back(MovingWalk(false, input));
    }
}

bool checkZeroSafeNum() {
    int cnt = 0;
    for (int i = 0; i < 2 * n; i++) {
        if (movingWalk[i].safe == 0) cnt++;
    }
    return cnt >= k;
}


void rotateMovingWalk() {
    // ȸ��
    movingWalk.push_front(movingWalk.back());
    movingWalk.pop_back();
    // down ������ ����� ������ ����� ������.
    if (movingWalk[down].isHuman) movingWalk[down].isHuman = false; // ��� ������
}

void movePeople() {
    // ���� ���� ź ������� üũ
    for (int i = down - 1; i >= up; i--) {
        if (!movingWalk[i].isHuman) continue;
        if (!movingWalk[i + 1].isHuman && movingWalk[i + 1].safe > 0) {
            movingWalk[i].isHuman = false;
            movingWalk[i + 1].isHuman = true;
            movingWalk[i + 1].safe--; // ������ ����
            // ��� ����� �̵��� �����ٸ�, down ��ġ�� ����� ������.
        }
    }
    if (movingWalk[down].isHuman) movingWalk[down].isHuman = false; // ��� ������ 
}

void upPeople() {
    // ���� �����ϸ� ����� �Ѹ� �� �ø���.
    if (!movingWalk[up].isHuman && movingWalk[up].safe > 0) {
        movingWalk[up].isHuman = true; // ��� �ø���
        movingWalk[up].safe--;// ������ ����
    }
}

int main() {

    init();
    input();

    while (true) {
        step++;
        rotateMovingWalk(); // ������ũ�� �ѹ��� ȸ����Ų��.
        movePeople(); // ����� ��ĭ�� �̵�
        upPeople(); // ����� up ��ġ�� �ø���
        if (checkZeroSafeNum()) break;
    }

    printf("%d", step);

    return 0;

}