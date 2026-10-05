# L10. Set · TreeSet · TreeMap · LinkedHashMap

> ⏱ 25분 · 🎯 중복 제거는 HashSet, **정렬 유지·이하/이상 찾기**는 TreeSet/TreeMap, 넣은 순서는 Linked
> 🔗 cote 연결 문제: 전화번호 목록, 영어 끝말잇기, 연속 부분 수열 합의 개수, 이중우선순위큐

## 1. HashSet — 중복 없는 주머니 (평균 O(1))

```java
Set<String> set = new HashSet<>();
set.add("a");          // true (새로 들어감)
set.add("a");          // false (이미 있음) ← 중복 판별에 바로 사용
set.contains("a");     // O(1) — List.contains(O(n))와의 결정적 차이
set.remove("a"); set.size();
Set<Integer> s2 = new HashSet<>(List.of(1, 2, 3));
s2.retainAll(other);   // 교집합 (s2가 바뀜)
s2.addAll(other);      // 합집합
s2.removeAll(other);   // 차집합
```

## 2. TreeSet — 항상 정렬된 Set (O(log n))

```java
TreeSet<Integer> ts = new TreeSet<>(List.of(5, 1, 9, 3));
ts.first(); ts.last();     // 1, 9
ts.floor(4);               // 3   4 이하 중 최대 (없으면 null)
ts.ceiling(4);             // 5   4 이상 중 최소
ts.lower(3); ts.higher(3); // 1, 5  (미만/초과)
ts.pollFirst(); ts.pollLast();   // 꺼내면서 삭제
new TreeSet<>(Collections.reverseOrder());   // 내림차순
```

## 3. TreeMap — 키가 정렬된 Map

```java
TreeMap<Integer, Integer> tm = new TreeMap<>();
tm.firstKey(); tm.lastKey(); tm.floorKey(k); tm.ceilingKey(k);
tm.pollFirstEntry();       // 최소 키 꺼내기
for (int k : tm.keySet())  // 키 오름차순 순회 보장
// 같은 값이 여러 개인 "정렬된 멀티셋" = TreeMap<값, 개수>  (이중우선순위큐에 딱)
```

## 4. LinkedHashMap / LinkedHashSet — 넣은 순서 유지

```java
Map<Character, Integer> m = new LinkedHashMap<>();   // 순회 순서 = 삽입 순서
```

| 필요한 것 | 선택 |
|---|---|
| 중복 제거 / 빠른 존재 확인 | HashSet |
| 정렬 순서 / 이하·이상 찾기 | TreeSet, TreeMap |
| 넣은 순서대로 | LinkedHashSet, LinkedHashMap |

## 🐍 파이썬이랑 다른 점

- 파이썬 `set` ≈ HashSet. 파이썬엔 TreeSet이 기본에 없음(sortedcontainers) → 자바의 강점
- 파이썬 3.7+ dict는 삽입 순서 유지 ≈ LinkedHashMap (HashMap은 순서 X)

## ⚠️ 함정

1. `floor/ceiling`이 없으면 **null** → `int x = ts.floor(v);`는 NPE 위험 → `Integer`로 받아 null 체크
2. HashSet 순회 순서를 믿고 답을 내면 틀림
3. 리스트에서 반복적으로 `contains` → O(n²) 시간 초과의 단골 원인

## 📌 핵심 요약 (치트시트)

```java
Set<T> s = new HashSet<>(); s.add(x)(중복이면 false) / contains O(1)
TreeSet: first/last/floor(≤)/ceiling(≥)/lower(<)/higher(>)/pollFirst  — 없으면 null
TreeMap: firstKey/lastKey/floorKey/ceilingKey/pollFirstEntry, 키 정렬 순회
LinkedHashMap/Set: 삽입 순서 유지
교집합 retainAll / 합집합 addAll / 차집합 removeAll
```

## 🧩 연습문제 힌트

- q1: `new TreeSet<>()`에 모두 add → 순서대로 배열에
- q2: 모든 번호를 HashSet에 → 각 번호의 접두어 `substring(0, i)`가 set에 있으면 false
- q3: 사용한 단어 Set, 이전 단어의 마지막 글자 = 현재 첫 글자 확인. 탈락자 번호 = i % n + 1, 차례 = i / n + 1
- q4: TreeSet `floor(x)` → null이면 -1
- q5: LinkedHashMap으로 개수 → 순회하며 1인 첫 키

## 🃏 복습 카드

- Q: HashSet의 `add`가 반환하는 값과 그 활용은?
  A: 새로 추가되면 true, 이미 있으면 false → 중복 판별을 한 줄로
- Q: TreeSet에서 x 이하 중 최댓값, x 이상 중 최솟값을 구하는 메서드는? 없으면?
  A: `floor(x)`, `ceiling(x)`. 없으면 null
- Q: List.contains와 HashSet.contains의 시간복잡도는?
  A: List O(n), HashSet 평균 O(1)
- Q: 삽입 순서를 유지하는 Map과, 키를 정렬 상태로 유지하는 Map은?
  A: LinkedHashMap, TreeMap
- Q: 같은 값이 여러 번 들어갈 수 있는 "정렬된 집합"을 자바로 흉내 내려면?
  A: `TreeMap<값, 개수>` — 넣을 때 merge(+1), 뺄 때 -1 후 0이면 remove
