#!/usr/bin/env python3
"""김영한의 자바 입문(인프런) 연동 트랙 K01~K23 생성기

  python3 java/_harness/course_k.py        → lessons/KNN_*/ (README.md, QN.java, QN.in, QN.out, answers/QN.java) 재생성 + 검증

- 하루 약 30분(강의 3~4개) 단위. 강의 → 출력 비교형 연습문제(강의처럼 main + println) → 다음 날부터 카드 복습
- 정답 코드를 실제로 실행해서 기대 출력(QN.out)을 만들고, 빈칸 버전은 그 출력과 달라야 통과
- 정답 표기는 build.py와 같음: // ▼ answer … // ▲ answer, 뒤에 // TODO: 기본 코드 / //> 버그 코드
"""
import os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build import to_exercise  # noqa: E402

ROOT = os.path.dirname(HERE)
LESSONS = os.path.join(ROOT, "lessons")
COURSE = "김영한의 자바 입문 - 코드로 시작하는 자바 첫걸음"
COURSE_ID = 332505
JAVA = ["java", "-Dstdout.encoding=UTF-8", "-Dstderr.encoding=UTF-8"]

# 강의 목록 (course-api.inflearn.com 커리큘럼, 2026-10-05 기준) — unitId: (섹션, 제목, 분)
UNITS = {
    194533: (1, "강의 소개", 4), 194537: (2, "개발 환경 설정", 14), 194538: (2, "다운로드 소스 코드 실행 방법", 4),
    194539: (2, "자바 프로그램 실행", 11), 194540: (2, "주석(comment)", 5), 194541: (2, "자바란?", 13),
    288261: (2, "섹션 2 퀴즈", 0),
    194543: (3, "변수 시작", 13), 194544: (3, "변수 값 변경", 3), 194545: (3, "변수 선언과 초기화", 13),
    194546: (3, "변수 타입1", 8), 194547: (3, "변수 타입2", 15), 194548: (3, "변수 명명 규칙", 8),
    194549: (3, "문제와 풀이", 11), 194550: (3, "정리", 6), 288273: (3, "섹션 3 퀴즈", 0),
    194560: (4, "산술 연산자", 11), 194561: (4, "문자열 더하기", 5), 194562: (4, "연산자 우선순위", 11),
    194563: (4, "증감 연산자", 16), 194564: (4, "비교 연산자", 9), 194565: (4, "논리 연산자", 7),
    194566: (4, "대입 연산자", 5), 194567: (4, "문제와 풀이", 6), 194568: (4, "정리", 5), 288285: (4, "섹션 4 퀴즈", 0),
    194569: (5, "if문1 - if, else", 10), 194570: (5, "if문2 - else if", 13), 194571: (5, "if문3 - if문과 else if문", 11),
    194572: (5, "switch문", 13), 194573: (5, "삼항 연산자", 5), 194574: (5, "문제와 풀이1", 6),
    194575: (5, "문제와 풀이2", 11), 194576: (5, "정리", 6), 288292: (5, "섹션 5 퀴즈", 0),
    194577: (6, "반복문 시작", 4), 194578: (6, "while문1", 6), 194579: (6, "while문2", 17), 194580: (6, "do-while문", 3),
    194581: (6, "break, continue", 8), 194582: (6, "for문1", 10), 194583: (6, "for문2", 6), 194584: (6, "중첩 반복문", 4),
    194585: (6, "문제와 풀이1", 8), 194586: (6, "문제와 풀이2", 9), 194587: (6, "정리", 5), 288298: (6, "섹션 6 퀴즈", 0),
    194588: (7, "스코프1 - 지역 변수와 스코프", 11), 194589: (7, "스코프2 - 스코프 존재 이유", 14),
    194590: (7, "형변환1 - 자동 형변환", 9), 194591: (7, "형변환2 - 명시적 형변환", 22), 194592: (7, "계산과 형변환", 9),
    194593: (7, "정리", 5), 288303: (7, "섹션 7 퀴즈", 0),
    194594: (8, "Scanner 학습", 12), 194595: (8, "Scanner - 기본 예제", 5), 194596: (8, "Scanner - 반복 예제", 9),
    194597: (8, "문제와 풀이1", 9), 194599: (8, "문제와 풀이2", 8), 194600: (8, "문제와 풀이3", 8),
    194601: (8, "문제와 풀이4", 15), 194602: (8, "정리", 3), 288364: (8, "섹션 8 퀴즈", 0),
    194603: (9, "배열 시작", 5), 194604: (9, "배열의 선언과 생성", 15), 194605: (9, "배열 사용", 12),
    194606: (9, "배열 리펙토링", 11), 194607: (9, "2차원 배열 - 시작", 5), 194608: (9, "2차원 배열 - 리팩토링1", 4),
    194609: (9, "2차원 배열 - 리팩토링2", 11), 194610: (9, "향상된 for문", 8), 194611: (9, "문제와 풀이1", 13),
    194612: (9, "문제와 풀이2", 15), 194613: (9, "문제와 풀이3", 13), 194614: (9, "정리", 9), 288377: (9, "섹션 9 퀴즈", 0),
    194615: (10, "메서드 시작", 9), 194616: (10, "메서드 사용", 21), 194617: (10, "메서드 정의", 6),
    194618: (10, "반환 타입", 8), 194619: (10, "메서드 호출과 값 전달1", 13), 194620: (10, "메서드 호출과 값 전달2", 12),
    194621: (10, "메서드와 형변환", 6), 194622: (10, "메서드 오버로딩", 12), 194623: (10, "문제와 풀이1", 19),
    194624: (10, "문제와 풀이2", 7), 194625: (10, "정리", 12), 288383: (10, "섹션 10 퀴즈", 0),
    194626: (11, "다음으로 (선택)", 27),
}
SECTIONS = {1: "강의 소개", 2: "Hello World", 3: "변수", 4: "연산자", 5: "조건문", 6: "반복문", 7: "스코프, 형변환",
            8: "훈련(Scanner)", 9: "배열", 10: "메서드", 11: "다음으로"}


def unit_url(uid):
    kind = "QUIZ" if uid >= 288000 else "LECTURE"
    return f"https://www.inflearn.com/courses/lecture?courseId={COURSE_ID}&type={kind}&unitId={uid}&subtitleLanguage=ko"


def P(desc, body, methods="", stdin=None, hint=""):
    return {"desc": desc.strip(), "body": body.strip("\n"), "methods": methods.strip("\n"), "stdin": stdin, "hint": hint.strip()}


# ---------------------------------------------------------------------------------------------
# 회차 데이터
# ---------------------------------------------------------------------------------------------
K = []

K.append(dict(slug="HelloWorld_실행", title="Hello World · 자바 프로그램 실행",
    units=[194533, 194537, 194538, 194539],
    cheat="""```java
public class HelloJava {                 // 클래스 이름 = 파일 이름(HelloJava.java)
    public static void main(String[] args) {   // 프로그램 시작점
        System.out.println("hello java"); // 출력 후 줄바꿈
        System.out.print("no newline");   // 줄바꿈 없음
    }                                     // 문장 끝은 ; , 블록은 { }
}
```
- 실행 흐름: `javac HelloJava.java`(컴파일 → .class) → `java HelloJava`(실행). 요즘은 `java HelloJava.java` 한 번에도 됨
- 이 트랙 연습문제도 `main` 안에 코드를 쓰고 `println`으로 출력하면 채점기가 출력을 비교해요""",
    cards=[
        ("자바 프로그램은 어디서부터 실행되나?", "public static void main(String[] args) 메서드부터 위에서 아래로"),
        ("System.out.println과 System.out.print의 차이는?", "println은 출력 후 줄바꿈, print는 줄바꿈 없음"),
        ("자바 문장의 끝과 코드 블록은 무엇으로 표시하나?", "문장 끝은 세미콜론(;), 블록은 중괄호 { }"),
        ("public class Hello가 들어 있는 파일의 이름은?", "Hello.java (public 클래스 이름과 파일 이름이 같아야 함, 대소문자 포함)"),
        ("javac와 java 명령은 각각 무엇을 하나?", "javac: .java 소스를 .class(바이트코드)로 컴파일 / java: .class를 JVM에서 실행"),
    ],
    problems=[
        P("두 줄을 출력하세요: 첫 줄 hello java, 둘째 줄 hello world", """
// ▼ answer
System.out.println("hello java");
System.out.println("hello world");
// ▲ answer""", hint="System.out.println(\"...\"); 두 번. 문자열은 큰따옴표"),
        P("print와 println을 섞어서 아래처럼 출력하세요 (첫 줄은 print 두 번으로 만들기)", """
// ▼ answer
System.out.print("Hello ");
System.out.print("Java");
System.out.println();
System.out.println("자바 첫걸음");
// ▲ answer""", hint="print는 줄바꿈이 없어요. 줄을 바꾸려면 마지막에 System.out.println(); 또는 println 사용"),
    ]))

