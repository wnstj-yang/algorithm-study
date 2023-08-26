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
    // tmp_map 초기화
    initMap(tmp_map);
    for (int r = 1; r <= n; r++) {
        for (int c = 1; c <= n; c++) {
            if (map[r][c].size() == 0) continue;
            for (int i = 0; i < map[r][c].size(); i++) {
                Atom atom = map[r][c][i];
                // 질량 0이면 사라져
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
    // 이동이 끝난 후 tmp_map을 map에 복사시킨다.
    copyMap(map, tmp_map);
}

void AddAndDivideAtom(int r, int c) {
    int update_mass = 0;
    int update_speed = 0;
    int cnt_udlr = 0; // 상하좌우 개수 세기
    int cnt_cross = 0;
    // 합친다.
    for (int i = 0; i < map[r][c].size(); i++) {
        update_mass += map[r][c][i].mass;
        update_speed += map[r][c][i].speed;
        // 상하좌우
        if (map[r][c][i].dir % 2 == 0) cnt_udlr++;
        else cnt_cross++;
    }
    update_mass /= 5;
    update_speed /= map[r][c].size();
    // 4개로 나눈다.
    map[r][c].clear();
    if (update_mass == 0) return; // 질량 0이면 함수 끝내기
    int next_dir = cnt_udlr == map[r][c].size() || cnt_cross == map[r][c].size() ? 0 : 1; // 2씩 더하면됨.
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
                AddAndDivideAtom(r, c); // (i,j) 위치의 원자들을 합치고 분할한다.
            }
        }
    }

    printf("%d", getTotalMass());

    return 0;

}