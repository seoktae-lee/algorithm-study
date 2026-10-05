# K11. 반복문 문제 · 반복문 정리 · 스코프1

> ⏱ 강의 약 33분 + 연습문제 10분 · 🎬 [김영한의 자바 입문 - 코드로 시작하는 자바 첫걸음](https://www.inflearn.com/course/김영한의-자바-입문) 섹션 6(반복문), 7(스코프, 형변환)
> 🧑‍💻 강의 예제는 직접 따라 치기 → 끝나면 터미널에서 Enter → 연습문제 3개 (출력 비교 자동 채점)

## 🎬 오늘 강의

- [섹션 6. 문제와 풀이1](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194585&subtitleLanguage=ko) · 8분
- [섹션 6. 문제와 풀이2](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194586&subtitleLanguage=ko) · 9분
- [섹션 6. 정리](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194587&subtitleLanguage=ko) · 5분
- [섹션 6. 섹션 6 퀴즈](https://www.inflearn.com/courses/lecture?courseId=332505&type=QUIZ&unitId=288298&subtitleLanguage=ko) · 퀴즈
- [섹션 7. 스코프1 - 지역 변수와 스코프](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194588&subtitleLanguage=ko) · 11분

## 📌 핵심 요약 (치트시트)

```java
// 별 피라미드: 바깥 = 줄, 안쪽 = 그 줄의 별 개수
for (int row = 1; row <= 4; row++) {
    for (int col = 1; col <= row; col++) {
        System.out.print("*");
    }
    System.out.println();
}

// 스코프: 변수는 '선언된 블록 { } 안에서만' 사용 가능
int m = 10;
if (true) {
    int x = 20;      // x는 이 if 블록 안에서만
    System.out.println(m + x);   // OK (바깥 m은 안에서 사용 가능)
}
// System.out.println(x);   // 컴파일 에러
```

## 🧩 연습문제 힌트

- Q1: 안쪽 for에서 print("*") (줄바꿈 X), 안쪽이 끝나면 println()
- Q2: int result = 1; 에서 시작해 result *= i
- Q3: x를 if 밖에서 먼저 선언(int x = 0;)하고, if 안에서는 x = 20; 으로 값만 넣기

## 🃏 복습 카드

- Q: 지역 변수의 스코프(사용 범위)는?
  A: 변수가 선언된 코드 블록 { } 안 (선언 이후부터 블록 끝까지)
- Q: for (int i = 0; ...) 에서 선언한 i를 for문 밖에서 쓸 수 있나?
  A: 없음. i의 스코프는 for문 안. 밖에서 필요하면 for 밖에서 선언
- Q: 중첩 반복문으로 직각 삼각형 별을 찍을 때 안쪽 반복의 조건은?
  A: col <= row (줄 번호만큼 별을 찍음), 안쪽 끝나고 println()으로 줄바꿈
- Q: n! (팩토리얼)을 반복문으로 구할 때 결과 변수의 시작값은?
  A: 1 (곱셈의 시작은 0이 아니라 1)