K.append(dict(slug="주석_자바란_변수시작", title="주석 · 자바란? · 변수 시작",
    units=[194540, 194541, 288261, 194543, 194544],
    cheat="""```java
// 한 줄 주석
/* 여러 줄
   주석 */
int a = 10;      // 변수 선언 + 값 넣기
a = 50;          // 값 변경: 기존 값은 사라지고 새 값
System.out.println(a);   // 50 (변수 이름 a를 쓰면 값이 나옴, "a"는 그냥 글자)
```
- 자바 소스(.java) → 컴파일 → 바이트코드(.class) → JVM이 실행 → OS가 달라도 같은 코드가 돌아감""",
    cards=[
        ("자바 주석 2가지 문법은?", "// 한 줄 주석, /* ... */ 여러 줄 주석. 실행되지 않음"),
        ("자바가 운영체제(윈도우·맥)에 상관없이 실행되는 이유는?", "컴파일된 바이트코드(.class)를 OS별 JVM(자바 가상 머신)이 실행하기 때문"),
        ("System.out.println(a)와 System.out.println(\"a\")의 차이는?", "a는 변수 a에 담긴 값, \"a\"는 글자 a 그대로"),
        ("int a = 10; a = 20; 이후 a의 값은?", "20. 대입(=)하면 기존 값은 사라지고 새 값이 저장됨"),
    ],
    problems=[
        P("변수 a에 10을 넣고 출력한 뒤, a를 50으로 바꾸고 다시 출력하세요", """
// ▼ answer
int a = 10;
System.out.println(a);
a = 50;
System.out.println(a);
// ▲ answer""", hint="int a = 10; → println(a) → a = 50; → println(a). 두 번째는 int를 다시 쓰지 않아요"),
        P("아래 코드에서 '두 번째 줄'만 주석 처리해서 1, 3번 줄만 출력되게 하세요 (지우지 말고 // 사용)", """
// ▼ answer
System.out.println("1번 줄");
//System.out.println("2번 줄");
System.out.println("3번 줄");
// ▲ answer
//> System.out.println("1번 줄");
//> System.out.println("2번 줄");
//> System.out.println("3번 줄");""", hint="줄 맨 앞에 // 를 붙이면 그 줄은 실행되지 않아요 (VS Code 단축키 ⌘/)"),
        P("변수 num에 3을 넣고, num을 이용해 'num = 3'을 출력하세요. 그다음 num을 7로 바꿔 'num = 7'을 출력하세요", """
// ▼ answer
int num = 3;
System.out.println("num = " + num);
num = 7;
System.out.println("num = " + num);
// ▲ answer""", hint="\"num = \" + num 처럼 문자열과 변수를 + 로 이어 붙일 수 있어요 (섹션 4에서 자세히)"),
    ]))

K.append(dict(slug="변수선언_초기화_타입", title="변수 선언과 초기화 · 변수 타입",
    units=[194545, 194546, 194547],
    cheat="""```java
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
- 실무·코테에서 주로: `int`, `long`, `double`, `boolean`, `String`""",
    cards=[
        ("변수의 '선언'과 '초기화'의 차이는?", "선언: 변수(상자)를 만드는 것 int a; / 초기화: 처음으로 값을 넣는 것 a = 10;"),
        ("int x; System.out.println(x); 는 어떻게 되나?", "컴파일 에러. 지역 변수는 초기화하지 않으면 읽을 수 없음"),
        ("long 리터럴과 float 리터럴을 쓸 때 붙이는 접미사는?", "long은 L (10000000000L), float는 f (3.14f)"),
        ("char와 String의 차이는?", "char는 문자 하나, 작은따옴표 'A' / String은 문자열, 큰따옴표 \"AB\""),
        ("실무에서 자주 쓰는 타입 5개는?", "정수 int(큰 수는 long), 실수 double, boolean, 문자열 String"),
    ],
    problems=[
        P("아래 6개 변수를 알맞은 타입으로 선언하고 한 줄에 하나씩 출력하세요: 정수 100, 큰 정수 10000000000, 실수 3.14, 참 true, 문자 A, 문자열 Java", """
// ▼ answer
int i = 100;
long l = 10000000000L;
double d = 3.14;
boolean b = true;
char c = 'A';
String s = "Java";
System.out.println(i);
System.out.println(l);
System.out.println(d);
System.out.println(b);
System.out.println(c);
System.out.println(s);
// ▲ answer""", hint="100억은 int(약 21억)를 넘으니 long, 끝에 L. 문자는 'A', 문자열은 \"Java\""),
        P("컴파일 에러를 고치세요: 변수 x를 10으로 초기화해서 10이 출력되게", """
// ▼ answer
int x = 10;
System.out.println(x);
// ▲ answer
//> int x;
//> System.out.println(x);""", hint="에러 메시지 'variable x might not have been initialized' = 초기화 안 됨"),
    ]))

K.append(dict(slug="명명규칙_변수정리_산술연산자", title="변수 명명 규칙 · 변수 문제 · 산술 연산자",
    units=[194548, 194549, 194550, 288273, 194560],
    cheat="""```java
int studentCount;        // 변수·메서드: 소문자 시작 camelCase
class HelloWorld {}      // 클래스: 대문자 시작
final int MAX_SIZE = 10; // 상수: 대문자 + _
// 숫자로 시작 X (1st), 공백 X, 예약어 X (int, class)

10 + 3   // 13
10 - 3   // 7
10 * 3   // 30
10 / 3   // 3   ← 정수끼리 나누면 소수점 버림
10 % 3   // 1   ← 나머지
10 / 0   // ArithmeticException (실행 중 에러)
```""",
    cards=[
        ("자바 변수 이름 규칙(필수)과 관례(camelCase)는?", "숫자로 시작 X, 공백 X, 예약어 X / 변수는 소문자로 시작하는 camelCase (studentCount)"),
        ("클래스 이름과 상수 이름의 관례는?", "클래스는 대문자로 시작 (HelloWorld), 상수는 전부 대문자 + _ (MAX_SIZE)"),
        ("자바에서 10 / 3과 10 % 3의 결과는?", "3과 1. 정수끼리 나누면 소수점 버림, %는 나머지"),
        ("정수를 0으로 나누면?", "ArithmeticException (/ by zero) 실행 중 에러"),
    ],
    problems=[
        P("num1=10, num2=20, num3=30 의 합(sum)과 평균(average, 정수)을 구해 sum, average 순서로 출력하세요", """
int num1 = 10;
int num2 = 20;
int num3 = 30;
// ▼ answer
int sum = num1 + num2 + num3;
int average = sum / 3;
System.out.println(sum);
System.out.println(average);
// ▲ answer""", hint="int sum = num1 + num2 + num3; int average = sum / 3;"),
        P("a=10, b=3 으로 a+b, a-b, a*b, a/b, a%b 를 한 줄에 하나씩 출력하세요", """
int a = 10;
int b = 3;
// ▼ answer
System.out.println(a + b);
System.out.println(a - b);
System.out.println(a * b);
System.out.println(a / b);
System.out.println(a % b);
// ▲ answer""", hint="10 / 3 은 3.33이 아니라 3이에요 (정수 나눗셈)"),
        P("totalSeconds=135초를 '분'과 '초'로 나눠 2, 15 를 한 줄씩 출력하세요 (/ 와 % 사용)", """
int totalSeconds = 135;
// ▼ answer
System.out.println(totalSeconds / 60);
System.out.println(totalSeconds % 60);
// ▲ answer""", hint="분 = 135 / 60, 초 = 135 % 60"),
    ]))

K.append(dict(slug="문자열더하기_우선순위_증감", title="문자열 더하기 · 연산자 우선순위 · 증감 연산자",
    units=[194561, 194562, 194563],
    cheat="""```java
"hello " + "java"   // "hello java"
"a + b = " + 30     // "a + b = 30"  문자열 + 숫자 → 문자열
"1" + 2 + 3         // "123"  왼쪽부터 계산
1 + 2 + "3"         // "33"   (1+2=3 먼저) + "3"
"합: " + (1 + 2)     // "합: 3"  괄호 먼저

2 + 3 * 4           // 14 (곱셈 먼저)
(2 + 3) * 4         // 20 → 헷갈리면 괄호!

int a = 5;
int b = ++a;   // 전위: 먼저 증가 → a=6, b=6
int c = a++;   // 후위: 대입 후 증가 → c=6, a=7
```""",
    cards=[
        ("\"a + b = \" + 10 + 20 의 결과는? 30이 나오게 하려면?", "\"a + b = 1020\" (왼쪽부터 문자열로 이어짐). \"a + b = \" + (10 + 20)"),
        ("1 + 2 + \"3\" 의 결과는?", "\"33\" (1+2=3을 먼저 계산한 뒤 \"3\"과 이어 붙임)"),
        ("연산자 우선순위가 헷갈릴 때 원칙은?", "괄호 ()를 써서 명확하게. 곱셈·나눗셈이 덧셈·뺄셈보다 먼저"),
        ("int a = 5; int b = ++a; int c = a++; 이후 a, b, c는?", "a=7, b=6, c=6 (++a는 먼저 증가, a++는 값을 쓴 뒤 증가)"),
    ],
    problems=[
        P("a=10, b=20 일 때 'a + b = 30' 을 출력하세요 (30은 직접 쓰지 말고 계산)", """
int a = 10;
int b = 20;
// ▼ answer
System.out.println("a + b = " + (a + b));
// ▲ answer
// TODO: System.out.println("a + b = " + a + b);""", hint="괄호가 없으면 \"a + b = 10\" + 20 → \"a + b = 1020\""),
        P("price=1000원짜리를 count=3개 사고 delivery=2500원 배송비를 낼 때 총액을 '총액: 5500원' 형태로 출력하세요", """
int price = 1000;
int count = 3;
int delivery = 2500;
// ▼ answer
int total = price * count + delivery;
System.out.println("총액: " + total + "원");
// ▲ answer""", hint="곱셈이 먼저라 price * count + delivery 그대로 OK"),
        P("x=5 에서 시작해 ++ 와 -- 만 사용해서 x를 6 → 7 → 6 으로 바꾸며 매번 출력하세요", """
int x = 5;
// ▼ answer
x++;
System.out.println(x);
x++;
System.out.println(x);
x--;
System.out.println(x);
// ▲ answer""", hint="x++; 는 x = x + 1; 과 같아요"),
    ]))

