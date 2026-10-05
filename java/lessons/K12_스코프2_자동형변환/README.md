# K12. 스코프 존재 이유 · 자동 형변환

> ⏱ 강의 약 23분 + 연습문제 10분 · 🎬 [김영한의 자바 입문 - 코드로 시작하는 자바 첫걸음](https://www.inflearn.com/course/김영한의-자바-입문) 섹션 7(스코프, 형변환)
> 🧑‍💻 강의 예제는 직접 따라 치기 → 끝나면 터미널에서 Enter → 연습문제 2개 (출력 비교 자동 채점)

## 🎬 오늘 강의

- [섹션 7. 스코프2 - 스코프 존재 이유](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194589&subtitleLanguage=ko) · 14분
- [섹션 7. 형변환1 - 자동 형변환](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194590&subtitleLanguage=ko) · 9분

## 📌 핵심 요약 (치트시트)

```java
// 스코프는 좁게: 필요한 블록 안에서만 변수 선언 → 메모리 절약, 코드 읽기 쉬움
if (m > 0) {
    int temp = m * 2;   // temp는 여기서만 필요
}

// 자동 형변환: 작은 범위 → 큰 범위는 저절로
int i = 10;
long l = i;       // 10
double d = i;     // 10.0
// 범위: byte < short < int < long < float < double

double r = 10 / 4;     // 2.0  (int끼리 먼저 나눔 → 2 → double)
double r2 = 10 / 4.0;  // 2.5  (한쪽이 double이면 double로 계산)
```

## 🧩 연습문제 힌트

- Q1: long l = i; double d = i; (캐스팅 없이 그냥 대입)
- Q2: 한쪽만 double이면 됨: a / (double) b 또는 (double) a / b

## 🃏 복습 카드

- Q: 변수의 스코프를 좁게(필요한 곳에서만) 선언하는 이유 2가지는?
  A: ① 블록이 끝나면 메모리에서 제거되어 효율적 ② 변수가 쓰이는 범위가 좁아 코드 읽기·유지보수가 쉬움
- Q: int → long → double 처럼 작은 범위에서 큰 범위로 대입하면?
  A: 자동 형변환(묵시적). 값 손실 없음. int 10 → double 10.0
- Q: double r = 10 / 4; 의 결과는? 2.5가 나오게 하려면?
  A: 2.0 (int끼리 먼저 나눔). 10 / 4.0 또는 (double) 10 / 4
- Q: 서로 다른 타입끼리 연산하면 결과 타입은?
  A: 더 큰 범위 타입으로 자동 변환되어 계산 (int + double → double)
