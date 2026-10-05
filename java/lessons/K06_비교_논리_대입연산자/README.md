# K06. 비교 · 논리 · 대입 연산자 · 연산자 정리

> ⏱ 강의 약 32분 + 연습문제 10분 · 🎬 [김영한의 자바 입문 - 코드로 시작하는 자바 첫걸음](https://www.inflearn.com/course/김영한의-자바-입문) 섹션 4(연산자)
> 🧑‍💻 강의 예제는 직접 따라 치기 → 끝나면 터미널에서 Enter → 연습문제 3개 (출력 비교 자동 채점)

## 🎬 오늘 강의

- [섹션 4. 비교 연산자](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194564&subtitleLanguage=ko) · 9분
- [섹션 4. 논리 연산자](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194565&subtitleLanguage=ko) · 7분
- [섹션 4. 대입 연산자](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194566&subtitleLanguage=ko) · 5분
- [섹션 4. 문제와 풀이](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194567&subtitleLanguage=ko) · 6분
- [섹션 4. 정리](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194568&subtitleLanguage=ko) · 5분
- [섹션 4. 섹션 4 퀴즈](https://www.inflearn.com/courses/lecture?courseId=332505&type=QUIZ&unitId=288285&subtitleLanguage=ko) · 퀴즈

## 📌 핵심 요약 (치트시트)

```java
a == b   a != b   a > b   a >= b      // 결과는 boolean
"hello".equals(str)   // 문자열 비교는 == 말고 equals!

a > 10 && a < 20   // 그리고 (10 < a < 20 은 문법 에러)
a < 0 || a > 100   // 또는
!flag              // 반대

x += 5;   // x = x + 5
x -= 3;   x *= 2;   x /= 2;   x %= 3;
```

## 🧩 연습문제 힌트

- Q1: a > 10 && a < 20
- Q2: == 는 다른 객체라 false. 내용 비교는 str1.equals(str2)
- Q3: x += 5; x *= 2; x -= 3;

## 🃏 복습 카드

- Q: 문자열이 같은지 비교할 때 == 대신 쓰는 것은?
  A: str1.equals(str2). ==는 같은 객체인지(참조) 비교라 문자열 내용 비교에 쓰면 안 됨
- Q: 변수 a가 10 초과 20 미만인지 검사하는 식은?
  A: a > 10 && a < 20 (10 < a < 20 은 컴파일 에러)
- Q: &&, ||, ! 의 뜻은?
  A: && 둘 다 참(AND), || 하나라도 참(OR), ! 참/거짓 반대(NOT)
- Q: int x = 10; x += 5; x *= 2; 이후 x는?
  A: 30 (x = 10+5 = 15 → 15*2 = 30)
