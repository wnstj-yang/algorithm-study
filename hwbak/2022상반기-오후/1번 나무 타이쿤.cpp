#include <iostream>
#include <vector>
#include <memory.h>

using namespace std;

int n, m, d, p;
int map[16][16];
bool isLiquid[16][16];
int dr[8] = { 0,-1,-1,-1,0,1,1,1 };
int dc[8] = { 1,1,0,-1,-1,-1,0,1 };
int dr_cross[4] = { -1,-1,1,1 };
int dc_cross[4] = { 1,-1,-1,1 };

void init() {
	memset(map, 0, sizeof(map));
}

void input() {
	scanf("%d %d", &n, &m);
	
	isLiquid[n - 1][0] = true;
	isLiquid[n - 2][0] = true;
	isLiquid[n - 1][1] = true;
	isLiquid[n - 2][1] = true;

	for (int r = 0; r < n; r++) {
		for (int c = 0; c < n; c++) {
			scanf("%d", &map[r][c]);
		}
	}
}

bool isRange(int r, int c) {
	return r >= 0 && r < n && c >= 0 && c < n;
}

void copyMap(bool (*origin)[16], bool (*tmp)[16]) {
	for (int r = 0; r < n; r++) {
		for (int c = 0; c < n; c++) {
			tmp[r][c] = origin[r][c];
		}
	}
}

void printMap(string title) {
	printf("%s\n", title.c_str());
	for (int r = 0; r < n; r++) {
		for (int c = 0; c < n; c++) {
			printf("%3d ", map[r][c]);
		}
		printf("\n");
	}
}

void printIsLquid(string title) {
	printf("%s\n", title.c_str());
	for (int r = 0; r < n; r++) {
		for (int c = 0; c < n; c++) {
			printf("%d  ", isLiquid[r][c]);
		}
		printf("\n");
	}
}

void moveLiquid() {
	bool after[16][16];
	memset(after, 0, sizeof(after));
	for (int r = 0; r < n; r++) {
		for (int c = 0; c < n; c++) {
			if (!isLiquid[r][c]) continue;
			int nr = (r + dr[d] * p + n * p) % n;
			int nc = (c + dc[d] * p + n * p) % n;
			after[nr][nc] = true;
		}
	}
	copyMap(after, isLiquid);
}

void injectLiquid() {
	for (int r = 0; r < n; r++) {
		for (int c = 0; c < n; c++) {
			if (!isLiquid[r][c]) continue;
			map[r][c]++;
		}
	}
}

void adjCrossGrowth() {
	for (int r = 0; r < n; r++) {
		for (int c = 0; c < n; c++) {
			if (!isLiquid[r][c]) continue;
			int cnt = 0;
			for (int k = 0; k < 4; k++) {
				int nr = r + dr_cross[k];
				int nc = c + dc_cross[k];
				if (isRange(nr, nc) && map[nr][nc] >= 1) cnt++;
			}
			printf("(%d, %d)가 %d만큼 자람\n", r, c, cnt);
			map[r][c] += cnt;
		}
	}
}

void cutTreeAndBuyLiquid() {
	bool after[16][16];
	memset(after, 0, sizeof(after));
	for (int r = 0; r < n; r++) {
		for (int c = 0; c < n; c++) {
			if (!isLiquid[r][c] && map[r][c] >= 2) {
				map[r][c] -= 2;
				after[r][c] = true;
			}
		}
	}
	copyMap(after, isLiquid);
}

int getRes() {
	int sum = 0;
	for (int r = 0; r < n; r++) {
		for (int c = 0; c < n; c++) {
			sum += map[r][c];
		}
	}
	return sum;
}


int main() {

	init();
	input();

	for (int i = 0; i < m; i++) {
		scanf("%d %d", &d, &p);
		d--;
		moveLiquid();
		printMap("영양제 이동 후 map");
		printIsLquid("영양제 이동 후 isLiquid");
		injectLiquid();
		printMap("영양제 주입 후 map");
		printIsLquid("영양제 주입후 isLiquid");
		adjCrossGrowth();
		printMap("대각선 방향 중 1개 이상 나무 개수만큼 자람 map");
		printIsLquid("대각선 방향 중 1개 이상 나무 개수만큼 자람 isLiquid");
		cutTreeAndBuyLiquid();
		printMap("나무 자른 후 map");
		printIsLquid("나무 자른 후 isLiquid");
	}

	printf("%d", getRes());

	return 0;
}