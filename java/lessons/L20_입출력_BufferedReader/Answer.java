import java.io.*;
import java.util.*;

class Exercise {
    // Q1. 첫 줄 N, 다음 N줄에 "a b" → 각 줄의 합을 한 줄씩 출력 (마지막 줄도 \n으로 끝남)
    String sumLines(String input) throws IOException {
        BufferedReader br = new BufferedReader(new StringReader(input));
        // ▼ answer
        int n = Integer.parseInt(br.readLine().trim());
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n; i++) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            int a = Integer.parseInt(st.nextToken());
            int b = Integer.parseInt(st.nextToken());
            sb.append(a + b).append('\n');
        }
        return sb.toString();
        // ▲ answer
        // TODO: return "";
    }

    // Q2. 첫 줄 "R C", 다음 R줄에 공백 없는 0/1 문자열 → '1'의 개수를 출력 (줄바꿈 없이)
    String countOnes(String input) throws IOException {
        BufferedReader br = new BufferedReader(new StringReader(input));
        // ▼ answer
        StringTokenizer st = new StringTokenizer(br.readLine());
        int R = Integer.parseInt(st.nextToken()), C = Integer.parseInt(st.nextToken());
        int cnt = 0;
        for (int r = 0; r < R; r++) {
            String line = br.readLine();
            for (int c = 0; c < C; c++) if (line.charAt(c) == '1') cnt++;
        }
        return String.valueOf(cnt);
        // ▲ answer
        // TODO: return "";
    }

    // Q3. 줄 수를 모름(EOF까지). 각 줄에 정수가 여러 개 → 전체 합을 출력 (줄바꿈 없이)
    String sumUntilEOF(String input) throws IOException {
        BufferedReader br = new BufferedReader(new StringReader(input));
        // ▼ answer
        long sum = 0;
        String line;
        while ((line = br.readLine()) != null) {
            StringTokenizer st = new StringTokenizer(line);
            while (st.hasMoreTokens()) sum += Long.parseLong(st.nextToken());
        }
        return String.valueOf(sum);
        // ▲ answer
        // TODO: return "";
    }

    // Q4. 첫 줄 N, 다음 N줄에 단어 → 역순으로 한 줄씩 출력 (마지막 줄도 \n)
    String reverseLines(String input) throws IOException {
        BufferedReader br = new BufferedReader(new StringReader(input));
        // ▼ answer
        int n = Integer.parseInt(br.readLine().trim());
        String[] w = new String[n];
        for (int i = 0; i < n; i++) w[i] = br.readLine();
        StringBuilder sb = new StringBuilder();
        for (int i = n - 1; i >= 0; i--) sb.append(w[i]).append('\n');
        return sb.toString();
        // ▲ answer
        // TODO: return "";
    }

    public static void main(String[] args) {
        Exercise e = new Exercise();
        Check.run("Q1 sumLines", () -> { try { return e.sumLines("3\n1 2\n3 4\n5 6\n"); } catch (IOException x) { throw new UncheckedIOException(x); } }, "3\n7\n11\n");
        Check.run("Q2 countOnes", () -> { try { return e.countOnes("2 3\n101\n011\n"); } catch (IOException x) { throw new UncheckedIOException(x); } }, "4");
        Check.run("Q3 sumUntilEOF", () -> { try { return e.sumUntilEOF("1 2\n3\n4 5 6\n"); } catch (IOException x) { throw new UncheckedIOException(x); } }, "21");
        Check.run("Q3 sumUntilEOF 큰 수", () -> { try { return e.sumUntilEOF("2000000000 2000000000"); } catch (IOException x) { throw new UncheckedIOException(x); } }, "4000000000");
        Check.run("Q4 reverseLines", () -> { try { return e.reverseLines("3\na\nb\nc\n"); } catch (IOException x) { throw new UncheckedIOException(x); } }, "c\nb\na\n");
        Check.done();
    }
}
