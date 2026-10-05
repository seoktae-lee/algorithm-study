// K23-Q1. int 배열의 최댓값을 돌려주는 getMax 메서드를 만들고 getMax({4, 11, 2, 8})을 출력하세요
//
// 기대 출력:
// 11
class Q1 {
    public static void main(String[] args) {
        int[] numbers = {4, 11, 2, 8};
        System.out.println(getMax(numbers));
    }

    public static int getMax(int[] arr) {
        int max = arr[0];
        for (int x : arr) {
            if (x > max) {
                max = x;
            }
        }
        return max;
    }
}
