// K08-Q3. num=7 이 짝수면 '짝수', 홀수면 '홀수'를 출력하세요
//
// 기대 출력:
// 홀수
class Q3 {
    public static void main(String[] args) {
        int num = 7;
        if (num % 2 == 0) {
            System.out.println("짝수");
        } else {
            System.out.println("홀수");
        }
    }
}
