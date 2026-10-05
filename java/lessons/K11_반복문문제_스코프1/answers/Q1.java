// K11-Q1. rows=4 일 때 별(*)로 직각 삼각형을 출력하세요 (1줄 *, 2줄 **, …, 4줄 ****)
//
// 기대 출력:
// *
// **
// ***
// ****
class Q1 {
    public static void main(String[] args) {
        int rows = 4;
        for (int row = 1; row <= rows; row++) {
            for (int col = 1; col <= row; col++) {
                System.out.print("*");
            }
            System.out.println();
        }
    }
}
