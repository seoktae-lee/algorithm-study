# K21. 메서드 호출과 값 전달 · 메서드와 형변환

> ⏱ 강의 약 31분 + 연습문제 10분 · 🎬 [김영한의 자바 입문 - 코드로 시작하는 자바 첫걸음](https://www.inflearn.com/course/김영한의-자바-입문) 섹션 10(메서드)
> 🧑‍💻 강의 예제는 직접 따라 치기 → 끝나면 터미널에서 Enter → 연습문제 3개 (출력 비교 자동 채점)

## 🎬 오늘 강의

- [섹션 10. 메서드 호출과 값 전달1](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194619&subtitleLanguage=ko) · 13분
- [섹션 10. 메서드 호출과 값 전달2](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194620&subtitleLanguage=ko) · 12분
- [섹션 10. 메서드와 형변환](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194621&subtitleLanguage=ko) · 6분

## 📌 핵심 요약 (치트시트)

```java
public static void change(int x) {
    x = 20;            // 복사본만 바뀜
}
int num = 10;
change(num);
System.out.println(num);   // 10 ← 자바는 값을 '복사'해서 넘김

// 바꾼 값을 쓰려면 return으로 돌려받기
public static int changeAndReturn(int x) { return 20; }
num = changeAndReturn(num);   // 20

public static void printDouble(double d) { ... }
printDouble(5);          // int → double 자동 형변환 OK (5.0)
public static void printInt(int i) { ... }
printInt((int) 1.5);     // double → int는 직접 캐스팅해야 호출 가능
```

## 🧩 연습문제 힌트

- Q1: 반환 타입을 int로 바꾸고 return x; → main에서 num = changeNumber(num);
- Q2: int 5를 넘겨도 double 매개변수가 받으면 5.0으로 출력돼요
- Q3: double → int는 (int) 캐스팅이 필요해요

## 🃏 복습 카드

- Q: 메서드 안에서 매개변수 값을 바꾸면 호출한 쪽 변수도 바뀌나?
  A: 안 바뀜. 자바는 항상 값을 복사해서 전달 (기본형 기준)
- Q: 메서드에서 바꾼 값을 호출한 쪽에서 쓰려면?
  A: return으로 돌려받아 대입: num = change(num);
- Q: double 매개변수 메서드에 int 인수를 넘기면?
  A: 자동 형변환되어 호출됨 (5 → 5.0)
- Q: int 매개변수 메서드에 1.5를 넘기려면?
  A: printInt((int) 1.5) 처럼 명시적 형변환 필요 (안 하면 컴파일 에러)
