# K05. 문자열 더하기 · 연산자 우선순위 · 증감 연산자

> ⏱ 강의 약 32분 + 연습문제 10분 · 🎬 [김영한의 자바 입문 - 코드로 시작하는 자바 첫걸음](https://www.inflearn.com/course/김영한의-자바-입문) 섹션 4(연산자)
> 🧑‍💻 강의 예제는 직접 따라 치기 → 끝나면 터미널에서 Enter → 연습문제 3개 (출력 비교 자동 채점)

## 🎬 오늘 강의

- [섹션 4. 문자열 더하기](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194561&subtitleLanguage=ko) · 5분
- [섹션 4. 연산자 우선순위](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194562&subtitleLanguage=ko) · 11분
- [섹션 4. 증감 연산자](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194563&subtitleLanguage=ko) · 16분

## 📌 핵심 요약 (치트시트)

```java
"hello " + "java"   // "hello java"
"a + b = " + 30     // "a + b = 30"  문자열 + 숫자 → 문자열
"1" + 2 + 3         // "123"  왼쪽부터 계산
1 + 2 + "3"         // "33"   (1+2=3 먼저) + "3"
"합: " + (1 + 2)     // "합: 3"  괄호 먼저

2 + 3 * 4           // 14 (곱셈 먼저)
(2 + 3) * 4         // 20 → 헷갈리면 괄호!

int a = 5;
int b = ++a;   // 전위: 먼저 증가 → a=6, b=6
int c = a++;   // 후위: 대입 후 증가 → c=6, a=7
```

## 🧩 연습문제 힌트

- Q1: 괄호가 없으면 "a + b = 10" + 20 → "a + b = 1020"
- Q2: 곱셈이 먼저라 price * count + delivery 그대로 OK
- Q3: x++; 는 x = x + 1; 과 같아요

## 🃏 복습 카드

- Q: "a + b = " + 10 + 20 의 결과는? 30이 나오게 하려면?
  A: "a + b = 1020" (왼쪽부터 문자열로 이어짐). "a + b = " + (10 + 20)
- Q: 1 + 2 + "3" 의 결과는?
  A: "33" (1+2=3을 먼저 계산한 뒤 "3"과 이어 붙임)
- Q: 연산자 우선순위가 헷갈릴 때 원칙은?
  A: 괄호 ()를 써서 명확하게. 곱셈·나눗셈이 덧셈·뺄셈보다 먼저
- Q: int a = 5; int b = ++a; int c = a++; 이후 a, b, c는?
  A: a=7, b=6, c=6 (++a는 먼저 증가, a++는 값을 쓴 뒤 증가)
