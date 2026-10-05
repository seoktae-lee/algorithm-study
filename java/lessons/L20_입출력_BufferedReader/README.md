# L20. 입출력 — BufferedReader · StringTokenizer · StringBuilder 출력

> ⏱ 25분 · 🎯 프로그래머스 밖(삼성 SW역량테스트·백준·SWEA·일부 기업)의 **표준 입출력 형식**에 대비
> 🔗 cote 연결: `cote track samsung on`, `cote ext` (외부 문제), 일부 기업 코테(구름·코드트리 환경)

## 1. 프로그래머스 vs 표준 입출력

- 프로그래머스: `solution(...)` 매개변수로 받고 return → 입출력 코드 없음
- 표준 입출력: `main`에서 **직접 읽고 출력**. 입력이 수십만 줄이면 읽는 방법이 시간을 좌우

## 2. 기본 템플릿 (외워 두기)

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());          // 한 줄에 숫자 하나
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n; i++) {
            StringTokenizer st = new StringTokenizer(br.readLine());   // 공백으로 자르기
            int a = Integer.parseInt(st.nextToken());
            int b = Integer.parseInt(st.nextToken());
            sb.append(a + b).append('\n');
        }
        System.out.print(sb);       // 출력은 모아서 한 번에
    }
}
```

## 3. 자주 나오는 입력 형태

```java
// 격자: 첫 줄 "R C", 다음 R줄 "0101" (공백 없음)
for (int r = 0; r < R; r++) {
    String line = br.readLine();
    for (int c = 0; c < C; c++) grid[r][c] = line.charAt(c) - '0';
}
// 격자: 숫자가 공백으로 구분 "0 1 0 1"
StringTokenizer st = new StringTokenizer(br.readLine());
for (int c = 0; c < C; c++) grid[r][c] = Integer.parseInt(st.nextToken());

// 입력 끝(EOF)까지 읽기
String line;
while ((line = br.readLine()) != null && !line.isEmpty()) { ... }

// 테스트케이스 T개 (삼성/SWEA): 출력 형식 "#1 답"
sb.append('#').append(tc).append(' ').append(ans).append('\n');
```

## 4. 왜 Scanner를 안 쓰나

| 방법 | 속도 | 비고 |
|---|---|---|
| `Scanner` | 느림 (정규식 파싱) | 입력 10^5줄 이상이면 시간 초과 위험 |
| `BufferedReader + StringTokenizer` | 빠름 | 코테 표준 |
| `System.out.println` 반복 | 느림 | 줄마다 flush |
| `StringBuilder` 모아서 `print` | 빠름 | 코테 표준 |

- `br.readLine()`은 IOException을 던질 수 있는 checked 예외 → `main(...) throws IOException`
- 백준·삼성은 클래스 이름이 **`Main`** 이어야 하는 경우가 많음 (SWEA는 `Solution`)

## 🐍 파이썬이랑 다른 점

- `input = sys.stdin.readline` ≈ `BufferedReader.readLine()`
- `map(int, input().split())` ≈ `StringTokenizer` + `Integer.parseInt` 반복
- 파이썬 `print`를 모아 `'\n'.join` ≈ StringBuilder

## ⚠️ 함정

1. `readLine()` 결과 끝의 공백·개행 → `trim()`
2. `throws IOException` 누락 → 컴파일 에러
3. 클래스명/패키지 선언(`package ...`)을 지우지 않아 컴파일 에러

## 📌 핵심 요약 (치트시트)

```java
BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
StringTokenizer st = new StringTokenizer(br.readLine());
int a = Integer.parseInt(st.nextToken());
while ((line = br.readLine()) != null) …   // EOF
StringBuilder sb; sb.append(x).append('\n'); System.out.print(sb);
public static void main(String[] args) throws IOException  · class Main
```

## 🧩 연습문제 힌트

연습문제는 입력을 문자열로 받아 `new BufferedReader(new StringReader(input))`로 읽고, 출력할 내용을 String으로 반환합니다. (실전에서는 `InputStreamReader(System.in)`만 다름)

- q1: 첫 줄 N → N줄 StringTokenizer로 두 수 → `sb.append(a + b).append('\n')`
- q2: 첫 줄 "R C" → R줄의 각 글자 `charAt(c) == '1'` 세기
- q3: `while ((line = br.readLine()) != null)` + 줄마다 StringTokenizer `hasMoreTokens()`
- q4: N개를 배열에 담고 뒤에서부터 append

## 🃏 복습 카드

- Q: 코테 표준 입력 2종 세트와 Scanner를 피하는 이유는?
  A: BufferedReader + StringTokenizer. Scanner는 내부 정규식 파싱으로 느려 대량 입력에서 시간 초과 위험
- Q: 출력이 많을 때 System.out.println 대신 쓰는 방법은?
  A: StringBuilder에 append하고 마지막에 한 번 `System.out.print(sb)`
- Q: 입력 끝(EOF)까지 한 줄씩 읽는 코드는?
  A: `String line; while ((line = br.readLine()) != null) { ... }`
- Q: BufferedReader를 쓸 때 main에 붙여야 하는 것과 이유는?
  A: `throws IOException`. readLine이 checked 예외인 IOException을 던질 수 있어서
- Q: 한 줄 "3 5 7"에서 정수를 차례로 꺼내는 코드는?
  A: `StringTokenizer st = new StringTokenizer(br.readLine()); while (st.hasMoreTokens()) Integer.parseInt(st.nextToken());`
