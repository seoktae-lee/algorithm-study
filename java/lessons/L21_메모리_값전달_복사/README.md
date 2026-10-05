# L21. 메모리 · 값 전달 · 얕은/깊은 복사

> ⏱ 25분 · 🎯 "메서드에서 배열을 바꿨더니 원본도 바뀌었다 / 결과 리스트가 전부 같은 값이다" 버그를 원리로 이해
> 🔗 cote 연결 문제: 크레인 인형뽑기(board 수정), 자물쇠와 열쇠(회전 복사), 백트래킹 결과 저장, 프렌즈4블록
> 💼 면접 단골: "Java는 Call by Value인가 Reference인가?"

## 1. 기본형 vs 참조형

```
스택(지역 변수)              힙(객체)
┌──────────────┐
│ int x = 5    │  값 자체
│ int[] a ─────┼──────▶ [1, 2, 3]
│ int[] b ─────┼──────▶ (같은 배열)   ← int[] b = a;
└──────────────┘
```

- 기본형(int, long, double, char, boolean…): 변수에 **값**이 들어 있음
- 참조형(배열, String, 객체, 컬렉션): 변수에 **객체의 주소**가 들어 있음

## 2. 자바는 항상 Call by Value (주소값을 복사해서 넘김)

```java
void change(int x) { x = 100; }               // 호출한 쪽 변수 그대로
void fill(int[] arr) { arr[0] = 100; }         // 같은 배열을 가리키므로 원본이 바뀜
void reassign(int[] arr) { arr = new int[3]; } // 매개변수가 다른 배열을 가리킬 뿐, 원본 그대로
```

> 정답 문장: "자바는 Call by Value다. 참조형은 **참조(주소)값이 복사**되어 전달되므로 메서드 안에서 객체 내용을 바꾸면 원본에 반영되지만, 매개변수에 새 객체를 대입해도 원본 변수는 바뀌지 않는다."

## 3. 얕은 복사 vs 깊은 복사

```java
int[] a = {1, 2, 3};
int[] b = a.clone();            // 1차원: 이걸로 충분 (원소가 기본형)

int[][] g = {{1, 2}, {3, 4}};
int[][] shallow = g.clone();    // ⚠️ 행 배열의 "주소"만 복사 → shallow[0][0] = 9 하면 g도 바뀜
int[][] deep = new int[g.length][];
for (int i = 0; i < g.length; i++) deep[i] = g[i].clone();   // 행마다 복사 = 깊은 복사

List<Integer> copy = new ArrayList<>(list);   // 리스트 복사 (원소가 불변 객체면 충분)
```

## 4. 백트래킹 결과 저장 버그 ⭐

```java
List<List<Integer>> result = new ArrayList<>();
List<Integer> cur = new ArrayList<>();
void dfs(...) {
    result.add(cur);                    // ❌ 같은 리스트 객체를 계속 넣음 → 끝나면 전부 빈 리스트
    result.add(new ArrayList<>(cur));   // ✅ 그 순간의 스냅숏을 복사해서 저장
}
```

## 5. 불변 객체

- String, Integer 등 래퍼 클래스는 불변 → "바꾸는" 메서드는 항상 새 객체를 반환
- `final int[] a`는 a가 다른 배열을 못 가리킬 뿐, `a[0] = 5`는 가능 (final ≠ 불변)

## 🐍 파이썬이랑 다른 점

- 파이썬도 같은 원리(객체 참조 전달). `b = a`가 복사가 아닌 것도 같음
- `copy.deepcopy` 같은 범용 함수가 없음 → 직접 행 단위로 복사

## ⚠️ 함정

1. 2차원 배열 `clone()`/`Arrays.copyOf`를 깊은 복사로 착각
2. 결과 리스트에 현재 리스트/배열을 그대로 add
3. 시뮬레이션에서 "원본 board를 보존해야 하는데" 직접 수정

## 📌 핵심 요약 (치트시트)

```java
자바 = Call by Value (참조형은 주소값 복사) → 내용 수정은 원본 반영, 재대입은 반영 X
int[] b = a.clone();                           // 1차원 복사
for (i) deep[i] = g[i].clone();                // 2차원 깊은 복사
result.add(new ArrayList<>(cur));              // 백트래킹 스냅숏
final 참조 ≠ 불변 객체
```

## 🧩 연습문제 힌트

- q1: `int[][] d = new int[a.length][]; for (i) d[i] = a[i].clone();`
- q2: 반환 없이 `a[i]++` — 원본이 바뀌는 걸 확인하는 문제
- q3: `new int[n]`에 `r[i] = a[(i + k) % n]` — 원본은 건드리지 않기
- q4: DFS 진입 시 `result.add(new ArrayList<>(cur))`, `for (i = start…) { cur.add(nums[i]); dfs(i + 1); cur.remove(cur.size() - 1); }`

## 🃏 복습 카드

- Q: "자바는 Call by Value인가 Reference인가?"에 대한 정확한 답은?
  A: Call by Value. 참조형은 참조(주소)값이 복사되어 전달되므로 객체 내용 변경은 원본에 반영되지만, 매개변수 재대입은 원본에 영향 없음
- Q: `int[][] c = g.clone();` 후 `c[0][0] = 9`를 하면 g는?
  A: g[0][0]도 9. 2차원 clone은 행 배열 주소만 복사하는 얕은 복사
- Q: 2차원 배열을 깊은 복사하는 코드는?
  A: `int[][] d = new int[g.length][]; for (int i = 0; i < g.length; i++) d[i] = g[i].clone();`
- Q: 백트래킹에서 `result.add(cur)` 했더니 결과가 전부 같은(빈) 리스트인 이유와 해결은?
  A: 같은 리스트 객체를 여러 번 넣었고 이후 계속 수정됨. `result.add(new ArrayList<>(cur))`
- Q: `final int[] a = {1,2};` 이후 `a[0] = 5;`와 `a = new int[3];`은?
  A: 앞은 가능(내용 변경), 뒤는 컴파일 에러(재대입 불가). final은 참조 고정이지 불변이 아님
