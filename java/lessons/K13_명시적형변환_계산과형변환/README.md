# K13. 명시적 형변환 · 계산과 형변환

> ⏱ 강의 약 36분 + 연습문제 10분 · 🎬 [김영한의 자바 입문 - 코드로 시작하는 자바 첫걸음](https://www.inflearn.com/course/김영한의-자바-입문) 섹션 7(스코프, 형변환)
> 🧑‍💻 강의 예제는 직접 따라 치기 → 끝나면 터미널에서 Enter → 연습문제 3개 (출력 비교 자동 채점)

## 🎬 오늘 강의

- [섹션 7. 형변환2 - 명시적 형변환](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194591&subtitleLanguage=ko) · 22분
- [섹션 7. 계산과 형변환](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194592&subtitleLanguage=ko) · 9분
- [섹션 7. 정리](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194593&subtitleLanguage=ko) · 5분
- [섹션 7. 섹션 7 퀴즈](https://www.inflearn.com/courses/lecture?courseId=332505&type=QUIZ&unitId=288303&subtitleLanguage=ko) · 퀴즈

## 📌 핵심 요약 (치트시트)

```java
double d = 1.9;
int i = (int) d;        // 1  큰 범위 → 작은 범위는 (타입)으로 '직접' 변환, 소수점 버림

int max = Integer.MAX_VALUE;   // 2147483647
max + 1                        // -2147483648  ← 오버플로 (에러 없이 이상한 값)
long big = 2147483648L;
int bad = (int) big;           // -2147483648  ← 범위를 넘는 값을 넣으면 깨짐

int sum = 7, n = 2;
sum / n            // 3     int / int = int
(double) sum / n   // 3.5   나누기 전에 double로
(double) (sum / n) // 3.0   이미 3이 된 뒤라 늦음
```

## 🧩 연습문제 힌트

- Q1: (int) d — 반올림이 아니라 버림
- Q2: long ok = (long) max + 1; — 더하기 '전에' long으로
- Q3: (double) sum / count — 나누기 전에 변환

## 🃏 복습 카드

- Q: double 3.9를 int로 바꾸면? 문법은?
  A: int i = (int) 3.9; → 3 (반올림이 아니라 소수점 버림)
- Q: int 최댓값(약 21억)에 1을 더하면?
  A: -2147483648. 에러 없이 음수가 되는 오버플로 → 큰 수는 처음부터 long
- Q: (double) sum / n 과 (double) (sum / n) 의 차이는? (sum=7, n=2)
  A: 3.5와 3.0. 뒤는 정수 나눗셈이 먼저 끝난 뒤 변환해서 소수점이 이미 사라짐
- Q: 같은 타입끼리 연산한 결과의 타입은?
  A: 같은 타입 (int / int → int). 다른 타입이면 큰 범위 타입으로
