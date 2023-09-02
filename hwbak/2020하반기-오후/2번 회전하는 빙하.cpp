#include <iostream>
#include <tuple>
#include <queue>
#include <vector>

#define MAX_N 6
#define MAX_Q 1000
#define MAX_GRID_SIZE 64
#define DIR_NUM 4

using namespace std;

int n, q;
int grid_size;

int grid[MAX_GRID_SIZE][MAX_GRID_SIZE];
int next_grid[MAX_GRID_SIZE][MAX_GRID_SIZE];

queue<pair<int, int> > bfs_q;
bool visited[MAX_GRID_SIZE][MAX_GRID_SIZE];

// ������ ���ǻ� ������, �Ʒ�, ��, ���� ������� �����մϴ�. 
int dx[DIR_NUM] = { 0, 1, -1, 0 };
int dy[DIR_NUM] = { 1, 0, 0, -1 };

bool InRange(int x, int y) {
    return 0 <= x && x < grid_size && 0 <= y && y < grid_size;
}

bool CanGo(int x, int y) {
    return InRange(x, y) && !visited[x][y] && grid[x][y];
}

// BFS�� ������ ���� �ش� �׷��� ũ�⸦ ��ȯ�մϴ�.
int BFS() {
    int group_size = 0;

    // BFS Ž���� �����մϴ�.
    while (!bfs_q.empty()) {
        pair<int, int> curr_pos = bfs_q.front();
        int curr_x, curr_y;
        tie(curr_x, curr_y) = curr_pos;
        group_size++;
        bfs_q.pop();

        for (int i = 0; i < DIR_NUM; i++) {
            int new_x = curr_x + dx[i];
            int new_y = curr_y + dy[i];

            if (CanGo(new_x, new_y)) {
                bfs_q.push(make_pair(new_x, new_y));
                visited[new_x][new_y] = true;
            }
        }
    }

    return group_size;
}

// �����ִ� ������ �� ���� ����մϴ�.
int GetNumOfIces() {
    int cnt = 0;
    for (int i = 0; i < grid_size; i++)
        for (int j = 0; j < grid_size; j++)
            cnt += grid[i][j];

    return cnt;
}

// ���� ���� �� �ִ� ũ�⸦ ���մϴ�.
int GetBiggestSize() {
    int max_size = 0;
    for (int i = 0; i < grid_size; i++)
        for (int j = 0; j < grid_size; j++)
            if (grid[i][j] && !visited[i][j]) {
                // ���� ��ġ�� queue�� �ְ� BFS�� �����մϴ�.
                // bfs ���� ���� ���� �׷��� ũ�� �� �ִ��� ã���ϴ�.
                visited[i][j] = true;
                bfs_q.push(make_pair(i, j));
                max_size = max(max_size, BFS());
            }

    return max_size;
}

// (start_row, start_col)���� half_size ũ���� ���ڸ� 
// move_dir �������� �̵��մϴ�.
void Move(int start_row, int start_col, int half_size, int move_dir) {
    for (int row = start_row; row < start_row + half_size; row++)
        for (int col = start_col; col < start_col + half_size; col++) {
            int next_row = row + dx[move_dir] * half_size;
            int next_col = col + dy[move_dir] * half_size;

            next_grid[next_row][next_col] = grid[row][col];
        }
}

void Rotate(int level) {
    // Step1.
    // rotate ������ ���¸� ������
    // �迭�� 0���� �ʱ�ȭ�մϴ�.
    for (int i = 0; i < grid_size; i++)
        for (int j = 0; j < grid_size; j++)
            next_grid[i][j] = 0;

    int box_size = (1 << level);
    int half_size = box_size / 2;

    // Step2. ���ǿ� �°� ȸ���� �����մϴ�.

    // Step2-1. ȸ���� 2^L * 2^L ũ�� ������ ���� �� �𼭸� ��ġ�� ����ϴ�.
    for (int i = 0; i < grid_size; i += box_size)
        for (int j = 0; j < grid_size; j += box_size) {
            // Step2-2. ���������ϴ� 2^(L - 1) * 2^(L - 1) ũ�� ������
            //          ���� �� �𼭸��� ���� ���
            //          �˸��� �������� �̵���ŵ�ϴ�.
            Move(i, j, half_size, 0);
            Move(i, j + half_size, half_size, 1);
            Move(i + half_size, j, half_size, 2);
            Move(i + half_size, j + half_size, half_size, 3);
        }

    // Step3.
    // rotate ������ ����� �ٽ�
    // grid �迭�� �����ɴϴ�.
    for (int i = 0; i < grid_size; i++)
        for (int j = 0; j < grid_size; j++)
            grid[i][j] = next_grid[i][j];
}

// ������ ���� �ִ� ������ ���� ���ϴ�.
int GetNeighborNums(int curr_x, int curr_y) {
    int cnt = 0;
    for (int i = 0; i < DIR_NUM; i++) {
        int new_x = curr_x + dx[i];
        int new_y = curr_y + dy[i];

        if (InRange(new_x, new_y) && grid[new_x][new_y])
            cnt++;
    }

    return cnt;
}

void Melt() {
    // Step1.
    // ���� ������ ���¸� ������
    // �迭�� 0���� �ʱ�ȭ�մϴ�.
    for (int i = 0; i < grid_size; i++)
        for (int j = 0; j < grid_size; j++)
            next_grid[i][j] = 0;

    // Step2.
    // ������ ĭ�� ���� 3�� ������ ���� ������ 
    // ã�� 1�� ���Դϴ�.

    for (int i = 0; i < grid_size; i++)
        for (int j = 0; j < grid_size; j++) {
            int cnt = GetNeighborNums(i, j);
            // Step2-1. ��°�쿡�� 1�� ���� �־��ݴϴ�.
            if (grid[i][j] && cnt < 3)
                next_grid[i][j] = grid[i][j] - 1;
            // Step2-2. ���� �ʴ� ��쿡�� �״�� �־��ݴϴ�.
            else
                next_grid[i][j] = grid[i][j];
        }

    // Step3.
    // ���� ������ ����� �ٽ�
    // grid �迭�� �����ɴϴ�.
    for (int i = 0; i < grid_size; i++)
        for (int j = 0; j < grid_size; j++)
            grid[i][j] = next_grid[i][j];
}

int main() {
    cin >> n >> q;
    grid_size = (1 << n);

    for (int i = 0; i < grid_size; i++)
        for (int j = 0; j < grid_size; j++)
            cin >> grid[i][j];

    // q���� ���� ȸ���� ��� ������ �����մϴ�.
    while (q--) {
        int level;
        cin >> level;

        if (level)
            Rotate(level);

        Melt();
    }

    cout << GetNumOfIces() << endl;
    cout << GetBiggestSize();
    return 0;
}