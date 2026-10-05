// K09-Q2. while문으로 1부터 10까지의 합을 구해 출력하세요
//
// 기대 출력:
// 55
class Q2 {
    public static void main(String[] args) {
        int sum = 0;
        int i = 1;
        while (i <= 10) {
            sum += i;
            i++;
        }
        System.out.println(sum);
    }
}
