// K22-Q2. 세 정수의 평균을 double로 돌려주는 average 메서드를 만들고 average(1, 2, 4)를 출력하세요
//
// 기대 출력:
// 2.3333333333333335
class Q2 {
    public static void main(String[] args) {
        System.out.println(average(1, 2, 4));
    }

    public static double average(int a, int b, int c) {
        int sum = a + b + c;
        return (double) sum / 3;
    }
}
