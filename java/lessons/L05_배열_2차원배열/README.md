# L05. 배열 · 2차원 배열

> ⏱ 25분 · 🎯 배열 생성·복사·출력과 **행/열 인덱스**를 헷갈리지 않기
> 🔗 cote 연결 문제: 행렬의 덧셈, 제일 작은 수 제거하기, 행렬의 곱셈, 크레인 인형뽑기 게임

## 1. 생성과 기본값

```java
int[] a = new int[5];          // [0,0,0,0,0]  숫자는 0, boolean은 false, 객체(String 등)는 null
int[] b = {3, 1, 2};           // 선언과 동시에 초기화
int[] c = new int[]{3, 1, 2};  // return 문에서 바로 쓸 때: return new int[]{-1};
a.length                       // 5 (괄호 없음!) · 크기는 고정 — 늘려야 하면 ArrayList (L08)
```

## 2. Arrays 유틸 (import java.util.*;)

```java
Arrays.toString(b)             // "[3, 1, 2]"  ← 그냥 println(b)하면 주소가 찍힘
Arrays.fill(a, -1)             // 전부 -1로 (dist 배열 초기화)
Arrays.copyOf(b, 5)            // [3,1,2,0,0]  길이 지정 복사 (늘리면 0으로 채움)
Arrays.copyOfRange(b, 1, 3)    // [1,2]        [from, to)
Arrays.equals(b, c)            // 내용 비교 (b == c는 주소 비교)
int[] copy = b.clone();        // 1차원 복사
```

## 3. 2차원 배열 = "배열의 배열"

```java
int[][] m = new int[3][4];     // 3행 4열
m.length        // 3 (행 수)
m[0].length     // 4 (열 수)
m[r][c]         // r행 c열 — "세로 위치 먼저, 가로 위치 나중"

int[][] g = {{1, 2, 3}, {4, 5, 6}};
for (int r = 0; r < g.length; r++)
    for (int c = 0; c < g[r].length; c++)
        System.out.print(g[r][c]);
Arrays.deepToString(g)         // "[[1, 2, 3], [4, 5, 6]]"
```

## 4. 회전·전치 공식

```
원본 R×C → 전치(transpose) C×R:      t[c][r] = m[r][c]
원본 R×C → 시계방향 90° 회전 C×R:    rot[c][R-1-r] = m[r][c]
```

## 🐍 파이썬이랑 다른 점

- 파이썬 리스트는 크기가 자유롭지만 자바 배열은 **생성 시 크기 고정**.
- `[[0]*m for _ in range(n)]` → `new int[n][m]` (0으로 자동 초기화, 공유 문제 없음)
- `print(arr)` 대신 `Arrays.toString(arr)`

## ⚠️ 함정

1. `int[] b = a;`는 복사가 아니라 **같은 배열을 가리킴** → 한쪽을 바꾸면 둘 다 바뀜 (L21)
2. 행 수 `m.length`와 열 수 `m[0].length`를 바꿔 쓰는 실수 (직사각형 행렬에서만 드러남)
3. 반복문 `i <= arr.length` → ArrayIndexOutOfBoundsException

## 📌 핵심 요약 (치트시트)

```java
int[] a = new int[n]; int[][] m = new int[R][C];  // 0으로 초기화
a.length / m.length(행) / m[0].length(열)
Arrays.toString(a) / Arrays.deepToString(m) / Arrays.fill(a, v)
Arrays.copyOf(a, len) / Arrays.copyOfRange(a, from, to) / a.clone()
return new int[]{-1};
회전: rot[c][R-1-r] = m[r][c]   전치: t[c][r] = m[r][c]
```

## 🧩 연습문제 힌트

- q1: `int[][] r = new int[a.length][a[0].length];` 후 이중 for
- q2: 최솟값을 먼저 찾고, 길이 n-1 배열에 최솟값이 아닌 것만 담기 (최솟값은 하나뿐이라고 가정)
- q3: 결과 크기는 `new int[C][R]`
- q4: `p[i] = p[i-1] + a[i]`
- q5: 결과 `new int[C][R]`, `rot[c][R-1-r] = m[r][c]`

## 🃏 복습 카드

- Q: 배열을 `System.out.println(arr)`로 출력하면? 내용을 보려면?
  A: 주소 같은 값([I@1b6d3586)이 찍힘. `Arrays.toString(arr)`, 2차원은 `Arrays.deepToString`
- Q: 2차원 배열 m의 행 수와 열 수는?
  A: 행 `m.length`, 열 `m[0].length`
- Q: `int[] b = a; b[0] = 9;` 이후 a[0]은?
  A: 9. 같은 배열을 가리키기 때문. 복사는 `a.clone()`이나 `Arrays.copyOf`
- Q: 배열의 일부 [1, 4)를 새 배열로 잘라내는 메서드는?
  A: `Arrays.copyOfRange(arr, 1, 4)`
- Q: R×C 행렬을 시계방향 90° 회전하는 인덱스 공식은?
  A: 결과는 C×R, `rot[c][R-1-r] = m[r][c]`
