# L15. 문자열 고급 · 정규식 · 포맷

> ⏱ 30분 · 🎯 카카오 문자열 문제(파싱·치환·시각 계산)를 **replaceAll·format·parseInt**로 짧게
> 🔗 cote 연결 문제: 신규 아이디 추천, 숫자 문자열과 영단어, [1차] 다트 게임, 주차 요금 계산, 오픈채팅방

## 1. 변환

```java
Integer.parseInt("-42")  Long.parseLong("10000000000")  Double.parseDouble("3.5")
String.valueOf(42)  Integer.toString(42)  "" + 42
String.join("-", List.of("a", "b"))       // "a-b"  (String 컬렉션/배열만)
```

## 2. String.format

```java
String.format("%02d:%02d", 9, 5)   // "09:05"  두 자리 0 채우기
String.format("%5d", 42)            // "   42"  폭 5 오른쪽 정렬
String.format("%.2f", 3.14159)      // "3.14"
String.format("%s님", name)
```

## 3. replace vs replaceAll

```java
s.replace(".", "")        // 글자 그대로 "." 치환 (정규식 아님)
s.replaceAll("[^a-z0-9._-]", "")   // 정규식: 허용 문자 외 전부 삭제
s.replaceAll("\\.{2,}", ".")       // 마침표 2개 이상 → 1개
s.replaceAll("^\\.|\\.$", "")      // 맨 앞/맨 뒤 마침표 제거
s.replaceAll("zero", "0")
```

## 4. 정규식 최소 문법

| 패턴 | 뜻 |
|---|---|
| `.` | 아무 글자 1개 (마침표 자체는 `\\.`) |
| `[abc]` / `[^abc]` / `[a-z0-9]` | 이 중 하나 / 이것 빼고 / 범위 |
| `\\d` `\\s` `\\w` | 숫자 / 공백 / 영숫자_ |
| `+` `*` `?` `{2,}` | 1개 이상 / 0개 이상 / 0~1개 / 2개 이상 |
| `^` `$` | 시작 / 끝 |
| `a\|b` | a 또는 b |

```java
"010-1234-5678".matches("\\d{3}-\\d{4}-\\d{4}")   // 전체가 패턴과 일치?
"a1b22c333".split("[a-z]")                          // ["", "1", "22", "333"]
```

## 5. 시각 "HH:MM" 다루기 → 분으로 바꿔 계산 후 되돌리기

```java
String[] t = "09:05".split(":");
int minutes = Integer.parseInt(t[0]) * 60 + Integer.parseInt(t[1]);   // 545
String back = String.format("%02d:%02d", minutes / 60, minutes % 60);  // "09:05"
```

## 🐍 파이썬이랑 다른 점

- `f"{h:02d}"` → `String.format("%02d", h)`
- `re.sub(p, r, s)` → `s.replaceAll(p, r)`, 자바 문자열 안에서 `\`는 `\\`로 두 번
- `"-".join(list)` → `String.join("-", list)` (숫자 리스트는 먼저 문자열로)

## ⚠️ 함정

1. `s.split(".")` → 정규식에서 `.`은 "아무 글자" → 결과가 빈 배열! `split("\\.")`
2. `replace`와 `replaceAll` 혼동 — `replaceAll(".", "")`은 전부 지워버림
3. `split("|")`도 정규식 → `split("\\|")`

## 📌 핵심 요약 (치트시트)

```java
String.format("%02d:%02d", h, m) / "%.2f" / "%5d"
s.replaceAll("[^a-z0-9._-]", "") / "\\.{2,}" / "^\\.|\\.$"
s.split("\\.") / s.split("\\|") / s.split("\\s+")   (split 인자는 정규식!)
s.matches("\\d+")
시각: h * 60 + m ↔ String.format("%02d:%02d", t / 60, t % 60)
```

## 🧩 연습문제 힌트

- q1: 소문자 → `replaceAll("[^a-z0-9._-]", "")` → `"\\.{2,}"`→"." → `"^\\.|\\.$"` 제거 → 빈 문자열이면 "a" → 16자 이상이면 15자로 자르고 끝 마침표 제거 → 2자 이하면 마지막 글자 반복
- q2: `String[] words = {"zero", ..., "nine"}` → `s = s.replaceAll(words[i], String.valueOf(i))`
- q3/q4: 위 시각 변환
- q5: `split(" ")` → parseInt 하며 min/max 갱신 → `min + " " + max`

## 🃏 복습 카드

- Q: `"a.b.c".split(".")`의 결과와 올바른 코드는?
  A: 빈 배열(.은 정규식의 '아무 글자'). `split("\\.")`
- Q: 9시 5분을 "09:05"로 만드는 코드는?
  A: `String.format("%02d:%02d", 9, 5)`
- Q: replace와 replaceAll의 차이는?
  A: replace는 글자 그대로 치환, replaceAll은 첫 인자를 정규식으로 해석
- Q: 소문자·숫자·`.`·`_`·`-` 외의 문자를 모두 지우는 코드는?
  A: `s.replaceAll("[^a-z0-9._-]", "")`
- Q: "HH:MM" 문자열을 분 단위 정수로 바꾸는 코드는?
  A: `String[] t = s.split(":"); int m = Integer.parseInt(t[0]) * 60 + Integer.parseInt(t[1]);`
