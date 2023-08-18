#include<iostream>
#include<memory.h>
#include<vector>

using namespace std;

int k, t, blueR, blueC;
int score;
bool board[11][11]; // ������� �� 4~9, �� 0~3 // ���� ���� �� 0~3, �� 4~9 / true: Ÿ�� ���� / false: ��ĭ
bool copyedBoard[11][11]; // �� �ű� �� ����� �迭
int edgeYellow[4]; // �� ���� ���� ���� �� ����. �� 10�� ĭ�� ����ٴ� ��. �� 4, 5�� ���� �κ���. �� 4�� ���� ����
int edgeRed[4]; // �� �࿡ ���� ���� �� ����. �� 10�� ĭ�� ����ٴ� ��. �� 4, 5�� ���� �κ���. �� 4�� ���� ����
vector<pair<int, int>> tile; // �Ķ����� �� Ÿ�� ��ǥ

void init() {
	score = 0;
	memset(board, false, sizeof(board));
	for (int i = 0; i < 4; i++) {
		edgeYellow[i] = 10;
		edgeRed[i] = 10;
	}
}

void copyBoard(bool (*origin)[11], bool (* newBoard)[11]) {
	for (int i = 0; i < 11; i++) {
		for (int j = 0; j < 11; j++) {
			newBoard[i][j] = origin[i][j];
		}
	}
}

void updateTile() {
	tile.clear();
	if (t == 1) {
		tile.push_back(make_pair(blueR, blueC));
	}
	else if (t == 2) {
		tile.push_back(make_pair(blueR, blueC));
		tile.push_back(make_pair(blueR, blueC + 1));
	}
	else if (t == 3) {
		tile.push_back(make_pair(blueR, blueC));
		tile.push_back(make_pair(blueR + 1, blueC));
	}
}

void pushToYellow(int r, int c) {
	board[--edgeYellow[c]][c] = true;
}

void pushToRed(int r, int c) {
	board[r][--edgeRed[r]] = true;
}

void pushTile() {
	updateTile(); // Ÿ�Կ� �°� Ÿ�� ��ǥ ������Ʈ
	for (int i = 0; i < tile.size(); i++) {
		pushToYellow(tile[i].first, tile[i].second); // ��� ���� ������ �б�
		pushToRed(tile[i].first, tile[i].second); // ���� ���� ������ �б�
	}
}

void updateYellowBoard(int r) { // r�࿡�� ���� �Ͼ
	copyBoard(board, copyedBoard);
	// 4�� ~ r-1����� ��ĭ�� �Ʒ��� �б�
	for (int i = 4; i <= r-1; i++) {
		for (int j = 0; j <= 3; j++) {
			board[i][j] = copyedBoard[i - 1][j];
		}
	}
	// �� ���� �ִ� �� ���� ������Ʈ
	for (int j = 0; j <= 3; j++) {
		for (int i = 4; i <= 9; i++) {
			if (board[i][j]) { // ó�� true�� ������ ��ǥ�� �ش� ������ ���� 
				edgeYellow[j] = i;
				break;
			}
		}
	}
}

void updateRedBoard(int c) { // c�࿡�� ���� �Ͼ
	copyBoard(board, copyedBoard);
	// 4�� ~ c-1������ ��ĭ�� �Ʒ��� �б�
	for (int j = 4; j <= c-1; j++) {
		for (int i = 0; i <= 3; i++) {
			board[i][j] = copyedBoard[i][j-1];
		}
	}
	// �� ���� �ִ� �� ���� ������Ʈ
	for (int i = 0; i <= 3; i++) {
		for (int j = 4; j <= 9; j++) {
			if (board[i][j]) { // ó�� true�� ������ ��ǥ�� �ش� ������ ���� 
				edgeYellow[i] = j;
				break;
			}
		}
	}
}

