import java.util.*;

class Exercise {
    int[] dr = {-1, 1, 0, 0}, dc = {0, 0, -1, 1};

    // Q1. 게임 맵 최단거리: (0,0)에서 (R-1,C-1)까지 지나가는 칸 수의 최솟값(시작·도착 칸 포함), 불가능하면 -1
    //     maps: 1 = 길, 0 = 벽
    int shortestMap(int[][] maps) {
        // ▼ answer
        int R = maps.length, C = maps[0].length;
        int[][] dist = new int[R][C];
        for (int[] row : dist) Arrays.fill(row, -1);
        Queue<int[]> q = new ArrayDeque<>();
        q.offer(new int[]{0, 0});
        dist[0][0] = 1;
        while (!q.isEmpty()) {
            int[] cur = q.poll();
            for (int d = 0; d < 4; d++) {
                int nr = cur[0] + dr[d], nc = cur[1] + dc[d];
                if (nr < 0 || nc < 0 || nr >= R || nc >= C) continue;
                if (maps[nr][nc] == 0 || dist[nr][nc] != -1) continue;
                dist[nr][nc] = dist[cur[0]][cur[1]] + 1;
                q.offer(new int[]{nr, nc});
            }
        }
        return dist[R - 1][C - 1];
        // ▲ answer
        // TODO: return 0;
    }

    // Q2. 네트워크: 인접 행렬 computers (computers[i][j] == 1이면 연결) → 네트워크(연결 요소) 개수
    int network(int n, int[][] computers) {
        // ▼ answer
        boolean[] visited = new boolean[n];
        int cnt = 0;
        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                dfs(i, computers, visited);
                cnt++;
            }
        }
        return cnt;
        // ▲ answer
        // TODO: return 0;
    }

    // ▼ answer
    void dfs(int u, int[][] g, boolean[] visited) {
        visited[u] = true;
        for (int v = 0; v < g.length; v++) {
            if (g[u][v] == 1 && !visited[v]) dfs(v, g, visited);
        }
    }
    // ▲ answer

    // Q3. 섬의 개수: grid의 '1'이 상하좌우로 이어진 덩어리 수
    int islands(String[] grid) {
        // ▼ answer
        int R = grid.length, C = grid[0].length();
        boolean[][] seen = new boolean[R][C];
        int cnt = 0;
        for (int r = 0; r < R; r++)
            for (int c = 0; c < C; c++) {
                if (grid[r].charAt(c) != '1' || seen[r][c]) continue;
                cnt++;
                Queue<int[]> q = new ArrayDeque<>();
                q.offer(new int[]{r, c});
                seen[r][c] = true;
                while (!q.isEmpty()) {
                    int[] cur = q.poll();
                    for (int d = 0; d < 4; d++) {
                        int nr = cur[0] + dr[d], nc = cur[1] + dc[d];
                        if (nr < 0 || nc < 0 || nr >= R || nc >= C) continue;
                        if (grid[nr].charAt(nc) != '1' || seen[nr][nc]) continue;
                        seen[nr][nc] = true;
                        q.offer(new int[]{nr, nc});
                    }
                }
            }
        return cnt;
        // ▲ answer
        // TODO: return 0;
    }

    // Q4. 무방향 그래프(노드 1..n)에서 start로부터의 최단 간선 수. 도달 불가 -1. 결과는 노드 1..n 순서
    int[] distancesFrom(int n, int[][] edges, int start) {
        // ▼ answer
        List<List<Integer>> g = new ArrayList<>();
        for (int i = 0; i <= n; i++) g.add(new ArrayList<>());
        for (int[] e : edges) {
            g.get(e[0]).add(e[1]);
            g.get(e[1]).add(e[0]);
        }
        int[] dist = new int[n + 1];
        Arrays.fill(dist, -1);
        Queue<Integer> q = new ArrayDeque<>();
        q.offer(start);
        dist[start] = 0;
        while (!q.isEmpty()) {
            int u = q.poll();
            for (int v : g.get(u)) {
                if (dist[v] != -1) continue;
                dist[v] = dist[u] + 1;
                q.offer(v);
            }
        }
        return Arrays.copyOfRange(dist, 1, n + 1);
        // ▲ answer
        // TODO: return new int[0];
    }

    public static void main(String[] args) {
        Exercise e = new Exercise();
        Check.run("Q1 shortestMap 11", () -> e.shortestMap(new int[][]{{1, 0, 1, 1, 1}, {1, 0, 1, 0, 1}, {1, 0, 1, 1, 1}, {1, 1, 1, 0, 1}, {0, 0, 0, 0, 1}}), 11);
        Check.run("Q1 shortestMap 불가능", () -> e.shortestMap(new int[][]{{1, 0, 1, 1, 1}, {1, 0, 1, 0, 1}, {1, 0, 1, 1, 1}, {1, 1, 1, 0, 0}, {0, 0, 0, 0, 1}}), -1);
        Check.run("Q2 network 2", () -> e.network(3, new int[][]{{1, 1, 0}, {1, 1, 0}, {0, 0, 1}}), 2);
        Check.run("Q2 network 1", () -> e.network(3, new int[][]{{1, 1, 0}, {1, 1, 1}, {0, 1, 1}}), 1);
        Check.run("Q3 islands", () -> e.islands(new String[]{"11000", "11000", "00100", "00011"}), 3);
        Check.run("Q3 islands 0", () -> e.islands(new String[]{"000"}), 0);
        Check.run("Q4 distancesFrom", () -> e.distancesFrom(5, new int[][]{{1, 2}, {1, 3}, {2, 4}}, 1), new int[]{0, 1, 1, 2, -1});
        Check.run("Q4 distancesFrom 사이클", () -> e.distancesFrom(4, new int[][]{{1, 2}, {2, 3}, {3, 4}, {4, 1}}, 2), new int[]{1, 0, 1, 2});
        Check.done();
    }
}
