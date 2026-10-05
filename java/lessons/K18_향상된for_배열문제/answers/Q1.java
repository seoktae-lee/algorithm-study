// K18-Q1. 향상된 for문으로 scores {90, 85, 72} 의 합과 평균(소수점 포함)을 한 줄씩 출력하세요
//
// 기대 출력:
// 247
// 82.33333333333333
class Q1 {
    public static void main(String[] args) {
        int[] scores = {90, 85, 72};
        int sum = 0;
        for (int score : scores) {
            sum += score;
        }
        System.out.println(sum);
        System.out.println((double) sum / scores.length);
    }
}
