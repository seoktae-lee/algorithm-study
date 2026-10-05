# L19. 그래프 표현 · BFS/DFS 템플릿

> ⏱ 35분 · 🎯 격자·인접 리스트에서 **BFS 최단거리, DFS 연결 요소**를 템플릿으로 바로 쓰기
> 🔗 cote 연결 문제: 게임 맵 최단거리, 네트워크, 타겟 넘버, 단어 변환, 전력망을 둘로 나누기, 무인도 여행, 미로 탈출

## 1. 그래프 표현

```java
// 간선 목록 [[1,2],[2,3]] (노드 1..n, 무방향) → 인접 리스트
List<List<Integer>> g = new ArrayList<>();
for (int i = 0; i <= n; i++) g.add(new ArrayList<>());
for (int[] e : edges) { g.get(e[0]).add(e[1]); g.get(e[1]).add(e[0]); }

// 인접 행렬 (computers[i][j] == 1이면 연결) — n이 작을 때 (≤ 1000)
// 격자 int[][] maps — 칸이 노드, 상하좌우가 간선
int[] dr = {-1, 1, 0, 0}, dc = {0, 0, -1, 1};
```

## 2. BFS — 가중치 없는 최단거리 (가까운 것부터 퍼짐)

```java
int[][] dist = new int[R][C];
for (int[] row : dist) Arrays.fill(row, -1);
Queue<int[]> q = new ArrayDeque<>();
q.offer(new int[]{0, 0}); dist[0][0] = 1;          // 넣을 때 방문 표시 ⭐
while (!q.isEmpty()) {
    int[] cur = q.poll();
    for (int d = 0; d < 4; d++) {
        int nr = cur[0] + dr[d], nc = cur[1] + dc[d];
        if (nr < 0 || nc < 0 || nr >= R || nc >= C) continue;   // 범위
        if (maps[nr][nc] == 0 || dist[nr][nc] != -1) continue; // 벽·방문
        dist[nr][nc] = dist[cur[0]][cur[1]] + 1;
        q.offer(new int[]{nr, nc});
    }
}
```

## 3. DFS — 연결 요소 세기 / 전부 방문

```java
boolean[] visited = new boolean[n];
void dfs(int u) {
    visited[u] = true;
    for (int v : g.get(u)) if (!visited[v]) dfs(v);
}
int components = 0;
for (int i = 0; i < n; i++) if (!visited[i]) { dfs(i); components++; }
```

> 깊이가 10^4을 넘을 수 있으면(큰 격자) 재귀 대신 **스택으로 반복 DFS**나 BFS로 — StackOverflowError 예방

## 4. 언제 무엇을

| 질문 | 도구 |
|---|---|
| 최단 거리/최소 횟수 (간선 비용 동일) | BFS |
| 연결된 덩어리 개수·크기, 경로 존재 | DFS 또는 BFS |
| 모든 경우 탐색(백트래킹) | DFS (L16) |
| 비용이 다른 최단거리 | 다익스트라 (PQ, 나중에) |

복잡도: 인접 리스트 O(V + E), 격자 O(R × C)

## 🐍 파이썬이랑 다른 점

- `deque` → `ArrayDeque`, `[[False]*m for _ in range(n)]` → `new boolean[n][m]`
- 파이썬 `dict` 그래프 대신 `List<List<Integer>>` (노드가 0..n 정수일 때)

## ⚠️ 함정

1. BFS에서 **꺼낼 때** 방문 표시 → 같은 칸이 큐에 여러 번 들어가 메모리·시간 폭발. **넣을 때** 표시
2. 범위 체크보다 배열 접근을 먼저 → IndexOutOfBounds. 조건 순서: 범위 → 벽 → 방문
3. 노드가 1번부터인데 크기 n으로 만들기 → `n + 1`

## 📌 핵심 요약 (치트시트)

```java
List<List<Integer>> g; for (i <= n) g.add(new ArrayList<>()); 양방향 add
int[] dr = {-1,1,0,0}, dc = {0,0,-1,1};
BFS: q.offer(start); 방문표시; while(!q.isEmpty()) { cur = poll; for 4방향: 범위→벽→방문 → 표시+offer }
DFS: visited[u] = true; for (v : g.get(u)) if (!visited[v]) dfs(v);
연결 요소: for i: if (!visited[i]) { dfs(i); cnt++; }
```

## 🧩 연습문제 힌트

- q1: BFS 템플릿, `dist[R-1][C-1]` 반환 (도달 못 하면 -1 그대로)
- q2: 인접 행렬 DFS — `for (j = 0; j < n; j++) if (computers[u][j] == 1 && !visited[j]) dfs(j)`
- q3: 격자의 '1' 칸마다 아직 방문 안 했으면 BFS/DFS로 덩어리 전체 방문 + 개수 +1
- q4: 인접 리스트 + BFS, `dist` 배열 -1로 초기화, 반환은 1..n 순서로 길이 n 배열

## 🃏 복습 카드

- Q: BFS에서 방문 표시는 큐에 넣을 때와 꺼낼 때 중 언제 하나? 이유는?
  A: 넣을 때. 꺼낼 때 하면 같은 칸이 여러 번 큐에 들어가 시간·메모리 낭비(최악엔 시간 초과)
- Q: 격자 상하좌우 이동을 위한 배열 선언은?
  A: `int[] dr = {-1, 1, 0, 0}, dc = {0, 0, -1, 1};`
- Q: 간선 목록으로 무방향 인접 리스트를 만드는 코드는?
  A: `for (i = 0; i <= n; i++) g.add(new ArrayList<>()); for (e : edges) { g.get(e[0]).add(e[1]); g.get(e[1]).add(e[0]); }`
- Q: 가중치 없는 그래프의 최단 거리는 BFS와 DFS 중 무엇으로 구하나?
  A: BFS (가까운 노드부터 방문하므로 처음 도달한 거리가 최단)
- Q: 연결 요소 개수를 세는 코드 뼈대는?
  A: `for (i : 모든 노드) if (!visited[i]) { dfs(i); count++; }`
