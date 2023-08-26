#include <iostream>
#include <memory.h>
#include <vector>

using namespace std;

struct Atom {
    int r, c;
    int mass;
    int speed;
    int dir;
    Atom(int r, int c, int mass, int speed, int dir) : r(r), c(c), mass(mass), speed(speed), dir(dir) {}
};

vector<Atom> map[51][51];
vector<Atom> tmp_map[51][51];
int n, m, k;
int x, y, mm, s, d;
int dr[8] = { -1,-1,0,1,1,1,0,-1 };
int dc[8] = { 0,1,1,1,0,-1,-1,-1 };



void input() {
    scanf("%d %d %d", &n, &m, &k);
    for (int i = 0; i < m; i++) {
        scanf("%d %d %d %d %d", &x, &y, &mm, &s, &d);
        map[x][y].push_back(Atom(x, y, mm, s, d));
    }
}

void initMap(vector<Atom>(*initMap)[51]) {
    for (int i = 0; i <= n; i++) {
        for (int j = 0; j <= n; j++) {
            initMap[i][j].clear();
        }
    }
}

void init() {
    initMap(map);
    initMap(tmp_map);
}

void copyMap(vector<Atom>(*origin)[51], vector<Atom>(*tmp)[51]) {
    initMap(map);
    for (int r = 1; r <= n; r++) {
        for (int c = 1; c <= n; c++) {
            if (tmp[r][c].size() == 0) continue;
            for (int i = 0; i < tmp[r][c].size(); i++) {
                origin[r][c].push_back(tmp[r][c][i]);
            }
        }
    }
}

void moveAtom() {
    // tmp_map �ʱ�ȭ
    initMap(tmp_map);
    for (int r = 1; r <= n; r++) {
        for (int c = 1; c <= n; c++) {
            if (map[r][c].size() == 0) continue;
            for (int i = 0; i < map[r][c].size(); i++) {
                Atom atom = map[r][c][i];
                // ���� 0�̸� �����
                if (atom.mass == 0) continue;
                int speed = atom.speed;
                int dir = atom.dir;
                int nr = (r + dr[dir] * speed + n * speed) % n + 1;
                int nc = (c + dc[dir] * speed + n * speed) % n + 1;
                map[r][c][i].r = nr;
                map[r][c][i].c = nc;
                tmp_map[nr][nc].push_back(atom);
            }
        }
    }
    // �̵��� ���� �� tmp_map�� map�� �����Ų��.
    copyMap(map, tmp_map);
}

void AddAndDivideAtom(int r, int c) {
    int update_mass = 0;
    int update_speed = 0;
    int cnt_udlr = 0; // �����¿� ���� ����
    int cnt_cross = 0;
    // ��ģ��.
    for (int i = 0; i < map[r][c].size(); i++) {
        update_mass += map[r][c][i].mass;
        update_speed += map[r][c][i].speed;
        // �����¿�
        if (map[r][c][i].dir % 2 == 0) cnt_udlr++;
        else cnt_cross++;
    }
    update_mass /= 5;
    update_speed /= map[r][c].size();
    // 4���� ������.
    map[r][c].clear();
    if (update_mass == 0) return; // ���� 0�̸� �Լ� ������
    int next_dir = cnt_udlr == map[r][c].size() || cnt_cross == map[r][c].size() ? 0 : 1; // 2�� ���ϸ��.
    for (int i = 0; i < 4; i++) {
        map[r][c].push_back(Atom(r, c, update_mass, update_speed, next_dir));
        next_dir += 2;
    }

}

int getTotalMass() {
    int sum = 0;
    for (int r = 1; r <= n; r++) {
        for (int c = 1; c <= n; c++) {
            if (map[r][c].size() == 0) continue;
            for (int i = 0; i < map[r][c].size(); i++) {
                sum += map[r][c][i].mass;
            }
        }
    }
    return sum;
}

int main() {

    init();
    input();

    while (k--) {
        moveAtom();
        for (int r = 1; r <= n; r++) {
            for (int c = 1; c <= n; c++) {
                if (map[r][c].size() < 2) continue;
                AddAndDivideAtom(r, c); // (i,j) ��ġ�� ���ڵ��� ��ġ�� �����Ѵ�.
            }
        }
    }

    printf("%d", getTotalMass());

    return 0;

}