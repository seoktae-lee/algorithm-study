import java.util.*;

class Exercise {
    // Q1. 중복 제거 + 오름차순
    int[] sortedUnique(int[] a) {
        // TODO 여기를 채우세요
        return new int[0];
    }

    // Q2. 전화번호 목록: 어떤 번호가 다른 번호의 접두어면 false, 아니면 true
    boolean phoneBook(String[] phoneBook) {
        // TODO 여기를 채우세요
        return false;
    }

    // Q3. 영어 끝말잇기: n명이 차례로 말함. 처음 탈락하는 [사람 번호, 그 사람의 몇 번째 차례], 없으면 [0, 0]
    //     탈락: 이전 단어의 마지막 글자로 시작하지 않거나, 이미 나온 단어
    int[] wordChain(int n, String[] words) {
        // TODO 여기를 채우세요
        return new int[]{0, 0};
    }

    // Q4. nums 중 x 이하인 값 중 가장 큰 값, 없으면 -1
    int closestLE(int[] nums, int x) {
        // TODO 여기를 채우세요
        return -1;
    }

    // Q5. 한 번만 나온 글자 중 가장 먼저 나온 글자, 없으면 '_'
    char firstUnique(String s) {
        // TODO 여기를 채우세요
        return '_';
    }

    public static void main(String[] args) {
        Exercise e = new Exercise();
        Check.run("Q1 sortedUnique([3,1,3,2])", () -> e.sortedUnique(new int[]{3, 1, 3, 2}), new int[]{1, 2, 3});
        Check.run("Q2 phoneBook 접두어 있음", () -> e.phoneBook(new String[]{"119", "97674223", "1195524421"}), false);
        Check.run("Q2 phoneBook 없음", () -> e.phoneBook(new String[]{"123", "456", "789"}), true);
        Check.run("Q2 phoneBook 접두어 있음 2", () -> e.phoneBook(new String[]{"12", "123", "1235", "567", "88"}), false);
        Check.run("Q3 wordChain 중복 단어", () -> e.wordChain(3, new String[]{"tank", "kick", "know", "wheel", "land", "dream", "mother", "robot", "tank"}), new int[]{3, 3});
        Check.run("Q3 wordChain 통과", () -> e.wordChain(5, new String[]{"hello", "observe", "effect", "take", "either", "recognize", "encourage",
                "ensure", "establish", "hang", "gather", "refer", "reference", "estimate", "executive"}), new int[]{0, 0});
        Check.run("Q3 wordChain 글자 불일치", () -> e.wordChain(2, new String[]{"hello", "one", "even", "never", "now", "world", "draw"}), new int[]{1, 3});
        Check.run("Q4 closestLE([5,1,9,3], 4)", () -> e.closestLE(new int[]{5, 1, 9, 3}, 4), 3);
        Check.run("Q4 closestLE([5,1,9], 0)", () -> e.closestLE(new int[]{5, 1, 9}, 0), -1);
        Check.run("Q4 closestLE([5,1,9], 9)", () -> e.closestLE(new int[]{5, 1, 9}, 9), 9);
        Check.run("Q5 firstUnique(\"leetcode\")", () -> e.firstUnique("leetcode"), 'l');
        Check.run("Q5 firstUnique(\"aabbcdc\")", () -> e.firstUnique("aabbcdc"), 'd');
        Check.run("Q5 firstUnique(\"aabb\")", () -> e.firstUnique("aabb"), '_');
        Check.done();
    }
}
