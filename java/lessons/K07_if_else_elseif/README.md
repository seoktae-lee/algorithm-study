# K07. if · else · else if

> ⏱ 강의 약 34분 + 연습문제 10분 · 🎬 [김영한의 자바 입문 - 코드로 시작하는 자바 첫걸음](https://www.inflearn.com/course/김영한의-자바-입문) 섹션 5(조건문)
> 🧑‍💻 강의 예제는 직접 따라 치기 → 끝나면 터미널에서 Enter → 연습문제 3개 (출력 비교 자동 채점)

## 🎬 오늘 강의

- [섹션 5. if문1 - if, else](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194569&subtitleLanguage=ko) · 10분
- [섹션 5. if문2 - else if](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194570&subtitleLanguage=ko) · 13분
- [섹션 5. if문3 - if문과 else if문](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194571&subtitleLanguage=ko) · 11분

## 📌 핵심 요약 (치트시트)

```java
if (score >= 90) {
    grade = "A";
} else if (score >= 80) {   // 위가 false일 때만 검사
    grade = "B";
} else {
    grade = "F";
}
// else if 체인: 위에서부터 '처음 참인 것 하나만' 실행 → 큰 범위 조건을 먼저

// 서로 독립된 조건(둘 다 적용 가능)은 if를 따로따로
if (price >= 10000) discount += 1000;
if (age <= 10) discount += 1000;
```

## 🧩 연습문제 힌트

- Q1: if (score >= 90) {...} else if (score >= 80) {...} ... else {...}
- Q2: else if로 이으면 하나만 적용돼요. 독립 조건은 if 두 개

## 🃏 복습 카드

- Q: if - else if - else 체인에서 실행되는 블록 수는?
  A: 조건이 처음 참인 블록 하나만 (없으면 else). 그래서 조건 순서가 중요
- Q: 점수로 등급(90+ A, 80+ B …)을 나눌 때 조건을 어떤 순서로 쓰나?
  A: 큰 값부터: score >= 90 → >= 80 → … (작은 것부터 쓰면 90점도 >= 60에 먼저 걸림)
- Q: else if 대신 if를 여러 개 따로 써야 하는 경우는?
  A: 조건이 서로 독립이라 여러 개가 동시에 적용될 수 있을 때 (예: 금액 할인 + 나이 할인)
- Q: if 뒤에 중괄호 {}를 생략하면?
  A: 바로 다음 한 문장만 if에 속함. 실수 방지를 위해 항상 {} 쓰기 권장
