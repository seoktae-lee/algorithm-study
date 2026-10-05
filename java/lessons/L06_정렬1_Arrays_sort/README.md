# L06. 정렬 ① Arrays.sort

> ⏱ 20분 · 🎯 오름차순·내림차순·부분 정렬을 **기본형/객체형 차이**까지 알고 쓰기
> 🔗 cote 연결 문제: K번째수, 나누어 떨어지는 숫자 배열, 문자열 내림차순으로 배치하기, 예산, H-Index

## 1. 오름차순

```java
int[] a = {5, 2, 9, 1};
Arrays.sort(a);                  // [1, 2, 5, 9]  배열 자체가 바뀜(반환값 없음)
Arrays.sort(a, 1, 3);            // 인덱스 [1, 3)만 정렬
String[] s = {"banana", "apple"};
Arrays.sort(s);                  // 사전순
char[] cs = str.toCharArray(); Arrays.sort(cs);   // 문자열의 글자 정렬
List<Integer> list = ...; Collections.sort(list);  // 리스트는 Collections.sort 또는 list.sort(null)
```

## 2. 내림차순 — 기본형(int[])은 Comparator를 못 받는다

```java
// ❌ Arrays.sort(a, Collections.reverseOrder());   int[]엔 컴파일 에러

// 방법 1: 오름차순 후 뒤집기 (가장 무난)
Arrays.sort(a);
for (int i = 0, j = a.length - 1; i < j; i++, j--) { int t = a[i]; a[i] = a[j]; a[j] = t; }

// 방법 2: Integer[]로 박싱 (객체 배열이라 Comparator 가능)
Integer[] boxed = {5, 2, 9, 1};
Arrays.sort(boxed, Collections.reverseOrder());

// 방법 3: 문자 내림차순 → 오름차순 정렬 후 StringBuilder.reverse()
```

## 3. 정렬 후 자주 하는 것

```java
Arrays.copyOfRange(arr, i - 1, j)  // 잘라서 정렬 (K번째수)
// 그리디: 작은 것부터 담기 (예산)
// 투 포인터: 정렬 후 양 끝에서 좁히기 (구명보트)
```

## 4. 시간복잡도

- `Arrays.sort(int[])`: 듀얼 피벗 퀵정렬, 평균 O(n log n)
- `Arrays.sort(Object[])`, `Collections.sort`: TimSort, O(n log n), **안정 정렬**(같은 값의 원래 순서 유지)
- n ≤ 10^6까지는 정렬 한 번 OK

## 🐍 파이썬이랑 다른 점

- `sorted(a, reverse=True)` 같은 한 방이 int[]엔 없음 → 뒤집거나 Integer[]
- `a.sort()`처럼 **제자리 정렬**이고 반환값이 void. `int[] b = Arrays.sort(a)` ❌

## ⚠️ 함정

1. `Arrays.sort(int[], Collections.reverseOrder())` 컴파일 에러
2. 원본 순서가 필요한데 정렬해 버림 → 먼저 `clone()`
3. 대문자가 소문자보다 앞(사전순 = 유니코드순): "Zebra" < "apple"

## 📌 핵심 요약 (치트시트)

```java
Arrays.sort(a);  Arrays.sort(a, from, to);   // int[] 오름차순 (void)
Integer[] b; Arrays.sort(b, Collections.reverseOrder());  // 내림차순은 객체 배열만
Collections.sort(list); list.sort(Collections.reverseOrder());
int[] 내림차순 = 오름차순 후 양끝 swap
문자열 내림차순 = toCharArray → sort → new StringBuilder(new String(cs)).reverse()
```

## 🧩 연습문제 힌트

- q1: ArrayList에 담고 → int[]로 옮긴 뒤 정렬. 없으면 `new int[]{-1}`. (L08 전이라면 개수를 먼저 세서 배열 크기 결정)
- q2: `toCharArray` → `Arrays.sort` → `new StringBuilder(new String(cs)).reverse().toString()`
- q3: 각 command `[i, j, k]` → `copyOfRange(array, i-1, j)` 정렬 후 `[k-1]`
- q4: `a.clone()` 정렬 후 뒤집기
- q5: 정렬 후 작은 것부터 budget에서 빼기, 모자라면 멈춤

## 🃏 복습 카드

- Q: `int[]`를 내림차순 정렬하는 방법 두 가지는?
  A: ① 오름차순 정렬 후 뒤집기 ② `Integer[]`로 바꿔 `Arrays.sort(b, Collections.reverseOrder())`
- Q: `Arrays.sort(arr)`의 반환값은?
  A: 없음(void). 배열 자체를 정렬한다
- Q: 배열의 인덱스 2~4(포함)만 정렬하는 코드는?
  A: `Arrays.sort(arr, 2, 5);` (끝은 미포함)
- Q: 객체 정렬(TimSort)이 "안정 정렬"이라는 건 무슨 뜻이고 언제 중요한가?
  A: 값이 같은 원소의 원래 순서가 유지됨. 여러 기준으로 차례로 정렬하거나 동점 시 입력 순서를 지켜야 할 때
- Q: 문자열 s의 글자를 사전 역순으로 정렬한 문자열을 만드는 코드는?
  A: `char[] c = s.toCharArray(); Arrays.sort(c); new StringBuilder(new String(c)).reverse().toString()`
