// K12-Q2. a=10, b=4 일 때 a / b 를 정수 나눗셈 결과(2)와 실수 나눗셈 결과(2.5)로 한 줄씩 출력하세요 (a, b는 int 그대로)
//
// 기대 출력:
// 2
// 2.5
class Q2 {
    public static void main(String[] args) {
        int a = 10;
        int b = 4;
        System.out.println(a / b);
        System.out.println(a / (double) b);
    }
}
