# K08. switch · 삼항 연산자 · 조건문 문제

> ⏱ 강의 약 35분 + 연습문제 10분 · 🎬 [김영한의 자바 입문 - 코드로 시작하는 자바 첫걸음](https://www.inflearn.com/course/김영한의-자바-입문) 섹션 5(조건문)
> 🧑‍💻 강의 예제는 직접 따라 치기 → 끝나면 터미널에서 Enter → 연습문제 3개 (출력 비교 자동 채점)

## 🎬 오늘 강의

- [섹션 5. switch문](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194572&subtitleLanguage=ko) · 13분
- [섹션 5. 삼항 연산자](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194573&subtitleLanguage=ko) · 5분
- [섹션 5. 문제와 풀이1](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194574&subtitleLanguage=ko) · 6분
- [섹션 5. 문제와 풀이2](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194575&subtitleLanguage=ko) · 11분

## 📌 핵심 요약 (치트시트)

```java
switch (grade) {            // 값이 '같은지'만 비교
    case 1:
        coupon = 1000;
        break;              // break 없으면 아래 case까지 계속 실행(fall-through)
    case 2:
        coupon = 2000;
        break;
    default:                // 어느 case도 아니면
        coupon = 500;
}
// 자바 14+ 새 switch
int coupon = switch (grade) {
    case 1 -> 1000;
    case 2 -> 2000;
    default -> 500;
};

String status = (age >= 18) ? "성인" : "미성년자";   // 조건 ? 참일 때 : 거짓일 때
num % 2 == 0   // 짝수 판별
```

## 🧩 연습문제 힌트

- Q1: case 2: coupon = 2000; break; … default: coupon = 500;
- Q3: num % 2 == 0 이면 짝수

## 🃏 복습 카드

- Q: switch에서 case 끝에 break를 빼먹으면?
  A: 조건에 맞는 case부터 아래 case들이 연달아 실행됨 (fall-through)
- Q: switch와 if의 차이는?
  A: switch는 값이 같은지만 비교(==), 범위 조건(>=)은 if로
- Q: 삼항 연산자의 형태는?
  A: 조건 ? 참일 때 값 : 거짓일 때 값  예) age >= 18 ? "성인" : "미성년자"
- Q: 어떤 수가 짝수인지 판별하는 식은?
  A: num % 2 == 0 (2로 나눈 나머지가 0)
