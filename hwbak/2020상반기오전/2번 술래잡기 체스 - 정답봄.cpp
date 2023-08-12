#include <iostream>
#include <tuple>
#include <algorithm>

#define SULE make_pair(-2, -2)
#define BLANK make_pair(-1, -1)

using namespace std;

int n = 4;

pair<int, int> board[4][4];

int dx[8] = { -1, -1,  0,  1, 1, 1, 0, -1 };
int dy[8] = { 0, -1, -1, -1, 0, 1, 1,  1 };

int max_score;

bool isRange(int x, int y) {
    return 0 <= x && x < n && 0 <= y && y < n;
}

bool isCanGo_doduk(int x, int y) { // (x,y)�� ������ �̵������Ѱ�
    return isRange(x, y) && board[x][y] != SULE;
}

bool isCanGo_sule(int x, int y) { //(x,y)�� ������ �̵������Ѱ�
    return isRange(x, y) && board[x][y] != BLANK;
}

bool Done(int x, int y, int d) {
    // ���� ��ġ���� �� ���̶� �� �� �ִ��� Ȯ���մϴ�.
    // �����Ѵٸ�, ���� ������ ������ �ʾҽ��ϴ�.
    for (int dist = 1; dist <= n; dist++) {
        int nx = x + dx[d] * dist, ny = y + dy[d] * dist;
        if (isCanGo_sule(nx, ny))
            return false;
    }

    return true;
}

tuple<int, int, int> GetNext(int r, int c, int dir) {
    for (int i = 0; i < 8; i++) { // �ε��� 1�� ������Ű�鼭 �ݽð� 45�� ���� ����
        int nd = (dir + i) % 8;
        int nr = r + dx[nd];
        int nc = c + dy[nd];
        if (isCanGo_doduk(nr, nc))
            return make_tuple(nr, nc, nd);
    }
    // �̵��� �Ұ����ϴٸ� ���� ��ġ, ���� ���� �״�� �����Ǿ���մϴ�.
    return make_tuple(r, c, dir);
}

void swapPos(int x, int y, int next_x, int next_y) {
    pair<int, int> temp_piece = board[x][y];
    board[x][y] = board[next_x][next_y];
    board[next_x][next_y] = temp_piece;
}

void Move(int target_num) {
    for (int x = 0; x < n; x++)
        for (int y = 0; y < n; y++) {
            int piece_num, move_dir;
            tie(piece_num, move_dir) = board[x][y];
            if (piece_num == target_num) {
                int next_x, next_y, next_dir;
                // �̵��ؾ��� ��ġ�� �ٶ󺸰� �� ������ ���մϴ�.
                tie(next_x, next_y, next_dir) = GetNext(x, y, move_dir);
                // ���� ���� ������ �ٲ��� ��, �� ���� ��ġ�� ��ȯ�մϴ�.
                board[x][y] = make_pair(piece_num, next_dir);
                swapPos(x, y, next_x, next_y);
                return;
            }
        }
}

void moveDoduks() { // ���� �����̱�
    for (int i = 1; i <= n * n; i++)
        Move(i);
}

// ���� �������� ��ġ�� (x, y), 
// �ٶ󺸰� �ִ� ������ d�̰�
// ���ݱ��� ���� ������ score�϶�
// Ž���� ��� �����ϴ� �Լ��Դϴ�.
void SearchMaxScore(int x, int y, int d, int score) {
    // �� �̻� ������ ���� ���ٸ�
    // ���� �����ϰ� ���մϴ�.
    if (Done(x, y, d)) {
        max_score = max(max_score, score);
        return;
    }

    // ���� �Ͽ� ������ �� �ִ� ���� ���� Ž���մϴ�.
    for (int dist = 1; dist <= n; dist++) {
        int nx = x + dx[d] * dist, ny = y + dy[d] * dist;
        // ������ �̵� �� �� ���� ��ġ���, �н��մϴ�.
        if (!isCanGo_sule(nx, ny))
            continue;

        // �� Ž���� ������ ����, �ʱ� ���·� �ٽ� ����� ����
        // temp �迭�� ���� board ���¸� �����س����ϴ�.
        pair<int, int> temp[4][4];

        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                temp[i][j] = board[i][j];

        // �ش� ��ġ�� ���ϸ��� ���
        int extra_score, next_dir;
        tie(extra_score, next_dir) = board[nx][ny];
        board[nx][ny] = SULE;
        board[x][y] = BLANK;

        // ��� ���ϸ��� �����Դϴ�.
        moveDoduks();

        // �� ���� Ž���� �����մϴ�. 
        SearchMaxScore(nx, ny, next_dir, score + extra_score);

        // �𰢽� �ٽ� ���� board�� ���� �־��ݴϴ�.
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                board[i][j] = temp[i][j];
    }
}

void input() {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            int p, d;
            cin >> p >> d;
            board[i][j] = make_pair(p, d - 1);
        }
    }
}

int main() {

    input();

    // ó�� (0, 0) �������, ��� ���ϸ��� �̵��� ������ �����մϴ�.
    int init_score, init_dir;
    tie(init_score, init_dir) = board[0][0];
    board[0][0] = SULE;

    moveDoduks();

    SearchMaxScore(0, 0, init_dir, init_score);
    cout << max_score;

    return 0;
}