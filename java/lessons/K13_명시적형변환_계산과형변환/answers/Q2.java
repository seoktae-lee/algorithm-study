// K13-Q2. int 최댓값 max 에 1을 더한 결과를 int로 한 번(오버플로), long으로 한 번(정상: 2147483648) 출력하세요
//
// 기대 출력:
// -2147483648
// 2147483648
class Q2 {
    public static void main(String[] args) {
        int max = Integer.MAX_VALUE;
        int overflow = max + 1;
        long ok = (long) max + 1;
        System.out.println(overflow);
        System.out.println(ok);
    }
}
