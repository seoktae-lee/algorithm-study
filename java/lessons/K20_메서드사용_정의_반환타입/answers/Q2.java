// K20-Q2. '= 시작 =' 을 출력하는 void 메서드 printHeader를 만들고 두 번 호출하세요
//
// 기대 출력:
// = 시작 =
// = 시작 =
class Q2 {
    public static void main(String[] args) {
        printHeader();
        printHeader();
    }

    public static void printHeader() {
        System.out.println("= 시작 =");
    }
}
