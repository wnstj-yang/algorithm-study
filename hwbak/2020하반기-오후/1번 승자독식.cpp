#include <iostream>
#include <vector>

using namespace std;

struct Board {
    bool isMonopoly;
    int player; // 독점 플레이어 아이디. -1이면 아직 독점 안됨.
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
    // 격자 채우기
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
    // 플레이어들 각자 초기 방향
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
    // 1000을 넘었을 때
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
    for (int i = 0; i < m; i++) { // i번째 플레이어
        int r = players[i].r;
        int c = players[i].c;
        int d = players[i].d;
        int cnt = 0; // 4방향에서 독점된 칸이 몇개인지?
        int tmp = 0; // 4방향 중 벽이 아닌 개수
        for (int k = 0; k < 4; k++) {
            // 현재 i번째 플레이어의 우선순위 방향대로 상하좌우 살피기!
            int nd = players[i].priority[d][k];
            int nr = r + dr[nd];
            int nc = c + dc[nd];
            if (isRange(nr, nc)) {
                tmp++;
                if (board[nr][nc].isMonopoly) cnt++;
                else { // 이동할 곳에 흔적만 남기기(모든 플레이어가 이동이 끝난 후 독점 진행!)
                    movedMap[nr][nc].push_back(i); // (nr, nc) 좌표에 i번째 플레이어가 이동했다는 의미
                    players[i].d = nd; // 그리고 방향까지만 기록!
                    break;
                }
            }
        }
        if (cnt == tmp) { // 4 방향 중 자기 땅으로 ㄱㄱ. 현재 자기 방향 반대로 이동하며됨
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
                // 첫번째 아이만 살리고 다 킬
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