import java.util.*;

class Exercise {
    // Q1. x부터 x씩 증가하는 n개의 수 (프로그래머스 'x만큼 간격이 있는 n개의 숫자')
    //     x는 -10,000,000 ~ 10,000,000, n은 1000 이하
    long[] xGap(int x, int n) {
        // TODO 여기를 채우세요
        return new long[0];
    }

    // Q2. a × b를 정확히 반환 (a, b는 int 범위)
    long mulSafe(int a, int b) {
        // TODO 여기를 채우세요
        return a * b;
    }

    // Q3. 양의 정수 a를 b로 나눈 몫의 올림 (실수 연산 없이)
    int ceilDiv(int a, int b) {
        // TODO 여기를 채우세요
        return 0;
    }

    // Q4. 배열의 평균 (소수점 포함)
    double average(int[] arr) {
        // TODO 여기를 채우세요
        return 0;
    }

    // Q5. 양의 정수 n의 각 자릿수 합 (문자열 변환 없이 %와 /로)
    int digitSum(int n) {
        // TODO 여기를 채우세요
        return 0;
    }

    public static void main(String[] args) {
        Exercise e = new Exercise();
        Check.run("Q1 xGap(2, 5)", () -> e.xGap(2, 5), new long[]{2, 4, 6, 8, 10});
        Check.run("Q1 xGap(-4, 2)", () -> e.xGap(-4, 2), new long[]{-4, -8});
        Check.run("Q1 xGap(10000000, 1000) 마지막 값", () -> e.xGap(10000000, 1000)[999], 10_000_000_000L);
        Check.run("Q2 mulSafe(100000, 100000)", () -> e.mulSafe(100000, 100000), 10_000_000_000L);
        Check.run("Q2 mulSafe(-3, 7)", () -> e.mulSafe(-3, 7), -21L);
        Check.run("Q3 ceilDiv(7, 2)", () -> e.ceilDiv(7, 2), 4);
        Check.run("Q3 ceilDiv(6, 2)", () -> e.ceilDiv(6, 2), 3);
        Check.run("Q3 ceilDiv(1, 5)", () -> e.ceilDiv(1, 5), 1);
        Check.run("Q4 average([1,2,3,4])", () -> e.average(new int[]{1, 2, 3, 4}), 2.5);
        Check.run("Q4 average([5,5])", () -> e.average(new int[]{5, 5}), 5.0);
        Check.run("Q5 digitSum(123)", () -> e.digitSum(123), 6);
        Check.run("Q5 digitSum(987)", () -> e.digitSum(987), 24);
        Check.done();
    }
}
