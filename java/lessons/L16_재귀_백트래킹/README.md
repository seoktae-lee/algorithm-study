# L16. 재귀 · 조합/순열/부분집합 템플릿 (백트래킹)

> ⏱ 30분 · 🎯 완전탐색 3종 템플릿을 **손이 기억하게** · 필드(전역 변수)로 결과 모으기
> 🔗 cote 연결 문제: 타겟 넘버, 소수 만들기, 피로도, 소수 찾기(순열), 모음사전, 양궁대회

## 1. 재귀의 뼈대

```java
int fact(int n) {
    if (n <= 1) return 1;        // ① 종료 조건 (없으면 StackOverflowError)
    return n * fact(n - 1);      // ② 더 작은 문제로
}
```

> 자바 기본 스택은 깊이 대략 수천~1만 단위. 깊이 10^5 재귀는 위험 → 반복문/스택으로

## 2. 프로그래머스에서 결과 모으기: 필드 사용

```java
class Solution {
    int answer = 0;               // 필드(인스턴스 변수) — 재귀 함수들이 공유
    int[] nums; int target;
    public int solution(int[] numbers, int target) {
        this.nums = numbers; this.target = target;
        dfs(0, 0);
        return answer;
    }
    void dfs(int idx, int sum) {
        if (idx == nums.length) { if (sum == target) answer++; return; }
        dfs(idx + 1, sum + nums[idx]);
        dfs(idx + 1, sum - nums[idx]);
    }
}
```

## 3. 3대 템플릿

```java
// ① 조합 nCr: start부터 고르기 (순서 무관, 중복 없음)
void comb(int start, int depth, int r) {
    if (depth == r) { /* picked[0..r-1] 사용 */ return; }
    for (int i = start; i < n; i++) {
        picked[depth] = arr[i];
        comb(i + 1, depth + 1, r);
    }
}

// ② 순열 nPr: visited로 "이미 쓴 것" 표시 (순서 중요)
void perm(int depth, int r) {
    if (depth == r) { /* 사용 */ return; }
    for (int i = 0; i < n; i++) {
        if (visited[i]) continue;
        visited[i] = true; picked[depth] = arr[i];
        perm(depth + 1, r);
        visited[i] = false;                  // ← 되돌리기(백트래킹)
    }
}

// ③ 부분집합: 넣는다/안 넣는다 두 갈래 (2^n)
void subset(int idx) {
    if (idx == n) { /* 사용 */ return; }
    chosen[idx] = true;  subset(idx + 1);
    chosen[idx] = false; subset(idx + 1);
}
```

| 템플릿 | 경우의 수 | n 한계(대략) |
|---|---|---|
| 순열 | n! | n ≤ 10 |
| 부분집합 | 2^n | n ≤ 20 |
| 조합 | nCr | 상황별 |

## 4. 메모이제이션 (중복 계산 제거 → DP의 시작)

```java
long[] memo = new long[n + 1];
long fib(int n) {
    if (n <= 1) return n;
    if (memo[n] != 0) return memo[n];
    return memo[n] = fib(n - 1) + fib(n - 2);   // O(2^n) → O(n)
}
```

## 🐍 파이썬이랑 다른 점

- `itertools.permutations/combinations`가 없음 → 위 템플릿을 직접
- 파이썬 `nonlocal`/전역 대신 **클래스 필드**로 공유
- 파이썬 기본 재귀 한도(1000)보다 자바가 깊게 가지만 무한은 아님

## ⚠️ 함정

1. 순열에서 `visited[i] = false` 되돌리기 누락
2. 조합에서 `comb(i + 1, …)` 대신 `comb(start + 1, …)` → 중복 조합 발생
3. 결과 리스트에 `current`를 그대로 add → 나중에 바뀜. `new ArrayList<>(current)`로 복사 (L21)

## 📌 핵심 요약 (치트시트)

```java
조합: for (i = start; i < n; i++) { pick; comb(i + 1, depth + 1); }
순열: for (i = 0; i < n; i++) if (!v[i]) { v[i] = true; perm(depth + 1); v[i] = false; }
부분집합: f(idx + 1) 넣고 / f(idx + 1) 안 넣고
결과는 필드에 모으기 · 리스트는 new ArrayList<>(cur)로 복사해서 저장
메모: if (memo[n] != 0) return memo[n]; return memo[n] = …;
```

## 🧩 연습문제 힌트

- q1: 위 2번 코드 (메서드 안에서 쓰려면 필드에 저장해 두기)
- q2: 조합 템플릿으로 3개 고르고 합이 소수면 +1
- q3: 순열 템플릿 + StringBuilder, 입력이 정렬돼 있으면 결과도 사전순
- q4: 순열 템플릿: 남은 피로도 ≥ 최소 필요도인 던전만 들어가며 최대 depth 갱신
- q5: `long[] memo` 메모이제이션 (int로 하면 넘침)

## 🃏 복습 카드

- Q: 조합(nCr) 백트래킹에서 중복 없이 고르기 위한 핵심 인자와 재귀 호출 형태는?
  A: 시작 인덱스 start. `for (i = start; i < n; i++) comb(i + 1, depth + 1)`
- Q: 순열 백트래킹에서 "백트래킹"에 해당하는 코드는?
  A: 재귀 호출 뒤 `visited[i] = false;`로 되돌리기
- Q: 순열·부분집합 완전탐색이 가능한 대략적인 n의 한계는?
  A: 순열 n! → n ≤ 10, 부분집합 2^n → n ≤ 20
- Q: 프로그래머스에서 재귀 함수의 결과를 모으는 방법은?
  A: Solution 클래스의 필드(인스턴스 변수)에 저장하고 solution에서 반환
- Q: 메모이제이션 피보나치에서 n=50일 때 int 대신 long을 쓰는 이유는?
  A: fib(50) = 12,586,269,025로 int 범위(약 21억)를 넘음
