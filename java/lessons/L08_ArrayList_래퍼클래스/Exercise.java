import java.util.*;

class Exercise {
    // Q1. 같은 숫자는 싫어: 연속으로 같은 숫자는 하나만 남기기
    int[] noRepeat(int[] arr) {
        // TODO 여기를 채우세요
        return new int[0];
    }

    // Q2. List<Integer> → int[]
    int[] toIntArray(List<Integer> list) {
        // TODO 여기를 채우세요
        return new int[0];
    }

    // Q3. 두 Integer의 값이 같은가 (null이 들어올 수도 있음: 둘 다 null이면 true)
    boolean sameValue(Integer a, Integer b) {
        // TODO 여기를 채우세요
        return a == b;
    }

    // Q4. 짝수를 뺀 새 리스트 (원본은 그대로)
    List<Integer> removeEvens(List<Integer> list) {
        // TODO 여기를 채우세요
        return list;
    }

    // Q5. 두 개 뽑아서 더하기: 서로 다른 인덱스의 두 수를 더해 만들 수 있는 모든 값 (중복 없이 오름차순)
    int[] twoSum(int[] numbers) {
        // TODO 여기를 채우세요
        return new int[0];
    }

    public static void main(String[] args) {
        Exercise e = new Exercise();
        Check.run("Q1 noRepeat([1,1,3,3,0,1,1])", () -> e.noRepeat(new int[]{1, 1, 3, 3, 0, 1, 1}), new int[]{1, 3, 0, 1});
        Check.run("Q1 noRepeat([4,4,4,3,3])", () -> e.noRepeat(new int[]{4, 4, 4, 3, 3}), new int[]{4, 3});
        Check.run("Q2 toIntArray([3,1,2])", () -> e.toIntArray(List.of(3, 1, 2)), new int[]{3, 1, 2});
        Check.run("Q3 sameValue(1000, 1000)", () -> e.sameValue(1000, 1000), true);
        Check.run("Q3 sameValue(5, 6)", () -> e.sameValue(5, 6), false);
        Check.run("Q3 sameValue(null, 1)", () -> e.sameValue(null, 1), false);
        List<Integer> src = new ArrayList<>(List.of(1, 2, 3, 4, 5));
        Check.run("Q4 removeEvens", () -> e.removeEvens(src), List.of(1, 3, 5));
        Check.run("Q4 원본 유지", () -> src, List.of(1, 2, 3, 4, 5));
        Check.run("Q5 twoSum([2,1,3,4,1])", () -> e.twoSum(new int[]{2, 1, 3, 4, 1}), new int[]{2, 3, 4, 5, 6, 7});
        Check.run("Q5 twoSum([5,0,2,7])", () -> e.twoSum(new int[]{5, 0, 2, 7}), new int[]{2, 5, 7, 9, 12});
        Check.done();
    }
}