K.append(dict(slug="비교_논리_대입연산자", title="비교 · 논리 · 대입 연산자 · 연산자 정리",
    units=[194564, 194565, 194566, 194567, 194568, 288285],
    cheat="""```java
a == b   a != b   a > b   a >= b      // 결과는 boolean
"hello".equals(str)   // 문자열 비교는 == 말고 equals!

a > 10 && a < 20   // 그리고 (10 < a < 20 은 문법 에러)
a < 0 || a > 100   // 또는
!flag              // 반대

x += 5;   // x = x + 5
x -= 3;   x *= 2;   x /= 2;   x %= 3;
```""",
    cards=[
        ("문자열이 같은지 비교할 때 == 대신 쓰는 것은?", "str1.equals(str2). ==는 같은 객체인지(참조) 비교라 문자열 내용 비교에 쓰면 안 됨"),
        ("변수 a가 10 초과 20 미만인지 검사하는 식은?", "a > 10 && a < 20 (10 < a < 20 은 컴파일 에러)"),
        ("&&, ||, ! 의 뜻은?", "&& 둘 다 참(AND), || 하나라도 참(OR), ! 참/거짓 반대(NOT)"),
        ("int x = 10; x += 5; x *= 2; 이후 x는?", "30 (x = 10+5 = 15 → 15*2 = 30)"),
    ],
    problems=[
        P("a=15 가 10보다 크고 20보다 작은지 true/false로 출력하세요", """
int a = 15;
// ▼ answer
boolean result = a > 10 && a < 20;
System.out.println(result);
// ▲ answer""", hint="a > 10 && a < 20"),
        P("str1과 str2의 '내용'이 같은지 출력하세요 (true가 나와야 함)", """
String str1 = "hello";
String str2 = new String("hello");
// ▼ answer
System.out.println(str1.equals(str2));
// ▲ answer
// TODO: System.out.println(str1 == str2);""", hint="== 는 다른 객체라 false. 내용 비교는 str1.equals(str2)"),
        P("x=10 에 대입 연산자만 써서 +5, *2, -3 을 차례로 한 뒤 x를 출력하세요", """
int x = 10;
// ▼ answer
x += 5;
x *= 2;
x -= 3;
// ▲ answer
System.out.println(x);""", hint="x += 5; x *= 2; x -= 3;"),
    ]))

K.append(dict(slug="if_else_elseif", title="if · else · else if",
    units=[194569, 194570, 194571],
    cheat="""```java
if (score >= 90) {
    grade = "A";
} else if (score >= 80) {   // 위가 false일 때만 검사
    grade = "B";
} else {
    grade = "F";
}
// else if 체인: 위에서부터 '처음 참인 것 하나만' 실행 → 큰 범위 조건을 먼저

// 서로 독립된 조건(둘 다 적용 가능)은 if를 따로따로
if (price >= 10000) discount += 1000;
if (age <= 10) discount += 1000;
```""",
    cards=[
        ("if - else if - else 체인에서 실행되는 블록 수는?", "조건이 처음 참인 블록 하나만 (없으면 else). 그래서 조건 순서가 중요"),
        ("점수로 등급(90+ A, 80+ B …)을 나눌 때 조건을 어떤 순서로 쓰나?", "큰 값부터: score >= 90 → >= 80 → … (작은 것부터 쓰면 90점도 >= 60에 먼저 걸림)"),
        ("else if 대신 if를 여러 개 따로 써야 하는 경우는?", "조건이 서로 독립이라 여러 개가 동시에 적용될 수 있을 때 (예: 금액 할인 + 나이 할인)"),
        ("if 뒤에 중괄호 {}를 생략하면?", "바로 다음 한 문장만 if에 속함. 실수 방지를 위해 항상 {} 쓰기 권장"),
    ],
    problems=[
        P("score=85 의 등급을 출력하세요 (90 이상 A, 80 이상 B, 70 이상 C, 60 이상 D, 나머지 F)", """
int score = 85;
// ▼ answer
if (score >= 90) {
    System.out.println("A");
} else if (score >= 80) {
    System.out.println("B");
} else if (score >= 70) {
    System.out.println("C");
} else if (score >= 60) {
    System.out.println("D");
} else {
    System.out.println("F");
}
// ▲ answer""", hint="if (score >= 90) {...} else if (score >= 80) {...} ... else {...}"),
        P("price=15000, age=8 일 때 할인 금액을 출력하세요. 금액 10000원 이상이면 1000원, 나이 10세 이하면 1000원 할인 (둘 다 해당되면 둘 다 적용) → '할인 금액: 2000'", """
int price = 15000;
int age = 8;
int discount = 0;
// ▼ answer
if (price >= 10000) {
    discount += 1000;
}
if (age <= 10) {
    discount += 1000;
}
// ▲ answer
System.out.println("할인 금액: " + discount);""", hint="else if로 이으면 하나만 적용돼요. 독립 조건은 if 두 개"),
        P("temperature=-3 일 때 0 미만이면 '영하', 0 이상 25 미만이면 '적당', 25 이상이면 '더움'을 출력하세요", """
int temperature = -3;
// ▼ answer
if (temperature < 0) {
    System.out.println("영하");
} else if (temperature < 25) {
    System.out.println("적당");
} else {
    System.out.println("더움");
}
// ▲ answer"""),
    ]))

K.append(dict(slug="switch_삼항연산자_조건문문제", title="switch · 삼항 연산자 · 조건문 문제",
    units=[194572, 194573, 194574, 194575],
    cheat="""```java
switch (grade) {            // 값이 '같은지'만 비교
    case 1:
        coupon = 1000;
        break;              // break 없으면 아래 case까지 계속 실행(fall-through)
    case 2:
        coupon = 2000;
        break;
    default:                // 어느 case도 아니면
        coupon = 500;
}
// 자바 14+ 새 switch
int coupon = switch (grade) {
    case 1 -> 1000;
    case 2 -> 2000;
    default -> 500;
};

String status = (age >= 18) ? "성인" : "미성년자";   // 조건 ? 참일 때 : 거짓일 때
num % 2 == 0   // 짝수 판별
```""",
    cards=[
        ("switch에서 case 끝에 break를 빼먹으면?", "조건에 맞는 case부터 아래 case들이 연달아 실행됨 (fall-through)"),
        ("switch와 if의 차이는?", "switch는 값이 같은지만 비교(==), 범위 조건(>=)은 if로"),
        ("삼항 연산자의 형태는?", "조건 ? 참일 때 값 : 거짓일 때 값  예) age >= 18 ? \"성인\" : \"미성년자\""),
        ("어떤 수가 짝수인지 판별하는 식은?", "num % 2 == 0 (2로 나눈 나머지가 0)"),
    ],
    problems=[
        P("grade=2 일 때 쿠폰 금액을 switch로 정해 '발급받은 쿠폰 2000' 을 출력하세요 (1등급 1000, 2등급 2000, 3등급 3000, 그 외 500)", """
int grade = 2;
int coupon;
// ▼ answer
switch (grade) {
    case 1:
        coupon = 1000;
        break;
    case 2:
        coupon = 2000;
        break;
    case 3:
        coupon = 3000;
        break;
    default:
        coupon = 500;
}
// ▲ answer
// TODO: coupon = 0;
System.out.println("발급받은 쿠폰 " + coupon);""", hint="case 2: coupon = 2000; break; … default: coupon = 500;"),
        P("age=17 일 때 삼항 연산자로 status에 '성인'(18 이상) 또는 '미성년자'를 넣어 출력하세요", """
int age = 17;
// ▼ answer
String status = (age >= 18) ? "성인" : "미성년자";
// ▲ answer
// TODO: String status = "";
System.out.println(status);"""),
        P("num=7 이 짝수면 '짝수', 홀수면 '홀수'를 출력하세요", """
int num = 7;
// ▼ answer
if (num % 2 == 0) {
    System.out.println("짝수");
} else {
    System.out.println("홀수");
}
// ▲ answer""", hint="num % 2 == 0 이면 짝수"),
    ]))

