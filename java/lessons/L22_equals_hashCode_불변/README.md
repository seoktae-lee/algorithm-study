# L22. equals · hashCode · String Pool · 불변 객체

> ⏱ 25분 · 🎯 직접 만든 클래스를 HashSet/HashMap에 넣어도 **제대로 동작**하게 · 면접 단골 개념 정리
> 🔗 cote 연결: 좌표·상태를 Set으로 방문 체크하는 모든 BFS/시뮬레이션
> 💼 면접 단골: "equals를 재정의하면 왜 hashCode도 재정의해야 하나요?", "String은 왜 불변인가요?"

## 1. == vs equals

| | `==` | `equals` |
|---|---|---|
| 기본형 | 값 비교 | (없음) |
| 참조형 | **같은 객체(주소)인가** | **내용이 같은가** (클래스가 재정의했을 때) |

`Object.equals`의 기본 구현은 `==`와 같습니다. String, Integer, List, record 등은 내용 비교로 재정의돼 있어요.

## 2. String Pool

```java
String a = "java";             // 리터럴 → String Pool에 하나만 저장
String b = "java";             // 같은 객체 재사용
String c = new String("java"); // 힙에 새 객체
String d = "ja" + "va";        // 컴파일 타임 상수 → pool의 같은 객체
String e = "ja"; e += "va";    // 런타임 연결 → 새 객체
a == b  // true   a == c  // false   a == d  // true   a == e  // false
a.equals(c) && a.equals(e)  // true  → 그래서 항상 equals
```

## 3. HashSet/HashMap이 키를 찾는 방법

```
1) key.hashCode()로 버킷(칸) 위치 계산
2) 그 버킷 안에서 key.equals(기존 키)로 같은지 확인
```

→ **equals가 같으면 hashCode도 반드시 같아야** 한다 (계약). equals만 재정의하면 같은 내용인데 다른 버킷을 찾아가서 `contains`가 false.

```java
static class Pos {
    final int r, c;
    Pos(int r, int c) { this.r = r; this.c = c; }
    @Override public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Pos p)) return false;
        return r == p.r && c == p.c;
    }
    @Override public int hashCode() { return Objects.hash(r, c); }   // 또는 31 * r + c
}
```

> record는 이걸 자동으로 해 줌 (L17). 직접 구현이 필요한 건 record를 못 쓰거나 일부 필드만 비교하고 싶을 때.

## 4. 불변 객체 (String이 불변인 이유)

- **캐싱/Pool 가능**: 바뀌지 않으니 여러 변수가 같은 객체를 공유해도 안전
- **해시 키로 안전**: 키의 내용이 바뀌면 hashCode가 달라져 Map에서 못 찾게 됨
- **스레드 안전**: 동기화 없이 공유 가능
- 보안: 파일 경로·URL 등이 중간에 바뀌지 않음

불변 클래스 만들기: 필드 `private final`, setter 없음, 가변 필드는 방어적 복사.

## 🐍 파이썬이랑 다른 점

- 파이썬 `==` ≈ 자바 `equals`, 파이썬 `is` ≈ 자바 `==`
- 파이썬 `__eq__`/`__hash__` ≈ 자바 `equals`/`hashCode`

## ⚠️ 함정

1. `equals(Pos o)`로 오버로드(매개변수 타입이 Object가 아님) → 재정의가 아니라서 HashSet이 안 씀. `@Override`를 붙이면 컴파일러가 잡아 줌
2. hashCode 미구현 → contains/get이 랜덤하게 실패
3. Set에 넣은 뒤 객체 필드를 바꿈 → 영영 못 찾음

## 📌 핵심 요약 (치트시트)

```java
== : 주소(참조형) / equals : 내용 (재정의된 클래스)
String 리터럴은 Pool 공유, new String/런타임 연결은 새 객체 → equals
equals 재정의 ⇒ hashCode도 재정의 (같으면 같은 해시)
@Override public boolean equals(Object o) { … instanceof … }
@Override public int hashCode() { return Objects.hash(r, c); }
record = 자동 equals/hashCode
```

## 🧩 연습문제 힌트

- q1: `a.equals(b)` — null이 올 수 있으면 `Objects.equals(a, b)`
- q2: Pos 클래스에 위 equals/hashCode를 구현하면 HashSet 크기가 맞아짐 (countDistinct는 이미 완성돼 있음)
- q3: 전부 `toLowerCase()`해서 HashSet에

## 🃏 복습 카드

- Q: equals를 재정의하면 hashCode도 재정의해야 하는 이유는?
  A: HashSet/HashMap은 hashCode로 버킷을 찾은 뒤 equals로 비교. equals가 같아도 hashCode가 다르면 다른 버킷을 찾아 같은 키를 못 찾음
- Q: `"java" == new String("java")`와 `"java" == "ja" + "va"`의 결과는?
  A: false, true (후자는 컴파일 타임 상수라 Pool의 같은 객체)
- Q: String이 불변으로 설계된 이유 3가지는?
  A: String Pool 공유(캐싱), 해시 키 안전성, 스레드 안전성 (+ 보안)
- Q: `public boolean equals(Pos o)`로 작성하면 생기는 문제는?
  A: Object를 받는 equals를 재정의한 게 아니라 오버로드 → 컬렉션은 Object.equals(주소 비교)를 사용. @Override로 예방
- Q: 파이썬의 `==`와 `is`는 자바의 무엇과 대응되나?
  A: 파이썬 `==` ↔ 자바 `equals`, 파이썬 `is` ↔ 자바 `==`
