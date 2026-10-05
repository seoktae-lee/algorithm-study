import java.util.*;

class Exercise {
    static class Pos {
        final int r, c;

        Pos(int r, int c) {
            this.r = r;
            this.c = c;
        }

        // Q2. HashSet이 같은 좌표를 하나로 보도록 equals와 hashCode를 재정의하세요
        // ▼ answer
        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (!(o instanceof Pos p)) return false;
            return r == p.r && c == p.c;
        }

        @Override
        public int hashCode() {
            return Objects.hash(r, c);
        }
        // ▲ answer
        // TODO:
    }

    // Q1. 두 문자열의 내용이 같은가 (null 가능)
    boolean sameString(String a, String b) {
        // ▼ answer
        return Objects.equals(a, b);
        // ▲ answer
        // TODO: return a == b;
    }

    // Q2. (이미 완성됨) 서로 다른 좌표 개수 — Pos의 equals/hashCode를 구현해야 맞게 나옴
    int countDistinct(int[][] pts) {
        Set<Pos> set = new HashSet<>();
        for (int[] p : pts) set.add(new Pos(p[0], p[1]));
        return set.size();
    }

    // Q3. 대소문자를 무시하고 서로 다른 단어 수
    int countWordsIgnoreCase(String[] words) {
        // ▼ answer
        Set<String> set = new HashSet<>();
        for (String w : words) set.add(w.toLowerCase());
        return set.size();
        // ▲ answer
        // TODO: return 0;
    }

    public static void main(String[] args) {
        Exercise e = new Exercise();
        Check.run("Q1 sameString(new String)", () -> e.sameString("java", new String("java")), true);
        Check.run("Q1 sameString(런타임 연결)", () -> {
            String x = "ja";
            x += "va";
            return e.sameString("java", x);
        }, true);
        Check.run("Q1 sameString(null, null)", () -> e.sameString(null, null), true);
        Check.run("Q2 countDistinct", () -> e.countDistinct(new int[][]{{1, 1}, {1, 1}, {2, 3}}), 2);
        Check.run("Q2 Set.contains", () -> {
            Set<Pos> s = new HashSet<>();
            s.add(new Pos(0, 0));
            return s.contains(new Pos(0, 0));
        }, true);
        Check.run("Q3 countWordsIgnoreCase", () -> e.countWordsIgnoreCase(new String[]{"Java", "java", "JAVA", "Spring"}), 2);
        Check.done();
    }
}
