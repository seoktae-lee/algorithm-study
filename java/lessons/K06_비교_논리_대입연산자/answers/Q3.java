// K06-Q3. x=10 에 대입 연산자만 써서 +5, *2, -3 을 차례로 한 뒤 x를 출력하세요
//
// 기대 출력:
// 27
class Q3 {
    public static void main(String[] args) {
        int x = 10;
        x += 5;
        x *= 2;
        x -= 3;
        System.out.println(x);
    }
}
