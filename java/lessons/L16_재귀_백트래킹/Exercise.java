import java.util.*;

class Exercise {
    int count;
    int[] nums;
    int target;

    // Q1. 타겟 넘버: 각 수에 + 또는 -를 붙여 target을 만드는 방법의 수
    int targetNumber(int[] numbers, int target) {
        // TODO 여기를 채우세요
        return 0;
    }

    // (필요하면 여기에 도우미 메서드를 만드세요)

    // Q2. 소수 만들기: 서로 다른 3개를 골라 더한 값이 소수인 경우의 수
    int primeTriples(int[] nums) {
        // TODO 여기를 채우세요
        return 0;
    }

    // (필요하면 여기에 도우미 메서드를 만드세요)

    // Q3. 서로 다른 글자로 된 정렬된 문자열의 모든 순열 (사전순)
    List<String> permutations(String s) {
        // TODO 여기를 채우세요
        return new ArrayList<>();
    }

    // (필요하면 여기에 도우미 메서드를 만드세요)

    // Q4. 피로도: 현재 피로도 k, dungeons[i] = [최소 필요 피로도, 소모 피로도] → 탐험 가능한 최대 던전 수
    int fatigue(int k, int[][] dungeons) {
        // TODO 여기를 채우세요
        return 0;
    }

    // (필요하면 여기에 도우미 메서드를 만드세요)

    // Q5. 피보나치 fib(0)=0, fib(1)=1 (n ≤ 90, 메모이제이션으로 빠르게)
    long fib(int n) {
        // TODO 여기를 채우세요
        return 0;
    }

    // (필요하면 여기에 도우미 메서드를 만드세요)

    public static void main(String[] args) {
        Exercise e = new Exercise();
        Check.run("Q1 targetNumber([1,1,1,1,1], 3)", () -> e.targetNumber(new int[]{1, 1, 1, 1, 1}, 3), 5);
        Check.run("Q1 targetNumber([4,1,2,1], 4)", () -> e.targetNumber(new int[]{4, 1, 2, 1}, 4), 2);
        Check.run("Q2 primeTriples([1,2,3,4])", () -> e.primeTriples(new int[]{1, 2, 3, 4}), 1);
        Check.run("Q2 primeTriples([1,2,7,6,4])", () -> e.primeTriples(new int[]{1, 2, 7, 6, 4}), 4);
        Check.run("Q3 permutations(\"abc\")", () -> e.permutations("abc"), List.of("abc", "acb", "bac", "bca", "cab", "cba"));
        Check.run("Q3 permutations(\"a\")", () -> e.permutations("a"), List.of("a"));
        Check.run("Q4 fatigue(80, ...)", () -> e.fatigue(80, new int[][]{{80, 20}, {50, 40}, {30, 10}}), 3);
        Check.run("Q4 fatigue(40, ...)", () -> e.fatigue(40, new int[][]{{80, 20}, {50, 40}, {30, 10}}), 1);
        Check.run("Q5 fib(10)", () -> e.fib(10), 55L);
        Check.run("Q5 fib(90)", () -> e.fib(90), 2880067194370816120L);
        Check.done();
    }
}