void updateScore() {
	// ������忡�� �� ���� �� ���� ����
	bool flag_yellow;
	bool flag_red;
	while (true) {
		printf("��? score = %d\n", score);
		// ��� ���� �� ���� üũ�ϱ�
		for (int i = 4; i <= 9; i++) {
			flag_yellow = true;
			for (int j = 0; j <= 3; j++) {
				if (!board[i][j]) flag_yellow = false; // ������� i���� �� ������ ����!
			}
			if (flag_yellow) { // ������� �ʿ��� ���� ����
				score++;
				updateYellowBoard(i);
				i--; // ������Ʈ �� ���忡�� ���� �࿡�� �� �ٽ� ������ ���� �� �ִ��� Ȯ��
			}
			else continue; // ���� ����
		}
		// ���� ���� �� ���� üũ�ϱ�
		for (int j = 4; j <= 9; j++) {
			flag_red = true;
			for (int i = 0; i <= 3; i++) {
				if (!board[i][j]) flag_red = false; // �������� j���� �� ������ ����!
			}
			if (flag_red) { // �������� �ʿ������� ����
				score++;
				updateRedBoard(j);
				j--; // ������Ʈ �� ���忡�� ���� ������ �� �ٽ� ������ ���� �� �ִ� �� Ȯ��.
			}
			else continue; // ���� ����
		}
	}

}

void removeTile() {
	int cnt = 0;
	// ���� ��� ���� - �� �� ���� cnt���� ��ŭ ����(cnt�� ���� �ٸ� �� ����)
	for (int i = 4; i <= 5; i++) {
		for (int j = 0; j <= 3; j++) {
			if (board[i][j]) {
				cnt++;
				break;
			}
		}
	}
	while (cnt--) updateYellowBoard(9);
	 
	// ���� ���� ���� - �� ������ ���� cnt���� ��ŭ ����(cnt�� ���� �ٸ� �� ����)

	for (int j = 4; j <= 5; j++) {
		for (int i = 0; i <= 3; i++) {
			if (board[i][j]) {
				cnt++;
				break;
			}
		}
	}
	while (cnt--) updateRedBoard(9);
}

int getSumTileCnt() {
	int cnt = 0;
	// ��� ���� Ÿ�� ���� ���ϱ�
	for (int i = 4; i <= 9; i++) {
		for (int j = 0; j <= 3; j++) {
			if (board[i][j]) cnt++;
		}
	}
	// ���� ���� Ÿ�� ���� ���ϱ�
	for (int j = 4; j <= 9; j++) {
		for (int i = 0; i <= 3; i++) {
			if (board[i][j]) cnt++;
		}
	}
	return cnt;
}

void printBoardStatus(int i) {
	printf("\n******************%d ��° ��ǥ************************\n", i);
	for (int i = 0;i < 10; i++) {
		for (int j = 0; j < 10; j++) {
			printf("%d ", board[i][j]);
		}
		printf("\n");
	}
	printf("YellowBoard �� ���� �� �ִ� ����: 0 => %d / 1 => %d / 2 => %d / 3 => %d\n", edgeYellow[0], edgeYellow[1], edgeYellow[2], edgeYellow[3]);
	printf("RedBoard �� ���� �� �ִ� ����: 0 => %d / 1 => %d / 2 => %d / 3 => %d\n", edgeRed[0], edgeRed[1], edgeRed[2], edgeRed[3]);
	printf("\n******************************************\n");
}

int main() {
	
	init();

	scanf("%d", &k);

	for (int i = 0; i < k; i++) {
		scanf("%d %d %d", &t, &blueR, &blueC);
		if (i == 0) {
			pushTile(); // ó������ Ÿ�� �о� �ֱ⸸ ����!
			printBoardStatus(i);
			continue;
		}
		updateScore(); // ���� ������Ʈ
		printf("�ĳĳ�1");
		removeTile(); // ���ѻ� ���� ���� �ݿ��ؼ� Ÿ�� ����
		printf("�ĳĳ�2");
		pushTile(); // ���, ���� ���忡 Ÿ�� �о�ֱ�
		printf("�ĳĳ�3");
		printBoardStatus(i);
	}

	printf("%d\n", score);
	printf("%d\n", getSumTileCnt());
	
	return 0;
}