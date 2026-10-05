// K22-Q1. add를 3개로 오버로딩해서 add(1, 2), add(1, 2, 3), add(1.5, 2.5) 결과를 한 줄씩 출력하세요
//
// 기대 출력:
// 3
// 6
// 4.0
class Q1 {
    public static void main(String[] args) {
        System.out.println(add(1, 2));
        System.out.println(add(1, 2, 3));
        System.out.println(add(1.5, 2.5));
    }

    public static int add(int a, int b) {
        return a + b;
    }

    public static int add(int a, int b, int c) {
        return a + b + c;
    }

    public static double add(double a, double b) {
        return a + b;
    }
}
