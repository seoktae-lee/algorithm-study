import java.util.*;

class Solution {
    public int[] solution(int[] arr, int divisor) {
        List<Integer> list = new ArrayList<>(); //담을 그릇 준비
        
        for (int num : arr) { //향상된 for문으로, 배열의 원소를 처음부터 하나씩 num에 넣는다.
            if (num % divisor == 0){ //나머지가 0인가?, 즉 나누어 떨어지나를 확인
                list.add(num);
            }
        }
        
        if (list.isEmpty()) {
            return new int[]{-1};
        }
        
        Collections.sort(list); //Collections.sort()는 리스트용, Arrays.sort()는 배열용
        int[] answer = new int[list.size()];
        for (int i = 0; i < list.size(); i++) {
            answer[i] = list.get(i);
        }
        return answer;
    }
} //크기를 모르면 list로 모으고, 마지막에 배열로 바꾼다.
