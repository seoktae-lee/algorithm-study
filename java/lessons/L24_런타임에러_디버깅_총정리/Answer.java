import java.util.*;

class Exercise {
    // Q1. 🐞 단어 배열에서 key의 등장 횟수 (없으면 0) — 지금은 없는 키에서 예외
    int countOf(String[] words, String key) {
        Map<String, Integer> map = new HashMap<>();
        for (String w : words) map.merge(w, 1, Integer::sum);
        // ▼ answer
        return map.getOrDefault(key, 0);
        // ▲ answer
        //> return map.get(key);
    }

    // Q2. 🐞 이웃한 두 원소 합의 최댓값 (길이 ≥ 2) — 지금은 범위 초과
    int maxAdjacentSum(int[] a) {
        int best = Integer.MIN_VALUE;
        // ▼ answer
        for (int i = 0; i < a.length - 1; i++) best = Math.max(best, a[i] + a[i + 1]);
        // ▲ answer
        //> for (int i = 0; i < a.length; i++) best = Math.max(best, a[i] + a[i + 1]);
        return best;
    }

    // Q3. 🐞 합계 — 지금은 큰 값에서 오답
    long sumBig(int[] a) {
        // ▼ answer
        long s = 0;
        // ▲ answer
        //> int s = 0;
        for (int v : a) s += v;
        return s;
    }

    // Q4. 🐞 0부터 n-1까지 숫자를 이어 붙인 문자열 — 지금은 n이 크면 너무 느림
    String concatNumbers(int n) {
        // ▼ answer
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n; i++) sb.append(i);
        return sb.toString();
        // ▲ answer
        //> String s = "";
        //> for (int i = 0; i < n; i++) s += i;
        //> return s;
    }

    // Q5. 🐞 음수를 제거한 리스트 반환 — 지금은 예외
    List<Integer> removeNegatives(List<Integer> list) {
        List<Integer> r = new ArrayList<>(list);
        // ▼ answer
        r.removeIf(x -> x < 0);
        // ▲ answer
        //> for (int x : r) if (x < 0) r.remove(Integer.valueOf(x));
        return r;
    }

    public static void main(String[] args) {
        Exercise e = new Exercise();
        Check.run("Q1 countOf 있음", () -> e.countOf(new String[]{"a", "b", "a"}, "a"), 2);
        Check.run("Q1 countOf 없음", () -> e.countOf(new String[]{"a", "b", "a"}, "z"), 0);
        Check.run("Q2 maxAdjacentSum([1,5,3])", () -> e.maxAdjacentSum(new int[]{1, 5, 3}), 8);
        Check.run("Q2 maxAdjacentSum([-1,-2])", () -> e.maxAdjacentSum(new int[]{-1, -2}), -3);
        Check.run("Q3 sumBig", () -> e.sumBig(new int[]{2_000_000_000, 2_000_000_000}), 4_000_000_000L);
        Check.run("Q4 concatNumbers(12)", () -> e.concatNumbers(12), "01234567891011");
        Check.run("Q4 concatNumbers(300000) 길이", () -> e.concatNumbers(300_000).length(), 1_688_890);
        Check.run("Q5 removeNegatives", () -> e.removeNegatives(List.of(1, -2, 3, -4)), List.of(1, 3));
        Check.done();
    }
}
