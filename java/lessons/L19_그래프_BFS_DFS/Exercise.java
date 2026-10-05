import java.util.*;

class Exercise {
    int[] dr = {-1, 1, 0, 0}, dc = {0, 0, -1, 1};

    // Q1. 게임 맵 최단거리: (0,0)에서 (R-1,C-1)까지 지나가는 칸 수의 최솟값(시작·도착 칸 포함), 불가능하면 -1
    //     maps: 1 = 길, 0 = 벽
    int shortestMap(int[][] maps) {
        // TODO 여기를 채우세요
        return 0;
    }

    // Q2. 네트워크: 인접 행렬 computers (computers[i][j] == 1이면 연결) → 네트워크(연결 요소) 개수
    int network(int n, int[][] computers) {
        // TODO 여기를 채우세요
        return 0;
    }

    // (필요하면 여기에 도우미 메서드를 만드세요)

    // Q3. 섬의 개수: grid의 '1'이 상하좌우로 이어진 덩어리 수
    int islands(String[] grid) {
        // TODO 여기를 채우세요
        return 0;
    }

    // Q4. 무방향 그래프(노드 1..n)에서 start로부터의 최단 간선 수. 도달 불가 -1. 결과는 노드 1..n 순서
    int[] distancesFrom(int n, int[][] edges, int start) {
        // TODO 여기를 채우세요
        return new int[0];
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
