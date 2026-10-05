# K20. 메서드 사용 · 정의 · 반환 타입

> ⏱ 강의 약 35분 + 연습문제 10분 · 🎬 [김영한의 자바 입문 - 코드로 시작하는 자바 첫걸음](https://www.inflearn.com/course/김영한의-자바-입문) 섹션 10(메서드)
> 🧑‍💻 강의 예제는 직접 따라 치기 → 끝나면 터미널에서 Enter → 연습문제 3개 (출력 비교 자동 채점)

## 🎬 오늘 강의

- [섹션 10. 메서드 사용](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194616&subtitleLanguage=ko) · 21분
- [섹션 10. 메서드 정의](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194617&subtitleLanguage=ko) · 6분
- [섹션 10. 반환 타입](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194618&subtitleLanguage=ko) · 8분

## 📌 핵심 요약 (치트시트)

```java
public static void printHeader() {       // 매개변수 없음, 반환 없음(void)
    System.out.println("= 시작 =");
}

public static boolean isEven(int n) {     // 반환 타입 boolean
    return n % 2 == 0;
}

public static String grade(int score) {
    if (score >= 60) {
        return "합격";
    }
    return "불합격";                         // 모든 경로에서 return 필요
}
// 호출할 때 넘기는 값 = 인수(argument), 받는 변수 = 매개변수(parameter)
```

## 🧩 연습문제 힌트

- Q2: 반환이 없으니 void. 호출은 printHeader();
- Q3: return n % 2 == 0; 처럼 비교식 결과(boolean)를 바로 돌려줄 수 있어요

## 🃏 복습 카드

- Q: 반환할 값이 없는 메서드의 반환 타입은?
  A: void (return 생략 가능, 중간에 끝내려면 return;)
- Q: 반환 타입이 int인 메서드에서 if 안에서만 return하면?
  A: 컴파일 에러. 모든 실행 경로에서 값을 return해야 함
- Q: 인수(argument)와 매개변수(parameter)의 차이는?
  A: 인수: 호출할 때 넘기는 값 add(5, 10)의 5, 10 / 매개변수: 메서드가 받는 변수 int a, int b
- Q: return을 만나면 그 뒤 코드는?
  A: 실행되지 않고 메서드가 즉시 끝나며 값을 호출한 곳으로 돌려줌
