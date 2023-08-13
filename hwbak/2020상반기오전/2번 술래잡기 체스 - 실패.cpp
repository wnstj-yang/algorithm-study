// 막혔던 부분: 어떻게 최댓값을 구하는가?
// 시간부족..

#include<iostream>
#include<vector>
#include<memory.h>

using namespace std;

struct Horse {
	int r, c;
	int dir; // 0부터 시작
	Horse(int num, int r, int c, int dir) : r(r), c(c), dir(dir) {}
};

int map[4][4]; // -1은 술래 위치
int dr[8] = {-1,-1,0,1,1,1,0,-1};
int dc[8] = {0,-1,1,-1,0,1,1,1};
vector<Horse> doduk; // 도둑 리스트
Horse sule; // 술래 구조체
bool isCatched[16];

void init() {
	doduk.clear();
	doduk.push_back(Horse(-1,-1,-1,-1)); // 도둑을 숫자와 인덱스를 동일하게 맞추기 위해 그냥 넣음
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

void swapPos(Horse* a, Horse* b) { // a와 b의 위치를 바꾼다.
	int a_r = a->r;
	int a_c = a->c;
	int b_r = b->r;
	int b_c = b->c;
	a->r = b_r;
	a->c = b_c;
	b->r = a_r;
	b->c = a_c;
}

void rotateDir45(Horse* a) { // 반시계 방향으로 45도 돌리기
	int d = a->dir;
	a->dir = (d + 1) % 8;
}

bool isCanGo(int r, int c) {
	// 빈공간 또는 도둑이 있으면 
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
		if (isCatched[i]) continue; // 잡힌 도둑은 움직이지 않음

	}
}

int main() {

	init();
	input();
	
	moveDoduks();

	return 0;
}