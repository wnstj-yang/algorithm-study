#include <iostream>
#include <vector>

using namespace std;

struct Board {
    bool isMonopoly;
    int player; // ���� �÷��̾� ���̵�. -1�̸� ���� ���� �ȵ�.
    int turn;
};

struct Player {
    int r, c;
    int d;
    int priority[4][4];
};

int n, m, k, res;
int dr[4] = { -1,1,0,0 };
int dc[4] = { 0,0,-1,1 };
vector<bool> isAlive;
Board board[21][21];
vector<Player> players;

void init() {
    res = 0;
    players.clear();
    isAlive.clear();
    for (int i = 0; i < 21; i++) {
        for (int j = 0; j < 21; j++) {
            board[i][j].isMonopoly = false;
            board[i][j].player = -1;
            board[i][j].turn = 0;
        }
    }
}

void input() {
    scanf("%d %d %d", &n, &m, &k);
    vector<Player> tmpPlayer(m);
    vector<bool> tmpisAlive(m);
    isAlive = tmpisAlive;
    players = tmpPlayer;
    int input;
    // ���� ä���
    for (int r = 0; r < n; r++) {
        for (int c = 0; c < n; c++) {
            scanf("%d", &input);
            if (input == 0) {
                board[r][c].isMonopoly = false;
                board[r][c].player = -1;
                board[r][c].turn = 0;
            }
            else {
                board[r][c].isMonopoly = true;
                board[r][c].player = input - 1;
                board[r][c].turn = k;
            }
        }
    }
    // �÷��̾�� ���� �ʱ� ����
    for (int i = 0; i < m; i++) {
        scanf("%d", &input);
        players[i].d = input - 1;
    }
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < 4; j++) {
            for (int k = 0; k < 4; k++) {
                scanf("%d", &input);
                players[i].priority[j][k] = input - 1;
            }
        }
    }
}

bool isContinue() {
    // 1000�� �Ѿ��� ��
    if (res > 1000) {
        res = -1;
        return false;
    }
    bool isAloneFirst = false;
    if (isAlive[0]) isAloneFirst = true;
    for (int i = 1; i < m; i++) {
        if (isAlive[i]) isAloneFirst = false;
    }

    return isAloneFirst;
}

bool isRange(int r, int c) {
    return r >= 0 && r < n&& c >= 0 && c < n;
}

void movePlayer() {
    vector<int> movedMap[21][21];
    for (int i = 0; i < m; i++) { // i��° �÷��̾�
        int r = players[i].r;
        int c = players[i].c;
        int d = players[i].d;
        int cnt = 0; // 4���⿡�� ������ ĭ�� �����?
        int tmp = 0; // 4���� �� ���� �ƴ� ����
        for (int k = 0; k < 4; k++) {
            // ���� i��° �÷��̾��� �켱���� ������ �����¿� ���Ǳ�!
            int nd = players[i].priority[d][k];
            int nr = r + dr[nd];
            int nc = c + dc[nd];
            if (isRange(nr, nc)) {
                tmp++;
                if (board[nr][nc].isMonopoly) cnt++;
                else { // �̵��� ���� ������ �����(��� �÷��̾ �̵��� ���� �� ���� ����!)
                    movedMap[nr][nc].push_back(i); // (nr, nc) ��ǥ�� i��° �÷��̾ �̵��ߴٴ� �ǹ�
                    players[i].d = nd; // �׸��� ��������� ���!
                    break;
                }
            }
        }
        if (cnt == tmp) { // 4 ���� �� �ڱ� ������ ����. ���� �ڱ� ���� �ݴ�� �̵��ϸ��
            int nr = r + dr[(d + 2) % 4];
            int nc = c + dc[(d + 2) % 4];
            movedMap[nr][nc].push_back(i);
        }
    }
    
    for (int r = 0; r < n; r++) {
        for (int c = 0; c < n; c++) {
            int num = movedMap[r][c].size();
            if (num == 0) continue;
            else if (num == 1) {
                int idx = movedMap[r][c][0];
                players[idx].r = r;
                players[idx].c = c;
            }
            else {
                // ù��° ���̸� �츮�� �� ų
                int idx = movedMap[r][c][0];
                players[idx].r = r;
                players[idx].c = c;
                for (int i = 1; i < movedMap[r][c].size(); i++) {
                    isAlive[i] = true;
                }
            }
        }
    }
    
}

void updateBoard() {
    for (int r = 0; r < n; r++) {
        for (int c = 0; c < n; c++){
            if (!board[r][c].isMonopoly) continue;
            board[r][c].turn--;
            if (board[r][c].turn < 0) {
                board[r][c].isMonopoly = false;
                board[r][c].player = -1;
                board[r][c].turn = -1;
            }
        }
    }
}

int main() {

    init();
    input();

    while (true) {
        if (!isContinue()) break;
        movePlayer();
        updateBoard();
        res++;
    }

    printf("%d", res);

    return 0;

}