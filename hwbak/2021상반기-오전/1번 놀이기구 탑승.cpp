#include <iostream>
#include <queue>
#include <vector>

using namespace std;

struct Seat {
	int student = -1;
	int r = 0, c = 0;
	int empty = 4;
	Seat() {}
	Seat(int r, int) : r(r), c(c) {}
};

struct cmp {
	bool operator()(Seat& a, Seat& b) {
		if (a.empty < b.empty) return true;
		else if (a.empty == b.empty) {
			if (a.r > b.r) return true;
			else if (a.r == b.r) return a.c > b.c;
			else return false;
		}
		else return false;
	}
};

int n, m;
vector<vector<int>> student; // 0�� �л� ���̵�, 1���� �����ϴ� ģ�� ���
Seat map[21][21];
int dr[4] = { 0,0,1,-1 };
int dc[4] = { 1,-1,0,0 };

void init() {
	
}

void input() {
	scanf("%d", &n);
	m = n * n;
	vector<vector<int>> tmp(m);
	student = tmp;
	int input;
	int st;
	for (int i = 0; i < m; i++) {
		scanf("%d", &st);
		student[i].push_back(st - 1);
		for (int j = 0; j < 4; j++) {
			scanf("%d", &input);
			student[i].push_back(input - 1);
		}
	}
}

bool isRange(int r, int c) {
	return r >= 0 && r < n && c >= 0 && c < n;
}

pair<int, int> findMySeat(int id) {
	vector<pair<int, int>> indicated;
	int maxFriendCnt = -1; // �ֺ��� ģ���� ���� ���� ��, �� ���� ģ��?
	for (int r = 0; r < n; r++) {
		for (int c = 0; c < n; c++) {
			int friendCnt = 0;
			for (int d = 0; d < 4; d++) {
				int nr = r + dr[d];
				int nc = c + dc[d];
				if (isRange(nr, nc) && map[nr][nc].student != -1) {
					for (int i = 1; i <= 4; i++) {
						if (map[nr][nc].student == student[id][i]) friendCnt++;
					}
				}
			}
			if (friendCnt == maxFriendCnt) indicated.push_back(make_pair(r, c));
			else if (friendCnt > maxFriendCnt) {
				maxFriendCnt = friendCnt;
				indicated.clear();
				indicated.push_back(make_pair(r, c));
			}
		}
	}

	if (indicated.size() == 1) return indicated[0];
	else {
		priority_queue<Seat, vector<Seat>, cmp> pq;
		for (int i = 0; i < indicated.size(); i++) {
			int r = indicated[i].first;
			int c = indicated[i].second;
			pq.push(map[r][c]);
		}
		Seat mySeat = pq.top();
		return {mySeat.r, mySeat.c};
	}
}

void seatStudent(int id, int r, int c) {
	map[r][c].student = id;
	// �ֺ� �ڸ��� empty�� 1����.
	for (int d = 0; d < 4; d++) {
		int nr = r + dr[d];
		int nc = c + dc[d];
		if (isRange(nr, nc)) map[nr][nc].empty--;
	}
}

int getScore() {
	int sum = 0;
	for (int r = 0; r < n; r++) {
		for (int c = 0; c < n; c++) {
			int cnt = 0;
			for (int d = 0; d < 4; d++) {
				int nr = r + dr[d];
				int nc = c + dc[d];
				if (isRange(nr, nc)) {
					for (int k = 0; k < 4; k++) {
						if (student[map[r][c].student][k] == map[nr][nc].student) {
							cnt++;
							break;
						}
					}
				}
			}
			if (cnt == 1) sum += 1;
			else if (cnt == 2) sum += 10;
			else if (cnt == 3) sum += 100;
			else if (cnt == 4) sum += 1000;
		}
	}
	return sum;
}

void printMap(string title) {
	printf("%s\n", title.c_str());
	for (int r = 0; r < n; r++) {
		for (int c = 0; c < n; c++) {
			printf("%d ", map[r][c].student);
		}
		printf("\n");
	}
}

int main() {

	init();
	input();
	
	for (int i = 0; i < m; i++) {
		pair<int, int> mySeat = findMySeat(student[i][0]); // i��° �л��� ���� ��ġ
		seatStudent(i, mySeat.first, mySeat.second); // i��° �л��� ������.
		printMap("�л�");
	}

	printf("%d", getScore());

	return 0;

}