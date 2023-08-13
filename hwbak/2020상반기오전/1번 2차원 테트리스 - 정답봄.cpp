#include<iostream>

#define BOARD_NUM 2
#define MAX_N 6
#define MAX_M 4
#define TILE_NUM 3

using namespace std;

int k, t, x, y, score;
int board[BOARD_NUM][MAX_N][MAX_M]; // BOARD_NUM가 0이면 노랑보드, 1이면 빨강보드
int shapes[TILE_NUM + 1][2][2] = { // 타입별 타일 모양 지정
	{},

	{{1, 0},
	 {0, 0}},

	{{1, 1},
	 {0, 0}},

	{{1, 0},
	 {1, 0}},
};


void init() {
	score = 0;
}

void input() {
	scanf("%d %d %d", &t, &x, &y);
}

bool isRange(int x, int y) { // 좌표 범위 체크
	return x >= 0 && x < 6 && y >= 0 && y < 4;
}

bool isCanGo(int b_num, int type, int x, int y) {
	// 격자를 벗어나는지 확인하기
	for (int dx = 0; dx < 2; dx++) {
		for (int dy = 0; dy < 2; dy++) {
			if (shapes[type][dx][dy]) {
				int nx = x + dx;
				int ny = y + dy;
				if (!isRange(nx, ny) || board[b_num][nx][ny]) return false;
			}
		}
	}
	return true;
}

void putTile(int b_num, int type, int x, int y){
	for (int dx = 0; dx < 2; dx++) {
		for (int dy = 0; dy < 2; dy++) {
			if (shapes[type][dx][dy]) {
				int nx = x + dx;
				int ny = y + dy;
				board[b_num][nx][ny] = 1;
			}
		}
	}
}

bool allFilled(int b_num, int row) {
	for (int col = 0; col < 4; col++) {
		if (board[b_num][row][col] == 0) return false;
	}
	return true;
}

void downOneLine(int b_num, int r) {
	for (int i = r; i >= 1; i--) {
		for (int j = 0; j < 4; j++) {
			board[b_num][i][j] = board[b_num][i - 1][j];
			board[b_num][i - 1][j] = 0;
		}
	}
}

void processDark(int b_num) { // 노랑보드 기준
	// 탐색 방향은 맨 밑에서 위로 ↑
	int r = 6 - 1;
	while (r >= 2) {
		if (allFilled(b_num, r)) { // r행이 모두 꽉 찼을때
			score++;
			downOneLine(b_num, r); // 꽉 찬 행을 없앤다.
		}
		else r--; // 윗 행 탐색하기~
	}
}

bool blockExist(int b_num, int i) {
	for (int j = 0; j < 4; j++) {
		if (board[b_num][i][j] == 1) return true;
	}
	return false;
}

void processLight(int b_num) {
	int drop_cnt = 0;
	// 블럭이 한개로 놓인 개수 세고, 그 만큼 줄을 없앤다.
	if (blockExist(b_num, 0)) drop_cnt++;
	if (blockExist(b_num, 1)) drop_cnt++;
	while (drop_cnt--) downOneLine(b_num, 6 - 1);
}

void dropTile(int b_num, int type, int j) { // 노랑보드 기준 - j 컬럼에 떨어뜨린다.
	for (int i = 0; i < 6; i++) {
		if (!isCanGo(b_num, type, i + 1, j)) { // 다음 행으로 넘어갈 수 없을 때
			putTile(b_num, type, i, j); // (i,j)에 타일 놓기
			break;
		}
	}
	processDark(b_num); // 빨강/노랑 보드 처리
	processLight(b_num); // 연한 빨강/노랑
}

void simulation() {
	dropTile(0,t,y); // 노랑보드로 타일을 떨어뜨린다
	// dropTile은 노랑보드 기준으로 작성된 함수기 때문에, 시계방향 90도 회전 시킨다.
	if (t == 1) dropTile(1, 1, 4 - 1 - x);
	else if(t == 2) dropTile(1, 3, 4 - 1 - x);
	else if(t == 3) dropTile(1, 2, 4 - 1 - (x + 1));
}

int getTileCnt() {
	int cnt = 0;
	for (int l = 0; l < 2; l++) {
		for (int i = 0; i < 6; i++) {
			for (int j = 0; j < 4; j++) {
				cnt += board[l][i][j];
			}
		}
	}
	return cnt;
}

int main() {

	init();

	scanf("%d", &k);

	while (k--) { // k번 돌리기
		input();
		simulation();
	}

	printf("%d\n", score);
	printf("%d", getTileCnt());

	return 0;
}