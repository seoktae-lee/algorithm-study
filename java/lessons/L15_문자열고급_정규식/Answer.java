import java.util.*;

class Exercise {
    // Q1. 신규 아이디 추천 (카카오 2021): 7단계 규칙
    //  1) 소문자로  2) 소문자·숫자·-·_·. 외 제거  3) 마침표 2개 이상 → 1개  4) 처음/끝 마침표 제거
    //  5) 빈 문자열이면 "a"  6) 16자 이상이면 앞 15자만, 그 후 끝 마침표 제거  7) 2자 이하면 마지막 글자를 길이 3까지 반복
    String newId(String id) {
        // ▼ answer
        String s = id.toLowerCase();
        s = s.replaceAll("[^a-z0-9._-]", "");
        s = s.replaceAll("\\.{2,}", ".");
        s = s.replaceAll("^\\.|\\.$", "");
        if (s.isEmpty()) s = "a";
        if (s.length() >= 16) s = s.substring(0, 15).replaceAll("\\.$", "");
        while (s.length() <= 2) s += s.charAt(s.length() - 1);
        return s;
        // ▲ answer
        // TODO: return id;
    }

    // Q2. 숫자 문자열과 영단어: "one4seveneight" → 1478
    int numberWords(String s) {
        // ▼ answer
        String[] words = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};
        for (int i = 0; i < 10; i++) s = s.replaceAll(words[i], String.valueOf(i));
        return Integer.parseInt(s);
        // ▲ answer
        // TODO: return 0;
    }

    // Q3. "HH:MM" → 자정부터 지난 분
    int toMinutes(String hhmm) {
        // ▼ answer
        String[] t = hhmm.split(":");
        return Integer.parseInt(t[0]) * 60 + Integer.parseInt(t[1]);
        // ▲ answer
        // TODO: return 0;
    }

    // Q4. 분 → "HH:MM"
    String fmtTime(int minutes) {
        // ▼ answer
        return String.format("%02d:%02d", minutes / 60, minutes % 60);
        // ▲ answer
        // TODO: return "";
    }

    // Q5. 최댓값과 최솟값: 공백으로 구분된 정수 문자열 → "최솟값 최댓값"
    String minMax(String s) {
        // ▼ answer
        int min = Integer.MAX_VALUE, max = Integer.MIN_VALUE;
        for (String t : s.split(" ")) {
            int v = Integer.parseInt(t);
            min = Math.min(min, v);
            max = Math.max(max, v);
        }
        return min + " " + max;
        // ▲ answer
        // TODO: return "";
    }

    public static void main(String[] args) {
        Exercise e = new Exercise();
        Check.run("Q1 newId 예1", () -> e.newId("...!@BaT#*..y.abcdefghijklm"), "bat.y.abcdefghi");
        Check.run("Q1 newId 예2", () -> e.newId("z-+.^."), "z--");
        Check.run("Q1 newId 예3", () -> e.newId("=.="), "aaa");
        Check.run("Q1 newId 예4", () -> e.newId("123_.def"), "123_.def");
        Check.run("Q1 newId 예5", () -> e.newId("abcdefghijklmn.p"), "abcdefghijklmn");
        Check.run("Q2 numberWords(\"one4seveneight\")", () -> e.numberWords("one4seveneight"), 1478);
        Check.run("Q2 numberWords(\"2three45sixseven\")", () -> e.numberWords("2three45sixseven"), 234567);
        Check.run("Q2 numberWords(\"123\")", () -> e.numberWords("123"), 123);
        Check.run("Q3 toMinutes(\"09:05\")", () -> e.toMinutes("09:05"), 545);
        Check.run("Q3 toMinutes(\"23:59\")", () -> e.toMinutes("23:59"), 1439);
        Check.run("Q4 fmtTime(545)", () -> e.fmtTime(545), "09:05");
        Check.run("Q4 fmtTime(0)", () -> e.fmtTime(0), "00:00");
        Check.run("Q5 minMax(\"1 2 3 4\")", () -> e.minMax("1 2 3 4"), "1 4");
        Check.run("Q5 minMax(\"-1 -2 -3 -4\")", () -> e.minMax("-1 -2 -3 -4"), "-4 -1");
        Check.done();
    }
}
