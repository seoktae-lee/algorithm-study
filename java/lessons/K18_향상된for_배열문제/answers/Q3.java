// K18-Q3. 배열 {1, 2, 3, 4, 5} 를 역순으로 한 줄에 '5 4 3 2 1 ' 처럼 출력하세요
//
// 기대 출력:
// 5 4 3 2 1
class Q3 {
    public static void main(String[] args) {
        int[] arr = {1, 2, 3, 4, 5};
        for (int i = arr.length - 1; i >= 0; i--) {
            System.out.print(arr[i] + " ");
        }
        System.out.println();
    }
}
