// K16-Q2. 배열 {3, 6, 9, 12, 15} 의 합을 for문으로 구해 출력하세요
//
// 기대 출력:
// 45
class Q2 {
    public static void main(String[] args) {
        int[] arr = {3, 6, 9, 12, 15};
        int sum = 0;
        for (int i = 0; i < arr.length; i++) {
            sum += arr[i];
        }
        System.out.println(sum);
    }
}
