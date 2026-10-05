import java.util.*;

class Solution {
    public int[] solution(int[] arr, int divisor) {
        List<Integer> list = new ArrayList<>();
        for (int n : arr) {
            if (n % divisor == 0) list.add(n);   // 나누어 떨어지면 가방에 담기
        }
        if (list.isEmpty()) return new int[]{-1}; // 하나도 없으면 [-1]

        Collections.sort(list);                   // 오름차순 정렬
        int[] answer = new int[list.size()];      // 개수 확정 → 계란판 생성
        for (int i = 0; i < list.size(); i++) answer[i] = list.get(i);
        return answer;
    }
}
