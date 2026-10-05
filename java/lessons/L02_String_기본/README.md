# L02. String 기본

> ⏱ 25분 · 🎯 문자열 문제에서 쓰는 String 메서드를 검색 없이 쓰기 · **`==` 대신 `equals`**
> 🔗 cote 연결 문제: 가운데 글자 가져오기, 이상한 문자 만들기, 최댓값과 최솟값

## 1. String은 불변(immutable) 객체

```java
String s = "hello";
s.toUpperCase();          // s는 그대로 "hello" — 새 문자열을 "반환"만 함
s = s.toUpperCase();      // 이렇게 다시 담아야 바뀜
```

## 2. 꼭 외울 메서드

```java
String s = "hello world";
s.length()                // 11      ← 배열은 arr.length(괄호 X), 리스트는 list.size()
s.charAt(0)               // 'h'     char 반환 (L04)
s.substring(0, 5)         // "hello" [시작, 끝) — 끝 인덱스는 미포함
s.substring(6)            // "world" 6부터 끝까지
s.indexOf("o")            // 4       없으면 -1
s.contains("wor")         // true
s.startsWith("he")        // true
s.replace("l", "L")       // "heLLo worLd" (전부 바꿈)
s.split(" ")              // ["hello", "world"]
s.toCharArray()           // ['h','e',...] → 정렬·수정할 때
s.isEmpty()               // 길이 0?
"ab".repeat(3)            // "ababab"
"  hi ".trim()            // "hi"
String.valueOf(123)       // "123"   숫자 → 문자열 (또는 "" + 123)
Integer.parseInt("123")   // 123     문자열 → 숫자
```

## 3. 비교: `==`는 주소, `equals`는 내용

```java
String a = "java";
String b = new String("java");
a == b          // false  ← 같은 객체인지(주소) 비교
a.equals(b)     // true   ← 내용 비교. 문자열 비교는 항상 equals!
a.compareTo("kotlin")  // 음수  사전순 비교 (a가 앞이면 음수, 같으면 0)
a.equalsIgnoreCase("JAVA") // true
```

## 4. split의 함정

```java
"a  b".split(" ")        // ["a", "", "b"]  ← 공백 2개면 빈 문자열이 생김
"a  b".split(" +")       // ["a", "b"]      정규식: 공백 1개 이상
"a,b,,".split(",")       // ["a", "b"]      끝의 빈 문자열은 버려짐
"a,b,,".split(",", -1)   // ["a", "b", "", ""]  -1이면 유지
"abc".split("")          // ["a", "b", "c"]
```

## 🐍 파이썬이랑 다른 점

- `s[0]` ❌ → `s.charAt(0)` / `s[1:3]` ❌ → `s.substring(1, 3)` / `len(s)` → `s.length()`
- 파이썬 `==`는 내용 비교지만 자바 `==`는 주소 비교 → 문자열은 `equals`
- `s[::-1]` 같은 건 없음 → `new StringBuilder(s).reverse().toString()` (L03)

## ⚠️ 함정

1. `if (s == "yes")` — 테스트에서 우연히 맞다가 채점에서 틀림. 항상 `equals`
2. `substring(a, b)`의 b는 미포함, 길이는 `b - a`
3. 공백이 여러 개일 수 있는 입력에 `split(" ")`

## 📌 핵심 요약 (치트시트)

```java
s.length() / s.charAt(i) / s.substring(a, b) [a,b)
s.equals(t)  (== 금지) / s.compareTo(t) 사전순
s.split(" ") / s.split(" +") / s.split(",", -1)
s.indexOf(x) -1 / s.contains(x) / s.replace(a, b)
Integer.parseInt(s) ↔ String.valueOf(n)
s.toCharArray() → 정렬·수정 → new String(chars)
```

## 🧩 연습문제 힌트

- q1: 길이 n이 홀수면 `substring(n/2, n/2+1)`, 짝수면 `substring(n/2-1, n/2+1)`
- q2: `i`와 `n-1-i`의 `charAt` 비교, 절반만 돌기
- q3: `split(" ")` 후 `w.equals(word)`로 세기
- q4: `split(" ")` → 각각 `Integer.parseInt` 해서 더하기
- q5: `split(" +")`로 단어 나누고 `String.join(" ", words)`... 또는 `trim()` 먼저

## 🃏 복습 카드

- Q: 문자열 두 개의 내용이 같은지 비교하는 올바른 방법과 `==`가 위험한 이유는?
  A: `a.equals(b)`. `==`는 같은 객체(주소)인지 비교해서 내용이 같아도 false가 나올 수 있다
- Q: `"hello".substring(1, 3)`의 결과는?
  A: "el" — [1, 3) 끝 인덱스 미포함
- Q: 문자열 길이, 배열 길이, 리스트 크기는 각각 어떻게 구하나?
  A: `s.length()`, `arr.length`(괄호 없음), `list.size()`
- Q: `"a  b".split(" ")`의 결과와, 공백이 여러 개여도 단어만 얻는 방법은?
  A: ["a", "", "b"]. `split(" +")` 또는 `trim().split("\\s+")`
- Q: 문자열 ↔ 정수 변환 메서드 두 개는?
  A: `Integer.parseInt("123")` → 123, `String.valueOf(123)` → "123"
