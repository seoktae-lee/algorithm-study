// K07-Q3. temperature=-3 일 때 0 미만이면 '영하', 0 이상 25 미만이면 '적당', 25 이상이면 '더움'을 출력하세요
//
// 기대 출력:
// 영하
class Q3 {
    public static void main(String[] args) {
        int temperature = -3;
        if (temperature < 0) {
            System.out.println("영하");
        } else if (temperature < 25) {
            System.out.println("적당");
        } else {
            System.out.println("더움");
        }
    }
}