K.append(dict(slug="while문", title="조건문 정리 · while문",
    units=[194576, 288292, 194577, 194578, 194579],
    cheat="""```java
int i = 1;            // ① 시작값
while (i <= 5) {      // ② 조건이 true인 동안 반복
    System.out.println(i);
    i++;              // ③ 증가 — 빠뜨리면 무한 루프!
}

int sum = 0;          // 누적은 반복문 '밖'에서 0으로 시작
int n = 1;
while (n <= 10) {
    sum += n;
    n++;
}
```
- 무한 루프에 빠지면 터미널에서 Ctrl + C (채점기는 20초 뒤 자동 중단)""",
    cards=[
        ("while문의 구조와 실행 순서는?", "while (조건) { 코드 } — 조건 검사 → true면 코드 실행 → 다시 조건 검사 … false면 종료"),
        ("while문이 무한 루프에 빠지는 흔한 원인은?", "반복 변수 증가(i++)를 빠뜨려서 조건이 영원히 true"),
        ("1부터 10까지 합을 구할 때 sum 변수는 어디서 선언하나?", "반복문 밖에서 int sum = 0; (안에서 선언하면 매번 0으로 초기화됨)"),
        ("while 조건이 처음부터 false면 몇 번 실행되나?", "0번 (한 번도 실행 안 됨)"),
    ],
    problems=[
        P("while문으로 1부터 5까지 한 줄에 하나씩 출력하세요", """
// ▼ answer
int i = 1;
while (i <= 5) {
    System.out.println(i);
    i++;
}
// ▲ answer""", hint="int i = 1; while (i <= 5) { println(i); i++; }"),
        P("while문으로 1부터 10까지의 합을 구해 출력하세요", """
// ▼ answer
int sum = 0;
int i = 1;
while (i <= 10) {
    sum += i;
    i++;
}
System.out.println(sum);
// ▲ answer"""),
        P("endNum=3 일 때 1부터 endNum까지 더해가며 'i=1 sum=1', 'i=2 sum=3', 'i=3 sum=6' 처럼 매번 출력하세요", """
int endNum = 3;
// ▼ answer
int sum = 0;
int i = 1;
while (i <= endNum) {
    sum += i;
    System.out.println("i=" + i + " sum=" + sum);
    i++;
}
// ▲ answer""", hint="sum += i 한 다음 \"i=\" + i + \" sum=\" + sum 출력"),
    ]))

K.append(dict(slug="dowhile_break_continue_for", title="do-while · break · continue · for · 중첩 반복문",
    units=[194580, 194581, 194582, 194583, 194584],
    cheat="""```java
do { ... } while (조건);    // 최소 1번은 실행

for (int i = 1; i <= 10; i++) {   // (초기식; 조건식; 증감식)
    if (i % 3 == 0) continue;     // 이번 회차만 건너뛰고 다음 i로
    if (i > 8) break;             // 반복문 즉시 종료
    System.out.println(i);
}

for (int i = 2; i <= 3; i++) {        // 바깥 2번
    for (int j = 1; j <= 3; j++) {    // 안쪽 3번 → 총 6번
        System.out.println(i + " * " + j + " = " + i * j);
    }
}
```""",
    cards=[
        ("do-while이 while과 다른 점은?", "조건을 나중에 검사하므로 조건이 처음부터 false여도 최소 1번은 실행"),
        ("break와 continue의 차이는?", "break: 반복문을 즉시 빠져나감 / continue: 이번 회차의 남은 코드를 건너뛰고 다음 회차로"),
        ("for문의 괄호 안 세 부분과 실행 순서는?", "(초기식; 조건식; 증감식) — 초기식 1번 → 조건 검사 → 본문 → 증감 → 조건 검사 …"),
        ("바깥 for가 3번, 안쪽 for가 4번 돌면 안쪽 본문은 총 몇 번 실행되나?", "12번 (3 × 4)"),
        ("for와 while은 언제 쓰나?", "반복 횟수가 정해져 있으면 for, 조건이 바뀔 때까지(횟수 모름)면 while"),
    ],
    problems=[
        P("1부터 차례로 더하다가 합이 10보다 커지는 순간 break로 멈추고 'i=5 sum=15' 를 출력하세요", """
int sum = 0;
int i = 1;
// ▼ answer
while (true) {
    sum += i;
    if (sum > 10) {
        break;
    }
    i++;
}
// ▲ answer
System.out.println("i=" + i + " sum=" + sum);""", hint="while (true) { sum += i; if (sum > 10) break; i++; }"),
        P("for와 continue로 1부터 10까지 중 3의 배수를 뺀 수를 한 줄씩 출력하세요", """
// ▼ answer
for (int i = 1; i <= 10; i++) {
    if (i % 3 == 0) {
        continue;
    }
    System.out.println(i);
}
// ▲ answer""", hint="if (i % 3 == 0) continue;"),
        P("중첩 for로 구구단 2단과 3단의 1~3까지를 '2 * 1 = 2' 형태로 출력하세요 (2*1, 2*2, 2*3, 3*1, ...)", """
// ▼ answer
for (int i = 2; i <= 3; i++) {
    for (int j = 1; j <= 3; j++) {
        System.out.println(i + " * " + j + " = " + i * j);
    }
}
// ▲ answer""", hint="바깥 i: 2~3, 안쪽 j: 1~3. i * j 는 곱셈이 먼저라 괄호 없어도 OK"),
    ]))

K.append(dict(slug="반복문문제_스코프1", title="반복문 문제 · 반복문 정리 · 스코프1",
    units=[194585, 194586, 194587, 288298, 194588],
    cheat="""```java
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
```""",
    cards=[
        ("지역 변수의 스코프(사용 범위)는?", "변수가 선언된 코드 블록 { } 안 (선언 이후부터 블록 끝까지)"),
        ("for (int i = 0; ...) 에서 선언한 i를 for문 밖에서 쓸 수 있나?", "없음. i의 스코프는 for문 안. 밖에서 필요하면 for 밖에서 선언"),
        ("중첩 반복문으로 직각 삼각형 별을 찍을 때 안쪽 반복의 조건은?", "col <= row (줄 번호만큼 별을 찍음), 안쪽 끝나고 println()으로 줄바꿈"),
        ("n! (팩토리얼)을 반복문으로 구할 때 결과 변수의 시작값은?", "1 (곱셈의 시작은 0이 아니라 1)"),
    ],
    problems=[
        P("rows=4 일 때 별(*)로 직각 삼각형을 출력하세요 (1줄 *, 2줄 **, …, 4줄 ****)", """
int rows = 4;
// ▼ answer
for (int row = 1; row <= rows; row++) {
    for (int col = 1; col <= row; col++) {
        System.out.print("*");
    }
    System.out.println();
}
// ▲ answer""", hint="안쪽 for에서 print(\"*\") (줄바꿈 X), 안쪽이 끝나면 println()"),
        P("n=5 의 팩토리얼(5! = 1×2×3×4×5)을 for로 구해 출력하세요", """
int n = 5;
// ▼ answer
int result = 1;
for (int i = 1; i <= n; i++) {
    result *= i;
}
System.out.println(result);
// ▲ answer""", hint="int result = 1; 에서 시작해 result *= i"),
        P("스코프 컴파일 에러를 고쳐서 30이 출력되게 하세요 (x를 if 블록 밖에서 쓰고 있어요)", """
int m = 10;
// ▼ answer
int x = 0;
if (true) {
    x = 20;
}
System.out.println(m + x);
// ▲ answer
//> if (true) {
//>     int x = 20;
//> }
//> System.out.println(m + x);""", hint="x를 if 밖에서 먼저 선언(int x = 0;)하고, if 안에서는 x = 20; 으로 값만 넣기"),
    ]))

K.append(dict(slug="스코프2_자동형변환", title="스코프 존재 이유 · 자동 형변환",
    units=[194589, 194590],
    cheat="""```java
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
```""",
    cards=[
        ("변수의 스코프를 좁게(필요한 곳에서만) 선언하는 이유 2가지는?", "① 블록이 끝나면 메모리에서 제거되어 효율적 ② 변수가 쓰이는 범위가 좁아 코드 읽기·유지보수가 쉬움"),
        ("int → long → double 처럼 작은 범위에서 큰 범위로 대입하면?", "자동 형변환(묵시적). 값 손실 없음. int 10 → double 10.0"),
        ("double r = 10 / 4; 의 결과는? 2.5가 나오게 하려면?", "2.0 (int끼리 먼저 나눔). 10 / 4.0 또는 (double) 10 / 4"),
        ("서로 다른 타입끼리 연산하면 결과 타입은?", "더 큰 범위 타입으로 자동 변환되어 계산 (int + double → double)"),
    ],
    problems=[
        P("int i=10 을 long 변수와 double 변수에 각각 대입해서 i, long 값, double 값을 한 줄씩 출력하세요", """
int i = 10;
// ▼ answer
long l = i;
double d = i;
System.out.println(i);
System.out.println(l);
System.out.println(d);
// ▲ answer""", hint="long l = i; double d = i; (캐스팅 없이 그냥 대입)"),
        P("a=10, b=4 일 때 a / b 를 정수 나눗셈 결과(2)와 실수 나눗셈 결과(2.5)로 한 줄씩 출력하세요 (a, b는 int 그대로)", """
int a = 10;
int b = 4;
// ▼ answer
System.out.println(a / b);
System.out.println(a / (double) b);
// ▲ answer""", hint="한쪽만 double이면 됨: a / (double) b 또는 (double) a / b"),
    ]))

