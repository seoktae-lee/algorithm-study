# L03. StringBuilder

> ⏱ 20분 · 🎯 문자열을 만들어 가는 문제에서 `+=` 대신 StringBuilder → 시간 초과 예방
> 🔗 cote 연결 문제: 이상한 문자 만들기, 시저 암호, 이진 변환 반복하기, 짝지어 제거하기

## 1. 왜 필요한가

String은 불변이라 `s += "a"`는 **매번 새 문자열을 통째로 복사**합니다. 반복문 n번이면 O(n²).

```java
String s = "";
for (int i = 0; i < 100000; i++) s += i;   // 느림: 매번 전체 복사

StringBuilder sb = new StringBuilder();
for (int i = 0; i < 100000; i++) sb.append(i);  // 빠름: 내부 버퍼에 이어 붙임
String result = sb.toString();
```

## 2. 메서드

```java
StringBuilder sb = new StringBuilder("abc");
sb.append("d").append(1).append('x');   // 체이닝 가능 → "abcd1x"
sb.length()                // 6
sb.charAt(0)               // 'a'
sb.setCharAt(0, 'A')       // "Abcd1x"
sb.insert(0, "<")          // "<Abcd1x"  앞에 끼워 넣기 (O(n)이라 남발 금지)
sb.deleteCharAt(sb.length() - 1)   // 마지막 글자 삭제 → 스택처럼 사용 가능
sb.reverse()               // 뒤집기 (sb 자체가 바뀜)
sb.toString()              // String으로 변환 — 반환할 땐 꼭!
sb.setLength(0)            // 비우기 (재사용)
```

## 3. 구분자 붙이기 패턴

```java
// "1,2,3" (마지막 쉼표 없이)
for (int i = 0; i < arr.length; i++) {
    if (i > 0) sb.append(',');
    sb.append(arr[i]);
}
// 또는 String.join(",", 문자열리스트) — 숫자 배열이면 변환 필요
```

## 🐍 파이썬이랑 다른 점

- 파이썬 `"".join(list)` 역할 = StringBuilder. 파이썬도 `+=` 반복은 느린 편인데 자바는 더 확실하게 느림.
- `s[::-1]` → `new StringBuilder(s).reverse().toString()`

## ⚠️ 함정

1. `sb.append('a' + 1)` → `"98"`이 붙음 (char + int = int). `(char) ('a' + 1)`로 감싸기
2. 반환 타입이 String인데 `return sb;` → 컴파일 에러. `sb.toString()`
3. `sb.equals(other)`는 내용 비교가 아님 → `sb.toString().equals(...)`

## 📌 핵심 요약 (치트시트)

```java
StringBuilder sb = new StringBuilder();
sb.append(x); sb.insert(0, x); sb.deleteCharAt(sb.length() - 1);
sb.reverse(); sb.setCharAt(i, c); sb.toString();
String rev = new StringBuilder(s).reverse().toString();
// 반복문 안 문자열 += 금지 → O(n²)
```

## 🧩 연습문제 힌트

- q1: `new StringBuilder(s).reverse().toString()`
- q2: 단어 안 위치 `idx`를 두고, 공백을 만나면 `idx = 0`. 짝수 idx면 `Character.toUpperCase(c)`
- q3: `if (i > 0) sb.append(',');`
- q4: 마지막에 넣은 글자(`sb.charAt(sb.length()-1)`)와 다를 때만 append
- q5: `n % 2`를 append 하고 `n /= 2`, 끝나면 reverse. n == 0이면 "0"

## 🃏 복습 카드

- Q: 반복문에서 `String s += x`가 느린 이유와 대안은?
  A: String은 불변이라 매번 전체를 새로 복사 → O(n²). StringBuilder.append 후 마지막에 toString()
- Q: StringBuilder로 마지막 글자를 지우는 코드는?
  A: `sb.deleteCharAt(sb.length() - 1);`
- Q: `sb.append('a' + 1)`을 하면 무엇이 붙나? 'b'를 붙이려면?
  A: "98"(char+int=int). `sb.append((char) ('a' + 1))`
- Q: 문자열 s를 뒤집는 한 줄 코드는?
  A: `new StringBuilder(s).reverse().toString()`
- Q: StringBuilder 두 개의 내용이 같은지 비교하려면?
  A: `sb1.toString().equals(sb2.toString())` (StringBuilder.equals는 주소 비교)
