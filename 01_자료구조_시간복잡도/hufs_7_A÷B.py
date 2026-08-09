# 문제: 훕코마 #7 A/B
# 접근: 입력 두 수 나누기 (실수 출력)
# 시간복잡도: O(1)
# 주의: 절대오차 또는 상대오차 10^-9 이하 허용

import sys
input = sys.stdin.readline

A, B = map(int, input().split())
print(A / B)
