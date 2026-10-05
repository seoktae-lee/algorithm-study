// K18-Q2. 배열 {3, -9, 14, 7, 0} 의 최댓값과 최솟값을 '최댓값: 14', '최솟값: -9' 로 출력하세요
//
// 기대 출력:
// 최댓값: 14
// 최솟값: -9
class Q2 {
    public static void main(String[] args) {
        int[] arr = {3, -9, 14, 7, 0};
        int max = arr[0];
        int min = arr[0];
        for (int x : arr) {
            if (x > max) {
                max = x;
            }
            if (x < min) {
                min = x;
            }
        }
        System.out.println("최댓값: " + max);
        System.out.println("최솟값: " + min);
    }
}