K.append(dict(slug="명시적형변환_계산과형변환", title="명시적 형변환 · 계산과 형변환",
    units=[194591, 194592, 194593, 288303],
    cheat="""```java
double d = 1.9;
int i = (int) d;        // 1  큰 범위 → 작은 범위는 (타입)으로 '직접' 변환, 소수점 버림

int max = Integer.MAX_VALUE;   // 2147483647
max + 1                        // -2147483648  ← 오버플로 (에러 없이 이상한 값)
long big = 2147483648L;
int bad = (int) big;           // -2147483648  ← 범위를 넘는 값을 넣으면 깨짐

int sum = 7, n = 2;
sum / n            // 3     int / int = int
(double) sum / n   // 3.5   나누기 전에 double로
(double) (sum / n) // 3.0   이미 3이 된 뒤라 늦음
```""",
    cards=[
        ("double 3.9를 int로 바꾸면? 문법은?", "int i = (int) 3.9; → 3 (반올림이 아니라 소수점 버림)"),
        ("int 최댓값(약 21억)에 1을 더하면?", "-2147483648. 에러 없이 음수가 되는 오버플로 → 큰 수는 처음부터 long"),
        ("(double) sum / n 과 (double) (sum / n) 의 차이는? (sum=7, n=2)", "3.5와 3.0. 뒤는 정수 나눗셈이 먼저 끝난 뒤 변환해서 소수점이 이미 사라짐"),
        ("같은 타입끼리 연산한 결과의 타입은?", "같은 타입 (int / int → int). 다른 타입이면 큰 범위 타입으로"),
    ],
    problems=[
        P("d=3.7 을 int로 명시적 형변환해서 출력하세요 (3)", """
double d = 3.7;
// ▼ answer
int i = (int) d;
System.out.println(i);
// ▲ answer""", hint="(int) d — 반올림이 아니라 버림"),
        P("int 최댓값 max 에 1을 더한 결과를 int로 한 번(오버플로), long으로 한 번(정상: 2147483648) 출력하세요", """
int max = Integer.MAX_VALUE;
// ▼ answer
int overflow = max + 1;
long ok = (long) max + 1;
System.out.println(overflow);
System.out.println(ok);
// ▲ answer""", hint="long ok = (long) max + 1; — 더하기 '전에' long으로"),
        P("세 과목 점수 합 sum=250 의 평균을 소수점까지(83.33…) 출력하세요", """
int sum = 250;
int count = 3;
// ▼ answer
double average = (double) sum / count;
// ▲ answer
// TODO: double average = sum / count;
System.out.println(average);""", hint="(double) sum / count — 나누기 전에 변환"),
    ]))

K.append(dict(slug="Scanner", title="Scanner (입력 받기) · 기본 · 반복 예제",
    units=[194594, 194595, 194596, 194597],
    cheat="""```java
import java.util.Scanner;   // 파일 맨 위

Scanner scanner = new Scanner(System.in);
String name = scanner.nextLine();   // 한 줄 전체
int age = scanner.nextInt();        // 정수 하나 (공백·줄바꿈으로 구분)
double d = scanner.nextDouble();

// ⚠️ nextInt() 다음에 nextLine()을 쓰면 남은 엔터(\\n)를 읽어서 빈 문자열이 됨
//    → nextInt() 뒤에 scanner.nextLine(); 한 번 더 호출해서 버리기

while (true) {               // 0이 들어올 때까지 반복
    int x = scanner.nextInt();
    if (x == 0) break;
}
```
- 채점기는 문제마다 정해진 입력(QN.in)을 자동으로 넣어 줘요. 직접 실행할 땐 키보드로 입력
- 🎯 프로그래머스는 입력을 `solution(매개변수)`로 주기 때문에 Scanner를 안 써요 (백준·삼성 SW는 씀)""",
    cards=[
        ("Scanner로 한 줄 문자열과 정수를 읽는 메서드는?", "nextLine() 한 줄 전체, nextInt() 정수 하나"),
        ("nextInt() 바로 뒤에 nextLine()을 호출하면 생기는 문제와 해결법은?", "남아 있던 엔터를 읽어서 빈 문자열이 됨 → nextInt() 뒤에 nextLine()을 한 번 호출해서 버림"),
        ("Scanner를 쓰려면 파일 맨 위에 무엇이 필요한가?", "import java.util.Scanner;"),
        ("0이 입력될 때까지 계속 숫자를 읽는 반복문의 형태는?", "while (true) { int x = sc.nextInt(); if (x == 0) break; ... }"),
    ],
    problems=[
        P("이름(한 줄)과 나이(정수)를 입력받아 '이름: Kim, 나이: 20' 형태로 출력하세요", """
Scanner scanner = new Scanner(System.in);
// ▼ answer
String name = scanner.nextLine();
int age = scanner.nextInt();
System.out.println("이름: " + name + ", 나이: " + age);
// ▲ answer""", stdin="Kim\n20\n", hint="String name = scanner.nextLine(); int age = scanner.nextInt();"),
        P("정수 두 개를 입력받아 '두 수의 합: 30' 형태로 출력하세요", """
Scanner scanner = new Scanner(System.in);
// ▼ answer
int a = scanner.nextInt();
int b = scanner.nextInt();
System.out.println("두 수의 합: " + (a + b));
// ▲ answer""", stdin="10 20\n"),
        P("정수를 계속 입력받다가 0이 들어오면 멈추고, 그때까지의 합을 출력하세요", """
Scanner scanner = new Scanner(System.in);
// ▼ answer
int sum = 0;
while (true) {
    int x = scanner.nextInt();
    if (x == 0) {
        break;
    }
    sum += x;
}
System.out.println(sum);
// ▲ answer""", stdin="3 5 7 1 0\n", hint="while (true) 안에서 읽고, 0이면 break, 아니면 sum += x"),
    ]))

K.append(dict(slug="Scanner_문제", title="훈련 문제 (Scanner + 조건 + 반복)",
    units=[194599, 194600, 194601],
    cheat="""```java
// 입력 → 계산 → 출력 패턴
Scanner sc = new Scanner(System.in);
int n = sc.nextInt();            // 개수 먼저
int sum = 0;
for (int i = 0; i < n; i++) {    // n번 반복하며 읽기
    sum += sc.nextInt();
}
double avg = (double) sum / n;
```""",
    cards=[
        ("첫 줄에 개수 n, 다음에 n개의 수가 주어질 때 읽는 방법은?", "int n = sc.nextInt(); for (int i = 0; i < n; i++) { int x = sc.nextInt(); ... }"),
        ("입력받은 수 n으로 n단 구구단을 출력하는 반복문은?", "for (int i = 1; i <= 9; i++) System.out.println(n + \" x \" + i + \" = \" + n * i);"),
        ("입력받은 정수들의 평균을 소수점까지 출력하려면?", "(double) sum / n — 나누기 전에 double로 변환"),
    ],
    problems=[
        P("정수 n을 입력받아 n단을 '3 x 1 = 3' 형태로 1부터 9까지 출력하세요", """
Scanner sc = new Scanner(System.in);
// ▼ answer
int n = sc.nextInt();
for (int i = 1; i <= 9; i++) {
    System.out.println(n + " x " + i + " = " + n * i);
}
// ▲ answer""", stdin="3\n"),
        P("상품 가격과 수량을 입력받아 '총 비용: 30000' 을 출력하세요", """
Scanner sc = new Scanner(System.in);
// ▼ answer
int price = sc.nextInt();
int quantity = sc.nextInt();
System.out.println("총 비용: " + price * quantity);
// ▲ answer""", stdin="10000 3\n"),
        P("첫 수는 개수 n, 그다음 n개의 정수가 주어집니다. 합을 출력하고 다음 줄에 평균(소수점 포함)을 출력하세요", """
Scanner sc = new Scanner(System.in);
// ▼ answer
int n = sc.nextInt();
int sum = 0;
for (int i = 0; i < n; i++) {
    sum += sc.nextInt();
}
System.out.println(sum);
System.out.println((double) sum / n);
// ▲ answer""", stdin="4\n10 20 30 45\n", hint="for로 n번 sc.nextInt() 해서 더하고, 평균은 (double) sum / n"),
    ]))

