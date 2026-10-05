# L11. Stack · Queue · Deque (ArrayDeque)

> ⏱ 30분 · 🎯 스택·큐는 **ArrayDeque 하나로**. 괄호·짝 제거·"순서대로 처리" 시뮬레이션
> 🔗 cote 연결 문제: 올바른 괄호, 짝지어 제거하기, 기능개발, 프로세스, 다리를 지나는 트럭, 주식가격, 크레인 인형뽑기

## 1. 스택 (LIFO: 나중에 넣은 게 먼저)

```java
Deque<Integer> stack = new ArrayDeque<>();
stack.push(1); stack.push(2);   // [2, 1]  (앞쪽에 쌓임)
stack.peek();                    // 2  맨 위 보기 (비었으면 null)
stack.pop();                     // 2  꺼내기 (비었으면 NoSuchElementException!)
stack.isEmpty(); stack.size();
```

## 2. 큐 (FIFO: 먼저 넣은 게 먼저)

```java
Queue<Integer> q = new ArrayDeque<>();
q.offer(1); q.offer(2);          // 뒤에 넣기
q.peek();                        // 1  맨 앞 보기 (비었으면 null)
q.poll();                        // 1  꺼내기 (비었으면 null)
```

## 3. 덱 (양쪽 다)

```java
Deque<Integer> dq = new ArrayDeque<>();
dq.offerFirst(x); dq.offerLast(x);
dq.pollFirst(); dq.pollLast();
dq.peekFirst(); dq.peekLast();
```

> **왜 `Stack` 클래스를 안 쓰나?** `Stack`은 오래된 Vector 기반(모든 메서드 동기화)이라 느리고 설계가 낡았어요. 자바 공식 문서도 `Deque`를 권장. `LinkedList`도 큐로 쓸 수 있지만 ArrayDeque가 더 빠름. (ArrayDeque는 null 저장 불가)

## 4. 대표 패턴

```java
// 괄호 짝: 여는 건 push, 닫는 건 top과 짝인지 확인 후 pop, 끝에 스택이 비어야 OK
// 짝지어 제거: top과 같으면 pop, 다르면 push
// 모노톤 스택(주식가격·다음 큰 수): 인덱스를 쌓고, 현재 값이 top보다 작으면(크면) pop하며 답 확정
for (int i = 0; i < n; i++) {
    while (!st.isEmpty() && prices[st.peek()] > prices[i]) {
        int j = st.pop(); ans[j] = i - j;
    }
    st.push(i);
}
// 큐 시뮬레이션: 작업을 큐에 넣고 시간/조건에 따라 poll
```

## 🐍 파이썬이랑 다른 점

- 파이썬 스택 `list.append/pop` → `push/pop`, 큐 `collections.deque` → `ArrayDeque` (`append/popleft` → `offer/poll`)
- 파이썬 `stack[-1]` → `stack.peek()`

## ⚠️ 함정

1. 빈 스택에서 `pop()` → 예외. 항상 `!isEmpty()` 먼저 (poll/peek은 null 반환)
2. `push`(앞에 넣기)와 `offer`(뒤에 넣기)를 한 덱에 섞으면 순서가 꼬임 → 스택이면 push/pop/peek만, 큐면 offer/poll/peek만
3. ArrayDeque에 null을 넣으면 NPE

## 📌 핵심 요약 (치트시트)

```java
Deque<Integer> st = new ArrayDeque<>();  push / pop / peek / isEmpty
Queue<Integer> q = new ArrayDeque<>();   offer / poll / peek   (비면 null)
Deque: offerFirst/offerLast/pollFirst/pollLast/peekFirst/peekLast
모노톤 스택: while (!st.isEmpty() && a[st.peek()] > a[i]) { j = st.pop(); ... } st.push(i);
Stack 클래스 X → ArrayDeque
```

## 🧩 연습문제 힌트

- q1: 여는 괄호 push, 닫는 괄호면 스택이 비었거나 top이 짝이 아니면 false
- q2: `Deque<Character>` — top과 같으면 pop, 아니면 push. 끝에 비었으면 1
- q3: 각 작업의 남은 일수 = `(100 - p + s - 1) / s`. 앞 작업의 일수보다 작거나 같으면 같이 배포
- q4: 열(move)마다 위에서부터 0이 아닌 첫 칸 → 꺼내서 0으로. 바구니 스택 top과 같으면 pop하고 +2
- q5: 위 모노톤 스택 패턴 + 끝까지 남은 인덱스는 `n - 1 - j`

## 🃏 복습 카드

- Q: 자바에서 스택과 큐로 권장되는 클래스와 그 이유는?
  A: ArrayDeque. Stack은 Vector 기반 레거시(동기화로 느림), ArrayDeque가 LinkedList보다도 빠름
- Q: 스택용 메서드 3개와 큐용 메서드 3개는?
  A: 스택 push/pop/peek, 큐 offer/poll/peek
- Q: 빈 ArrayDeque에서 pop()과 poll()은 각각 어떻게 되나?
  A: pop은 NoSuchElementException, poll은 null
- Q: '주식가격'·'다음 큰 수' 류에서 쓰는 자료구조와 핵심 동작은?
  A: 인덱스를 담는 모노톤 스택. 현재 값이 top의 조건을 깨면 pop하면서 그 인덱스의 답을 확정, O(n)
- Q: '올바른 괄호'를 스택으로 푸는 규칙은?
  A: 여는 괄호 push, 닫는 괄호는 스택이 비었거나 top이 짝이 아니면 실패, 아니면 pop. 끝나고 스택이 비어야 성공
