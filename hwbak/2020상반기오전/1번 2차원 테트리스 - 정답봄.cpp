#include<iostream>

#define BOARD_NUM 2
#define MAX_N 6
#define MAX_M 4
#define TILE_NUM 3

using namespace std;

int k, t, x, y, score;
int board[BOARD_NUM][MAX_N][MAX_M]; // BOARD_NUM�� 0�̸� �������, 1�̸� ��������
int shapes[TILE_NUM + 1][2][2] = { // Ÿ�Ժ� Ÿ�� ��� ����
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

bool isRange(int x, int y) { // ��ǥ ���� üũ
	return x >= 0 && x < 6 && y >= 0 && y < 4;
}

bool isCanGo(int b_num, int type, int x, int y) {
	// ���ڸ� ������� Ȯ���ϱ�
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

void processDark(int b_num) { // ������� ����
	// Ž�� ������ �� �ؿ��� ���� ��
	int r = 6 - 1;
	while (r >= 2) {
		if (allFilled(b_num, r)) { // r���� ��� �� á����
			score++;
			downOneLine(b_num, r); // �� �� ���� ���ش�.
		}
		else r--; // �� �� Ž���ϱ�~
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
	// ���� �Ѱ��� ���� ���� ����, �� ��ŭ ���� ���ش�.
	if (blockExist(b_num, 0)) drop_cnt++;
	if (blockExist(b_num, 1)) drop_cnt++;
	while (drop_cnt--) downOneLine(b_num, 6 - 1);
}

void dropTile(int b_num, int type, int j) { // ������� ���� - j �÷��� ����߸���.
	for (int i = 0; i < 6; i++) {
		if (!isCanGo(b_num, type, i + 1, j)) { // ���� ������ �Ѿ �� ���� ��
			putTile(b_num, type, i, j); // (i,j)�� Ÿ�� ����
			break;
		}
	}
	processDark(b_num); // ����/��� ���� ó��
	processLight(b_num); // ���� ����/���
}

void simulation() {
	dropTile(0,t,y); // �������� Ÿ���� ����߸���
	// dropTile�� ������� �������� �ۼ��� �Լ��� ������, �ð���� 90�� ȸ�� ��Ų��.
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

	while (k--) { // k�� ������
		input();
		simulation();
	}

	printf("%d\n", score);
	printf("%d", getTileCnt());

	return 0;
}