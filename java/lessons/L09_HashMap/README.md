# L09. HashMap

> ⏱ 30분 · 🎯 **개수 세기·그룹 묶기·빠른 조회**를 HashMap 한두 줄로
> 🔗 cote 연결 문제: 완주하지 못한 선수, 폰켓몬, 의상, 신고 결과 받기, 성격 유형 검사하기, 베스트앨범

## 1. 기본 (평균 O(1))

```java
Map<String, Integer> map = new HashMap<>();
map.put("leo", 1);               // 넣기/덮어쓰기
map.get("leo");                  // 1, 없으면 null ⚠️
map.getOrDefault("kim", 0);      // 없으면 기본값 ← 가장 많이 씀
map.containsKey("leo");          // 있나?
map.remove("leo");
map.size(); map.isEmpty();
map.putIfAbsent("a", 0);         // 없을 때만 넣기
```

## 2. 3대 패턴

```java
// ① 개수 세기
for (String s : arr) map.put(s, map.getOrDefault(s, 0) + 1);
for (String s : arr) map.merge(s, 1, Integer::sum);      // 같은 의미, 더 짧게

// ② 그룹 묶기 (키 → 리스트)
Map<String, List<String>> group = new HashMap<>();
group.computeIfAbsent(type, k -> new ArrayList<>()).add(name);

// ③ 값 → 인덱스 빠른 조회
Map<String, Integer> idx = new HashMap<>();
for (int i = 0; i < ids.length; i++) idx.put(ids[i], i);
```

## 3. 순회

```java
for (String k : map.keySet()) { ... }
for (int v : map.values()) { ... }
for (Map.Entry<String, Integer> e : map.entrySet()) {
    String k = e.getKey(); int v = e.getValue();
}
// ⚠️ HashMap은 순서 보장 X → 정렬된 순서가 필요하면 TreeMap, 넣은 순서면 LinkedHashMap (L10)
// 값 기준 정렬: List<Map.Entry<..>> list = new ArrayList<>(map.entrySet()); list.sort(Map.Entry.comparingByValue());
```

## 🐍 파이썬이랑 다른 점

- `d[k]` → `map.get(k)` (없으면 KeyError 대신 **null**), `d.get(k, 0)` → `getOrDefault(k, 0)`
- `Counter(arr)` → `merge(x, 1, Integer::sum)` 반복
- `defaultdict(list)` → `computeIfAbsent(k, x -> new ArrayList<>())`

## ⚠️ 함정

1. `int v = map.get(k);` — 키가 없으면 null 언박싱 → **NullPointerException**
2. `map.get(k) == map.get(j)` — Integer 비교 함정(L08). `equals` 사용
3. `int[]`나 배열을 키로 쓰면 내용이 같아도 다른 키 (L17에서 record로 해결)

## 📌 핵심 요약 (치트시트)

```java
Map<K, V> m = new HashMap<>();
m.put(k, v) / m.get(k)(없으면 null) / m.getOrDefault(k, 0) / m.containsKey(k)
m.merge(k, 1, Integer::sum);                         // 카운팅
m.computeIfAbsent(k, x -> new ArrayList<>()).add(v); // 그룹핑
for (Map.Entry<K, V> e : m.entrySet()) e.getKey(), e.getValue()
```

## 🧩 연습문제 힌트

- q1: 참가자는 +1, 완주자는 -1 → 값이 0이 아닌 키
- q2: 종류 수 = `map.size()` (또는 Set) → `Math.min(종류 수, n / 2)`
- q3: 종류별 개수 → (각 개수+1)을 모두 곱하고 -1 (아무것도 안 입는 경우 제외)
- q4: `Map<String, Set<String>> reported` (신고당한 사람 → 신고한 사람들, Set으로 중복 제거) → k명 이상이면 신고자들 메일 +1
- q5: 개수 세고, 최대 개수인 단어 중 `compareTo`가 가장 작은 것

## 🃏 복습 카드

- Q: HashMap으로 문자열 배열의 등장 횟수를 세는 한 줄(루프 안) 코드 두 가지는?
  A: `map.put(s, map.getOrDefault(s, 0) + 1);` 또는 `map.merge(s, 1, Integer::sum);`
- Q: `int v = map.get("x");`에서 키가 없으면?
  A: get이 null을 반환 → 언박싱하다 NullPointerException. getOrDefault 사용
- Q: 키별로 리스트에 모으는(그룹핑) 코드는?
  A: `map.computeIfAbsent(key, k -> new ArrayList<>()).add(value);`
- Q: Map의 키와 값을 함께 순회하는 코드는?
  A: `for (Map.Entry<K, V> e : map.entrySet()) { e.getKey(); e.getValue(); }`
- Q: '의상' 문제에서 조합 수를 구하는 공식은?
  A: 종류별 (개수 + 1)을 모두 곱한 뒤 1을 뺀다 (각 종류를 안 입는 경우 포함, 전부 안 입는 경우 제외)
