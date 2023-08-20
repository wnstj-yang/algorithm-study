// 1시간 40분 소요
// 12ms


#include <iostream>
#include <vector>
#include <memory.h>
#include <queue>

#define INF 2147483647

using namespace std;

struct Info {
    int id, dist, r, c;
    Info(int id, int dist, int r, int c) : id(id), dist(dist), r(r), c(c) {}
};

struct cmp {
    bool operator()(Info& a, Info& b) {
        if (a.dist > b.dist) return true;
        else if (a.dist == b.dist) {
            if (a.r > b.r) return true;
            else if (a.r == b.r) return a.c > b.c;
            else return false;
        }
        else return false;
    }
};

struct Taxi {
    int r, c;
    int battery;
};

int n, m, c;
int road[21][21];
int dist[21][21]; // 현재거리에서 다른 칸까지 최소 거리 저장
bool visited[21][21];
bool complete[400];
int dr[4] = { 0,0,1,-1 };
int dc[4] = { 1,-1,0,0 };
Taxi taxi;
vector<pair<int, int>> start; // 승객 출발지
vector<pair<int, int>> destination; // 승객 도착지


void init() {
    memset(road, 0, sizeof(road));
    memset(dist, 0, sizeof(dist));
    memset(complete, false, sizeof(complete));
}

void input() {
    scanf("%d %d %d", &n, &m, &c);
    taxi.battery = c;
    vector<pair<int, int>> tmp_start(m);
    vector<pair<int, int>> tmp_destination(m);
    start = tmp_start;
    destination = tmp_destination;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            scanf("%d", &road[i][j]);
        }
    }
    scanf("%d %d", &taxi.r, &taxi.c);
    for (int i = 0; i < m; i++) {
        scanf("%d %d %d %d", &start[i].first, &start[i].second, &destination[i].first, &destination[i].second);
    }
}

bool isRange(int r, int c) {
    return r >= 1 && r <= n && c >= 1 && c <= n;
}

void bfs() {
    for (int i = 0; i <= n; i++) {
        for (int j = 0; j <= n; j++) {
            dist[i][j] = INF;
            visited[i][j] = false;
        }
    }
    queue<pair<int, int>> q;
    q.push(make_pair(taxi.r, taxi.c));
    dist[taxi.r][taxi.c] = 0;
    visited[taxi.r][taxi.c] = true;
    while (!q.empty()) {
        int r = q.front().first;
        int c = q.front().second;
        q.pop();
        for (int i = 0; i < 4; i++) {
            int nr = r + dr[i];
            int nc = c + dc[i];
            if (isRange(nr, nc) && road[nr][nc] == 0 && !visited[nr][nc] && dist[nr][nc] > dist[r][c] + 1) {
                visited[nr][nc] = true;
                dist[nr][nc] = dist[r][c] + 1;
                q.push(make_pair(nr, nc));
            }
        }
    }

}

Info getPriorityGuest() {
    priority_queue<Info, vector<Info>, cmp> pq;
    for (int i = 0; i < m; i++) {
        if (complete[i]) continue;
        int r = start[i].first;
        int c = start[i].second;
        pq.push(Info(i,dist[r][c], r, c));
    }
    return pq.top();
}

int main() {

    init();
    input();

    for (int i = 0; i < m; i++) { 
        bfs(); // 택시 현재 위치에서 모든 칸까지의 최소 거리 구하기
        Info guest = getPriorityGuest(); // 1순위 손님 인덱스
        // 손님 출발지까지 가기엔 배터리가 부족. 즉시 종료~!
        if (taxi.battery - guest.dist < 0) {
            printf("-1");
            exit(0);
        }
        else {
            // 손님 출발지점까지 이동해서 배터리 소모됨.
            taxi.battery -= guest.dist;
            //taxi.battery += 2 * diff;
            taxi.r = guest.r;
            taxi.c = guest.c;
        }
        bfs(); // 다시 bfs돌려서 택시 현재 위치에서 모든 칸가지의 최소 거리 구하기
        int r = destination[guest.id].first;
        int c = destination[guest.id].second;
        if (taxi.battery - dist[r][c] < 0) {
            printf("-1");
            exit(0);
        }
        else {
            taxi.battery += dist[r][c];
            taxi.r = r;
            taxi.c = c;
            complete[guest.id] = true;
        }
    }
   
    printf("%d", taxi.battery);

    return 0;

}