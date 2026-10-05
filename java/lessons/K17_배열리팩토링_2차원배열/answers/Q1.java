// K17-Q1. 2차원 배열 {{1,2,3},{4,5,6}} 을 행마다 '1 2 3' 처럼 공백으로 구분해 출력하세요 (줄 끝 공백은 괜찮아요)
//
// 기대 출력:
// 1 2 3
// 4 5 6
class Q1 {
    public static void main(String[] args) {
        int[][] arr = {
            {1, 2, 3},
            {4, 5, 6}
        };
        for (int row = 0; row < arr.length; row++) {
            for (int col = 0; col < arr[row].length; col++) {
                System.out.print(arr[row][col] + " ");
            }
            System.out.println();
        }
    }
}
