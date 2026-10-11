class Solution {
     "Solution이라는 클래스(코드 묶음)를 정의한다"

    public int[] solution(int[] arr) {
         "누구나 호출할 수 있고, 정수 배열을 돌려주는 solution 메서드.
          입력으로 정수 배열 arr 하나를 받는다"

        if (arr.length == 1) return new int[]{-1};
             "만약 arr의 길이가 1이라면,
              -1 하나만 들어 있는 배열을 새로 만들어 돌려주고 즉시 끝내라"

        int min = arr[0];
             "min이라는 정수 변수를 만들고, 일단 arr의 0번째 값을 넣어라
              (첫 번째 값을 임시 최솟값으로 가정)"

        for (int n : arr) {
             "arr 안에 있는 각각의 int를 n이라 부르면서 반복해라"

            if (n < min) min = n;
                 "만약 n이 지금까지의 min보다 작으면, min을 n으로 바꿔라"
        }

        int[] answer = new int[arr.length - 1];
             "arr 길이보다 1 작은 크기의 정수 배열을 만들어 answer라 이름 붙여라
              (최솟값 하나를 뺄 거니까)"

        int idx = 0;
             "answer의 몇 번째 칸에 넣을 차례인지 기록할 idx 변수를 0으로 시작"

        for (int n : arr) {
             "arr 안에 있는 각각의 int를 n이라 부르면서 반복해라"

            if (n != min) answer[idx++] = n;
                 "만약 n이 최솟값이 아니라면,
                  answer의 idx번째 칸에 n을 넣고, 그 다음 idx를 1 늘려라"
        }

        return answer;
             "완성된 answer 배열을 결과로 돌려주고 끝내라"
    }
}
