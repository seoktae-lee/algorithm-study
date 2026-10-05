# K18. 향상된 for문 · 배열 문제

> ⏱ 강의 약 36분 + 연습문제 10분 · 🎬 [김영한의 자바 입문 - 코드로 시작하는 자바 첫걸음](https://www.inflearn.com/course/김영한의-자바-입문) 섹션 9(배열)
> 🧑‍💻 강의 예제는 직접 따라 치기 → 끝나면 터미널에서 Enter → 연습문제 3개 (출력 비교 자동 채점)

## 🎬 오늘 강의

- [섹션 9. 향상된 for문](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194610&subtitleLanguage=ko) · 8분
- [섹션 9. 문제와 풀이1](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194611&subtitleLanguage=ko) · 13분
- [섹션 9. 문제와 풀이2](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194612&subtitleLanguage=ko) · 15분

## 📌 핵심 요약 (치트시트)

```java
int[] numbers = {1, 2, 3, 4, 5};
for (int number : numbers) {        // 향상된 for (for-each): 값만 차례로
    System.out.println(number);
}
// 인덱스가 필요하면(역순, i번째 표시, 값 변경) 일반 for

int max = numbers[0];               // 최댓값: 첫 원소로 시작
for (int n : numbers) {
    if (n > max) max = n;
}

for (int i = numbers.length - 1; i >= 0; i--) { ... }   // 역순
```

## 🧩 연습문제 힌트

- Q1: for (int score : scores) sum += score; 평균은 (double) sum / scores.length
- Q3: i = arr.length - 1 에서 시작해 i >= 0 동안 i--

## 🃏 복습 카드

- Q: 향상된 for문의 형태는?
  A: for (int x : arr) { ... } — 배열 값을 처음부터 하나씩 x에 담아 반복
- Q: 향상된 for문을 쓸 수 없는(일반 for가 필요한) 경우는?
  A: 인덱스가 필요할 때: 역순·일부 구간·i번째 출력·배열 값 변경
- Q: 배열 최댓값을 구할 때 max의 시작값으로 좋은 것은?
  A: arr[0] (0으로 시작하면 전부 음수인 배열에서 틀림)
- Q: 배열을 역순으로 도는 for문은?
  A: for (int i = arr.length - 1; i >= 0; i--)
