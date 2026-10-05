# K19. 배열 문제 · 배열 정리 · 메서드 시작

> ⏱ 강의 약 31분 + 연습문제 10분 · 🎬 [김영한의 자바 입문 - 코드로 시작하는 자바 첫걸음](https://www.inflearn.com/course/김영한의-자바-입문) 섹션 9(배열), 10(메서드)
> 🧑‍💻 강의 예제는 직접 따라 치기 → 끝나면 터미널에서 Enter → 연습문제 2개 (출력 비교 자동 채점)

## 🎬 오늘 강의

- [섹션 9. 문제와 풀이3](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194613&subtitleLanguage=ko) · 13분
- [섹션 9. 정리](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194614&subtitleLanguage=ko) · 9분
- [섹션 9. 섹션 9 퀴즈](https://www.inflearn.com/courses/lecture?courseId=332505&type=QUIZ&unitId=288377&subtitleLanguage=ko) · 퀴즈
- [섹션 10. 메서드 시작](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194615&subtitleLanguage=ko) · 9분

## 📌 핵심 요약 (치트시트)

```java
public class Main {
    public static void main(String[] args) {
        int sum = add(5, 10);          // 메서드 호출: 이름(인수)
        System.out.println(sum);       // 15
    }

    // 제어자  반환타입 메서드이름(매개변수)
    public static int add(int a, int b) {
        return a + b;                  // 결과를 돌려줌
    }
}
```
- 같은 코드를 여러 번 쓰는 대신 메서드로 묶고 이름으로 호출 → 중복 제거
- 메서드는 class 안, main **밖**에 만들어요 (메서드 안에 메서드 X)

## 🧩 연습문제 힌트

- Q1: 최댓값 대신 최댓값의 인덱스(maxIndex)를 기억하고 names[maxIndex]
- Q2: public static int add(int a, int b) { return a + b; } 를 main 아래(클래스 안)에

## 🃏 복습 카드

- Q: 메서드 선언의 구성 요소는?
  A: 제어자(public static) 반환타입 메서드이름(매개변수) { 본문 } 예) public static int add(int a, int b)
- Q: 메서드를 쓰는 이유는?
  A: 같은 코드 중복 제거, 이름으로 의미를 드러내 읽기 쉬움, 한 곳만 고치면 됨
- Q: 메서드는 코드의 어디에 작성하나?
  A: 클래스 안, 다른 메서드(main) 밖. 메서드 안에 메서드를 만들 수 없음
- Q: 이름과 가격이 다른 배열에 있을 때 가장 비싼 상품 이름을 찾는 방법은?
  A: 가격 배열에서 최댓값의 '인덱스'를 기억해 두고 names[maxIndex] 출력
