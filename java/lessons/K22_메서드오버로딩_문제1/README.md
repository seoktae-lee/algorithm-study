# K22. 메서드 오버로딩 · 메서드 문제

> ⏱ 강의 약 31분 + 연습문제 10분 · 🎬 [김영한의 자바 입문 - 코드로 시작하는 자바 첫걸음](https://www.inflearn.com/course/김영한의-자바-입문) 섹션 10(메서드)
> 🧑‍💻 강의 예제는 직접 따라 치기 → 끝나면 터미널에서 Enter → 연습문제 3개 (출력 비교 자동 채점)

## 🎬 오늘 강의

- [섹션 10. 메서드 오버로딩](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194622&subtitleLanguage=ko) · 12분
- [섹션 10. 문제와 풀이1](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194623&subtitleLanguage=ko) · 19분

## 📌 핵심 요약 (치트시트)

```java
// 오버로딩: 이름은 같고 매개변수(타입·개수·순서)가 다른 메서드 여러 개
public static int add(int a, int b)          { return a + b; }
public static int add(int a, int b, int c)   { return a + b + c; }
public static double add(double a, double b) { return a + b; }

add(1, 2);        // 첫 번째
add(1, 2, 3);     // 두 번째
add(1.5, 2.5);    // 세 번째
// 반환 타입만 다른 건 오버로딩 X (컴파일 에러)
// 메서드 시그니처 = 이름 + 매개변수 타입 목록
```

## 🧩 연습문제 힌트

- Q2: (double) sum / 3 — 정수 나눗셈 주의

## 🃏 복습 카드

- Q: 메서드 오버로딩이란?
  A: 이름이 같고 매개변수의 타입·개수·순서가 다른 메서드를 여러 개 정의하는 것
- Q: 반환 타입만 다르게 같은 이름 메서드를 만들면?
  A: 컴파일 에러. 오버로딩은 매개변수가 달라야 함
- Q: 메서드 시그니처란?
  A: 메서드 이름 + 매개변수 타입(순서) — 자바가 메서드를 구분하는 기준
- Q: add(int,int)와 add(double,double)가 있을 때 add(1, 2)는 어느 쪽?
  A: 정확히 일치하는 add(int,int) 우선. 없을 때만 형변환 가능한 쪽
