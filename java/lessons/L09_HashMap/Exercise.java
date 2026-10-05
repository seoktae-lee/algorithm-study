import java.util.*;

class Exercise {
    // Q1. 완주하지 못한 선수 (동명이인 있음, 완주 못 한 사람은 정확히 1명)
    String notFinished(String[] participant, String[] completion) {
        // TODO 여기를 채우세요
        return "";
    }

    // Q2. 폰켓몬: N마리 중 N/2마리를 고를 때 고를 수 있는 종류 수의 최댓값
    int ponketmon(int[] nums) {
        // TODO 여기를 채우세요
        return 0;
    }

    // Q3. 의상: [이름, 종류] 목록 → 하루에 최소 한 개는 입는 서로 다른 조합 수
    int clothes(String[][] clothes) {
        // TODO 여기를 채우세요
        return 0;
    }

    // Q4. 신고 결과 받기: report = "신고자 피신고자", 같은 사람이 같은 사람을 여러 번 신고해도 1회.
    //     k번 이상 신고당한 사람은 정지, 그 사람을 신고한 사람들이 메일 1통씩 받음 → id_list 순서대로 메일 수
    int[] report(String[] idList, String[] report, int k) {
        // TODO 여기를 채우세요
        return new int[0];
    }

    // Q5. 가장 많이 나온 단어 (동점이면 사전순으로 앞선 단어)
    String mostCommonWord(String[] words) {
        // TODO 여기를 채우세요
        return "";
    }

    public static void main(String[] args) {
        Exercise e = new Exercise();
        Check.run("Q1 notFinished 기본", () -> e.notFinished(new String[]{"leo", "kiki", "eden"}, new String[]{"eden", "kiki"}), "leo");
        Check.run("Q1 notFinished 동명이인", () -> e.notFinished(new String[]{"mislav", "stanko", "mislav", "ana"}, new String[]{"stanko", "ana", "mislav"}), "mislav");
        Check.run("Q2 ponketmon([3,1,2,3])", () -> e.ponketmon(new int[]{3, 1, 2, 3}), 2);
        Check.run("Q2 ponketmon([3,3,3,2,2,4])", () -> e.ponketmon(new int[]{3, 3, 3, 2, 2, 4}), 3);
        Check.run("Q2 ponketmon([3,3,3,2,2,2])", () -> e.ponketmon(new int[]{3, 3, 3, 2, 2, 2}), 2);
        Check.run("Q3 clothes 5", () -> e.clothes(new String[][]{{"yellow_hat", "headgear"}, {"blue_sunglasses", "eyewear"}, {"green_turban", "headgear"}}), 5);
        Check.run("Q3 clothes 3", () -> e.clothes(new String[][]{{"crow_mask", "face"}, {"blue_sunglasses", "face"}, {"smoky_makeup", "face"}}), 3);
        Check.run("Q4 report 기본", () -> e.report(new String[]{"muzi", "frodo", "apeach", "neo"},
                new String[]{"muzi frodo", "apeach frodo", "frodo neo", "muzi neo", "apeach muzi"}, 2), new int[]{2, 1, 1, 0});
        Check.run("Q4 report 중복 신고", () -> e.report(new String[]{"con", "ryan"},
                new String[]{"ryan con", "ryan con", "ryan con", "ryan con"}, 3), new int[]{0, 0});
        Check.run("Q5 mostCommonWord", () -> e.mostCommonWord(new String[]{"b", "a", "b", "a", "c"}), "a");
        Check.run("Q5 mostCommonWord 2", () -> e.mostCommonWord(new String[]{"x", "y", "y"}), "y");
        Check.done();
    }
}
