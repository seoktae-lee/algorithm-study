import java.util.*;

class Exercise {
    // Q1. 가운데 글자 (길이가 짝수면 가운데 두 글자)
    String middle(String s) {
        // ▼ answer
        int n = s.length();
        return n % 2 == 1 ? s.substring(n / 2, n / 2 + 1) : s.substring(n / 2 - 1, n / 2 + 1);
        // ▲ answer
        // TODO: return "";
    }

    // Q2. 앞뒤가 같은 문자열(회문)인가
    boolean isPalindrome(String s) {
        // ▼ answer
        int n = s.length();
        for (int i = 0; i < n / 2; i++) {
            if (s.charAt(i) != s.charAt(n - 1 - i)) return false;
        }
        return true;
        // ▲ answer
        // TODO: return false;
    }

    // Q3. 공백 하나로 구분된 문장에서 단어 word가 몇 번 나오나
    int countWord(String sentence, String word) {
        // ▼ answer
        int cnt = 0;
        for (String w : sentence.split(" ")) {
            if (w.equals(word)) cnt++;
        }
        return cnt;
        // ▲ answer
        // TODO: return 0;
    }

    // Q4. 공백으로 구분된 정수 문자열의 합 ("12 30 5" → 47, 음수 포함 가능)
    int toNumberSum(String s) {
        // ▼ answer
        int sum = 0;
        for (String t : s.split(" ")) sum += Integer.parseInt(t);
        return sum;
        // ▲ answer
        // TODO: return 0;
    }

    // Q5. 단어 사이 공백이 여러 개일 수 있고 앞뒤 공백도 있을 때, 단어 사이를 공백 하나로 정리
    //     "  hello   java  world " → "hello java world"
    String normalizeSpaces(String s) {
        // ▼ answer
        return String.join(" ", s.trim().split(" +"));
        // ▲ answer
        // TODO: return s;
    }

    public static void main(String[] args) {
        Exercise e = new Exercise();
        Check.run("Q1 middle(\"abcde\")", () -> e.middle("abcde"), "c");
        Check.run("Q1 middle(\"qwer\")", () -> e.middle("qwer"), "we");
        Check.run("Q1 middle(\"a\")", () -> e.middle("a"), "a");
        Check.run("Q2 isPalindrome(\"level\")", () -> e.isPalindrome("level"), true);
        Check.run("Q2 isPalindrome(\"java\")", () -> e.isPalindrome("java"), false);
        Check.run("Q2 isPalindrome(\"abba\")", () -> e.isPalindrome("abba"), true);
        Check.run("Q3 countWord(\"a b a c a\", \"a\")", () -> e.countWord("a b a c a", "a"), 3);
        Check.run("Q3 countWord(new String 비교)", () -> e.countWord("java is java", new String("java")), 2);
        Check.run("Q4 toNumberSum(\"12 30 5\")", () -> e.toNumberSum("12 30 5"), 47);
        Check.run("Q4 toNumberSum(\"-1 -2 10\")", () -> e.toNumberSum("-1 -2 10"), 7);
        Check.run("Q5 normalizeSpaces", () -> e.normalizeSpaces("  hello   java  world "), "hello java world");
        Check.run("Q5 normalizeSpaces(\"one\")", () -> e.normalizeSpaces("one"), "one");
        Check.done();
    }
}
