// K20-Q3. 짝수면 true를 돌려주는 isEven 메서드를 만들고 isEven(4), isEven(7)을 한 줄씩 출력하세요
//
// 기대 출력:
// true
// false
class Q3 {
    public static void main(String[] args) {
        System.out.println(isEven(4));
        System.out.println(isEven(7));
    }

    public static boolean isEven(int n) {
        return n % 2 == 0;
    }
}
