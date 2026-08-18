# 8/18 코테 - 팩토리얼
#
# 핵심내용:
# N! = N × (N-1) × ... × 2 × 1
# 0! = 1
#
# 핵심 사고:
# 처음 결과를 1로 두고
# 1부터 N까지 차례대로 곱한다.
#
# 핵심 플로우:
# N 입력
# → result = 1
# → 1 ~ N 반복
# → result *= i
# → 결과 출력
#
# N = 0이면 range(1, 1)이므로 반복하지 않고
# result = 1이 그대로 유지되어 0! = 1을 처리한다.

N = int(input())

result = 1

for i in range(1, N + 1):
    result *= i

print(result)

# 시간복잡도: O(n)
# 공간복잡도: O(1)
