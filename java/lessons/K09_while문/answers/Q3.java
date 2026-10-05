// K09-Q3. endNum=3 일 때 1부터 endNum까지 더해가며 'i=1 sum=1', 'i=2 sum=3', 'i=3 sum=6' 처럼 매번 출력하세요
//
// 기대 출력:
// i=1 sum=1
// i=2 sum=3
// i=3 sum=6
class Q3 {
    public static void main(String[] args) {
        int endNum = 3;
        int sum = 0;
        int i = 1;
        while (i <= endNum) {
            sum += i;
            System.out.println("i=" + i + " sum=" + sum);
            i++;
        }
    }
}
