import java.util.*;

class Exercise {
    // Q1. 길이 오름차순, 길이가 같으면 사전순 (원본은 유지하고 새 배열 반환)
    String[] byLengthThenLex(String[] words) {
        // TODO 여기를 채우세요
        return words;
    }

    // Q2. 구간 [시작, 끝]을 시작 오름차순, 시작이 같으면 끝 내림차순으로 (배열 자체를 정렬해서 반환)
    int[][] sortIntervals(int[][] iv) {
        // TODO 여기를 채우세요
        return iv;
    }

    // Q3. 문자열 내 마음대로 정렬하기: 각 문자열의 n번째 글자 기준 오름차순, 같으면 사전순
    String[] sortByNthChar(String[] strings, int n) {
        // TODO 여기를 채우세요
        return strings;
    }

    // Q4. 실패율: 스테이지 1~N의 실패율 내림차순으로 번호 반환 (같으면 작은 번호 먼저)
    //     실패율 = 그 스테이지에 머문 사람 수 / 그 스테이지에 도달한 사람 수 (도달자 0이면 실패율 0)
    //     stages[i] = i번 사용자가 머물러 있는 스테이지 (N+1이면 모두 클리어)
    int[] failureRate(int N, int[] stages) {
        // TODO 여기를 채우세요
        return new int[0];
    }

    // Q5. 가장 큰 수: 0 이상의 정수들을 이어 붙여 만들 수 있는 가장 큰 수 (문자열)
    String largestNumber(int[] numbers) {
        // TODO 여기를 채우세요
        return "";
    }

    public static void main(String[] args) {
        Exercise e = new Exercise();
        Check.run("Q1 byLengthThenLex", () -> e.byLengthThenLex(new String[]{"banana", "kiwi", "apple", "fig", "date"}),
                new String[]{"fig", "date", "kiwi", "apple", "banana"});
        Check.run("Q2 sortIntervals", () -> e.sortIntervals(new int[][]{{1, 3}, {0, 2}, {1, 5}}), new int[][]{{0, 2}, {1, 5}, {1, 3}});
        Check.run("Q2 sortIntervals 큰 값(오버플로 주의)", () -> e.sortIntervals(new int[][]{{2_000_000_000, 1}, {-2_000_000_000, 1}}),
                new int[][]{{-2_000_000_000, 1}, {2_000_000_000, 1}});
        Check.run("Q3 sortByNthChar([sun,bed,car], 1)", () -> e.sortByNthChar(new String[]{"sun", "bed", "car"}, 1), new String[]{"car", "bed", "sun"});
        Check.run("Q3 sortByNthChar([abce,abcd,cdx], 2)", () -> e.sortByNthChar(new String[]{"abce", "abcd", "cdx"}, 2), new String[]{"abcd", "abce", "cdx"});
        Check.run("Q4 failureRate(5, ...)", () -> e.failureRate(5, new int[]{2, 1, 2, 6, 2, 4, 3, 3}), new int[]{3, 4, 2, 1, 5});
        Check.run("Q4 failureRate(4, [4,4,4,4,4])", () -> e.failureRate(4, new int[]{4, 4, 4, 4, 4}), new int[]{4, 1, 2, 3});
        Check.run("Q5 largestNumber([6,10,2])", () -> e.largestNumber(new int[]{6, 10, 2}), "6210");
        Check.run("Q5 largestNumber([3,30,34,5,9])", () -> e.largestNumber(new int[]{3, 30, 34, 5, 9}), "9534330");
        Check.run("Q5 largestNumber([0,0])", () -> e.largestNumber(new int[]{0, 0}), "0");
        Check.done();
    }
}
