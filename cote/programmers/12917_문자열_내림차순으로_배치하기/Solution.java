import java.util.Arrays;

class Solution {
    public String solution(String s) {
        String answer = "";
        
        char[] chars = s.toCharArray();
        Arrays.sort(chars);
        answer = new StringBuilder(new String(chars))
            .reverse()
            .toString();
        return answer;
    }
}
