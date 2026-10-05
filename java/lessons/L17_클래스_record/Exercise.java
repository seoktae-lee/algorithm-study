import java.util.*;

class Exercise {
    // (필요하면 여기에 도우미 메서드를 만드세요)

    // Q1. 서로 다른 좌표의 개수 (pts[i] = [x, y])
    int distinctPoints(int[][] pts) {
        // TODO 여기를 채우세요
        return 0;
    }

    // Q2. 방문 길이: (0,0)에서 U/D/R/L로 이동, 좌표는 -5~5 (밖으로 나가는 명령은 무시).
    //     처음 걸어 본 길(양방향 동일)의 길이
    int visitedLength(String dirs) {
        // TODO 여기를 채우세요
        return 0;
    }

    // Q3. 점수 내림차순, 같으면 이름 사전순으로 정렬한 이름 목록
    String[] sortStudents(String[] names, int[] scores) {
        // TODO 여기를 채우세요
        return names;
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
