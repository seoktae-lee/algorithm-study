import java.util.*;

class Exercise {
    // Q1. arr 중 divisor로 나누어 떨어지는 값을 오름차순으로. 하나도 없으면 [-1]
    int[] divisible(int[] arr, int divisor) {
        // TODO 여기를 채우세요
        return new int[0];
    }

    // Q2. 글자를 큰 것부터 작은 순으로 정렬 (대문자는 소문자보다 작은 것으로 간주 = 유니코드 순)
    String sortDesc(String s) {
        // TODO 여기를 채우세요
        return "";
    }

    // Q3. K번째수: 각 command [i, j, k] → array의 i~j번째(1부터)를 잘라 정렬했을 때 k번째 수
    int[] kth(int[] array, int[][] commands) {
        // TODO 여기를 채우세요
        return new int[0];
    }

    // Q4. int 배열 내림차순 (원본은 바꾸지 말고 새 배열 반환)
    int[] sortDescInt(int[] a) {
        // TODO 여기를 채우세요
        return a;
    }

    // Q5. 예산: 부서별 신청액 d, 총예산 budget → 신청액 전액을 지원할 수 있는 최대 부서 수
    int budget(int[] d, int budget) {
        // TODO 여기를 채우세요
        return 0;
    }

    public static void main(String[] args) {
        Exercise e = new Exercise();
        Check.run("Q1 divisible([5,9,7,10], 5)", () -> e.divisible(new int[]{5, 9, 7, 10}, 5), new int[]{5, 10});
        Check.run("Q1 divisible([2,36,1,3], 1)", () -> e.divisible(new int[]{2, 36, 1, 3}, 1), new int[]{1, 2, 3, 36});
        Check.run("Q1 divisible([3,2,6], 10)", () -> e.divisible(new int[]{3, 2, 6}, 10), new int[]{-1});
        Check.run("Q2 sortDesc(\"Zbcdefg\")", () -> e.sortDesc("Zbcdefg"), "gfedcbZ");
        Check.run("Q3 kth", () -> e.kth(new int[]{1, 5, 2, 6, 3, 7, 4}, new int[][]{{2, 5, 3}, {4, 4, 1}, {1, 7, 3}}), new int[]{5, 6, 3});
        int[] orig = {3, 1, 2};
        Check.run("Q4 sortDescInt([3,1,2])", () -> e.sortDescInt(orig), new int[]{3, 2, 1});
        Check.run("Q4 원본 유지", () -> orig, new int[]{3, 1, 2});
        Check.run("Q5 budget([1,3,2,5,4], 9)", () -> e.budget(new int[]{1, 3, 2, 5, 4}, 9), 3);
        Check.run("Q5 budget([2,2,3,3], 10)", () -> e.budget(new int[]{2, 2, 3, 3}, 10), 4);
        Check.done();
    }
}
