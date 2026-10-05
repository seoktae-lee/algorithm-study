// K21-Q1. changeNumber가 값을 '돌려주도록' 고쳐서 num이 20으로 바뀐 뒤 '변경 후 num: 20' 이 출력되게 하세요
//
// 기대 출력:
// 변경 후 num: 20
class Q1 {
    public static void main(String[] args) {
        int num = 10;
        changeNumber(num);
        System.out.println("변경 후 num: " + num);
    }

    public static void changeNumber(int x) {
        x = 20;
    }
}
