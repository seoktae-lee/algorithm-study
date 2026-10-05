// K17-Q2. 3행 3열 int 배열을 만들고 1부터 9까지 순서대로 채운 뒤 위와 같은 형태로 출력하세요
//
// 기대 출력:
// 1 2 3
// 4 5 6
// 7 8 9
class Q2 {
    public static void main(String[] args) {
        int[][] arr = new int[3][3];
        int value = 1;
        for (int row = 0; row < arr.length; row++) {
            for (int col = 0; col < arr[row].length; col++) {
                arr[row][col] = value;
                value++;
            }
        }
        for (int row = 0; row < arr.length; row++) {
            for (int col = 0; col < arr[row].length; col++) {
                System.out.print(arr[row][col] + " ");
            }
            System.out.println();
        }
    }
}
