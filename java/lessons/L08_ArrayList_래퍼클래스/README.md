# L08. ArrayList · 래퍼 클래스(Integer)

> ⏱ 25분 · 🎯 크기를 모르는 결과는 ArrayList에 담고 **int[]로 변환**해서 반환 · `Integer ==` 함정 피하기
> 🔗 cote 연결 문제: 같은 숫자는 싫어, 두 개 뽑아서 더하기, 로또의 최고 순위와 최저 순위

## 1. 기본

```java
List<Integer> list = new ArrayList<>();   // 왼쪽은 인터페이스(List), 오른쪽은 구현체
list.add(3);            // 뒤에 추가 O(1)
list.add(0, 7);         // 0번 위치에 끼우기 O(n)
list.get(0);            // 7
list.set(0, 9);         // 0번 값을 9로
list.size();            // 개수 (length 아님)
list.contains(3);       // O(n) 선형 탐색! 많이 부르면 Set을 쓰기 (L10)
list.indexOf(3);        // 없으면 -1
list.isEmpty(); list.clear();
Collections.max(list); Collections.min(list); Collections.reverse(list);
Collections.frequency(list, 3);   // 3의 개수
```

## 2. 래퍼 클래스와 오토박싱

컬렉션에는 **객체만** 들어갑니다. `int` → `Integer`, `long` → `Long`, `char` → `Character`, `double` → `Double`, `boolean` → `Boolean`

```java
List<int> x;            // ❌ 컴파일 에러
list.add(5);            // 자동으로 Integer.valueOf(5) (오토박싱)
int v = list.get(0);    // 자동으로 .intValue() (언박싱) — null이면 NullPointerException!
```

### `Integer ==` 함정 ⚠️

```java
Integer a = 127, b = 127;   a == b  // true  (-128~127은 캐시된 같은 객체)
Integer c = 1000, d = 1000; c == d  // false (다른 객체!) → c.equals(d)
list.get(i) == list.get(j)          // 값이 128 이상이면 틀림 → equals 또는 int에 담아서 비교
```

## 3. remove 두 가지

```java
List<Integer> l = new ArrayList<>(List.of(10, 20, 30));
l.remove(1);                    // 인덱스 1 삭제 → [10, 30]
l.remove(Integer.valueOf(30));  // 값 30 삭제   → [10]
// 반복 중 삭제는 ConcurrentModificationException → removeIf
l.removeIf(x -> x % 2 == 0);
```

## 4. List ↔ 배열 변환 (매우 자주 씀)

```java
// List<Integer> → int[]
int[] arr = new int[list.size()];
for (int i = 0; i < arr.length; i++) arr[i] = list.get(i);
int[] arr2 = list.stream().mapToInt(Integer::intValue).toArray();   // 한 줄 (조금 느림)

// int[] → List<Integer>
List<Integer> l2 = new ArrayList<>();
for (int v : arr) l2.add(v);

List.of(1, 2, 3)          // 불변 리스트 (add하면 UnsupportedOperationException)
new ArrayList<>(List.of(1, 2, 3))   // 수정 가능한 복사본
```

## 🐍 파이썬이랑 다른 점

- 파이썬 `list` ≈ 자바 `ArrayList`. `a[i]` → `list.get(i)`, `len(a)` → `list.size()`, `a.append(x)` → `list.add(x)`
- 파이썬 `x in a` ≈ `list.contains(x)` — 둘 다 O(n)
- 파이썬엔 int/Integer 구분이 없지만 자바는 컬렉션에 Integer만 들어감

## ⚠️ 함정

1. `Integer` 끼리 `==` (128 이상에서 false)
2. `list.remove(3)`은 **인덱스 3** 삭제. 값 3을 지우려면 `remove(Integer.valueOf(3))`
3. for-each 안에서 `list.remove` → ConcurrentModificationException
4. `List.of`/`Arrays.asList` 결과에 add → 예외

## 📌 핵심 요약 (치트시트)

```java
List<Integer> list = new ArrayList<>();
add / get / set / size / contains(O(n)) / indexOf / remove(idx) / remove(Integer.valueOf(v))
list.removeIf(x -> 조건);  Collections.sort/max/min/reverse/frequency
int[] arr = list.stream().mapToInt(Integer::intValue).toArray();
Integer 비교는 equals (== 는 -128~127만 우연히 맞음)
```

## 🧩 연습문제 힌트

- q1: 리스트가 비었거나 마지막 값과 다를 때만 add → 마지막에 int[]로
- q2: `new int[list.size()]` 후 반복 대입
- q3: `a.equals(b)` (null 처리: `Objects.equals(a, b)`)
- q4: `List<Integer> r = new ArrayList<>(list); r.removeIf(x -> x % 2 == 0);`
- q5: 이중 for로 합을 만들고 `contains`로 중복 체크 → 정렬 → int[]

## 🃏 복습 카드

- Q: `Integer a = 1000, b = 1000; a == b`의 결과와 이유는?
  A: false. ==는 객체 주소 비교이고, -128~127만 캐시되어 같은 객체. 값 비교는 `a.equals(b)`
- Q: `List<Integer> list`에서 값 3을 삭제하는 코드는? `list.remove(3)`은?
  A: `list.remove(Integer.valueOf(3))`. `remove(3)`은 인덱스 3 삭제
- Q: `List<Integer>`를 `int[]`로 바꾸는 한 줄 코드는?
  A: `list.stream().mapToInt(Integer::intValue).toArray()`
- Q: for-each로 리스트를 돌면서 원소를 지우면? 대안은?
  A: ConcurrentModificationException. `list.removeIf(x -> 조건)` 또는 Iterator.remove
- Q: `List.of(1,2,3)`에 add하면?
  A: UnsupportedOperationException(불변 리스트). 수정하려면 `new ArrayList<>(List.of(...))`
