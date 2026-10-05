import java.util.*;

class Exercise {
    // Q1. 제네릭 메서드: 리스트의 최댓값 (Integer, String 등 Comparable이면 무엇이든)
    static <T extends Comparable<T>> T maxOf(List<T> list) {
        // TODO 여기를 채우세요
        return null;
    }

    // Q2. 두 배열에 공통으로 들어 있는 서로 다른 값의 개수 (각 배열 최대 200,000개 → O(n)으로)
    int countCommon(int[] a, int[] b) {
        // TODO 여기를 채우세요
        return 0;
    }

    // Q3. 입력 크기 n → 허용되는 가장 느린 복잡도
    //     n ≤ 11: "O(n!)", ≤ 20: "O(2^n)", ≤ 500: "O(n^3)", ≤ 5000: "O(n^2)", ≤ 1000000: "O(n log n)", 그 외 "O(n)"
    String chooseComplexity(int n) {
        // TODO 여기를 채우세요
        return "";
    }

    public static void main(String[] args) {
        Exercise e = new Exercise();
        Check.run("Q1 maxOf([3,9,2])", () -> maxOf(List.of(3, 9, 2)), 9);
        Check.run("Q1 maxOf([b,z,a])", () -> maxOf(List.of("b", "z", "a")), "z");
        Check.run("Q2 countCommon 작은 입력", () -> e.countCommon(new int[]{1, 2, 2, 3}, new int[]{2, 3, 4}), 2);
        Check.run("Q2 countCommon 200,000개 (빨라야 함)", () -> {
            int n = 200_000;
            int[] a = new int[n], b = new int[n];
            for (int i = 0; i < n; i++) {
                a[i] = i;
                b[i] = i + 100_000;
            }
            return e.countCommon(a, b);
        }, 100_000);
        Check.run("Q3 n=10", () -> e.chooseComplexity(10), "O(n!)");
        Check.run("Q3 n=20", () -> e.chooseComplexity(20), "O(2^n)");
        Check.run("Q3 n=300", () -> e.chooseComplexity(300), "O(n^3)");
        Check.run("Q3 n=3000", () -> e.chooseComplexity(3000), "O(n^2)");
        Check.run("Q3 n=100000", () -> e.chooseComplexity(100_000), "O(n log n)");
        Check.run("Q3 n=100000000", () -> e.chooseComplexity(100_000_000), "O(n)");
        Check.done();
    }
}
