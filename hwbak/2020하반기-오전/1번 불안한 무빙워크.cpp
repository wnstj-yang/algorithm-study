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
    // up과 down은 항상 고정
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
    // 회전
    movingWalk.push_front(movingWalk.back());
    movingWalk.pop_back();
    // down 지점에 사람이 있으면 사람을 내린다.
    if (movingWalk[down].isHuman) movingWalk[down].isHuman = false; // 사람 내리기
}

void movePeople() {
    // 가장 먼저 탄 사람부터 체크
    for (int i = down - 1; i >= up; i--) {
        if (!movingWalk[i].isHuman) continue;
        if (!movingWalk[i + 1].isHuman && movingWalk[i + 1].safe > 0) {
            movingWalk[i].isHuman = false;
            movingWalk[i + 1].isHuman = true;
            movingWalk[i + 1].safe--; // 안정성 감소
            // 모든 사람의 이동이 끝났다면, down 위치에 사람을 내린다.
        }
    }
    if (movingWalk[down].isHuman) movingWalk[down].isHuman = false; // 사람 내리기 
}

void upPeople() {
    // 조건 만족하면 사람을 한명 더 올린다.
    if (!movingWalk[up].isHuman && movingWalk[up].safe > 0) {
        movingWalk[up].isHuman = true; // 사람 올리기
        movingWalk[up].safe--;// 안정성 감소
    }
}

int main() {

    init();
    input();

    while (true) {
        step++;
        rotateMovingWalk(); // 무빙워크를 한바퀴 회전시킨다.
        movePeople(); // 사람들 한칸씩 이동
        upPeople(); // 사람을 up 위치에 올리기
        if (checkZeroSafeNum()) break;
    }

    printf("%d", step);

    return 0;

}