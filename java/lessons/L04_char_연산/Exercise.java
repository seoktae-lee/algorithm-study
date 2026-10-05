import java.util.*;

class Exercise {
    // Q1. 시저 암호: 알파벳을 n칸 밀기 (대소문자 유지, z→a 순환, 공백은 그대로)
    String caesar(String s, int n) {
        // TODO 여기를 채우세요
        return "";
    }

    // Q2. 문자열 속 숫자 문자들의 합 "a1b2c3" → 6
    int digitSum(String s) {
        // TODO 여기를 채우세요
        return 0;
    }

    // Q3. 소문자 문자열에서 가장 많이 나온 글자 (동점이면 알파벳 순으로 앞선 글자)
    char mostFrequent(String s) {
        // TODO 여기를 채우세요
        return ' ';
    }

    // Q4. 대문자 ↔ 소문자 바꾸기 (알파벳 외 문자는 그대로)
    String swapCase(String s) {
        // TODO 여기를 채우세요
        return "";
    }

    // Q5. 두 소문자 문자열이 애너그램(글자 구성이 같음)인가
    boolean isAnagram(String a, String b) {
        // TODO 여기를 채우세요
        return false;
    }

    public static void main(String[] args) {
        Exercise e = new Exercise();
        Check.run("Q1 caesar(\"AB\", 1)", () -> e.caesar("AB", 1), "BC");
        Check.run("Q1 caesar(\"z\", 1)", () -> e.caesar("z", 1), "a");
        Check.run("Q1 caesar(\"a B z\", 4)", () -> e.caesar("a B z", 4), "e F d");
        Check.run("Q2 digitSum(\"a1b2c3\")", () -> e.digitSum("a1b2c3"), 6);
        Check.run("Q2 digitSum(\"abc\")", () -> e.digitSum("abc"), 0);
        Check.run("Q3 mostFrequent(\"banana\")", () -> e.mostFrequent("banana"), 'a');
        Check.run("Q3 mostFrequent(\"abcabcbb\")", () -> e.mostFrequent("abcabcbb"), 'b');
        Check.run("Q3 mostFrequent(\"zzyy\") 동점", () -> e.mostFrequent("zzyy"), 'y');
        Check.run("Q4 swapCase(\"Hello World\")", () -> e.swapCase("Hello World"), "hELLO wORLD");
        Check.run("Q4 swapCase(\"a1B!\")", () -> e.swapCase("a1B!"), "A1b!");
        Check.run("Q5 isAnagram(\"listen\", \"silent\")", () -> e.isAnagram("listen", "silent"), true);
        Check.run("Q5 isAnagram(\"rat\", \"car\")", () -> e.isAnagram("rat", "car"), false);
        Check.run("Q5 isAnagram(\"ab\", \"abc\")", () -> e.isAnagram("ab", "abc"), false);
        Check.done();
    }
}
