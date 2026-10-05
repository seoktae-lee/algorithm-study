// K22-Q3. 메시지와 횟수를 받아 그 횟수만큼 메시지를 출력하는 printMessage(String message, int times)를 만들고 printMessage("안녕", 3)을 호출하세요
//
// 기대 출력:
// 안녕
// 안녕
// 안녕
class Q3 {
    public static void main(String[] args) {
        printMessage("안녕", 3);
    }

    public static void printMessage(String message, int times) {
        for (int i = 0; i < times; i++) {
            System.out.println(message);
        }
    }
}
