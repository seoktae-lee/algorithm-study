import java.util.*;

class Exercise {
    // Q1. 행렬의 덧셈 (같은 크기)
    int[][] addMatrix(int[][] a, int[][] b) {
        // ▼ answer
        int[][] r = new int[a.length][a[0].length];
        for (int i = 0; i < a.length; i++)
            for (int j = 0; j < a[0].length; j++)
                r[i][j] = a[i][j] + b[i][j];
        return r;
        // ▲ answer
        // TODO: return new int[0][0];
    }

    // Q2. 제일 작은 수 제거 (원래 순서 유지). 결과가 빈 배열이면 [-1]
    int[] removeMin(int[] arr) {
        // ▼ answer
        if (arr.length == 1) return new int[]{-1};
        int min = Integer.MAX_VALUE;
        for (int v : arr) min = Math.min(min, v);
        int[] r = new int[arr.length - 1];
        int k = 0;
        for (int v : arr) if (v != min) r[k++] = v;
        return r;
        // ▲ answer
        // TODO: return new int[0];
    }

    // Q3. 전치 행렬 (R×C → C×R)
    int[][] transpose(int[][] m) {
        // ▼ answer
        int R = m.length, C = m[0].length;
        int[][] t = new int[C][R];
        for (int r = 0; r < R; r++)
            for (int c = 0; c < C; c++)
                t[c][r] = m[r][c];
        return t;
        // ▲ answer
        // TODO: return new int[0][0];
    }

    // Q4. 누적합 배열 p[i] = a[0] + ... + a[i]
    int[] prefixSum(int[] a) {
        // ▼ answer
        int[] p = new int[a.length];
        for (int i = 0; i < a.length; i++) p[i] = (i > 0 ? p[i - 1] : 0) + a[i];
        return p;
        // ▲ answer
        // TODO: return new int[0];
    }

    // Q5. 시계방향 90° 회전 (직사각형도 가능)
    int[][] rotate90(int[][] m) {
        // ▼ answer
        int R = m.length, C = m[0].length;
        int[][] rot = new int[C][R];
        for (int r = 0; r < R; r++)
            for (int c = 0; c < C; c++)
                rot[c][R - 1 - r] = m[r][c];
        return rot;
        // ▲ answer
        // TODO: return new int[0][0];
    }

    public static void main(String[] args) {
        Exercise e = new Exercise();
        Check.run("Q1 addMatrix", () -> e.addMatrix(new int[][]{{1, 2}, {2, 3}}, new int[][]{{3, 4}, {5, 6}}), new int[][]{{4, 6}, {7, 9}});
        Check.run("Q1 addMatrix 1×3", () -> e.addMatrix(new int[][]{{1, 2, 3}}, new int[][]{{1, 1, 1}}), new int[][]{{2, 3, 4}});
        Check.run("Q2 removeMin([4,3,2,1])", () -> e.removeMin(new int[]{4, 3, 2, 1}), new int[]{4, 3, 2});
        Check.run("Q2 removeMin([5,1,7])", () -> e.removeMin(new int[]{5, 1, 7}), new int[]{5, 7});
        Check.run("Q2 removeMin([10])", () -> e.removeMin(new int[]{10}), new int[]{-1});
        Check.run("Q3 transpose 2×3", () -> e.transpose(new int[][]{{1, 2, 3}, {4, 5, 6}}), new int[][]{{1, 4}, {2, 5}, {3, 6}});
        Check.run("Q4 prefixSum([1,2,3,4])", () -> e.prefixSum(new int[]{1, 2, 3, 4}), new int[]{1, 3, 6, 10});
        Check.run("Q5 rotate90 2×2", () -> e.rotate90(new int[][]{{1, 2}, {3, 4}}), new int[][]{{3, 1}, {4, 2}});
        Check.run("Q5 rotate90 2×3", () -> e.rotate90(new int[][]{{1, 2, 3}, {4, 5, 6}}), new int[][]{{4, 1}, {5, 2}, {6, 3}});
        Check.done();
    }
}
