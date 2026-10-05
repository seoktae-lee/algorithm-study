# K23. 메서드 문제 · 메서드 정리 · 다음으로 → 프로그래머스

> ⏱ 강의 약 46분 + 연습문제 10분 · 🎬 [김영한의 자바 입문 - 코드로 시작하는 자바 첫걸음](https://www.inflearn.com/course/김영한의-자바-입문) 섹션 10(메서드), 11(다음으로)
> 🧑‍💻 강의 예제는 직접 따라 치기 → 끝나면 터미널에서 Enter → 연습문제 3개 (출력 비교 자동 채점)

## 🎬 오늘 강의

- [섹션 10. 문제와 풀이2](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194624&subtitleLanguage=ko) · 7분
- [섹션 10. 정리](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194625&subtitleLanguage=ko) · 12분
- [섹션 10. 섹션 10 퀴즈](https://www.inflearn.com/courses/lecture?courseId=332505&type=QUIZ&unitId=288383&subtitleLanguage=ko) · 퀴즈
- [섹션 11. 다음으로 (선택)](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194626&subtitleLanguage=ko) · 27분

## 📌 핵심 요약 (치트시트)

```java
// 프로그래머스 문제 = 'solution 메서드'를 완성하는 것
class Solution {
    public int solution(int[] arr) {     // 입력은 매개변수로
        int answer = 0;
        for (int x : arr) answer += x;
        return answer;                   // 출력은 return으로 (println 아님!)
    }
}
// main은 없음 — 채점기가 new Solution().solution(...)을 대신 호출

// 배열도 메서드에 넘길 수 있음
public static int getMax(int[] arr) { ... }
```
- 🎉 입문 강의 완주! 다음부터는 코테용 레슨 L01~L24 (String·정렬·ArrayList·HashMap·Stack/Queue·BFS…)
- '다음으로' 강의(27분)는 다음 강의(자바 기본편) 소개라 선택

## 🧩 연습문제 힌트

- Q2: 잔액은 돌려받아야 바뀌어요: balance = deposit(balance, 1000);
- Q3: for (int x : arr) answer += x; — 프로그래머스에선 이 메서드만 쓰고 제출해요

## 🃏 복습 카드

- Q: 프로그래머스 문제에서 입력과 출력은 어떻게 주고받나?
  A: 입력은 solution 메서드의 매개변수, 출력은 return 값 (main·Scanner·println 안 씀)
- Q: int 배열을 받아 최댓값을 돌려주는 메서드의 선언부는?
  A: public static int getMax(int[] arr)
- Q: 잔액보다 큰 금액을 출금하려 할 때처럼 '예외 상황'을 메서드에서 처리하는 방법은?
  A: if로 먼저 검사해서 안내 메시지 출력 후 원래 값을 그대로 return
- Q: 메서드를 잘 나누면 좋은 점 3가지는?
  A: 중복 제거, 이름으로 의미 전달(읽기 쉬움), 수정할 곳이 한 곳
