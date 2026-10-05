# K10. do-while · break · continue · for · 중첩 반복문

> ⏱ 강의 약 31분 + 연습문제 10분 · 🎬 [김영한의 자바 입문 - 코드로 시작하는 자바 첫걸음](https://www.inflearn.com/course/김영한의-자바-입문) 섹션 6(반복문)
> 🧑‍💻 강의 예제는 직접 따라 치기 → 끝나면 터미널에서 Enter → 연습문제 3개 (출력 비교 자동 채점)

## 🎬 오늘 강의

- [섹션 6. do-while문](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194580&subtitleLanguage=ko) · 3분
- [섹션 6. break, continue](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194581&subtitleLanguage=ko) · 8분
- [섹션 6. for문1](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194582&subtitleLanguage=ko) · 10분
- [섹션 6. for문2](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194583&subtitleLanguage=ko) · 6분
- [섹션 6. 중첩 반복문](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194584&subtitleLanguage=ko) · 4분

## 📌 핵심 요약 (치트시트)

```java
do { ... } while (조건);    // 최소 1번은 실행

for (int i = 1; i <= 10; i++) {   // (초기식; 조건식; 증감식)
    if (i % 3 == 0) continue;     // 이번 회차만 건너뛰고 다음 i로
    if (i > 8) break;             // 반복문 즉시 종료
    System.out.println(i);
}

for (int i = 2; i <= 3; i++) {        // 바깥 2번
    for (int j = 1; j <= 3; j++) {    // 안쪽 3번 → 총 6번
        System.out.println(i + " * " + j + " = " + i * j);
    }
}
```

## 🧩 연습문제 힌트

- Q1: while (true) { sum += i; if (sum > 10) break; i++; }
- Q2: if (i % 3 == 0) continue;
- Q3: 바깥 i: 2~3, 안쪽 j: 1~3. i * j 는 곱셈이 먼저라 괄호 없어도 OK

## 🃏 복습 카드

- Q: do-while이 while과 다른 점은?
  A: 조건을 나중에 검사하므로 조건이 처음부터 false여도 최소 1번은 실행
- Q: break와 continue의 차이는?
  A: break: 반복문을 즉시 빠져나감 / continue: 이번 회차의 남은 코드를 건너뛰고 다음 회차로
- Q: for문의 괄호 안 세 부분과 실행 순서는?
  A: (초기식; 조건식; 증감식) — 초기식 1번 → 조건 검사 → 본문 → 증감 → 조건 검사 …
- Q: 바깥 for가 3번, 안쪽 for가 4번 돌면 안쪽 본문은 총 몇 번 실행되나?
  A: 12번 (3 × 4)
- Q: for와 while은 언제 쓰나?
  A: 반복 횟수가 정해져 있으면 for, 조건이 바뀔 때까지(횟수 모름)면 while
