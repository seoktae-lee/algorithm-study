# K16. 훈련 정리 · 배열 시작 · 선언과 생성 · 배열 사용

> ⏱ 강의 약 35분 + 연습문제 10분 · 🎬 [김영한의 자바 입문 - 코드로 시작하는 자바 첫걸음](https://www.inflearn.com/course/김영한의-자바-입문) 섹션 8(훈련(Scanner)), 9(배열)
> 🧑‍💻 강의 예제는 직접 따라 치기 → 끝나면 터미널에서 Enter → 연습문제 3개 (출력 비교 자동 채점)

## 🎬 오늘 강의

- [섹션 8. 정리](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194602&subtitleLanguage=ko) · 3분
- [섹션 8. 섹션 8 퀴즈](https://www.inflearn.com/courses/lecture?courseId=332505&type=QUIZ&unitId=288364&subtitleLanguage=ko) · 퀴즈
- [섹션 9. 배열 시작](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194603&subtitleLanguage=ko) · 5분
- [섹션 9. 배열의 선언과 생성](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194604&subtitleLanguage=ko) · 15분
- [섹션 9. 배열 사용](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194605&subtitleLanguage=ko) · 12분

## 📌 핵심 요약 (치트시트)

```java
int[] students = new int[5];        // 크기 5, 기본값 0으로 채워짐
students[0] = 90;                   // 인덱스는 0부터
students[4] = 50;                   // 마지막 = length - 1
// students[5] = 1;                 // ArrayIndexOutOfBoundsException

int[] arr = {1, 2, 3, 4, 5};        // 선언과 동시에 값 넣기
arr.length                          // 5 (괄호 없음)

for (int i = 0; i < arr.length; i++) {
    System.out.println(arr[i]);
}
// 기본값: int 0, double 0.0, boolean false, String null
```

## 🧩 연습문제 힌트

- Q1: 인덱스는 0부터지만 학생 번호는 i + 1

## 🃏 복습 카드

- Q: 크기 5인 int 배열을 만드는 코드와, 처음 들어 있는 값은?
  A: int[] arr = new int[5]; 모두 0 (boolean은 false, String은 null)
- Q: 배열 인덱스 범위와 범위를 벗어나면 나는 에러는?
  A: 0 ~ length-1. 벗어나면 ArrayIndexOutOfBoundsException
- Q: 배열 길이를 구하는 코드는?
  A: arr.length (괄호 없음. String은 s.length() 괄호 있음)
- Q: 배열 전체를 for로 도는 표준 형태는?
  A: for (int i = 0; i < arr.length; i++) { arr[i] ... }
