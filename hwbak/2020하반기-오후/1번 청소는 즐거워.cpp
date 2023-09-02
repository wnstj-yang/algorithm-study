#include <iostream>
#include <memory.h>

using namespace std;

struct Brush {
    int r, c;
    int dir;
};

int n, res, moveCnt, dist; // moveCnt�� �ѹ������� �̵��� �� �ִ� ĭ�� ����
Brush brush;
int map[500][500];
int dr_brush[4] = { 0,1,0,-1 };
int dc_brush[4] = { -1,0,1,0 };
int ratio_map[5][5] = { {0,0,2,0,0},
                        {0,10,7,1,0},
                        {5,0,0,0,0},
                        {0,10,7,1,0},
                        {0,0,2,0,0}}; // �켱 a�ڸ��� 0����!

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

void rotateRatio() { // ratio_map�� �ݽð� ������
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
    //printf("�귯���� (%d, %d)�� �̵���\n", nr, nc);
}

void cleanDust() {
    map[brush.r][brush.c] = 0;
}

void spreadDust() {

    // �̵��� ��ģ �귯���� ��ġ���� ������ �۶߸���.
    int origin_dust = map[brush.r][brush.c];
    int spreadAmount = 0; // �������� ������ �� ��.

    // ���� ��ġ���� ������ �������� ���� ������!
    for (int r = 0; r < 5; r++) {
        for (int c = 0; c < 5; c++) {
            if (ratio_map[r][c] == 0) continue;
            int ratio = ratio_map[r][c];
            // �߾� (2,2)���� �󸶳� ������ �ִ��� üũ
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

    // ����������, ���� ���ڷ��� ���� ��ġ�� a�� ���� ����
    // ���ư� ������ �� �������� a�ڸ��� ��
    int a_r = brush.r + dr_brush[brush.dir];
    int a_c = brush.c + dc_brush[brush.dir];
    if(isRange(a_r, a_c)) map[a_r][a_c] += origin_dust - spreadAmount;
    else res += origin_dust - spreadAmount;

}

int main() {

    init();
    input();

    // �귯�� ó�� ��ġ ��
    brush.r = n / 2;
    brush.c = n / 2;
    brush.dir = 0;
    bool flag = false;
    while (true) {
        moveCnt++;
        for (int cnt = 0; cnt < dist; cnt++) { // moveCnt��ŭ ĭ �̵� ����
            moveBrush();
            spreadDust();
            cleanDust();
            if (brush.r == 0 && brush.c == 0) {
                flag = true;
                break;
            }
        }
        if (flag) break;
         // �ѹ������� ĭ �̵��� ������? ���� �������� �ٲٱ�!
         brush.dir = (brush.dir + 1) % 4;
         rotateRatio(); // ratio_map�� �Բ� �ݽð� 90�� ȸ��

         if (moveCnt == 2) {
             moveCnt = 0;
             dist++;
         }
    }

    printf("%d", res);

    return 0;

}