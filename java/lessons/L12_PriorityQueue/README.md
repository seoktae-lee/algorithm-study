# L12. PriorityQueue (힙)

> ⏱ 25분 · 🎯 "매번 가장 작은/큰 것을 꺼내기"를 O(log n)으로 · 최대 힙·객체 정렬 기준 자유롭게
> 🔗 cote 연결 문제: 더 맵게, 디스크 컨트롤러, 이중우선순위큐, 야근 지수, 디펜스 게임

## 1. 기본 = 최소 힙

```java
PriorityQueue<Integer> pq = new PriorityQueue<>();
pq.offer(5); pq.offer(1); pq.offer(3);   // O(log n)
pq.peek();      // 1  가장 작은 값 보기 O(1) (비면 null)
pq.poll();      // 1  꺼내기 O(log n)     (비면 null)
pq.size(); pq.isEmpty();
new PriorityQueue<>(list);   // 리스트로 한 번에 만들기 O(n)
```

## 2. 최대 힙 / 사용자 기준

```java
PriorityQueue<Integer> maxPq = new PriorityQueue<>(Collections.reverseOrder());
PriorityQueue<Integer> maxPq2 = new PriorityQueue<>((a, b) -> Integer.compare(b, a));

// int[] 원소: [요청시각, 소요시간] → 소요시간 짧은 순, 같으면 요청 빠른 순
PriorityQueue<int[]> jobs = new PriorityQueue<>((x, y) -> x[1] != y[1] ? Integer.compare(x[1], y[1]) : Integer.compare(x[0], y[0]));
```

## 3. 대표 패턴

```java
// ① 가장 작은 두 개 꺼내 섞기 (더 맵게)
while (pq.size() >= 2 && pq.peek() < K) { int a = pq.poll(), b = pq.poll(); pq.offer(a + b * 2); }

// ② 상위 K개: 크기 K인 "최소" 힙 유지 → 넘치면 가장 작은 것 버림 → O(n log K)
for (int v : nums) { pq.offer(v); if (pq.size() > k) pq.poll(); }

// ③ 시간 시뮬레이션 (디스크 컨트롤러): 요청 시각 순으로 정렬해 두고,
//    현재 시각까지 도착한 작업만 PQ에 넣고, PQ에서 가장 짧은 작업을 처리
```

## 4. 주의: 순회 순서 ≠ 정렬 순서

```java
for (int v : pq) ...          // 내부 배열 순서(힙 구조) — 정렬 안 되어 있음!
System.out.println(pq);       // [1, 5, 3] 처럼 보일 수 있음
// 정렬 순서로 보려면 poll을 반복
```

## 🐍 파이썬이랑 다른 점

- 파이썬 `heapq`는 리스트 + 함수, 최소 힙만 → 최대 힙은 `-x` 트릭. 자바는 Comparator로 바로 최대 힙
- `heappush/heappop` → `offer/poll`, `heap[0]` → `peek()`

## ⚠️ 함정

1. `(a, b) -> b - a` 오버플로 → `Integer.compare(b, a)` 또는 `Collections.reverseOrder()`
2. PQ를 for-each로 돌며 "정렬된 결과"라고 믿기
3. 이중우선순위큐처럼 최소·최대를 둘 다 지워야 하면 PQ 2개보다 `TreeMap<값, 개수>`가 깔끔

## 📌 핵심 요약 (치트시트)

```java
PriorityQueue<Integer> min = new PriorityQueue<>();
PriorityQueue<Integer> max = new PriorityQueue<>(Collections.reverseOrder());
PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> Integer.compare(a[1], b[1]));
offer / poll / peek  O(log n) / O(log n) / O(1)
Top-K: 크기 K 최소 힙 · 순회 순서는 정렬 아님
```

## 🧩 연습문제 힌트

- q1: 위 패턴 ① 후 `pq.peek() >= K`면 횟수, 아니면 -1
- q2: 패턴 ② 후 poll 하면 작은 것부터 나오니 뒤에서부터 채우기
- q3: `TreeMap<Integer, Integer>` 개수 관리. "D 1"은 lastKey, "D -1"은 firstKey. 비었으면 [0,0]
- q4: 최대 힙에서 두 개 꺼내 차이가 0이 아니면 다시 넣기. 남으면 그 값, 없으면 0
- q5: jobs를 요청 시각 순 정렬 → time, idx 관리. PQ가 비었으면 다음 작업 요청 시각으로 time 점프

## 🃏 복습 카드

- Q: 자바 PriorityQueue의 기본 순서와 최대 힙 만드는 코드는?
  A: 최소 힙. `new PriorityQueue<>(Collections.reverseOrder())`
- Q: PriorityQueue의 offer/poll/peek 시간복잡도는?
  A: O(log n) / O(log n) / O(1)
- Q: 배열 n개 중 상위 K개를 효율적으로 구하는 방법은?
  A: 크기 K짜리 최소 힙 유지(넘치면 poll) → O(n log K)
- Q: PriorityQueue를 for-each로 출력하면 정렬된 순서인가?
  A: 아니다. 내부 힙 배열 순서. 정렬 순서는 poll을 반복해야 얻음
- Q: int[] {요청시각, 소요시간}을 소요시간 오름차순으로 꺼내는 PQ 선언은?
  A: `new PriorityQueue<int[]>((a, b) -> Integer.compare(a[1], b[1]))`
