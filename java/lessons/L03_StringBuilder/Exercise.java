import java.util.*;

class Exercise {
    // Q1. 문자열 뒤집기
    String reverse(String s) {
        // TODO 여기를 채우세요
        return "";
    }

    // Q2. 이상한 문자 만들기: 각 단어의 짝수 번째(0부터) 글자는 대문자, 홀수 번째는 소문자.
    //     공백은 그대로 유지(연속 공백 가능)
    String weird(String s) {
        // TODO 여기를 채우세요
        return "";
    }

    // Q3. 정수 배열을 "1,2,3" 형태로 (마지막 쉼표 없이, 빈 배열이면 "")
    String join(int[] arr) {
        // TODO 여기를 채우세요
        return "";
    }

    // Q4. 연속으로 같은 글자는 하나만 남기기 "aabbbcca" → "abca"
    String removeDup(String s) {
        // TODO 여기를 채우세요
        return "";
    }

    // Q5. 0 이상의 정수를 2진수 문자열로 (Integer.toBinaryString 쓰지 말고 직접)
    String toBinary(int n) {
        // TODO 여기를 채우세요
        return "";
    }

    public static void main(String[] args) {
        Exercise e = new Exercise();
        Check.run("Q1 reverse(\"hello\")", () -> e.reverse("hello"), "olleh");
        Check.run("Q1 reverse(\"\")", () -> e.reverse(""), "");
        Check.run("Q2 weird(\"try hello world\")", () -> e.weird("try hello world"), "TrY HeLlO WoRlD");
        Check.run("Q2 weird(\"  ab  CDE\")", () -> e.weird("  ab  CDE"), "  Ab  CdE");
        Check.run("Q3 join([1,2,3])", () -> e.join(new int[]{1, 2, 3}), "1,2,3");
        Check.run("Q3 join([])", () -> e.join(new int[]{}), "");
        Check.run("Q4 removeDup(\"aabbbcca\")", () -> e.removeDup("aabbbcca"), "abca");
        Check.run("Q4 removeDup(\"\")", () -> e.removeDup(""), "");
        Check.run("Q5 toBinary(10)", () -> e.toBinary(10), "1010");
        Check.run("Q5 toBinary(0)", () -> e.toBinary(0), "0");
        Check.run("Q5 toBinary(255)", () -> e.toBinary(255), "11111111");
        Check.done();
    }
}
