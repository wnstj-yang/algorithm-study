#include <iostream>
#include <memory.h>

using namespace std;

struct Brush {
    int r, c;
    int dir;
};

int n, res, moveCnt, dist; // moveCnt는 한방향으로 이동할 수 있는 칸의 개수
Brush brush;
int map[500][500];
int dr_brush[4] = { 0,1,0,-1 };
int dc_brush[4] = { -1,0,1,0 };
int ratio_map[5][5] = { {0,0,2,0,0},
                        {0,10,7,1,0},
                        {5,0,0,0,0},
                        {0,10,7,1,0},
                        {0,0,2,0,0}}; // 우선 a자리도 0으로!

void rotateRatio();

void init() {
    memset(map, 0, sizeof(map));
    res = 0;
    moveCnt = 0;
    dist = 1;
}

void input() {
    scanf("%d", &n);
    for (int r = 0; r < n; r++) {
        for (int c = 0; c < n; c++) {
            scanf("%d", &map[r][c]);
        }
    }
}

bool isRange(int r, int c) {
    return r >= 0 && r < n&& c >= 0 && c < n;
}

bool isComplete() {
    return brush.r == 0 && brush.c == 0;
}

void rotateRatio() { // ratio_map을 반시계 돌리기
    int tmp[5][5];
    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            tmp[i][j] = ratio_map[i][j];
        }
    }
    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            ratio_map[5-j-1][i] = tmp[i][j];
        }
    }
    
}

void moveBrush() {
    int nr = brush.r + dr_brush[brush.dir];
    int nc = brush.c + dc_brush[brush.dir];
    brush.r = nr;
    brush.c = nc;
    //printf("브러쉬가 (%d, %d)로 이동됨\n", nr, nc);
}

void cleanDust() {
    map[brush.r][brush.c] = 0;
}

void spreadDust() {

    // 이동을 마친 브러시의 위치에서 먼지를 퍼뜨린다.
    int origin_dust = map[brush.r][brush.c];
    int spreadAmount = 0; // 퍼져나간 먼지의 총 양.

    // 현재 위치에서 먼지가 퍼져나갈 양을 구하자!
    for (int r = 0; r < 5; r++) {
        for (int c = 0; c < 5; c++) {
            if (ratio_map[r][c] == 0) continue;
            int ratio = ratio_map[r][c];
            // 중앙 (2,2)에서 얼마나 떨어져 있는지 체크
            int diff_r = 2 - r;
            int diff_c = 2 - c;
            int nr = brush.r - diff_r;
            int nc = brush.c - diff_c;
            int calculated = (origin_dust * ratio) / 100;
            spreadAmount += calculated;
            if (isRange(nr, nc)) map[nr][nc] += calculated;
            else res += calculated;
        }
    }

    // 마지막으로, 현재 빗자루의 다음 위치인 a의 먼지 업뎃
    // 날아간 먼지를 뺀 나머지가 a자리로 ㄱ
    int a_r = brush.r + dr_brush[brush.dir];
    int a_c = brush.c + dc_brush[brush.dir];
    if(isRange(a_r, a_c)) map[a_r][a_c] += origin_dust - spreadAmount;
    else res += origin_dust - spreadAmount;

}

int main() {

    init();
    input();

    // 브러시 처음 위치 셋
    brush.r = n / 2;
    brush.c = n / 2;
    brush.dir = 0;
    bool flag = false;
    while (true) {
        moveCnt++;
        for (int cnt = 0; cnt < dist; cnt++) { // moveCnt만큼 칸 이동 ㄱㄱ
            moveBrush();
            spreadDust();
            cleanDust();
            if (brush.r == 0 && brush.c == 0) {
                flag = true;
                break;
            }
        }
        if (flag) break;
         // 한방향으로 칸 이동이 끝나면? 다음 방향으로 바꾸기!
         brush.dir = (brush.dir + 1) % 4;
         rotateRatio(); // ratio_map도 함께 반시계 90도 회전

         if (moveCnt == 2) {
             moveCnt = 0;
             dist++;
         }
    }

    printf("%d", res);

    return 0;

}