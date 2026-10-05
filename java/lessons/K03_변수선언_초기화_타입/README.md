# K03. 변수 선언과 초기화 · 변수 타입

> ⏱ 강의 약 36분 + 연습문제 10분 · 🎬 [김영한의 자바 입문 - 코드로 시작하는 자바 첫걸음](https://www.inflearn.com/course/김영한의-자바-입문) 섹션 3(변수)
> 🧑‍💻 강의 예제는 직접 따라 치기 → 끝나면 터미널에서 Enter → 연습문제 2개 (출력 비교 자동 채점)

## 🎬 오늘 강의

- [섹션 3. 변수 선언과 초기화](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194545&subtitleLanguage=ko) · 13분
- [섹션 3. 변수 타입1](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194546&subtitleLanguage=ko) · 8분
- [섹션 3. 변수 타입2](https://www.inflearn.com/courses/lecture?courseId=332505&type=LECTURE&unitId=194547&subtitleLanguage=ko) · 15분

## 📌 핵심 요약 (치트시트)

```java
int a;            // 선언 (상자만 만듦)
a = 10;           // 초기화 (처음 값 넣기)
int b = 20, c = 30;

int i = 100;              // 정수 (기본)
long l = 10000000000L;    // 큰 정수, 끝에 L
double d = 3.14;          // 실수 (기본)
float f = 3.14f;          // 끝에 f (거의 안 씀)
boolean ok = true;        // true / false
char ch = 'A';            // 문자 하나, 작은따옴표
String s = "Java";        // 문자열, 큰따옴표 (S 대문자)
```
- 지역 변수는 **초기화 안 하고 읽으면 컴파일 에러**
- 실무·코테에서 주로: `int`, `long`, `double`, `boolean`, `String`

## 🧩 연습문제 힌트

- Q1: 100억은 int(약 21억)를 넘으니 long, 끝에 L. 문자는 'A', 문자열은 "Java"
- Q2: 에러 메시지 'variable x might not have been initialized' = 초기화 안 됨

## 🃏 복습 카드

- Q: 변수의 '선언'과 '초기화'의 차이는?
  A: 선언: 변수(상자)를 만드는 것 int a; / 초기화: 처음으로 값을 넣는 것 a = 10;
- Q: int x; System.out.println(x); 는 어떻게 되나?
  A: 컴파일 에러. 지역 변수는 초기화하지 않으면 읽을 수 없음
- Q: long 리터럴과 float 리터럴을 쓸 때 붙이는 접미사는?
  A: long은 L (10000000000L), float는 f (3.14f)
- Q: char와 String의 차이는?
  A: char는 문자 하나, 작은따옴표 'A' / String은 문자열, 큰따옴표 "AB"
- Q: 실무에서 자주 쓰는 타입 5개는?
  A: 정수 int(큰 수는 long), 실수 double, boolean, 문자열 String
