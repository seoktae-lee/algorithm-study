import java.util.*;

class Exercise {
    // Q1. [1차] 비밀지도: 두 지도 중 하나라도 벽(1)이면 '#', 둘 다 공백(0)이면 ' ' (각 줄 n칸)
    String[] secretMap(int n, int[] arr1, int[] arr2) {
        // ▼ answer
        String[] ans = new String[n];
        for (int i = 0; i < n; i++) {
            int row = arr1[i] | arr2[i];
            StringBuilder sb = new StringBuilder();
            for (int b = n - 1; b >= 0; b--) sb.append(((row >> b) & 1) == 1 ? '#' : ' ');
            ans[i] = sb.toString();
        }
        return ans;
        // ▲ answer
        // TODO: return new String[0];
    }

    // Q2. 다음 큰 숫자: n보다 크고, 2진수 1의 개수가 같은 가장 작은 수
    int nextBigger(int n) {
        // ▼ answer
        int c = Integer.bitCount(n);
        int x = n + 1;
        while (Integer.bitCount(x) != c) x++;
        return x;
        // ▲ answer
        // TODO: return 0;
    }

    // Q3. 이진 변환 반복하기: 0을 모두 제거 → 남은 길이를 2진수 문자열로, "1"이 될 때까지.
    //     [변환 횟수, 제거한 0의 총개수]
    int[] binaryTransform(String s) {
        // ▼ answer
        int rounds = 0, zeros = 0;
        while (!s.equals("1")) {
            int ones = 0;
            for (char c : s.toCharArray()) {
                if (c == '1') ones++;
                else zeros++;
            }
            s = Integer.toBinaryString(ones);
            rounds++;
        }
        return new int[]{rounds, zeros};
        // ▲ answer
        // TODO: return new int[0];
    }

    // Q4. 부분집합 중 합이 target인 것의 개수 (n ≤ 20, 비트마스크)
    int countSubsetSum(int[] nums, int target) {
        // ▼ answer
        int n = nums.length, cnt = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            int sum = 0;
            for (int i = 0; i < n; i++) {
                if ((mask & (1 << i)) != 0) sum += nums[i];
            }
            if (sum == target) cnt++;
        }
        return cnt;
        // ▲ answer
        // TODO: return 0;
    }

    // Q5. 2의 거듭제곱인가 (반복문 없이)
    boolean isPowerOfTwo(int n) {
        // ▼ answer
        return n > 0 && (n & (n - 1)) == 0;
        // ▲ answer
        // TODO: return false;
    }

    public static void main(String[] args) {
        Exercise e = new Exercise();
        Check.run("Q1 secretMap 5", () -> e.secretMap(5, new int[]{9, 20, 28, 18, 11}, new int[]{30, 1, 21, 17, 28}),
                new String[]{"#####", "# # #", "### #", "#  ##", "#####"});
        Check.run("Q1 secretMap 6", () -> e.secretMap(6, new int[]{46, 33, 33, 22, 31, 50}, new int[]{27, 56, 19, 14, 14, 10}),
                new String[]{"######", "###  #", "##  ##", " #### ", " #####", "### # "});
        Check.run("Q2 nextBigger(78)", () -> e.nextBigger(78), 83);
        Check.run("Q2 nextBigger(15)", () -> e.nextBigger(15), 23);
        Check.run("Q3 binaryTransform(\"110010101001\")", () -> e.binaryTransform("110010101001"), new int[]{3, 8});
        Check.run("Q3 binaryTransform(\"01110\")", () -> e.binaryTransform("01110"), new int[]{3, 3});
        Check.run("Q3 binaryTransform(\"1111111\")", () -> e.binaryTransform("1111111"), new int[]{4, 1});
        Check.run("Q4 countSubsetSum([1,2,3,4], 5)", () -> e.countSubsetSum(new int[]{1, 2, 3, 4}, 5), 2);
        Check.run("Q4 countSubsetSum([1,1,1], 2)", () -> e.countSubsetSum(new int[]{1, 1, 1}, 2), 3);
        Check.run("Q5 isPowerOfTwo(16)", () -> e.isPowerOfTwo(16), true);
        Check.run("Q5 isPowerOfTwo(18)", () -> e.isPowerOfTwo(18), false);
        Check.run("Q5 isPowerOfTwo(1)", () -> e.isPowerOfTwo(1), true);
        Check.run("Q5 isPowerOfTwo(0)", () -> e.isPowerOfTwo(0), false);
        Check.done();
    }
}
