// K19-Q2. 두 수를 더해 돌려주는 메서드 add를 만들고, main에서 add(5, 10)과 add(15, 20)의 결과를 한 줄씩 출력하세요
//
// 기대 출력:
// 15
// 35
class Q2 {
    public static void main(String[] args) {
        System.out.println(add(5, 10));
        System.out.println(add(15, 20));
    }

    public static int add(int a, int b) {
        return a + b;
    }
}
