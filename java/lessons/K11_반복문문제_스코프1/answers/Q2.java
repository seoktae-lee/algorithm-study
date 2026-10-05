// K11-Q2. n=5 의 팩토리얼(5! = 1×2×3×4×5)을 for로 구해 출력하세요
//
// 기대 출력:
// 120
class Q2 {
    public static void main(String[] args) {
        int n = 5;
        int result = 1;
        for (int i = 1; i <= n; i++) {
            result *= i;
        }
        System.out.println(result);
    }
}
