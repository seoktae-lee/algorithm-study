// K07-Q1. score=85 의 등급을 출력하세요 (90 이상 A, 80 이상 B, 70 이상 C, 60 이상 D, 나머지 F)
//
// 기대 출력:
// B
class Q1 {
    public static void main(String[] args) {
        int score = 85;
        if (score >= 90) {
            System.out.println("A");
        } else if (score >= 80) {
            System.out.println("B");
        } else if (score >= 70) {
            System.out.println("C");
        } else if (score >= 60) {
            System.out.println("D");
        } else {
            System.out.println("F");
        }
    }
}
