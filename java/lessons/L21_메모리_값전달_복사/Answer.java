import java.util.*;

class Exercise {
    // Q1. 2차원 배열 깊은 복사 (복사본을 바꿔도 원본은 그대로여야 함)
    int[][] deepCopy(int[][] a) {
        // ▼ answer
        int[][] d = new int[a.length][];
        for (int i = 0; i < a.length; i++) d[i] = a[i].clone();
        return d;
        // ▲ answer
        // TODO: return a.clone();
    }

    // Q2. 배열의 모든 원소에 1을 더하기 (반환 없이 원본을 수정)
    void addOne(int[] a) {
        // ▼ answer
        for (int i = 0; i < a.length; i++) a[i]++;
        // ▲ answer
        // TODO:
    }

    // Q3. 왼쪽으로 k칸 회전한 "새 배열" (원본은 그대로)  [1,2,3,4,5], 2 → [3,4,5,1,2]
    int[] rotateLeftCopy(int[] a, int k) {
        // ▼ answer
        int n = a.length;
        int[] r = new int[n];
        for (int i = 0; i < n; i++) r[i] = a[(i + k) % n];
        return r;
        // ▲ answer
        // TODO: return a;
    }

    // Q4. 모든 부분집합 (DFS 순서: [], [1], [1,2], [2] …) — 결과에 리스트를 넣을 때 복사가 핵심
    List<List<Integer>> subsets(int[] nums) {
        // ▼ answer
        List<List<Integer>> result = new ArrayList<>();
        dfs(nums, 0, new ArrayList<>(), result);
        return result;
        // ▲ answer
        // TODO: return new ArrayList<>();
    }

    // ▼ answer
    void dfs(int[] nums, int start, List<Integer> cur, List<List<Integer>> result) {
        result.add(new ArrayList<>(cur));
        for (int i = start; i < nums.length; i++) {
            cur.add(nums[i]);
            dfs(nums, i + 1, cur, result);
            cur.remove(cur.size() - 1);
        }
    }
    // ▲ answer

    public static void main(String[] args) {
        Exercise e = new Exercise();
        Check.run("Q1 deepCopy 값", () -> e.deepCopy(new int[][]{{1, 2}, {3, 4}}), new int[][]{{1, 2}, {3, 4}});
        Check.run("Q1 deepCopy 독립성", () -> {
            int[][] orig = {{1, 2}, {3, 4}};
            int[][] c = e.deepCopy(orig);
            c[0][0] = 99;
            return orig[0][0];
        }, 1);
        Check.run("Q2 addOne 원본 수정", () -> {
            int[] a = {1, 2, 3};
            e.addOne(a);
            return a;
        }, new int[]{2, 3, 4});
        Check.run("Q3 rotateLeftCopy", () -> e.rotateLeftCopy(new int[]{1, 2, 3, 4, 5}, 2), new int[]{3, 4, 5, 1, 2});
        Check.run("Q3 원본 유지", () -> {
            int[] a = {1, 2, 3};
            e.rotateLeftCopy(a, 1);
            return a;
        }, new int[]{1, 2, 3});
        Check.run("Q4 subsets([1,2])", () -> e.subsets(new int[]{1, 2}), List.of(List.of(), List.of(1), List.of(1, 2), List.of(2)));
        Check.run("Q4 subsets([1,2,3]) 개수", () -> e.subsets(new int[]{1, 2, 3}).size(), 8);
        Check.done();
    }
}
