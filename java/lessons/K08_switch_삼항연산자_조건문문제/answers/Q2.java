// K08-Q2. age=17 일 때 삼항 연산자로 status에 '성인'(18 이상) 또는 '미성년자'를 넣어 출력하세요
//
// 기대 출력:
// 미성년자
class Q2 {
    public static void main(String[] args) {
        int age = 17;
        String status = (age >= 18) ? "성인" : "미성년자";
        System.out.println(status);
    }
}
