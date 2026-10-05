# L07. 정렬 ② Comparator · Comparable

> ⏱ 30분 · 🎯 "A 기준 내림차순, 같으면 B 기준 오름차순" 같은 **다중 정렬 기준**을 자유롭게
> 🔗 cote 연결 문제: 실패율, 문자열 내 마음대로 정렬하기, 가장 큰 수, 베스트앨범, 디스크 컨트롤러

## 1. Comparator = "두 개를 비교하는 규칙"

`compare(a, b)`가 **음수면 a가 앞**, 양수면 b가 앞, 0이면 같음.

```java
Integer[] a = {3, 1, 2};
Arrays.sort(a, (x, y) -> x - y);              // 오름차순
Arrays.sort(a, (x, y) -> y - x);              // 내림차순
Arrays.sort(a, (x, y) -> Integer.compare(y, x));  // 내림차순 (오버플로 안전 ✅)
```

> `x - y`는 x, y가 ±10억 근처면 오버플로로 부호가 뒤집힘 → **`Integer.compare`가 정석**

## 2. 객체 배열·2차원 배열 정렬

```java
int[][] iv = {{1, 3}, {0, 2}, {1, 5}};
Arrays.sort(iv, (p, q) -> p[0] != q[0] ? Integer.compare(p[0], q[0])   // 시작 오름차순
                                       : Integer.compare(q[1], p[1])); // 같으면 끝 내림차순

String[] w = {"banana", "kiwi", "fig"};
Arrays.sort(w, (s, t) -> s.length() != t.length() ? s.length() - t.length() : s.compareTo(t));
```

## 3. Comparator 조합 메서드 (가독성 ↑)

```java
Arrays.sort(w, Comparator.comparing(String::length)           // 길이 오름차순
                         .thenComparing(Comparator.naturalOrder()));  // 같으면 사전순
Arrays.sort(iv, Comparator.comparingInt((int[] p) -> p[0])
                          .thenComparing((int[] p) -> p[1], Comparator.reverseOrder()));
list.sort(Comparator.comparing(Student::score).reversed());  // .reversed()는 앞 전체를 뒤집음
```

## 4. Comparable = 클래스에 "기본 순서" 심기

```java
class Stage implements Comparable<Stage> {
    int no; double rate;
    public int compareTo(Stage o) {                 // 실패율 내림차순, 같으면 번호 오름차순
        if (rate != o.rate) return Double.compare(o.rate, rate);
        return Integer.compare(no, o.no);
    }
}
Collections.sort(stages);   // compareTo 기준
```

## 5. 인덱스를 정렬하기 (값으로 순서를 정하고 번호를 반환할 때)

```java
Integer[] idx = new Integer[n];
for (int i = 0; i < n; i++) idx[i] = i;
Arrays.sort(idx, (i, j) -> Double.compare(rate[j], rate[i]));  // 값 기준으로 인덱스 정렬
```

## 🐍 파이썬이랑 다른 점

- 파이썬 `key=lambda x: (-x[0], x[1])` 한 줄 → 자바는 compare 함수로 "어느 쪽이 앞인지"를 직접 정의
- 기본형 배열(int[])은 Comparator 불가 → `Integer[]`, `int[][]`, `List`는 가능

## ⚠️ 함정

1. `(a, b) -> a - b`의 오버플로 → `Integer.compare(a, b)`
2. double 비교에 `(int)(a - b)` → 0.3 차이가 0이 됨 → `Double.compare`
3. `thenComparing` 뒤에 `.reversed()`를 붙이면 **전체**가 뒤집힘

## 📌 핵심 요약 (치트시트)

```java
Arrays.sort(objArr, (a, b) -> Integer.compare(a, b));       // 음수면 a가 앞
Arrays.sort(iv, (p, q) -> p[0] != q[0] ? Integer.compare(p[0], q[0]) : Integer.compare(q[1], p[1]));
Comparator.comparing(f).thenComparing(g).reversed()
Double.compare(x, y) / Integer.compare / s.compareTo(t)
class X implements Comparable<X> { public int compareTo(X o) {...} }
인덱스 정렬: Integer[] idx + Arrays.sort(idx, (i, j) -> ...)
```

## 🧩 연습문제 힌트

- q1: 길이 다르면 길이 차, 같으면 `compareTo`. 원본을 `clone()`해서 정렬
- q2: 위 예제 그대로
- q3: n번째 글자 비교, 같으면 문자열 전체 `compareTo`
- q4: 스테이지 i의 도달자 = 스테이지 번호 ≥ i인 사람 수, 실패율 = (i에 머문 사람)/(도달자), 도달자 0이면 0. 인덱스 정렬
- q5: 숫자를 문자열로 바꾸고 `(a, b) -> (b + a).compareTo(a + b)`. 맨 앞이 "0"이면 "0"

## 🃏 복습 카드

- Q: Comparator의 `compare(a, b)`가 음수를 반환하면 정렬 결과에서 누가 앞인가?
  A: a가 앞
- Q: `(a, b) -> a - b` 대신 `Integer.compare(a, b)`를 써야 하는 이유는?
  A: a - b가 int 범위를 넘으면 부호가 뒤집혀 정렬이 틀어짐(오버플로)
- Q: int[][] 구간을 시작 오름차순, 같으면 끝 내림차순으로 정렬하는 코드는?
  A: `Arrays.sort(iv, (p, q) -> p[0] != q[0] ? Integer.compare(p[0], q[0]) : Integer.compare(q[1], p[1]));`
- Q: '가장 큰 수' 문제에서 숫자 문자열 a, b의 비교 기준은?
  A: `(b + a).compareTo(a + b)` — 이어 붙였을 때 더 큰 쪽이 앞. 결과가 "0..."이면 "0"
- Q: Comparable과 Comparator의 차이는?
  A: Comparable은 클래스 안에 compareTo로 "기본 순서"를 정의, Comparator는 밖에서 넘기는 "별도 규칙"(여러 개 가능)
