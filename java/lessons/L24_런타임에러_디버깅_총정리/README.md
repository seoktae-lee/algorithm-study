# L24. 런타임 에러 · 시간 초과 · 디버깅 총정리 (버그 고치기)

> ⏱ 30분 · 🎯 "런타임 에러/시간 초과/틀렸습니다"를 보면 **원인 후보를 바로 떠올리고** 고치기
> 🔗 cote 연결: 모든 문제의 제출 전 점검, 💡/❌ 문제 재풀이
> 💼 면접 단골: "Checked와 Unchecked 예외의 차이"

## 1. 자주 만나는 예외와 원인

| 예외 | 흔한 원인 | 처방 |
|---|---|---|
| `ArrayIndexOutOfBoundsException` | `i <= n`, `i + 1` 접근, 빈 배열 `arr[0]` | 경계 조건, 빈 입력 체크 |
| `NullPointerException` | `map.get(k)` 언박싱, 초기화 안 한 배열/객체 | `getOrDefault`, 초기화 |
| `NumberFormatException` | `parseInt("")`, 공백 포함, int 범위 초과 | `trim()`, `Long.parseLong` |
| `ArithmeticException: / by zero` | 0으로 나누기·나머지 | 분모 0 체크 |
| `StackOverflowError` | 종료 조건 없는 재귀, 깊이 10^5 재귀 | 종료 조건, 반복문/스택 |
| `ConcurrentModificationException` | for-each 중 remove/add | `removeIf`, Iterator, 새 리스트 |
| `OutOfMemoryError` | `new int[100000][100000]`, BFS 중복 방문 | 크기 계산, 넣을 때 방문 표시 |
| `ClassCastException` | 잘못된 캐스팅 | 제네릭 타입 확인 |

## 2. 에러 없이 틀리는 것들 (가장 무서움)

- **int 오버플로**: 합·곱이 21억 넘음 → long
- **정수 나눗셈**: `a / b`에서 소수점 버려짐
- **문자열 ==**, **Integer ==** (128 이상)
- **얕은 복사**로 원본 오염
- 정렬 기준 동점 처리 누락

## 3. 시간 초과 원인 체크리스트

1. 입력 크기 대비 복잡도 (L23 표) — 진짜 원인의 대부분
2. 반복문 안의 `String +=`, `list.contains`, `list.remove(0)`
3. BFS에서 꺼낼 때 방문 표시
4. 메모 없는 재귀 (같은 계산 반복)
5. 핫루프 안의 Stream, Scanner/println 대량 입출력

## 4. 디버깅 방법 (프로그래머스)

```java
System.out.println("i=" + i + " sum=" + sum);   // 출력은 채점에 영향 없음(제출 전 삭제 권장)
System.out.println(Arrays.toString(arr));
System.out.println(Arrays.deepToString(grid));
```

**제출 전 엣지 케이스**: 빈 배열/문자열, 원소 1개, 전부 같은 값, 최댓값 입력, 음수, 정답이 0/없음(-1)

## 5. 예외 기초 (면접)

```java
try {
    int x = Integer.parseInt(s);
} catch (NumberFormatException e) {
    // 처리
} finally {
    // 항상 실행
}
```

- **Checked 예외** (IOException 등): 컴파일러가 처리 강제 → try-catch 또는 `throws`
- **Unchecked 예외** (RuntimeException 하위: NPE, IndexOutOfBounds…): 강제 없음, 대부분 코드 버그
- Error (StackOverflowError, OutOfMemoryError): 복구 대상 아님

## 🐍 파이썬이랑 다른 점

- 파이썬 IndexError/KeyError ≈ 자바 IndexOutOfBounds/(get은 null 반환 → NPE)
- 파이썬엔 오버플로가 없어서 자바로 옮길 때 가장 많이 틀리는 지점

## ⚠️ 함정

1. 예외를 try-catch로 삼켜서 숨기기 → 원인 파악이 늦어짐
2. 로컬에서 예제만 통과하고 엣지 케이스 미검증

## 📌 핵심 요약 (치트시트)

```
AIOOBE: 경계(i <= n, i+1) / NPE: map.get 언박싱 / NFE: parseInt 공백·범위
CME: for-each 중 수정 → removeIf / SOE: 재귀 종료·깊이
조용한 오답: 오버플로 · 정수 나눗셈 · ==비교 · 얕은 복사
TLE: 복잡도 → String+= → list.contains/remove(0) → BFS 방문 시점 → 메모 없는 재귀
엣지: 빈 입력 · 1개 · 같은 값 · 최대 · 음수 · 답 없음
Checked(컴파일 강제: IOException) vs Unchecked(RuntimeException)
```

## 🧩 연습문제 힌트

이번 연습문제는 **이미 작성된 코드에 버그가 있어요.** 실행해서 어떤 예외/오답이 나는지 보고 고치세요.

- q1: 없는 키 → `getOrDefault`
- q2: 반복 범위 `i < a.length - 1`
- q3: 누적 변수를 long으로
- q4: `String +=` → StringBuilder (20초 제한)
- q5: for-each 안 remove → `removeIf` 또는 새 리스트

## 🃏 복습 카드

- Q: `int cnt = map.get(key);`에서 NPE가 나는 이유는?
  A: 키가 없으면 get이 null을 반환하고, null을 int로 언박싱하다 예외. getOrDefault(key, 0)
- Q: 에러 없이 조용히 틀리는 대표 원인 3가지는?
  A: int 오버플로, 정수 나눗셈, 참조형 ==비교(String/Integer) (+ 얕은 복사)
- Q: 시간 초과가 나면 가장 먼저 확인할 것은?
  A: 입력 크기 대비 시간복잡도(n=10^5인데 O(n²)인지). 그다음 String+=, list.contains/remove(0), BFS 방문 시점
- Q: Checked 예외와 Unchecked 예외의 차이와 예시는?
  A: Checked는 컴파일러가 처리(try-catch/throws)를 강제(IOException), Unchecked는 RuntimeException 하위로 강제 없음(NPE, IndexOutOfBounds)
- Q: 제출 전에 확인할 엣지 케이스 5가지는?
  A: 빈 입력, 원소 1개, 전부 같은 값, 최대 크기/최댓값, 음수·답이 없는 경우
