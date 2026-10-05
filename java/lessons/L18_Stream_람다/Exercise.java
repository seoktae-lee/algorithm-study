import java.util.*;
import java.util.stream.*;

class Exercise {
    // Q1. 짝수만 골라 제곱한 합 (스트림으로)
    int sumOfSquaresEven(int[] a) {
        // TODO 여기를 채우세요
        return 0;
    }

    // Q2. 중복 제거 후 내림차순
    int[] distinctSortedDesc(int[] a) {
        // TODO 여기를 채우세요
        return a;
    }

    // Q3. 단어 길이별 개수 {길이=개수}
    Map<Integer, Long> countByLength(String[] words) {
        // TODO 여기를 채우세요
        return new HashMap<>();
    }

    // Q4. 3글자 이상 단어만 대문자로 바꿔 "-"로 연결
    String joinUpper(List<String> words) {
        // TODO 여기를 채우세요
        return "";
    }

    // Q5. 평균 (빈 배열이면 0.0)
    double avg(int[] a) {
        // TODO 여기를 채우세요
        return -1;
    }

    public static void main(String[] args) {
        Exercise e = new Exercise();
        Check.run("Q1 sumOfSquaresEven([1,2,3,4])", () -> e.sumOfSquaresEven(new int[]{1, 2, 3, 4}), 20);
        Check.run("Q2 distinctSortedDesc([3,1,3,2])", () -> e.distinctSortedDesc(new int[]{3, 1, 3, 2}), new int[]{3, 2, 1});
        Check.run("Q3 countByLength", () -> e.countByLength(new String[]{"a", "bb", "cc", "d", "eee"}), Map.of(1, 2L, 2, 2L, 3, 1L));
        Check.run("Q4 joinUpper", () -> e.joinUpper(List.of("java", "is", "fun")), "JAVA-FUN");
        Check.run("Q5 avg([1,2,3,4])", () -> e.avg(new int[]{1, 2, 3, 4}), 2.5);
        Check.run("Q5 avg([])", () -> e.avg(new int[]{}), 0.0);
        Check.done();
    }
}
