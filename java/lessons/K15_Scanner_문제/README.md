# K15. 훈련 문제 (Scanner + 조건 + 반복)

> ⏱ 강의 약 31분 + 연습문제 10분 · 🎬 [김영한의 자바 입문 - 코드로 시작하는 자바 첫걸음](https://www.inflearn.com/course/김영한의-자바-입문) 섹션 8(훈련(Scanner))
> 🧑‍💻 강의 예제는 직접 따라 치기 → 끝나면 터미널에서 Enter → 연습문제 3개 (출력 비교 자동 채점)

## 🎬 오늘 강의

- [섹션 8. 문제와 풀이2](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194599&subtitleLanguage=ko) · 8분
- [섹션 8. 문제와 풀이3](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194600&subtitleLanguage=ko) · 8분
- [섹션 8. 문제와 풀이4](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194601&subtitleLanguage=ko) · 15분

## 📌 핵심 요약 (치트시트)

```java
// 입력 → 계산 → 출력 패턴
Scanner sc = new Scanner(System.in);
int n = sc.nextInt();            // 개수 먼저
int sum = 0;
for (int i = 0; i < n; i++) {    // n번 반복하며 읽기
    sum += sc.nextInt();
}
double avg = (double) sum / n;
```

## 🧩 연습문제 힌트

- Q3: for로 n번 sc.nextInt() 해서 더하고, 평균은 (double) sum / n

## 🃏 복습 카드

- Q: 첫 줄에 개수 n, 다음에 n개의 수가 주어질 때 읽는 방법은?
  A: int n = sc.nextInt(); for (int i = 0; i < n; i++) { int x = sc.nextInt(); ... }
- Q: 입력받은 수 n으로 n단 구구단을 출력하는 반복문은?
  A: for (int i = 1; i <= 9; i++) System.out.println(n + " x " + i + " = " + n * i);
- Q: 입력받은 정수들의 평균을 소수점까지 출력하려면?
  A: (double) sum / n — 나누기 전에 double로 변환
