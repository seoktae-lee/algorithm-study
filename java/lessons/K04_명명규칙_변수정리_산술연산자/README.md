# K04. 변수 명명 규칙 · 변수 문제 · 산술 연산자

> ⏱ 강의 약 36분 + 연습문제 10분 · 🎬 [김영한의 자바 입문 - 코드로 시작하는 자바 첫걸음](https://www.inflearn.com/course/김영한의-자바-입문) 섹션 3(변수), 4(연산자)
> 🧑‍💻 강의 예제는 직접 따라 치기 → 끝나면 터미널에서 Enter → 연습문제 3개 (출력 비교 자동 채점)

## 🎬 오늘 강의

- [섹션 3. 변수 명명 규칙](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194548&subtitleLanguage=ko) · 8분
- [섹션 3. 문제와 풀이](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194549&subtitleLanguage=ko) · 11분
- [섹션 3. 정리](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194550&subtitleLanguage=ko) · 6분
- [섹션 3. 섹션 3 퀴즈](https://www.inflearn.com/courses/lecture?courseId=332505&type=QUIZ&unitId=288273&subtitleLanguage=ko) · 퀴즈
- [섹션 4. 산술 연산자](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194560&subtitleLanguage=ko) · 11분

## 📌 핵심 요약 (치트시트)

```java
int studentCount;        // 변수·메서드: 소문자 시작 camelCase
class HelloWorld {}      // 클래스: 대문자 시작
final int MAX_SIZE = 10; // 상수: 대문자 + _
// 숫자로 시작 X (1st), 공백 X, 예약어 X (int, class)

10 + 3   // 13
10 - 3   // 7
10 * 3   // 30
10 / 3   // 3   ← 정수끼리 나누면 소수점 버림
10 % 3   // 1   ← 나머지
10 / 0   // ArithmeticException (실행 중 에러)
```

## 🧩 연습문제 힌트

- Q1: int sum = num1 + num2 + num3; int average = sum / 3;
- Q2: 10 / 3 은 3.33이 아니라 3이에요 (정수 나눗셈)
- Q3: 분 = 135 / 60, 초 = 135 % 60

## 🃏 복습 카드

- Q: 자바 변수 이름 규칙(필수)과 관례(camelCase)는?
  A: 숫자로 시작 X, 공백 X, 예약어 X / 변수는 소문자로 시작하는 camelCase (studentCount)
- Q: 클래스 이름과 상수 이름의 관례는?
  A: 클래스는 대문자로 시작 (HelloWorld), 상수는 전부 대문자 + _ (MAX_SIZE)
- Q: 자바에서 10 / 3과 10 % 3의 결과는?
  A: 3과 1. 정수끼리 나누면 소수점 버림, %는 나머지
- Q: 정수를 0으로 나누면?
  A: ArithmeticException (/ by zero) 실행 중 에러