K.append(dict(slug="배열시작_선언_사용", title="훈련 정리 · 배열 시작 · 선언과 생성 · 배열 사용",
    units=[194602, 288364, 194603, 194604, 194605],
    cheat="""```java
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
```""",
    cards=[
        ("크기 5인 int 배열을 만드는 코드와, 처음 들어 있는 값은?", "int[] arr = new int[5]; 모두 0 (boolean은 false, String은 null)"),
        ("배열 인덱스 범위와 범위를 벗어나면 나는 에러는?", "0 ~ length-1. 벗어나면 ArrayIndexOutOfBoundsException"),
        ("배열 길이를 구하는 코드는?", "arr.length (괄호 없음. String은 s.length() 괄호 있음)"),
        ("배열 전체를 for로 도는 표준 형태는?", "for (int i = 0; i < arr.length; i++) { arr[i] ... }"),
    ],
    problems=[
        P("크기 5인 int 배열 students를 만들고 90, 80, 70, 60, 50 을 넣은 뒤 for문으로 '학생1 점수: 90' … '학생5 점수: 50' 을 출력하세요", """
// ▼ answer
int[] students = new int[5];
students[0] = 90;
students[1] = 80;
students[2] = 70;
students[3] = 60;
students[4] = 50;
for (int i = 0; i < students.length; i++) {
    System.out.println("학생" + (i + 1) + " 점수: " + students[i]);
}
// ▲ answer""", hint="인덱스는 0부터지만 학생 번호는 i + 1"),
        P("배열 {3, 6, 9, 12, 15} 의 합을 for문으로 구해 출력하세요", """
int[] arr = {3, 6, 9, 12, 15};
// ▼ answer
int sum = 0;
for (int i = 0; i < arr.length; i++) {
    sum += arr[i];
}
System.out.println(sum);
// ▲ answer"""),
        P("new int[3] 으로 만든 배열의 길이와 arr[0]의 기본값을 한 줄씩 출력하세요", """
// ▼ answer
int[] arr = new int[3];
System.out.println(arr.length);
System.out.println(arr[0]);
// ▲ answer"""),
    ]))

K.append(dict(slug="배열리팩토링_2차원배열", title="배열 리팩토링 · 2차원 배열",
    units=[194606, 194607, 194608, 194609],
    cheat="""```java
int[][] arr = new int[2][3];        // 2행 3열
arr[0][1] = 5;                      // [행][열]

int[][] arr2 = {
    {1, 2, 3},
    {4, 5, 6}
};
arr2.length       // 2 (행 개수)
arr2[0].length    // 3 (열 개수)

for (int row = 0; row < arr2.length; row++) {
    for (int col = 0; col < arr2[row].length; col++) {
        System.out.print(arr2[row][col] + " ");
    }
    System.out.println();
}
```""",
    cards=[
        ("2차원 배열 int[][] arr = new int[2][3]; 에서 arr.length와 arr[0].length는?", "2(행 개수)와 3(열 개수)"),
        ("2차원 배열 전체를 출력하는 반복문 구조는?", "바깥 for: row < arr.length, 안쪽 for: col < arr[row].length, 안쪽 끝나면 println()"),
        ("int[] arr = {1, 2, 3}; 처럼 {}로 값을 바로 넣는 문법은 언제 쓸 수 있나?", "선언과 동시에만. 이미 선언된 변수에는 arr = new int[]{1, 2, 3}; 으로"),
        ("배열을 쓰면 변수 여러 개(student1, student2…)보다 좋은 점은?", "반복문으로 한 번에 처리 가능 → 개수가 늘어도 코드가 그대로"),
    ],
    problems=[
        P("2차원 배열 {{1,2,3},{4,5,6}} 을 행마다 '1 2 3' 처럼 공백으로 구분해 출력하세요 (줄 끝 공백은 괜찮아요)", """
int[][] arr = {
    {1, 2, 3},
    {4, 5, 6}
};
// ▼ answer
for (int row = 0; row < arr.length; row++) {
    for (int col = 0; col < arr[row].length; col++) {
        System.out.print(arr[row][col] + " ");
    }
    System.out.println();
}
// ▲ answer""", hint="안쪽에서 print(값 + \" \"), 안쪽이 끝나면 println()"),
        P("3행 3열 int 배열을 만들고 1부터 9까지 순서대로 채운 뒤 위와 같은 형태로 출력하세요", """
// ▼ answer
int[][] arr = new int[3][3];
int value = 1;
for (int row = 0; row < arr.length; row++) {
    for (int col = 0; col < arr[row].length; col++) {
        arr[row][col] = value;
        value++;
    }
}
for (int row = 0; row < arr.length; row++) {
    for (int col = 0; col < arr[row].length; col++) {
        System.out.print(arr[row][col] + " ");
    }
    System.out.println();
}
// ▲ answer""", hint="int value = 1; 을 두고 칸마다 arr[row][col] = value; value++;"),
        P("int[][] grid = new int[4][7]; 의 행 개수와 열 개수를 '4 7' 로 출력하세요", """
int[][] grid = new int[4][7];
// ▼ answer
System.out.println(grid.length + " " + grid[0].length);
// ▲ answer"""),
    ]))

K.append(dict(slug="향상된for_배열문제", title="향상된 for문 · 배열 문제",
    units=[194610, 194611, 194612],
    cheat="""```java
int[] numbers = {1, 2, 3, 4, 5};
for (int number : numbers) {        // 향상된 for (for-each): 값만 차례로
    System.out.println(number);
}
// 인덱스가 필요하면(역순, i번째 표시, 값 변경) 일반 for

int max = numbers[0];               // 최댓값: 첫 원소로 시작
for (int n : numbers) {
    if (n > max) max = n;
}

for (int i = numbers.length - 1; i >= 0; i--) { ... }   // 역순
```""",
    cards=[
        ("향상된 for문의 형태는?", "for (int x : arr) { ... } — 배열 값을 처음부터 하나씩 x에 담아 반복"),
        ("향상된 for문을 쓸 수 없는(일반 for가 필요한) 경우는?", "인덱스가 필요할 때: 역순·일부 구간·i번째 출력·배열 값 변경"),
        ("배열 최댓값을 구할 때 max의 시작값으로 좋은 것은?", "arr[0] (0으로 시작하면 전부 음수인 배열에서 틀림)"),
        ("배열을 역순으로 도는 for문은?", "for (int i = arr.length - 1; i >= 0; i--)"),
    ],
    problems=[
        P("향상된 for문으로 scores {90, 85, 72} 의 합과 평균(소수점 포함)을 한 줄씩 출력하세요", """
int[] scores = {90, 85, 72};
// ▼ answer
int sum = 0;
for (int score : scores) {
    sum += score;
}
System.out.println(sum);
System.out.println((double) sum / scores.length);
// ▲ answer""", hint="for (int score : scores) sum += score; 평균은 (double) sum / scores.length"),
        P("배열 {3, -9, 14, 7, 0} 의 최댓값과 최솟값을 '최댓값: 14', '최솟값: -9' 로 출력하세요", """
int[] arr = {3, -9, 14, 7, 0};
// ▼ answer
int max = arr[0];
int min = arr[0];
for (int x : arr) {
    if (x > max) {
        max = x;
    }
    if (x < min) {
        min = x;
    }
}
System.out.println("최댓값: " + max);
System.out.println("최솟값: " + min);
// ▲ answer"""),
        P("배열 {1, 2, 3, 4, 5} 를 역순으로 한 줄에 '5 4 3 2 1 ' 처럼 출력하세요", """
int[] arr = {1, 2, 3, 4, 5};
// ▼ answer
for (int i = arr.length - 1; i >= 0; i--) {
    System.out.print(arr[i] + " ");
}
System.out.println();
// ▲ answer""", hint="i = arr.length - 1 에서 시작해 i >= 0 동안 i--"),
    ]))

K.append(dict(slug="배열문제3_메서드시작", title="배열 문제 · 배열 정리 · 메서드 시작",
    units=[194613, 194614, 288377, 194615],
    cheat="""```java
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
- 메서드는 class 안, main **밖**에 만들어요 (메서드 안에 메서드 X)""",
    cards=[
        ("메서드 선언의 구성 요소는?", "제어자(public static) 반환타입 메서드이름(매개변수) { 본문 } 예) public static int add(int a, int b)"),
        ("메서드를 쓰는 이유는?", "같은 코드 중복 제거, 이름으로 의미를 드러내 읽기 쉬움, 한 곳만 고치면 됨"),
        ("메서드는 코드의 어디에 작성하나?", "클래스 안, 다른 메서드(main) 밖. 메서드 안에 메서드를 만들 수 없음"),
        ("이름과 가격이 다른 배열에 있을 때 가장 비싼 상품 이름을 찾는 방법은?", "가격 배열에서 최댓값의 '인덱스'를 기억해 두고 names[maxIndex] 출력"),
    ],
    problems=[
        P("상품 이름 배열과 가격 배열이 있을 때 가장 비싼 상품의 이름을 출력하세요", """
String[] names = {"연필", "공책", "가방", "지우개"};
int[] prices = {500, 1500, 25000, 300};
// ▼ answer
int maxIndex = 0;
for (int i = 1; i < prices.length; i++) {
    if (prices[i] > prices[maxIndex]) {
        maxIndex = i;
    }
}
System.out.println(names[maxIndex]);
// ▲ answer""", hint="최댓값 대신 최댓값의 인덱스(maxIndex)를 기억하고 names[maxIndex]"),
        P("두 수를 더해 돌려주는 메서드 add를 만들고, main에서 add(5, 10)과 add(15, 20)의 결과를 한 줄씩 출력하세요", """
// ▼ answer
System.out.println(add(5, 10));
System.out.println(add(15, 20));
// ▲ answer""", methods="""
// ▼ answer
public static int add(int a, int b) {
    return a + b;
}
// ▲ answer
// TODO: // 여기에 add 메서드를 만드세요""", hint="public static int add(int a, int b) { return a + b; } 를 main 아래(클래스 안)에"),
    ]))

