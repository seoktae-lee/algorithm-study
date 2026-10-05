// K12-Q1. int i=10 을 long 변수와 double 변수에 각각 대입해서 i, long 값, double 값을 한 줄씩 출력하세요
//
// 기대 출력:
// 10
// 10
// 10.0
class Q1 {
    public static void main(String[] args) {
        int i = 10;
        long l = i;
        double d = i;
        System.out.println(i);
        System.out.println(l);
        System.out.println(d);
    }
}
