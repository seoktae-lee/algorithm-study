import java.util.*;

class Exercise {
    // Q1. 행렬의 덧셈 (같은 크기)
    int[][] addMatrix(int[][] a, int[][] b) {
        // TODO 여기를 채우세요
        return new int[0][0];
    }

    // Q2. 제일 작은 수 제거 (원래 순서 유지). 결과가 빈 배열이면 [-1]
    int[] removeMin(int[] arr) {
        // TODO 여기를 채우세요
        return new int[0];
    }

    // Q3. 전치 행렬 (R×C → C×R)
    int[][] transpose(int[][] m) {
        // TODO 여기를 채우세요
        return new int[0][0];
    }

    // Q4. 누적합 배열 p[i] = a[0] + ... + a[i]
    int[] prefixSum(int[] a) {
        // TODO 여기를 채우세요
        return new int[0];
    }

    // Q5. 시계방향 90° 회전 (직사각형도 가능)
    int[][] rotate90(int[][] m) {
        // TODO 여기를 채우세요
        return new int[0][0];
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
