# K17. 배열 리팩토링 · 2차원 배열

> ⏱ 강의 약 31분 + 연습문제 10분 · 🎬 [김영한의 자바 입문 - 코드로 시작하는 자바 첫걸음](https://www.inflearn.com/course/김영한의-자바-입문) 섹션 9(배열)
> 🧑‍💻 강의 예제는 직접 따라 치기 → 끝나면 터미널에서 Enter → 연습문제 3개 (출력 비교 자동 채점)

## 🎬 오늘 강의

- [섹션 9. 배열 리펙토링](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194606&subtitleLanguage=ko) · 11분
- [섹션 9. 2차원 배열 - 시작](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194607&subtitleLanguage=ko) · 5분
- [섹션 9. 2차원 배열 - 리팩토링1](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194608&subtitleLanguage=ko) · 4분
- [섹션 9. 2차원 배열 - 리팩토링2](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194609&subtitleLanguage=ko) · 11분

## 📌 핵심 요약 (치트시트)

```java
int[][] arr = new int[2][3];        // 2행 3열
arr[0][1] = 5;                      // [행][열]

int[][] arr2 = {
    {1, 2, 3},
    {4, 5, 6}
};
arr2.length       // 2 (행 개수)
arr2[0].length    // 3 (열 개수)

for (int row = 0; row < arr2.length; row++) {
    for (int col = 0; col < arr2[row].length; col++) {
        System.out.print(arr2[row][col] + " ");
    }
    System.out.println();
}
```

## 🧩 연습문제 힌트

- Q1: 안쪽에서 print(값 + " "), 안쪽이 끝나면 println()
- Q2: int value = 1; 을 두고 칸마다 arr[row][col] = value; value++;

## 🃏 복습 카드

- Q: 2차원 배열 int[][] arr = new int[2][3]; 에서 arr.length와 arr[0].length는?
  A: 2(행 개수)와 3(열 개수)
- Q: 2차원 배열 전체를 출력하는 반복문 구조는?
  A: 바깥 for: row < arr.length, 안쪽 for: col < arr[row].length, 안쪽 끝나면 println()
- Q: int[] arr = {1, 2, 3}; 처럼 {}로 값을 바로 넣는 문법은 언제 쓸 수 있나?
  A: 선언과 동시에만. 이미 선언된 변수에는 arr = new int[]{1, 2, 3}; 으로
- Q: 배열을 쓰면 변수 여러 개(student1, student2…)보다 좋은 점은?
  A: 반복문으로 한 번에 처리 가능 → 개수가 늘어도 코드가 그대로
