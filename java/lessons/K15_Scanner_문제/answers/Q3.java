import java.util.*;

// K15-Q3. 첫 수는 개수 n, 그다음 n개의 정수가 주어집니다. 합을 출력하고 다음 줄에 평균(소수점 포함)을 출력하세요
//
// 입력 (채점기가 자동으로 넣어 줌):
// 4
// 10 20 30 45
//
// 기대 출력:
// 105
// 26.25
class Q3 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int sum = 0;
        for (int i = 0; i < n; i++) {
            sum += sc.nextInt();
        }
        System.out.println(sum);
        System.out.println((double) sum / n);
    }
}
