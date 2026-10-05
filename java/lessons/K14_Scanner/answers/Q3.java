import java.util.*;

// K14-Q3. 정수를 계속 입력받다가 0이 들어오면 멈추고, 그때까지의 합을 출력하세요
//
// 입력 (채점기가 자동으로 넣어 줌):
// 3 5 7 1 0
//
// 기대 출력:
// 16
class Q3 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int sum = 0;
        while (true) {
            int x = scanner.nextInt();
            if (x == 0) {
                break;
            }
            sum += x;
        }
        System.out.println(sum);
    }
}
