# L23. 컬렉션 프레임워크 구조 · 시간복잡도 · 제네릭

> ⏱ 30분 · 🎯 문제 조건(n의 크기)을 보고 **허용 복잡도와 자료구조를 즉시 고르기**
> 🔗 cote 연결: 모든 문제의 "입력 크기 → 풀이 선택" 단계, 시간 초과 디버깅
> 💼 면접 단골: "ArrayList와 LinkedList 차이", "HashMap 동작 원리", "제네릭을 쓰는 이유"

## 1. 지도 한 장

```
Collection
├── List   (순서 O, 중복 O)   ArrayList · LinkedList
├── Set    (중복 X)           HashSet · LinkedHashSet · TreeSet
└── Queue / Deque             ArrayDeque · PriorityQueue · LinkedList
Map (키-값, Collection 아님)  HashMap · LinkedHashMap · TreeMap
```

선언은 인터페이스 타입으로: `List<Integer> list = new ArrayList<>();` → 나중에 구현체만 바꾸면 됨

## 2. 시간복잡도 표 (외우기)

| 연산 | ArrayList | LinkedList | HashSet/Map | TreeSet/Map | ArrayDeque | PriorityQueue |
|---|---|---|---|---|---|---|
| 끝에 추가 | O(1)* | O(1) | O(1) | O(log n) | O(1) | O(log n) |
| 앞에 추가/삭제 | **O(n)** | O(1) | - | - | O(1) | - |
| 인덱스 접근 get(i) | O(1) | **O(n)** | - | - | - | - |
| contains | **O(n)** | O(n) | **O(1)** | O(log n) | O(n) | O(n) |
| 최소/최대 | O(n) | O(n) | O(n) | O(log n) | - | O(1) peek |

\* 배열이 꽉 차면 1.5배로 늘리며 복사 → 평균 O(1)

- `list.remove(0)`을 반복 = O(n²) → 큐가 필요하면 ArrayDeque
- `list.contains`를 반복 = O(n²) → HashSet

## 3. 입력 크기 → 허용 복잡도 (1초 ≈ 10^8 단순 연산)

| n | 허용 | 대표 풀이 |
|---|---|---|
| ≤ 11 | O(n!) | 순열 완전탐색 |
| ≤ 20 | O(2^n) | 부분집합·비트마스크 |
| ≤ 500 | O(n³) | 3중 for, 플로이드 |
| ≤ 5,000 | O(n²) | 2중 for, 간단 DP |
| ≤ 1,000,000 | O(n log n) | 정렬, 힙, 이분탐색 |
| 그 이상 | O(n) / O(log n) | 투 포인터, 해시, 수학 |

## 4. HashMap 동작 원리 (면접 한 문단)

키의 `hashCode()`로 버킷 배열의 인덱스를 정하고, 같은 버킷에 여러 키가 오면(충돌) 연결 리스트로 잇되 한 버킷에 8개를 넘으면 레드-블랙 트리로 바꿔 최악 O(log n)을 보장한다. 원소 수가 용량 × 0.75(load factor)를 넘으면 배열을 2배로 늘리고 재배치(rehash)한다. 같은 키 판별은 hashCode → equals 순서.

## 5. 제네릭

```java
List<String> names = new ArrayList<>();   // <> 다이아몬드: 오른쪽 타입 생략
// 장점: 컴파일 타임 타입 체크 + 꺼낼 때 캐스팅 불필요
// 기본형 불가: List<int> ❌ → List<Integer> (박싱 비용 → 대량이면 int[]가 빠름)

static <T extends Comparable<T>> T maxOf(List<T> list) {   // 제네릭 메서드
    T best = list.get(0);
    for (T x : list) if (x.compareTo(best) > 0) best = x;
    return best;
}
```

## 🐍 파이썬이랑 다른 점

- 파이썬 list ≈ ArrayList (`pop(0)`도 O(n)), `in` 연산 list O(n) / set O(1) — 원리 동일
- 파이썬은 타입이 런타임에 정해지지만 자바 제네릭은 컴파일 타임 체크 (런타임엔 지워짐 = 타입 소거)

## ⚠️ 함정

1. ArrayList를 큐처럼 `remove(0)` 
2. 반복문 안 `list.contains` / `list.indexOf`
3. n = 10^5인데 O(n²) 풀이 → 10^10 연산 → 시간 초과 확정

## 📌 핵심 요약 (치트시트)

```
n ≤ 11 n! / ≤ 20 2^n / ≤ 500 n³ / ≤ 5천 n² / ≤ 100만 n log n / 그 이상 n
ArrayList get O(1), 앞 삽입·삭제·contains O(n)
HashSet/Map O(1) · TreeSet/Map O(log n) · PQ offer/poll O(log n) · ArrayDeque 양끝 O(1)
List<Integer> list = new ArrayList<>();   (인터페이스 타입으로 선언)
<T extends Comparable<T>> T f(List<T> l)
```

## 🧩 연습문제 힌트

- q1: `T best = list.get(0); for (T x : list) if (x.compareTo(best) > 0) best = x;`
- q2: b를 HashSet으로 만들고, a의 원소 중 set에 있는 것을 또 다른 HashSet에 담아 크기 (List.contains로 하면 20초 제한에 걸림)
- q3: 위 표의 경계값 그대로 if 문

## 🃏 복습 카드

- Q: ArrayList와 LinkedList의 get(i), 맨 앞 삽입 시간복잡도는?
  A: ArrayList get O(1)·앞 삽입 O(n), LinkedList get O(n)·앞 삽입 O(1). 코테에선 거의 ArrayList + ArrayDeque
- Q: n ≤ 100,000일 때 허용되는 대략적인 시간복잡도와 대표 풀이는?
  A: O(n log n) 이하 — 정렬, 힙, 이분탐색, 해시
- Q: HashMap의 동작 원리를 한 문장으로?
  A: hashCode로 버킷을 정하고 equals로 같은 키를 찾음. 충돌은 리스트(8개 초과 시 트리)로 처리, 0.75 넘으면 2배 확장
- Q: 제네릭의 장점 2가지와 제약 1가지는?
  A: 컴파일 타임 타입 체크, 캐스팅 불필요 / 기본형 사용 불가(Integer 등 래퍼 필요)
- Q: `List<Integer> list = new ArrayList<>()`처럼 인터페이스 타입으로 선언하는 이유는?
  A: 구현체를 바꿔도 나머지 코드를 그대로 쓸 수 있음(유연성, 다형성)
