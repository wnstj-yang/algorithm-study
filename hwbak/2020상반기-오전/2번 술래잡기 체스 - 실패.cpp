// ������ �κ�: ��� �ִ��� ���ϴ°�?
// �ð�����..

#include<iostream>
#include<vector>
#include<memory.h>

using namespace std;

struct Horse {
	int r, c;
	int dir; // 0���� ����
	Horse(int num, int r, int c, int dir) : r(r), c(c), dir(dir) {}
};

int map[4][4]; // -1�� ���� ��ġ
int dr[8] = {-1,-1,0,1,1,1,0,-1};
int dc[8] = {0,-1,1,-1,0,1,1,1};
vector<Horse> doduk; // ���� ����Ʈ
Horse sule; // ���� ����ü
bool isCatched[16];

void init() {
	doduk.clear();
	doduk.push_back(Horse(-1,-1,-1,-1)); // ������ ���ڿ� �ε����� �����ϰ� ���߱� ���� �׳� ����
	memset(isCatched, false, sizeof(isCatched));
}

void input() {
	for (int i = 0; i < 4; i++) {
		for (int j = 0; j < 8; j++) {
			int num, d;
			scanf("%d %d", &num, &d);
			doduk.push_back(Horse(num, i, j, d));
		}
	}
}

bool isRange(int x, int y) {
	return x >= 0 && x < 4 && y >= 0 && y < 4;
}

void swapPos(Horse* a, Horse* b) { // a�� b�� ��ġ�� �ٲ۴�.
	int a_r = a->r;
	int a_c = a->c;
	int b_r = b->r;
	int b_c = b->c;
	a->r = b_r;
	a->c = b_c;
	b->r = a_r;
	b->c = a_c;
}

void rotateDir45(Horse* a) { // �ݽð� �������� 45�� ������
	int d = a->dir;
	a->dir = (d + 1) % 8;
}

bool isCanGo(int r, int c) {
	// ����� �Ǵ� ������ ������ 
}

void dfs(int r, int c, int d) {
	for (int i = 0; i < 8; i++) {
		int dir = (d + i) % 8;
		int nr = r + dr[dir];
		int nc = c + dc[dir];
		if (isRange(nr, nc) && isCanGo(nr, nc), ) {

		}
	}
}

void moveDoduks() {
	for (int i = 0; i < 16; i++) {
		if (isCatched[i]) continue; // ���� ������ �������� ����

	}
}

int main() {

	init();
	input();
	
	moveDoduks();

	return 0;
}