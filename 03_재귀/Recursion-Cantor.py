# 8/18 코테 - 칸토어 집합
#
# 핵심내용:
# 칸토어 집합은 기존 선을 3등분하고
# 가운데 부분을 공백으로 만드는 과정을 반복한다.
#
# 핵심 사고:
# 현재 단계 N을 직접 만드는 대신
# N-1 단계의 결과를 먼저 재귀적으로 구한다.
#
# N = 0
# -
#
# N = 1
# - -
#
# N = 2
# - -   - -
#
# N = 3
# - -   - -         - -   - -
#
# 핵심 플로우:
# 1. n == 0 → "-"
# 2. prev = cantor(n - 1)
# 3. prev + len(prev)만큼 공백 + prev
# 4. 현재 단계 결과 반환
#
# 즉:
# 현재 결과 = 이전 결과 + 같은 길이의 공백 + 이전 결과

def cantor(n):
    if n == 0:
        return "-"

    prev = cantor(n - 1)

    return prev + " " * len(prev) + prev


for line in __import__("sys").stdin:
    line = line.strip()

    if line:
        n = int(line)
        print(cantor(n))

# 시간복잡도: 출력 크기 자체가 3^n이므로 O(3^n)
# 공간복잡도: 재귀 깊이 O(n)
