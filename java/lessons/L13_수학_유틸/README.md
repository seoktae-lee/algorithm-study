# L13. 수학 유틸 (GCD · 소수 · 약수 · 모듈러)

> ⏱ 25분 · 🎯 코테 수학 단골 4종을 **외워서 바로 쓰기**
> 🔗 cote 연결 문제: 최대공약수와 최소공배수, 소수 찾기, 소수 만들기, N개의 최소공배수, 예상 대진표

## 1. 최대공약수·최소공배수 (유클리드 호제법)

```java
int gcd(int a, int b) { return b == 0 ? a : gcd(b, a % b); }   // O(log n)
long lcm(long a, long b) { return a / gcd(a, b) * b; }         // 나누기 먼저 → 오버플로 예방
// 여러 수의 LCM: 누적  l = lcm(l, arr[i])
```

## 2. 소수

```java
boolean isPrime(int n) {
    if (n < 2) return false;
    for (int i = 2; (long) i * i <= n; i++)   // √n까지만, i*i 오버플로 방지
        if (n % i == 0) return false;
    return true;
}

// 에라토스테네스의 체: 1~n 전체 소수 O(n log log n)
boolean[] composite = new boolean[n + 1];
for (int i = 2; (long) i * i <= n; i++)
    if (!composite[i])
        for (int j = i * i; j <= n; j += i) composite[j] = true;
// composite[x] == false && x >= 2 → 소수
```

## 3. 약수

```java
int cnt = 0;
for (int i = 1; (long) i * i <= n; i++) {
    if (n % i == 0) cnt += (i * i == n) ? 1 : 2;   // i와 n/i 쌍
}
```

## 4. 모듈러 (답을 1,000,000,007로 나눈 나머지)

```java
final int MOD = 1_000_000_007;
(a + b) % MOD
(a * b) % MOD          // a, b가 int여도 곱은 long으로: (long) a * b % MOD
(a - b + MOD) % MOD    // 뺄셈은 음수 방지
// 빠른 거듭제곱 O(log e)
long pow(long b, long e, long m) {
    long r = 1; b %= m;
    while (e > 0) { if ((e & 1) == 1) r = r * b % m; b = b * b % m; e >>= 1; }
    return r;
}
```

## 🐍 파이썬이랑 다른 점

- 파이썬 `math.gcd`, `pow(b, e, m)` 내장 → 자바는 직접 구현 (BigInteger에 `gcd`, `modPow`가 있지만 느리고 장황)
- 파이썬은 큰 수 걱정이 없지만 자바는 모듈러 곱셈에서 long 필수

## ⚠️ 함정

1. `a * b / gcd` → 곱셈에서 오버플로. `a / gcd * b`
2. `i * i <= n`에서 i*i가 int 범위를 넘을 수 있음 → `(long) i * i` 또는 `i <= n / i`
3. 1은 소수가 아님, 2는 소수

## 📌 핵심 요약 (치트시트)

```java
gcd(a, b) = b == 0 ? a : gcd(b, a % b);   lcm = a / gcd * b
isPrime: for (i = 2; (long) i * i <= n; i++)
체: for i*i<=n, if !c[i], for j = i*i; j <= n; j += i → c[j] = true
약수 개수: i*i<=n 쌍으로 세기 (제곱수는 1)
MOD: (long) a * b % MOD, (a - b + MOD) % MOD, 빠른 거듭제곱
```

## 🧩 연습문제 힌트

- q1: `int g = gcd(n, m); return new int[]{g, n / g * m};`
- q2: 체를 만들고 2~n 중 false 개수
- q3: 위 빠른 거듭제곱
- q4: `l = l / gcd(l, x) * x` 누적
- q5: √n까지 쌍으로 세기

## 🃏 복습 카드

- Q: 유클리드 호제법으로 gcd를 구하는 한 줄 코드는?
  A: `int gcd(int a, int b) { return b == 0 ? a : gcd(b, a % b); }`
- Q: lcm을 `a / gcd(a,b) * b` 순서로 계산하는 이유는?
  A: `a * b`를 먼저 하면 오버플로 가능. 나누기를 먼저 하면 중간값이 작아짐
- Q: 에라토스테네스의 체에서 안쪽 루프 j의 시작값과 이유는?
  A: `i * i`. 그보다 작은 i의 배수는 더 작은 소수가 이미 지웠기 때문
- Q: 1,000,000,007로 나눈 나머지를 구할 때 곱셈에서 주의할 점은?
  A: int끼리 곱하면 넘침 → `(long) a * b % MOD`
- Q: 빠른 거듭제곱의 시간복잡도와 핵심 아이디어는?
  A: O(log e). 지수를 2진수로 보고, 비트가 1일 때만 결과에 곱하며 밑을 제곱해 나감