K.append(dict(slug="메서드사용_정의_반환타입", title="메서드 사용 · 정의 · 반환 타입",
    units=[194616, 194617, 194618],
    cheat="""```java
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
```""",
    cards=[
        ("반환할 값이 없는 메서드의 반환 타입은?", "void (return 생략 가능, 중간에 끝내려면 return;)"),
        ("반환 타입이 int인 메서드에서 if 안에서만 return하면?", "컴파일 에러. 모든 실행 경로에서 값을 return해야 함"),
        ("인수(argument)와 매개변수(parameter)의 차이는?", "인수: 호출할 때 넘기는 값 add(5, 10)의 5, 10 / 매개변수: 메서드가 받는 변수 int a, int b"),
        ("return을 만나면 그 뒤 코드는?", "실행되지 않고 메서드가 즉시 끝나며 값을 호출한 곳으로 돌려줌"),
    ],
    problems=[
        P("두 정수의 곱을 돌려주는 multiply 메서드를 만들고 multiply(3, 4)를 출력하세요", """
// ▼ answer
System.out.println(multiply(3, 4));
// ▲ answer""", methods="""
// ▼ answer
public static int multiply(int a, int b) {
    return a * b;
}
// ▲ answer
// TODO: // 여기에 multiply 메서드를 만드세요"""),
        P("'= 시작 =' 을 출력하는 void 메서드 printHeader를 만들고 두 번 호출하세요", """
// ▼ answer
printHeader();
printHeader();
// ▲ answer""", methods="""
// ▼ answer
public static void printHeader() {
    System.out.println("= 시작 =");
}
// ▲ answer
// TODO: // 여기에 printHeader 메서드를 만드세요""", hint="반환이 없으니 void. 호출은 printHeader();"),
        P("짝수면 true를 돌려주는 isEven 메서드를 만들고 isEven(4), isEven(7)을 한 줄씩 출력하세요", """
// ▼ answer
System.out.println(isEven(4));
System.out.println(isEven(7));
// ▲ answer""", methods="""
// ▼ answer
public static boolean isEven(int n) {
    return n % 2 == 0;
}
// ▲ answer
// TODO: // 여기에 isEven 메서드를 만드세요""", hint="return n % 2 == 0; 처럼 비교식 결과(boolean)를 바로 돌려줄 수 있어요"),
    ]))

K.append(dict(slug="메서드값전달_형변환", title="메서드 호출과 값 전달 · 메서드와 형변환",
    units=[194619, 194620, 194621],
    cheat="""```java
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
```""",
    cards=[
        ("메서드 안에서 매개변수 값을 바꾸면 호출한 쪽 변수도 바뀌나?", "안 바뀜. 자바는 항상 값을 복사해서 전달 (기본형 기준)"),
        ("메서드에서 바꾼 값을 호출한 쪽에서 쓰려면?", "return으로 돌려받아 대입: num = change(num);"),
        ("double 매개변수 메서드에 int 인수를 넘기면?", "자동 형변환되어 호출됨 (5 → 5.0)"),
        ("int 매개변수 메서드에 1.5를 넘기려면?", "printInt((int) 1.5) 처럼 명시적 형변환 필요 (안 하면 컴파일 에러)"),
    ],
    problems=[
        P("changeNumber가 값을 '돌려주도록' 고쳐서 num이 20으로 바뀐 뒤 '변경 후 num: 20' 이 출력되게 하세요", """
int num = 10;
// ▼ answer
num = changeNumber(num);
// ▲ answer
//> changeNumber(num);
System.out.println("변경 후 num: " + num);""", methods="""
// ▼ answer
public static int changeNumber(int x) {
    x = 20;
    return x;
}
// ▲ answer
//> public static void changeNumber(int x) {
//>     x = 20;
//> }""", hint="반환 타입을 int로 바꾸고 return x; → main에서 num = changeNumber(num);"),
        P("double을 받아 출력하는 printDouble 메서드를 만들고, int 값 5와 double 값 2.5로 각각 호출하세요", """
// ▼ answer
printDouble(5);
printDouble(2.5);
// ▲ answer""", methods="""
// ▼ answer
public static void printDouble(double d) {
    System.out.println(d);
}
// ▲ answer
// TODO: // 여기에 printDouble 메서드를 만드세요""", hint="int 5를 넘겨도 double 매개변수가 받으면 5.0으로 출력돼요"),
        P("int를 받는 printInt(이미 있음)에 값 3.99를 넘겨 3이 출력되게 하세요 (컴파일 에러 고치기)", """
// ▼ answer
printInt((int) 3.99);
// ▲ answer
//> printInt(3.99);""", methods="""
public static void printInt(int i) {
    System.out.println(i);
}""", hint="double → int는 (int) 캐스팅이 필요해요"),
    ]))

K.append(dict(slug="메서드오버로딩_문제1", title="메서드 오버로딩 · 메서드 문제",
    units=[194622, 194623],
    cheat="""```java
// 오버로딩: 이름은 같고 매개변수(타입·개수·순서)가 다른 메서드 여러 개
public static int add(int a, int b)          { return a + b; }
public static int add(int a, int b, int c)   { return a + b + c; }
public static double add(double a, double b) { return a + b; }

add(1, 2);        // 첫 번째
add(1, 2, 3);     // 두 번째
add(1.5, 2.5);    // 세 번째
// 반환 타입만 다른 건 오버로딩 X (컴파일 에러)
// 메서드 시그니처 = 이름 + 매개변수 타입 목록
```""",
    cards=[
        ("메서드 오버로딩이란?", "이름이 같고 매개변수의 타입·개수·순서가 다른 메서드를 여러 개 정의하는 것"),
        ("반환 타입만 다르게 같은 이름 메서드를 만들면?", "컴파일 에러. 오버로딩은 매개변수가 달라야 함"),
        ("메서드 시그니처란?", "메서드 이름 + 매개변수 타입(순서) — 자바가 메서드를 구분하는 기준"),
        ("add(int,int)와 add(double,double)가 있을 때 add(1, 2)는 어느 쪽?", "정확히 일치하는 add(int,int) 우선. 없을 때만 형변환 가능한 쪽"),
    ],
    problems=[
        P("add를 3개로 오버로딩해서 add(1, 2), add(1, 2, 3), add(1.5, 2.5) 결과를 한 줄씩 출력하세요", """
// ▼ answer
System.out.println(add(1, 2));
System.out.println(add(1, 2, 3));
System.out.println(add(1.5, 2.5));
// ▲ answer""", methods="""
// ▼ answer
public static int add(int a, int b) {
    return a + b;
}

public static int add(int a, int b, int c) {
    return a + b + c;
}

public static double add(double a, double b) {
    return a + b;
}
// ▲ answer
// TODO: // 여기에 add 메서드 3개를 만드세요"""),
        P("세 정수의 평균을 double로 돌려주는 average 메서드를 만들고 average(1, 2, 4)를 출력하세요", """
// ▼ answer
System.out.println(average(1, 2, 4));
// ▲ answer""", methods="""
// ▼ answer
public static double average(int a, int b, int c) {
    int sum = a + b + c;
    return (double) sum / 3;
}
// ▲ answer
// TODO: // 여기에 average 메서드를 만드세요""", hint="(double) sum / 3 — 정수 나눗셈 주의"),
        P("메시지와 횟수를 받아 그 횟수만큼 메시지를 출력하는 printMessage(String message, int times)를 만들고 printMessage(\"안녕\", 3)을 호출하세요", """
// ▼ answer
printMessage("안녕", 3);
// ▲ answer""", methods="""
// ▼ answer
public static void printMessage(String message, int times) {
    for (int i = 0; i < times; i++) {
        System.out.println(message);
    }
}
// ▲ answer
// TODO: // 여기에 printMessage 메서드를 만드세요"""),
    ]))

