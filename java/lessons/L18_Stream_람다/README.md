# L18. 람다 · Stream — 언제 쓰고 언제 피하나

> ⏱ 25분 · 🎯 짧은 변환은 Stream으로 한 줄, **반복이 많은 핵심 로직은 for문** (성능)
> 🔗 cote 연결 문제: 대부분의 Lv.1 배열 문제(합·필터·정렬), 베스트앨범(groupingBy), 귤 고르기

## 1. 람다와 메서드 참조

```java
(a, b) -> a + b          // 매개변수 -> 식
x -> { int y = x * 2; return y; }   // 여러 줄
Integer::parseInt        // 메서드 참조 = s -> Integer.parseInt(s)
String::length           // s -> s.length()
```

## 2. 기본형 스트림 (int[] 다루기)

```java
int[] a = {3, 1, 4, 1, 5};
Arrays.stream(a).sum();                 // 14
Arrays.stream(a).max().getAsInt();      // 5 (OptionalInt)
Arrays.stream(a).average().orElse(0);   // 2.8
Arrays.stream(a).filter(x -> x % 2 == 1).map(x -> x * x).toArray();
Arrays.stream(a).distinct().sorted().toArray();
IntStream.range(0, n)                   // 0 ~ n-1
IntStream.rangeClosed(1, n).sum();
```

## 3. 객체 스트림과 변환

```java
// int[] → 내림차순 int[]
Arrays.stream(a).boxed().sorted(Comparator.reverseOrder()).mapToInt(Integer::intValue).toArray();
// List<Integer> → int[]
list.stream().mapToInt(Integer::intValue).toArray();
// String[] → 필터/변환 → List
List<String> r = Arrays.stream(words).filter(w -> w.length() >= 3).map(String::toUpperCase).collect(Collectors.toList());
// 또는 .toList() (Java 16+, 불변 리스트)
String joined = r.stream().collect(Collectors.joining("-"));
```

## 4. 그룹핑 (import java.util.stream.*;)

```java
Map<Integer, Long> byLen = Arrays.stream(words)
        .collect(Collectors.groupingBy(String::length, Collectors.counting()));
Map<String, List<Integer>> byGenre = ...groupingBy(i -> genres[i]);
```

## 5. 언제 쓰나 / 피하나

| 상황 | 추천 |
|---|---|
| 입력 변환·합계·한 번 정렬·결과 변환 | Stream OK (가독성 ↑) |
| 반복문 안에서 수만 번 호출되는 코드, DFS/BFS 내부 | **for문** (Stream 생성 비용이 누적되어 시간 초과 위험) |
| 인덱스가 필요한 로직, 중간에 break | for문 |

> 실측 감각: 단순 합계 10^7번이면 for문이 Stream보다 수 배 빠른 경우가 흔함. 코테에서 "정답인데 시간 초과"의 원인이 될 수 있음.

## 🐍 파이썬이랑 다른 점

- 리스트 컴프리헨션 `[x*x for x in a if x%2]` ≈ `stream().filter().map()`
- `sum(a)` ≈ `Arrays.stream(a).sum()` — 자바는 int[]용 IntStream과 객체 Stream이 따로

## ⚠️ 함정

1. `Arrays.stream(int[]).sorted(Comparator.reverseOrder())` ❌ → `boxed()` 먼저
2. `max()`는 Optional → `getAsInt()`(빈 배열이면 예외) / `orElse(기본값)`
3. 람다 안에서 바깥 지역 변수를 바꿀 수 없음(effectively final) → 배열 `int[] cnt = {0}`이나 필드로

## 📌 핵심 요약 (치트시트)

```java
Arrays.stream(a).sum() / .max().getAsInt() / .average().orElse(0)
.filter(x -> …).map(x -> …).distinct().sorted().toArray()
.boxed().sorted(Comparator.reverseOrder()).mapToInt(Integer::intValue).toArray()
list.stream().mapToInt(Integer::intValue).toArray()
Collectors.groupingBy(f, Collectors.counting()) / Collectors.joining("-")
핫루프(DFS·BFS·이중 for 내부)에서는 Stream 대신 for
```

## 🧩 연습문제 힌트

- q1: `Arrays.stream(a).filter(x -> x % 2 == 0).map(x -> x * x).sum()`
- q2: `distinct()` → `boxed()` → `sorted(Comparator.reverseOrder())` → `mapToInt` → `toArray`
- q3: `Collectors.groupingBy(String::length, Collectors.counting())`
- q4: `filter` → `map(String::toUpperCase)` → `Collectors.joining("-")`
- q5: `average().orElse(0)`

## 🃏 복습 카드

- Q: int[]를 내림차순 int[]로 바꾸는 스트림 한 줄은?
  A: `Arrays.stream(a).boxed().sorted(Comparator.reverseOrder()).mapToInt(Integer::intValue).toArray()`
- Q: 단어 배열을 길이별 개수로 묶는 코드는?
  A: `Arrays.stream(w).collect(Collectors.groupingBy(String::length, Collectors.counting()))`
- Q: 코테에서 Stream을 피해야 하는 상황은?
  A: DFS/BFS 내부나 이중 루프 안처럼 수만~수백만 번 실행되는 곳 (생성 오버헤드로 시간 초과 위험)
- Q: `Arrays.stream(a).max()`의 반환 타입과 값을 꺼내는 방법은?
  A: OptionalInt. `getAsInt()`(비었으면 예외) 또는 `orElse(기본값)`
- Q: 람다 안에서 바깥 지역 변수 count++가 안 되는 이유와 우회법은?
  A: 람다는 effectively final인 지역 변수만 캡처 가능. `int[] cnt = {0}; cnt[0]++` 또는 필드 사용
