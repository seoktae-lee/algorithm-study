# L17. 클래스 · record로 상태 묶기

> ⏱ 25분 · 🎯 좌표·노드·학생처럼 **여러 값을 하나로 묶고**, HashSet/HashMap 키로 안전하게 쓰기
> 🔗 cote 연결 문제: 방문 길이, 게임 맵 최단거리, 베스트앨범, 거리두기 확인하기, 주차 요금 계산

## 1. 왜 필요한가

`int[]{r, c}`도 묶음이지만 **HashSet/HashMap 키로 쓰면 깨집니다** — 배열은 내용이 아니라 주소로 비교되기 때문.

```java
Set<int[]> set = new HashSet<>();
set.add(new int[]{1, 2});
set.contains(new int[]{1, 2});   // false!! (다른 배열 객체)
```

## 2. record (Java 16+) — 값 묶음 한 줄

```java
record Point(int r, int c) {}          // 생성자·getter·equals·hashCode·toString 자동

Point p = new Point(1, 2);
p.r(); p.c();                          // getter는 필드 이름 그대로 (getR 아님)
Set<Point> visited = new HashSet<>();
visited.add(new Point(1, 2));
visited.contains(new Point(1, 2));     // true ✅ 내용으로 비교
```

> 프로그래머스 Java 버전이 낮아 record가 안 될 때를 대비해 아래 클래스 방식이나 **문자열/정수 키**도 알아 두기:
> `r + "," + c` 또는 `r * W + c` (W = 열 수)

## 3. static 중첩 클래스 (record가 안 될 때 / 값이 바뀌어야 할 때)

```java
class Solution {
    static class Node {
        int r, c, dist;
        Node(int r, int c, int dist) { this.r = r; this.c = c; this.dist = dist; }
    }
    public int solution(int[][] maps) {
        Queue<Node> q = new ArrayDeque<>();
        q.offer(new Node(0, 0, 1));
        ...
    }
}
```

- `static`을 붙이면 바깥 Solution 객체 없이 만들 수 있음 (보통 static으로)
- 이 클래스를 Set/Map 키로 쓰려면 `equals`와 `hashCode`를 직접 구현해야 함 (L22)

## 4. Comparable로 기본 정렬 순서 심기

```java
record Student(String name, int score) implements Comparable<Student> {
    public int compareTo(Student o) {
        if (score != o.score) return Integer.compare(o.score, score);   // 점수 내림차순
        return name.compareTo(o.name);                                  // 이름 오름차순
    }
}
List<Student> list = ...; Collections.sort(list);
```

## 🐍 파이썬이랑 다른 점

- 파이썬 튜플 `(r, c)`는 바로 set/dict 키가 되지만 자바 배열은 안 됨 → record
- 파이썬 `@dataclass(frozen=True)` ≈ 자바 record (불변, equals/hash 자동)

## ⚠️ 함정

1. `int[]`/`List`를 키로 쓰고 contains가 안 맞는다고 헤매기 (List는 내용 비교가 되지만 넣은 뒤 바꾸면 깨짐)
2. 직접 만든 클래스를 키로 쓰면서 equals/hashCode 미구현
3. record 필드는 final → 값 변경 불가 (새로 만들기)

## 📌 핵심 요약 (치트시트)

```java
record Point(int r, int c) {}   // equals/hashCode 자동 → Set<Point>, Map<Point, V> OK
p.r()  p.c()
static class Node { int r, c, d; Node(int r, int c, int d) {...} }   // BFS 큐 원소
대안 키: r + "," + c  /  r * W + c
record X(...) implements Comparable<X> { public int compareTo(X o) {...} }
```

## 🧩 연습문제 힌트

- q1: `record P(int x, int y)`를 메서드 밖(클래스 안)에 선언하고 HashSet에 add → size
- q2: 이동 전 (x,y), 이동 후 (nx,ny). 길은 방향이 없으니 두 점을 정렬해서(작은 점 먼저) record로 저장. 경계(-5~5) 밖이면 무시
- q3: `record Student(String name, int score) implements Comparable<Student>` → 정렬 후 이름만

## 🃏 복습 카드

- Q: `Set<int[]>`에 {1,2}를 넣고 `contains(new int[]{1,2})`가 false인 이유는?
  A: 배열은 equals/hashCode가 주소 기반이라 내용이 같아도 다른 객체로 취급
- Q: 좌표를 HashSet 키로 쓰는 방법 3가지는?
  A: ① `record Point(int r, int c)` ② 문자열 키 `r + "," + c` ③ 정수 키 `r * W + c`
- Q: record가 자동으로 만들어 주는 것들은?
  A: 생성자, 필드 이름과 같은 getter(p.r()), equals, hashCode, toString (필드는 final)
- Q: 중첩 클래스에 static을 붙이는 이유는?
  A: 바깥 클래스(Solution) 인스턴스 없이 생성 가능하고, 불필요한 바깥 참조를 갖지 않음
- Q: '방문 길이'에서 같은 길을 반대로 지나간 경우를 하나로 세는 방법은?
  A: 간선의 두 끝점을 정렬(작은 점 먼저)해서 저장하거나, 양방향을 모두 Set에 넣고 size/2
