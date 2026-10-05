// K04-Q3. totalSeconds=135초를 '분'과 '초'로 나눠 2, 15 를 한 줄씩 출력하세요 (/ 와 % 사용)
//
// 기대 출력:
// 2
// 15
class Q3 {
    public static void main(String[] args) {
        int totalSeconds = 135;
        System.out.println(totalSeconds / 60);
        System.out.println(totalSeconds % 60);
    }
}
