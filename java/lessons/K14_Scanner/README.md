# K14. Scanner (입력 받기) · 기본 · 반복 예제

> ⏱ 강의 약 35분 + 연습문제 10분 · 🎬 [김영한의 자바 입문 - 코드로 시작하는 자바 첫걸음](https://www.inflearn.com/course/김영한의-자바-입문) 섹션 8(훈련(Scanner))
> 🧑‍💻 강의 예제는 직접 따라 치기 → 끝나면 터미널에서 Enter → 연습문제 3개 (출력 비교 자동 채점)

## 🎬 오늘 강의

- [섹션 8. Scanner 학습](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194594&subtitleLanguage=ko) · 12분
- [섹션 8. Scanner - 기본 예제](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194595&subtitleLanguage=ko) · 5분
- [섹션 8. Scanner - 반복 예제](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194596&subtitleLanguage=ko) · 9분
- [섹션 8. 문제와 풀이1](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194597&subtitleLanguage=ko) · 9분

## 📌 핵심 요약 (치트시트)

```java
import java.util.Scanner;   // 파일 맨 위

Scanner scanner = new Scanner(System.in);
String name = scanner.nextLine();   // 한 줄 전체
int age = scanner.nextInt();        // 정수 하나 (공백·줄바꿈으로 구분)
double d = scanner.nextDouble();

// ⚠️ nextInt() 다음에 nextLine()을 쓰면 남은 엔터(\n)를 읽어서 빈 문자열이 됨
//    → nextInt() 뒤에 scanner.nextLine(); 한 번 더 호출해서 버리기

while (true) {               // 0이 들어올 때까지 반복
    int x = scanner.nextInt();
    if (x == 0) break;
}
```
- 채점기는 문제마다 정해진 입력(QN.in)을 자동으로 넣어 줘요. 직접 실행할 땐 키보드로 입력
- 🎯 프로그래머스는 입력을 `solution(매개변수)`로 주기 때문에 Scanner를 안 써요 (백준·삼성 SW는 씀)

## 🧩 연습문제 힌트

- Q1: String name = scanner.nextLine(); int age = scanner.nextInt();
- Q3: while (true) 안에서 읽고, 0이면 break, 아니면 sum += x

## 🃏 복습 카드

- Q: Scanner로 한 줄 문자열과 정수를 읽는 메서드는?
  A: nextLine() 한 줄 전체, nextInt() 정수 하나
- Q: nextInt() 바로 뒤에 nextLine()을 호출하면 생기는 문제와 해결법은?
  A: 남아 있던 엔터를 읽어서 빈 문자열이 됨 → nextInt() 뒤에 nextLine()을 한 번 호출해서 버림
- Q: Scanner를 쓰려면 파일 맨 위에 무엇이 필요한가?
  A: import java.util.Scanner;
- Q: 0이 입력될 때까지 계속 숫자를 읽는 반복문의 형태는?
  A: while (true) { int x = sc.nextInt(); if (x == 0) break; ... }
