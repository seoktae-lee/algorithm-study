import java.util.*;

class Exercise {
    int gcd(int a, int b) {
        return b == 0 ? a : gcd(b, a % b);
    }

    // Q1. [최대공약수, 최소공배수]
    int[] gcdLcm(int n, int m) {
        // ▼ answer
        int g = gcd(n, m);
        return new int[]{g, n / g * m};
        // ▲ answer
        // TODO: return new int[0];
    }

    // Q2. 2 이상 n 이하 소수의 개수 (n ≤ 1,000,000 → 에라토스테네스의 체)
    int countPrimes(int n) {
        // ▼ answer
        boolean[] composite = new boolean[n + 1];
        int cnt = 0;
        for (int i = 2; i <= n; i++) {
            if (composite[i]) continue;
            cnt++;
            for (long j = (long) i * i; j <= n; j += i) composite[(int) j] = true;
        }
        return cnt;
        // ▲ answer
        // TODO: return 0;
    }

    // Q3. b^e mod m (e는 최대 10^18 → 빠른 거듭제곱)
    long modPow(long b, long e, long m) {
        // ▼ answer
        long r = 1;
        b %= m;
        while (e > 0) {
            if ((e & 1) == 1) r = r * b % m;
            b = b * b % m;
            e >>= 1;
        }
        return r;
        // ▲ answer
        // TODO: return 0;
    }

    // Q4. N개의 최소공배수
    int lcmOfArray(int[] arr) {
        // ▼ answer
        int l = 1;
        for (int x : arr) l = l / gcd(l, x) * x;
        return l;
        // ▲ answer
        // TODO: return 0;
    }

    // Q5. 약수의 개수 (n ≤ 10^9)
    int divisorCount(int n) {
        // ▼ answer
        int cnt = 0;
        for (int i = 1; (long) i * i <= n; i++) {
            if (n % i == 0) cnt += (i * i == n) ? 1 : 2;
        }
        return cnt;
        // ▲ answer
        // TODO: return 0;
    }

    public static void main(String[] args) {
        Exercise e = new Exercise();
        Check.run("Q1 gcdLcm(3, 12)", () -> e.gcdLcm(3, 12), new int[]{3, 12});
        Check.run("Q1 gcdLcm(2, 5)", () -> e.gcdLcm(2, 5), new int[]{1, 10});
        Check.run("Q2 countPrimes(10)", () -> e.countPrimes(10), 4);
        Check.run("Q2 countPrimes(5)", () -> e.countPrimes(5), 3);
        Check.run("Q2 countPrimes(1000000)", () -> e.countPrimes(1_000_000), 78498);
        Check.run("Q3 modPow(2, 10, 1000)", () -> e.modPow(2, 10, 1000), 24L);
        Check.run("Q3 modPow(3, 200, 1e9+7)", () -> e.modPow(3, 200, 1_000_000_007), 136318165L);
        Check.run("Q3 modPow(2, 10^18, 1e9+7) 빠르게", () -> e.modPow(2, 1_000_000_000_000_000_000L, 1_000_000_007) >= 0, true);
        Check.run("Q4 lcmOfArray([2,6,8,14])", () -> e.lcmOfArray(new int[]{2, 6, 8, 14}), 168);
        Check.run("Q4 lcmOfArray([1,2,3])", () -> e.lcmOfArray(new int[]{1, 2, 3}), 6);
        Check.run("Q5 divisorCount(12)", () -> e.divisorCount(12), 6);
        Check.run("Q5 divisorCount(16)", () -> e.divisorCount(16), 5);
        Check.run("Q5 divisorCount(1)", () -> e.divisorCount(1), 1);
        Check.run("Q5 divisorCount(2147483647)", () -> e.divisorCount(2147483647), 2);
        Check.done();
    }
}
