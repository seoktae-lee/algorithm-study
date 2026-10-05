# L14. 비트 연산 · 진법 변환

> ⏱ 25분 · 🎯 2진수 다루기, **부분집합을 비트마스크로** 전부 돌기
> 🔗 cote 연결 문제: [1차] 비밀지도, 다음 큰 숫자, 이진 변환 반복하기, 3진법 뒤집기, 피로도(비트마스크로도 가능)

## 1. 연산자

```java
a & b    // AND   둘 다 1
a | b    // OR    하나라도 1
a ^ b    // XOR   다르면 1 (같은 수 두 번 XOR하면 0)
~a       // NOT   비트 반전 (~5 == -6)
a << k   // 왼쪽 시프트 = a × 2^k
a >> k   // 오른쪽 시프트 = a ÷ 2^k (부호 유지)
a >>> k  // 부호 없는 오른쪽 시프트
```

## 2. 자주 쓰는 한 줄

```java
(n & 1) == 1          // 홀수?
(n >> i) & 1          // i번째 비트 (0부터)
n | (1 << i)          // i번째 비트 켜기
n & ~(1 << i)         // i번째 비트 끄기
(n & (n - 1)) == 0    // n > 0일 때 2의 거듭제곱?
Integer.bitCount(n)   // 1의 개수
```

## 3. 진법 변환

```java
Integer.toBinaryString(10)     // "1010"
Integer.toString(10, 3)        // "101"  (3진법)
Integer.parseInt("1010", 2)    // 10
Integer.parseInt("101", 3)     // 10
Long.parseLong(s, 2)           // 긴 2진수
String.format("%5s", Integer.toBinaryString(9)).replace(' ', '0')  // "01001" 자릿수 맞추기
```

## 4. 비트마스크로 부분집합 전부 돌기 (n ≤ 20)

```java
for (int mask = 0; mask < (1 << n); mask++) {   // 2^n가지
    int sum = 0;
    for (int i = 0; i < n; i++)
        if ((mask & (1 << i)) != 0) sum += nums[i];   // i번째 원소가 포함됨
}
```

## 🐍 파이썬이랑 다른 점

- `bin(10)` → `Integer.toBinaryString(10)` ("0b" 접두사 없음), `int("1010", 2)` → `Integer.parseInt("1010", 2)`
- 파이썬 int는 무한 비트, 자바 int는 32비트 → `1 << 31`은 음수, `1 << 32`는 1(!) → 큰 마스크는 `1L << k`

## ⚠️ 함정

1. 연산자 우선순위: `a & b == 0`은 `a & (b == 0)` → 컴파일 에러. **항상 괄호** `(a & b) == 0`
2. `1 << 40` (int) → 의도와 다름. `1L << 40`
3. toBinaryString은 앞의 0을 안 붙임 → 자릿수 맞추기 필요 (비밀지도)

## 📌 핵심 요약 (치트시트)

```java
& | ^ ~ << >>   (괄호 필수: (a & b) == 0)
(n >> i) & 1 / n | (1 << i) / Integer.bitCount(n)
Integer.toBinaryString(n) / Integer.toString(n, r) / Integer.parseInt(s, r)
for (mask = 0; mask < 1 << n; mask++) for i: if ((mask >> i & 1) == 1) …
```

## 🧩 연습문제 힌트

- q1: `arr1[i] | arr2[i]` → 오른쪽(낮은 비트)부터 n자리를 보며 1이면 '#', 0이면 ' '
- q2: `Integer.bitCount(n)`과 같은 다음 수를 n+1부터 찾기
- q3: 0의 개수를 세서 더하고, 남은 1의 개수(길이)를 2진수 문자열로 → "1"이 될 때까지
- q4: 위 비트마스크 패턴. 빈 집합(mask=0)은 target이 0일 때만 세짐
- q5: `n > 0 && (n & (n - 1)) == 0`

## 🃏 복습 카드

- Q: 정수 n의 i번째 비트(0부터)가 1인지 확인하는 식은?
  A: `((n >> i) & 1) == 1` 또는 `(n & (1 << i)) != 0`
- Q: n개의 원소로 만들 수 있는 모든 부분집합을 비트마스크로 도는 반복문은?
  A: `for (int mask = 0; mask < (1 << n); mask++)` 안에서 `(mask & (1 << i)) != 0`이면 i번째 포함
- Q: 10진수 ↔ 2진수 문자열 변환 메서드는?
  A: `Integer.toBinaryString(10)` → "1010", `Integer.parseInt("1010", 2)` → 10
- Q: `if (a & b == 0)`의 문제는?
  A: ==가 &보다 우선순위가 높아 `a & (b == 0)`으로 해석됨. `(a & b) == 0`
- Q: n이 2의 거듭제곱인지 비트로 판별하는 식은?
  A: `n > 0 && (n & (n - 1)) == 0`
