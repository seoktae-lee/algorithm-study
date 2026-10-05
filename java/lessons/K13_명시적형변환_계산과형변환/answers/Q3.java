// K13-Q3. 세 과목 점수 합 sum=250 의 평균을 소수점까지(83.33…) 출력하세요
//
// 기대 출력:
// 83.33333333333333
class Q3 {
    public static void main(String[] args) {
        int sum = 250;
        int count = 3;
        double average = (double) sum / count;
        System.out.println(average);
    }
}
