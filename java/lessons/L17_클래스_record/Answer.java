import java.util.*;

class Exercise {
    // ▼ answer
    record P(int x, int y) {}

    record Edge(int x1, int y1, int x2, int y2) {}

    record Student(String name, int score) implements Comparable<Student> {
        public int compareTo(Student o) {
            if (score != o.score) return Integer.compare(o.score, score);
            return name.compareTo(o.name);
        }
    }
    // ▲ answer

    // Q1. 서로 다른 좌표의 개수 (pts[i] = [x, y])
    int distinctPoints(int[][] pts) {
        // ▼ answer
        Set<P> set = new HashSet<>();
        for (int[] p : pts) set.add(new P(p[0], p[1]));
        return set.size();
        // ▲ answer
        // TODO: return 0;
    }

    // Q2. 방문 길이: (0,0)에서 U/D/R/L로 이동, 좌표는 -5~5 (밖으로 나가는 명령은 무시).
    //     처음 걸어 본 길(양방향 동일)의 길이
    int visitedLength(String dirs) {
        // ▼ answer
        Set<Edge> seen = new HashSet<>();
        int x = 0, y = 0;
        for (char d : dirs.toCharArray()) {
            int nx = x, ny = y;
            if (d == 'U') ny++;
            else if (d == 'D') ny--;
            else if (d == 'R') nx++;
            else nx--;
            if (nx < -5 || nx > 5 || ny < -5 || ny > 5) continue;
            boolean firstSmaller = x < nx || (x == nx && y < ny);
            seen.add(firstSmaller ? new Edge(x, y, nx, ny) : new Edge(nx, ny, x, y));
            x = nx;
            y = ny;
        }
        return seen.size();
        // ▲ answer
        // TODO: return 0;
    }

    // Q3. 점수 내림차순, 같으면 이름 사전순으로 정렬한 이름 목록
    String[] sortStudents(String[] names, int[] scores) {
        // ▼ answer
        List<Student> list = new ArrayList<>();
        for (int i = 0; i < names.length; i++) list.add(new Student(names[i], scores[i]));
        Collections.sort(list);
        String[] r = new String[list.size()];
        for (int i = 0; i < r.length; i++) r[i] = list.get(i).name();
        return r;
        // ▲ answer
        // TODO: return names;
    }

    public static void main(String[] args) {
        Exercise e = new Exercise();
        Check.run("Q1 distinctPoints", () -> e.distinctPoints(new int[][]{{1, 2}, {1, 2}, {3, 4}}), 2);
        Check.run("Q1 distinctPoints 음수", () -> e.distinctPoints(new int[][]{{-1, 0}, {0, -1}, {-1, 0}, {0, 0}}), 3);
        Check.run("Q2 visitedLength(\"ULURRDLLU\")", () -> e.visitedLength("ULURRDLLU"), 7);
        Check.run("Q2 visitedLength(\"LULLLLLLU\")", () -> e.visitedLength("LULLLLLLU"), 7);
        Check.run("Q2 visitedLength(\"UDUD\") 왕복", () -> e.visitedLength("UDUD"), 1);
        Check.run("Q3 sortStudents", () -> e.sortStudents(new String[]{"kim", "lee", "park"}, new int[]{90, 95, 90}), new String[]{"lee", "kim", "park"});
        Check.done();
    }
}