K.append(dict(slug="메서드문제2_정리_다음으로", title="메서드 문제 · 메서드 정리 · 다음으로 → 프로그래머스",
    units=[194624, 194625, 288383, 194626],
    cheat="""```java
// 프로그래머스 문제 = 'solution 메서드'를 완성하는 것
class Solution {
    public int solution(int[] arr) {     // 입력은 매개변수로
        int answer = 0;
        for (int x : arr) answer += x;
        return answer;                   // 출력은 return으로 (println 아님!)
    }
}
// main은 없음 — 채점기가 new Solution().solution(...)을 대신 호출

// 배열도 메서드에 넘길 수 있음
public static int getMax(int[] arr) { ... }
```
- 🎉 입문 강의 완주! 다음부터는 코테용 레슨 L01~L24 (String·정렬·ArrayList·HashMap·Stack/Queue·BFS…)
- '다음으로' 강의(27분)는 다음 강의(자바 기본편) 소개라 선택""",
    cards=[
        ("프로그래머스 문제에서 입력과 출력은 어떻게 주고받나?", "입력은 solution 메서드의 매개변수, 출력은 return 값 (main·Scanner·println 안 씀)"),
        ("int 배열을 받아 최댓값을 돌려주는 메서드의 선언부는?", "public static int getMax(int[] arr)"),
        ("잔액보다 큰 금액을 출금하려 할 때처럼 '예외 상황'을 메서드에서 처리하는 방법은?", "if로 먼저 검사해서 안내 메시지 출력 후 원래 값을 그대로 return"),
        ("메서드를 잘 나누면 좋은 점 3가지는?", "중복 제거, 이름으로 의미 전달(읽기 쉬움), 수정할 곳이 한 곳"),
    ],
    problems=[
        P("int 배열의 최댓값을 돌려주는 getMax 메서드를 만들고 getMax({4, 11, 2, 8})을 출력하세요", """
int[] numbers = {4, 11, 2, 8};
// ▼ answer
System.out.println(getMax(numbers));
// ▲ answer""", methods="""
// ▼ answer
public static int getMax(int[] arr) {
    int max = arr[0];
    for (int x : arr) {
        if (x > max) {
            max = x;
        }
    }
    return max;
}
// ▲ answer
// TODO: // 여기에 getMax 메서드를 만드세요"""),
        P("입금 deposit(balance, amount)와 출금 withdraw(balance, amount) 메서드를 만드세요. 출금액이 잔액보다 크면 '잔액이 부족합니다.'를 출력하고 잔액을 그대로 돌려줍니다. 10000원에서 1000원 입금 → 20000원 출금 시도 → 2000원 출금 후 '최종 잔액: 9000' 출력", """
int balance = 10000;
// ▼ answer
balance = deposit(balance, 1000);
balance = withdraw(balance, 20000);
balance = withdraw(balance, 2000);
// ▲ answer
System.out.println("최종 잔액: " + balance);""", methods="""
// ▼ answer
public static int deposit(int balance, int amount) {
    return balance + amount;
}

public static int withdraw(int balance, int amount) {
    if (amount > balance) {
        System.out.println("잔액이 부족합니다.");
        return balance;
    }
    return balance - amount;
}
// ▲ answer
// TODO: // 여기에 deposit, withdraw 메서드를 만드세요""", hint="잔액은 돌려받아야 바뀌어요: balance = deposit(balance, 1000);"),
        P("🎯 프로그래머스 맛보기: 배열 원소의 합을 return하는 solution 메서드를 완성하세요 (출력은 main이 대신 해 줌)", """
System.out.println(solution(new int[]{1, 2, 3, 4}));
System.out.println(solution(new int[]{10, -5}));""", methods="""
public static int solution(int[] arr) {
    int answer = 0;
    // ▼ answer
    for (int x : arr) {
        answer += x;
    }
    // ▲ answer
    return answer;
}""", hint="for (int x : arr) answer += x; — 프로그래머스에선 이 메서드만 쓰고 제출해요"),
    ]))


# ---------------------------------------------------------------------------------------------
# 생성
# ---------------------------------------------------------------------------------------------

def java_file(cls, p, desc_lines):
    body = "\n".join(("        " + l) if l.strip() else "" for l in p["body"].split("\n"))
    methods = ""
    if p["methods"]:
        methods = "\n\n" + "\n".join(("    " + l) if l.strip() else "" for l in p["methods"].split("\n"))
    imports = "import java.util.*;\n\n" if "Scanner" in p["body"] else ""
    return (f"{imports}{desc_lines}\nclass {cls} {{\n    public static void main(String[] args) {{\n{body}\n    }}{methods}\n}}\n")


def run(path, stdin):
    try:
        p = subprocess.run([*JAVA, os.path.basename(path)], cwd=os.path.dirname(path), input=stdin or "",
                           capture_output=True, text=True, timeout=60)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "timeout"


def norm(s):
    return "\n".join(l.rstrip() for l in s.strip("\n").split("\n"))


def comment(text):
    return "\n".join("// " + l if l else "//" for l in text.split("\n"))


def build_session(no, s):
    key = f"K{no:02d}"
    d = os.path.join(LESSONS, f"{key}_{s['slug']}")
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(os.path.join(d, "answers"))
    errors = []
    hints = []
    for qi, p in enumerate(s["problems"], 1):
        cls = f"Q{qi}"
        # 1) 정답 실행 → 기대 출력
        with tempfile.TemporaryDirectory() as t:
            ap = os.path.join(t, f"{cls}.java")
            with open(ap, "w", encoding="utf-8") as f:
                f.write(java_file(cls, p, ""))
            rc, out, err = run(ap, p["stdin"])
        if rc != 0:
            errors.append(f"{key} {cls} 정답 실행 실패:\n{err}")
            continue
        expected = norm(out)
        header = comment(f"{key}-{cls}. {p['desc']}") + "\n//\n"
        if p["stdin"]:
            header += "// 입력 (채점기가 자동으로 넣어 줌):\n" + comment(p["stdin"].strip("\n")) + "\n//\n"
        header += "// 기대 출력:\n" + comment(expected)
        answer_src = java_file(cls, p, header)
        with open(os.path.join(d, "answers", f"{cls}.java"), "w", encoding="utf-8") as f:
            f.write(answer_src)
        ex_src = to_exercise(answer_src)
        with open(os.path.join(d, f"{cls}.java"), "w", encoding="utf-8") as f:
            f.write(ex_src)
        with open(os.path.join(d, f"{cls}.out"), "w", encoding="utf-8") as f:
            f.write(expected + "\n")
        if p["stdin"]:
            with open(os.path.join(d, f"{cls}.in"), "w", encoding="utf-8") as f:
                f.write(p["stdin"])
        # 2) 빈칸 버전: 기대 출력과 달라야 함
        with tempfile.TemporaryDirectory() as t:
            ep = os.path.join(t, f"{cls}.java")
            shutil.copy(os.path.join(d, f"{cls}.java"), ep)
            rc2, out2, err2 = run(ep, p["stdin"])
        if rc2 == 0 and norm(out2) == expected:
            errors.append(f"{key} {cls}: 빈칸 버전이 이미 정답과 같은 출력")
        if p["hint"]:
            hints.append(f"- Q{qi}: {p['hint']}")
    # answers 폴더의 ▼▲ 표시·TODO/버그 줄 제거 (읽기용 정답)
    for name in os.listdir(os.path.join(d, "answers")):
        ap = os.path.join(d, "answers", name)
        with open(ap, encoding="utf-8") as f:
            lines = f.read().split("\n")
        keep = [l for l in lines if l.strip() not in ("// ▼ answer", "// ▲ answer")
                and not l.strip().startswith("//>") and not l.strip().startswith("// TODO:")]
        with open(ap, "w", encoding="utf-8") as f:
            f.write("\n".join(keep))

    secs = sorted({UNITS[u][0] for u in s["units"]})
    total_min = sum(UNITS[u][2] for u in s["units"])
    unit_lines = []
    for u in s["units"]:
        sec, t, m = UNITS[u]
        unit_lines.append(f"- [섹션 {sec}. {t}]({unit_url(u)})" + (f" · {m}분" if m else " · 퀴즈"))
    cards = "\n".join(f"- Q: {q}\n  A: {a}" for q, a in s["cards"])
    readme = f"""# {key}. {s['title']}

> ⏱ 강의 약 {total_min}분 + 연습문제 10분 · 🎬 [{COURSE}](https://www.inflearn.com/course/김영한의-자바-입문) 섹션 {', '.join(f'{x}({SECTIONS[x]})' for x in secs)}
> 🧑‍💻 강의 예제는 직접 따라 치기 → 끝나면 터미널에서 Enter → 연습문제 {len(s['problems'])}개 (출력 비교 자동 채점)

## 🎬 오늘 강의

{chr(10).join(unit_lines)}

## 📌 핵심 요약 (치트시트)

{s['cheat']}

## 🧩 연습문제 힌트

{chr(10).join(hints) if hints else '- 강의 예제 코드를 다시 보세요'}

## 🃏 복습 카드

{cards}
"""
    with open(os.path.join(d, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme)
    return key, total_min, len(s["problems"]), errors


def main():
    for name in os.listdir(LESSONS):
        if re.match(r"K\d+_", name):
            shutil.rmtree(os.path.join(LESSONS, name))
    covered = [u for s in K for u in s["units"]]
    assert len(covered) == len(set(covered)), "강의가 두 회차에 중복"
    missing = [u for u in UNITS if u not in covered]
    bad = 0
    for i, s in enumerate(K, 1):
        key, mins, nq, errors = build_session(i, s)
        print(f"{'✅' if not errors else '❌'} {key} {s['title']} · 강의 {mins}분 · 문제 {nq}")
        for e in errors:
            print("   " + e)
        bad += bool(errors)
    if missing:
        print("⚠️ 회차에 안 들어간 강의:", missing)
    sys.exit(1 if bad or missing else 0)


if __name__ == "__main__":
    main()
