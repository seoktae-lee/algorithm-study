# K09. 조건문 정리 · while문

> ⏱ 강의 약 33분 + 연습문제 10분 · 🎬 [김영한의 자바 입문 - 코드로 시작하는 자바 첫걸음](https://www.inflearn.com/course/김영한의-자바-입문) 섹션 5(조건문), 6(반복문)
> 🧑‍💻 강의 예제는 직접 따라 치기 → 끝나면 터미널에서 Enter → 연습문제 3개 (출력 비교 자동 채점)

## 🎬 오늘 강의

- [섹션 5. 정리](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194576&subtitleLanguage=ko) · 6분
- [섹션 5. 섹션 5 퀴즈](https://www.inflearn.com/courses/lecture?courseId=332505&type=QUIZ&unitId=288292&subtitleLanguage=ko) · 퀴즈
- [섹션 6. 반복문 시작](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194577&subtitleLanguage=ko) · 4분
- [섹션 6. while문1](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194578&subtitleLanguage=ko) · 6분
- [섹션 6. while문2](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194579&subtitleLanguage=ko) · 17분

## 📌 핵심 요약 (치트시트)

```java
int i = 1;            // ① 시작값
while (i <= 5) {      // ② 조건이 true인 동안 반복
    System.out.println(i);
    i++;              // ③ 증가 — 빠뜨리면 무한 루프!
}

int sum = 0;          // 누적은 반복문 '밖'에서 0으로 시작
int n = 1;
while (n <= 10) {
    sum += n;
    n++;
}
```
- 무한 루프에 빠지면 터미널에서 Ctrl + C (채점기는 20초 뒤 자동 중단)

## 🧩 연습문제 힌트

- Q1: int i = 1; while (i <= 5) { println(i); i++; }
- Q3: sum += i 한 다음 "i=" + i + " sum=" + sum 출력

## 🃏 복습 카드

- Q: while문의 구조와 실행 순서는?
  A: while (조건) { 코드 } — 조건 검사 → true면 코드 실행 → 다시 조건 검사 … false면 종료
- Q: while문이 무한 루프에 빠지는 흔한 원인은?
  A: 반복 변수 증가(i++)를 빠뜨려서 조건이 영원히 true
- Q: 1부터 10까지 합을 구할 때 sum 변수는 어디서 선언하나?
  A: 반복문 밖에서 int sum = 0; (안에서 선언하면 매번 0으로 초기화됨)
- Q: while 조건이 처음부터 false면 몇 번 실행되나?
  A: 0번 (한 번도 실행 안 됨)
