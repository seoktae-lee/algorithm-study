# L04. char 연산

> ⏱ 25분 · 🎯 문자 = 숫자라는 걸 이용해 **알파벳 이동·숫자 변환·빈도 세기**를 한 줄로
> 🔗 cote 연결 문제: 시저 암호, 숫자 문자열과 영단어, 신규 아이디 추천, 문자열 내림차순으로 배치하기

## 1. char는 사실 숫자(유니코드)

```java
char c = 'a';
int code = c;            // 97   char → int는 자동
char next = (char) (c + 1);  // 'b'  int → char는 캐스팅 필요
'A' = 65, 'a' = 97, '0' = 48     // 외울 필요는 없고 "빼서" 씁니다
```

## 2. 3대 패턴

```java
// ① 숫자 문자 → 정수
int d = '7' - '0';           // 7

// ② 알파벳 → 0~25 인덱스 (빈도 세기)
int[] cnt = new int[26];
for (char ch : s.toCharArray()) cnt[ch - 'a']++;

// ③ 알파벳 n칸 밀기 (z 다음은 a)
char shifted = (char) ('a' + (c - 'a' + n) % 26);
```

## 3. Character 유틸

```java
Character.isDigit(c)       // '0'~'9'?
Character.isLetter(c)      // 알파벳(한글 포함)?
Character.isUpperCase(c) / isLowerCase(c)
Character.toUpperCase(c) / toLowerCase(c)   // char 반환
Character.isLetterOrDigit(c)
Character.getNumericValue('7')  // 7 (c - '0'과 같음)
String.valueOf(c)          // char → String
```

## 4. char 배열로 정렬·수정

```java
char[] arr = s.toCharArray();
Arrays.sort(arr);                 // 오름차순 (대문자가 소문자보다 앞: 'Z'(90) < 'a'(97))
String sorted = new String(arr);  // char[] → String
```

## 🐍 파이썬이랑 다른 점

- 파이썬 `ord('a')`, `chr(97)` → 자바는 `(int) 'a'`, `(char) 97`
- 자바는 `'a'`(char, 작은따옴표)와 `"a"`(String, 큰따옴표)가 **다른 타입**. `"a".equals('a')`는 false

## ⚠️ 함정

1. `char + char`는 int: `'a' + 'b'` = 195. 문자열로 붙이려면 `"" + a + b` 또는 StringBuilder
2. `c - 'a'`는 소문자일 때만 0~25. 대문자는 `c - 'A'`
3. 밀기 연산에서 `% 26`을 빼먹으면 'z' 다음이 '{'

## 📌 핵심 요약 (치트시트)

```java
int d = c - '0';                       // 숫자 문자 → int
int idx = c - 'a';  int[] cnt = new int[26];  // 빈도
char s = (char) ('a' + (c - 'a' + n) % 26);    // 알파벳 밀기
Character.isDigit/isLetter/isUpperCase/toUpperCase(c)
char[] a = s.toCharArray(); Arrays.sort(a); new String(a)
```

## 🧩 연습문제 힌트

- q1: 공백이면 그대로, 대문자면 base='A', 소문자면 base='a' → `(char) (base + (c - base + n) % 26)`
- q2: `Character.isDigit(c)`이면 `sum += c - '0'`
- q3: `int[26]`에 세고, 가장 큰 칸의 인덱스 i → `(char) ('a' + i)`. 앞에서부터 보면 동점일 때 알파벳 순 첫 글자
- q4: 대문자면 `toLowerCase`, 소문자면 `toUpperCase`
- q5: 두 문자열의 `int[26]` 빈도를 비교, 또는 `toCharArray` 정렬 후 `Arrays.equals`

## 🃏 복습 카드

- Q: 문자 '7'을 정수 7로 바꾸는 가장 짧은 식은?
  A: `'7' - '0'`
- Q: 소문자 c를 알파벳 순서 n칸 뒤로 미는 식(z 다음은 a)은?
  A: `(char) ('a' + (c - 'a' + n) % 26)`
- Q: 소문자 문자열의 알파벳 빈도를 세는 대표 코드는?
  A: `int[] cnt = new int[26]; for (char c : s.toCharArray()) cnt[c - 'a']++;`
- Q: `'a' + 'b'`의 결과 타입과 값은?
  A: int, 195 (char끼리 더하면 int)
- Q: char 배열을 정렬한 뒤 다시 String으로 만드는 코드는?
  A: `char[] a = s.toCharArray(); Arrays.sort(a); String r = new String(a);`
