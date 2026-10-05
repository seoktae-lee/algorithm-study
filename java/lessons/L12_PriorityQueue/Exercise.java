import java.util.*;

class Exercise {
    // Q1. 더 맵게: 가장 안 매운 a와 두 번째 b를 섞어 a + 2b. 모든 음식이 K 이상이 될 때까지 최소 섞은 횟수, 불가능하면 -1
    int scoville(int[] scoville, int K) {
        // TODO 여기를 채우세요
        return 0;
    }

    // Q2. 가장 큰 k개를 내림차순으로
    int[] topK(int[] nums, int k) {
        // TODO 여기를 채우세요
        return new int[0];
    }

    // Q3. 이중우선순위큐: "I n" 삽입, "D 1" 최댓값 삭제, "D -1" 최솟값 삭제 (비었으면 무시)
    //     끝나고 [최댓값, 최솟값], 비었으면 [0, 0]
    int[] dualPQ(String[] operations) {
        // TODO 여기를 채우세요
        return new int[]{0, 0};
    }

    // Q4. 돌 부수기: 가장 무거운 두 돌 x ≤ y를 부딪쳐 같으면 둘 다 사라지고, 다르면 y-x가 남음. 마지막 돌 무게(없으면 0)
    int lastStone(int[] stones) {
        // TODO 여기를 채우세요
        return 0;
    }

    // Q5. 디스크 컨트롤러: jobs[i] = [요청 시각, 소요 시간]. 디스크가 비면 대기 중인 작업 중
    //     소요 시간 짧은 것 → 요청 시각 빠른 것 → 번호 작은 것 순으로 처리. 반환 시간(완료-요청) 평균의 정수 부분
    int diskController(int[][] jobs) {
        // TODO 여기를 채우세요
        return 0;
    }

    public static void main(String[] args) {
        Exercise e = new Exercise();
        Check.run("Q1 scoville([1,2,3,9,10,12], 7)", () -> e.scoville(new int[]{1, 2, 3, 9, 10, 12}, 7), 2);
        Check.run("Q1 scoville([1,1], 100) 불가능", () -> e.scoville(new int[]{1, 1}, 100), -1);
        Check.run("Q1 scoville([10,20], 5) 이미 충분", () -> e.scoville(new int[]{10, 20}, 5), 0);
        Check.run("Q2 topK([3,1,5,12,2,11], 3)", () -> e.topK(new int[]{3, 1, 5, 12, 2, 11}, 3), new int[]{12, 11, 5});
        Check.run("Q3 dualPQ 1", () -> e.dualPQ(new String[]{"I 16", "I -5643", "D -1", "D 1", "D 1", "I 123", "D -1"}), new int[]{0, 0});
        Check.run("Q3 dualPQ 2", () -> e.dualPQ(new String[]{"I -45", "I 653", "D 1", "I -642", "I 45", "I 97", "D 1", "D -1", "I 333"}), new int[]{333, -45});
        Check.run("Q4 lastStone([2,7,4,1,8,1])", () -> e.lastStone(new int[]{2, 7, 4, 1, 8, 1}), 1);
        Check.run("Q4 lastStone([2,2])", () -> e.lastStone(new int[]{2, 2}), 0);
        Check.run("Q5 diskController", () -> e.diskController(new int[][]{{0, 3}, {1, 9}, {3, 5}}), 8);
        Check.run("Q5 diskController 공백 구간", () -> e.diskController(new int[][]{{0, 1}, {10, 2}}), 1);
        Check.done();
    }
}
