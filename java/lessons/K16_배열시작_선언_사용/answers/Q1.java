// K16-Q1. 크기 5인 int 배열 students를 만들고 90, 80, 70, 60, 50 을 넣은 뒤 for문으로 '학생1 점수: 90' … '학생5 점수: 50' 을 출력하세요
//
// 기대 출력:
// 학생1 점수: 90
// 학생2 점수: 80
// 학생3 점수: 70
// 학생4 점수: 60
// 학생5 점수: 50
class Q1 {
    public static void main(String[] args) {
        int[] students = new int[5];
        students[0] = 90;
        students[1] = 80;
        students[2] = 70;
        students[3] = 60;
        students[4] = 50;
        for (int i = 0; i < students.length; i++) {
            System.out.println("학생" + (i + 1) + " 점수: " + students[i]);
        }
    }
}
