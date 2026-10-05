import java.util.*;

class Exercise {
    // Q1. (), [], {} 괄호가 올바르게 짝지어졌나
    boolean validParen(String s) {
        // ▼ answer
        Deque<Character> st = new ArrayDeque<>();
        for (char c : s.toCharArray()) {
            if (c == '(' || c == '[' || c == '{') st.push(c);
            else {
                if (st.isEmpty()) return false;
                char top = st.pop();
                if ((c == ')' && top != '(') || (c == ']' && top != '[') || (c == '}' && top != '{')) return false;
            }
        }
        return st.isEmpty();
        // ▲ answer
        // TODO: return false;
    }

    // Q2. 짝지어 제거하기: 붙어 있는 같은 글자 쌍을 반복 제거해서 전부 없어지면 1, 아니면 0
    int removePairs(String s) {
        // ▼ answer
        Deque<Character> st = new ArrayDeque<>();
        for (char c : s.toCharArray()) {
            if (!st.isEmpty() && st.peek() == c) st.pop();
            else st.push(c);
        }
        return st.isEmpty() ? 1 : 0;
        // ▲ answer
        // TODO: return 0;
    }

    // Q3. 기능개발: 진도와 하루 속도 → 배포마다 몇 개의 기능이 배포되나 (앞 기능이 배포될 때 함께)
    int[] progress(int[] progresses, int[] speeds) {
        // ▼ answer
        Queue<Integer> q = new ArrayDeque<>();
        for (int i = 0; i < progresses.length; i++) q.offer((100 - progresses[i] + speeds[i] - 1) / speeds[i]);
        List<Integer> ans = new ArrayList<>();
        while (!q.isEmpty()) {
            int day = q.poll(), cnt = 1;
            while (!q.isEmpty() && q.peek() <= day) {
                q.poll();
                cnt++;
            }
            ans.add(cnt);
        }
        return ans.stream().mapToInt(Integer::intValue).toArray();
        // ▲ answer
        // TODO: return new int[0];
    }

    // Q4. 크레인 인형뽑기: board[r][c] (0은 빈칸), moves는 1부터 시작하는 열 번호.
    //     바구니 맨 위와 같은 인형이 들어오면 둘 다 사라짐 → 사라진 인형 수
    int crane(int[][] board, int[] moves) {
        // ▼ answer
        Deque<Integer> basket = new ArrayDeque<>();
        int gone = 0;
        for (int m : moves) {
            int c = m - 1;
            for (int r = 0; r < board.length; r++) {
                if (board[r][c] != 0) {
                    int doll = board[r][c];
                    board[r][c] = 0;
                    if (!basket.isEmpty() && basket.peek() == doll) {
                        basket.pop();
                        gone += 2;
                    } else basket.push(doll);
                    break;
                }
            }
        }
        return gone;
        // ▲ answer
        // TODO: return 0;
    }

    // Q5. 주식가격: 각 시점의 가격이 떨어지지 않은 기간(초)
    int[] stockPrices(int[] prices) {
        // ▼ answer
        int n = prices.length;
        int[] ans = new int[n];
        Deque<Integer> st = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            while (!st.isEmpty() && prices[st.peek()] > prices[i]) {
                int j = st.pop();
                ans[j] = i - j;
            }
            st.push(i);
        }
        while (!st.isEmpty()) {
            int j = st.pop();
            ans[j] = n - 1 - j;
        }
        return ans;
        // ▲ answer
        // TODO: return new int[0];
    }

    public static void main(String[] args) {
        Exercise e = new Exercise();
        Check.run("Q1 validParen(\"{[]}()\")", () -> e.validParen("{[]}()"), true);
        Check.run("Q1 validParen(\"([)]\")", () -> e.validParen("([)]"), false);
        Check.run("Q1 validParen(\")()(\")", () -> e.validParen(")()("), false);
        Check.run("Q1 validParen(\"(()(\")", () -> e.validParen("(()("), false);
        Check.run("Q2 removePairs(\"baabaa\")", () -> e.removePairs("baabaa"), 1);
        Check.run("Q2 removePairs(\"cdcd\")", () -> e.removePairs("cdcd"), 0);
        Check.run("Q3 progress 1", () -> e.progress(new int[]{93, 30, 55}, new int[]{1, 30, 5}), new int[]{2, 1});
        Check.run("Q3 progress 2", () -> e.progress(new int[]{95, 90, 99, 99, 80, 99}, new int[]{1, 1, 1, 1, 1, 1}), new int[]{1, 3, 2});
        Check.run("Q4 crane", () -> e.crane(new int[][]{{0, 0, 0, 0, 0}, {0, 0, 1, 0, 3}, {0, 2, 5, 0, 1}, {4, 2, 4, 4, 2}, {3, 5, 1, 3, 1}},
                new int[]{1, 5, 3, 5, 1, 2, 1, 4}), 4);
        Check.run("Q5 stockPrices([1,2,3,2,3])", () -> e.stockPrices(new int[]{1, 2, 3, 2, 3}), new int[]{4, 3, 1, 1, 0});
        Check.done();
    }
}
