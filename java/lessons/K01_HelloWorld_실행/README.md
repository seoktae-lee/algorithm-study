# K01. Hello World · 자바 프로그램 실행

> ⏱ 강의 약 33분 + 연습문제 10분 · 🎬 [김영한의 자바 입문 - 코드로 시작하는 자바 첫걸음](https://www.inflearn.com/course/김영한의-자바-입문) 섹션 1(강의 소개), 2(Hello World)
> 🧑‍💻 강의 예제는 직접 따라 치기 → 끝나면 터미널에서 Enter → 연습문제 2개 (출력 비교 자동 채점)

## 🎬 오늘 강의

- [섹션 1. 강의 소개](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194533&subtitleLanguage=ko) · 4분
- [섹션 2. 개발 환경 설정](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194537&subtitleLanguage=ko) · 14분
- [섹션 2. 다운로드 소스 코드 실행 방법](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194538&subtitleLanguage=ko) · 4분
- [섹션 2. 자바 프로그램 실행](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194539&subtitleLanguage=ko) · 11분

## 📌 핵심 요약 (치트시트)

```java
public class HelloJava {                 // 클래스 이름 = 파일 이름(HelloJava.java)
    public static void main(String[] args) {   // 프로그램 시작점
        System.out.println("hello java"); // 출력 후 줄바꿈
        System.out.print("no newline");   // 줄바꿈 없음
    }                                     // 문장 끝은 ; , 블록은 { }
}
```
- 실행 흐름: `javac HelloJava.java`(컴파일 → .class) → `java HelloJava`(실행). 요즘은 `java HelloJava.java` 한 번에도 됨
- 이 트랙 연습문제도 `main` 안에 코드를 쓰고 `println`으로 출력하면 채점기가 출력을 비교해요

## 🧩 연습문제 힌트

- Q1: System.out.println("..."); 두 번. 문자열은 큰따옴표
- Q2: print는 줄바꿈이 없어요. 줄을 바꾸려면 마지막에 System.out.println(); 또는 println 사용

## 🃏 복습 카드

- Q: 자바 프로그램은 어디서부터 실행되나?
  A: public static void main(String[] args) 메서드부터 위에서 아래로
- Q: System.out.println과 System.out.print의 차이는?
  A: println은 출력 후 줄바꿈, print는 줄바꿈 없음
- Q: 자바 문장의 끝과 코드 블록은 무엇으로 표시하나?
  A: 문장 끝은 세미콜론(;), 블록은 중괄호 { }
- Q: public class Hello가 들어 있는 파일의 이름은?
  A: Hello.java (public 클래스 이름과 파일 이름이 같아야 함, 대소문자 포함)
- Q: javac와 java 명령은 각각 무엇을 하나?
  A: javac: .java 소스를 .class(바이트코드)로 컴파일 / java: .class를 JVM에서 실행
