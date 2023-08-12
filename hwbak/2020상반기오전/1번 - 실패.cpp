#include<iostream>
#include<memory.h>
#include<vector>

using namespace std;

int k, t, blueR, blueC;
int score;
bool board[11][11]; // 노랑보드 행 4~9, 열 0~3 // 빨강 보드 행 0~3, 열 4~9 / true: 타일 있음 / false: 빈칸
bool copyedBoard[11][11]; // 값 옮길 때 사용할 배열
int edgeYellow[4]; // 각 열에 대한 현재 행 높이. 값 10은 칸이 비었다는 뜻. 값 4, 5가 연한 부분임. 값 4가 가장 높음
int edgeRed[4]; // 각 행에 대한 현재 열 높이. 값 10은 칸이 비었다는 뜻. 값 4, 5가 연한 부분임. 값 4가 가장 높음
vector<pair<int, int>> tile; // 파랑보드 상 타일 좌표

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
	updateTile(); // 타입에 맞게 타일 좌표 업데이트
	for (int i = 0; i < tile.size(); i++) {
		pushToYellow(tile[i].first, tile[i].second); // 노랑 보드 쪽으로 밀기
		pushToRed(tile[i].first, tile[i].second); // 빨강 보드 쪽으로 밀기
	}
}

void updateYellowBoard(int r) { // r행에서 득점 일어남
	copyBoard(board, copyedBoard);
	// 4행 ~ r-1행까지 한칸씩 아래로 밀기
	for (int i = 4; i <= r-1; i++) {
		for (int j = 0; j <= 3; j++) {
			board[i][j] = copyedBoard[i - 1][j];
		}
	}
	// 각 열의 최대 행 높이 업데이트
	for (int j = 0; j <= 3; j++) {
		for (int i = 4; i <= 9; i++) {
			if (board[i][j]) { // 처음 true가 나오는 좌표가 해당 열에서 가장 
				edgeYellow[j] = i;
				break;
			}
		}
	}
}

void updateRedBoard(int c) { // c행에서 득점 일어남
	copyBoard(board, copyedBoard);
	// 4열 ~ c-1열까지 한칸씩 아래로 밀기
	for (int j = 4; j <= c-1; j++) {
		for (int i = 0; i <= 3; i++) {
			board[i][j] = copyedBoard[i][j-1];
		}
	}
	// 각 행의 최대 열 높이 업데이트
	for (int i = 0; i <= 3; i++) {
		for (int j = 4; j <= 9; j++) {
			if (board[i][j]) { // 처음 true가 나오는 좌표가 해당 열에서 가장 
				edgeYellow[i] = j;
				break;
			}
		}
	}
}

void updateScore() {
	// 노란보드에선 한 행이 꽉 차면 득점
	bool flag_yellow;
	bool flag_red;
	while (true) {
		printf("냐? score = %d\n", score);
		// 노랑 보드 쪽 득점 체크하기
		for (int i = 4; i <= 9; i++) {
			flag_yellow = true;
			for (int j = 0; j <= 3; j++) {
				if (!board[i][j]) flag_yellow = false; // 노랑보드 i행이 꽉 차있지 않음!
			}
			if (flag_yellow) { // 노랑보드 쪽에서 득점 성공
				score++;
				updateYellowBoard(i);
				i--; // 업데이트 된 보드에서 같은 행에서 또 다시 득점을 얻을 수 있는지 확인
			}
			else continue; // 득점 실패
		}
		// 빨강 보드 쪽 득점 체크하기
		for (int j = 4; j <= 9; j++) {
			flag_red = true;
			for (int i = 0; i <= 3; i++) {
				if (!board[i][j]) flag_red = false; // 빨강보드 j열이 꽉 차있지 않음!
			}
			if (flag_red) { // 빨강보드 쪽에서득점 성공
				score++;
				updateRedBoard(j);
				j--; // 업데이트 된 보드에서 같은 열에서 또 다시 득점을 얻을 수 있는 지 확인.
			}
			else continue; // 득점 실패
		}
	}

}

void removeTile() {
	int cnt = 0;
	// 연한 노랑 보드 - 맨 밑 행이 cnt개수 만큼 제거(cnt는 서로 다른 행 개수)
	for (int i = 4; i <= 5; i++) {
		for (int j = 0; j <= 3; j++) {
			if (board[i][j]) {
				cnt++;
				break;
			}
		}
	}
	while (cnt--) updateYellowBoard(9);
	 
	// 연한 빨강 보드 - 맨 오른쪽 열이 cnt개수 만큼 제거(cnt는 서로 다른 열 개수)

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
	// 노랑 보드 타일 개수 구하기
	for (int i = 4; i <= 9; i++) {
		for (int j = 0; j <= 3; j++) {
			if (board[i][j]) cnt++;
		}
	}
	// 빨강 보드 타일 개수 구하기
	for (int j = 4; j <= 9; j++) {
		for (int i = 0; i <= 3; i++) {
			if (board[i][j]) cnt++;
		}
	}
	return cnt;
}

void printBoardStatus(int i) {
	printf("\n******************%d 번째 좌표************************\n", i);
	for (int i = 0;i < 10; i++) {
		for (int j = 0; j < 10; j++) {
			printf("%d ", board[i][j]);
		}
		printf("\n");
	}
	printf("YellowBoard 각 열의 행 최대 높이: 0 => %d / 1 => %d / 2 => %d / 3 => %d\n", edgeYellow[0], edgeYellow[1], edgeYellow[2], edgeYellow[3]);
	printf("RedBoard 각 열의 행 최대 높이: 0 => %d / 1 => %d / 2 => %d / 3 => %d\n", edgeRed[0], edgeRed[1], edgeRed[2], edgeRed[3]);
	printf("\n******************************************\n");
}

int main() {
	
	init();

	scanf("%d", &k);

	for (int i = 0; i < k; i++) {
		scanf("%d %d %d", &t, &blueR, &blueC);
		if (i == 0) {
			pushTile(); // 처음에는 타일 밀어 넣기만 실행!
			printBoardStatus(i);
			continue;
		}
		updateScore(); // 점수 업데이트
		printf("냐냐냐1");
		removeTile(); // 연한색 보드 상태 반영해서 타일 제거
		printf("냐냐냐2");
		pushTile(); // 노랑, 빨강 보드에 타일 밀어넣기
		printf("냐냐냐3");
		printBoardStatus(i);
	}

	printf("%d\n", score);
	printf("%d\n", getSumTileCnt());
	
	return 0;
}