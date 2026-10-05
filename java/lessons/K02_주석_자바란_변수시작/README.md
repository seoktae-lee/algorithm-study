# K02. 주석 · 자바란? · 변수 시작

> ⏱ 강의 약 34분 + 연습문제 10분 · 🎬 [김영한의 자바 입문 - 코드로 시작하는 자바 첫걸음](https://www.inflearn.com/course/김영한의-자바-입문) 섹션 2(Hello World), 3(변수)
> 🧑‍💻 강의 예제는 직접 따라 치기 → 끝나면 터미널에서 Enter → 연습문제 3개 (출력 비교 자동 채점)

## 🎬 오늘 강의

- [섹션 2. 주석(comment)](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194540&subtitleLanguage=ko) · 5분
- [섹션 2. 자바란?](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194541&subtitleLanguage=ko) · 13분
- [섹션 2. 섹션 2 퀴즈](https://www.inflearn.com/courses/lecture?courseId=332505&type=QUIZ&unitId=288261&subtitleLanguage=ko) · 퀴즈
- [섹션 3. 변수 시작](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194543&subtitleLanguage=ko) · 13분
- [섹션 3. 변수 값 변경](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194544&subtitleLanguage=ko) · 3분

## 📌 핵심 요약 (치트시트)

```java
// 한 줄 주석
/* 여러 줄
   주석 */
int a = 10;      // 변수 선언 + 값 넣기
a = 50;          // 값 변경: 기존 값은 사라지고 새 값
System.out.println(a);   // 50 (변수 이름 a를 쓰면 값이 나옴, "a"는 그냥 글자)
```
- 자바 소스(.java) → 컴파일 → 바이트코드(.class) → JVM이 실행 → OS가 달라도 같은 코드가 돌아감

## 🧩 연습문제 힌트

- Q1: int a = 10; → println(a) → a = 50; → println(a). 두 번째는 int를 다시 쓰지 않아요
- Q2: 줄 맨 앞에 // 를 붙이면 그 줄은 실행되지 않아요 (VS Code 단축키 ⌘/)
- Q3: "num = " + num 처럼 문자열과 변수를 + 로 이어 붙일 수 있어요 (섹션 4에서 자세히)

## 🃏 복습 카드

- Q: 자바 주석 2가지 문법은?
  A: // 한 줄 주석, /* ... */ 여러 줄 주석. 실행되지 않음
- Q: 자바가 운영체제(윈도우·맥)에 상관없이 실행되는 이유는?
  A: 컴파일된 바이트코드(.class)를 OS별 JVM(자바 가상 머신)이 실행하기 때문
- Q: System.out.println(a)와 System.out.println("a")의 차이는?
  A: a는 변수 a에 담긴 값, "a"는 글자 a 그대로
- Q: int a = 10; a = 20; 이후 a의 값은?
  A: 20. 대입(=)하면 기존 값은 사라지고 새 값이 저장됨
