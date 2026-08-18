# 8/18 코테 - 재귀의 귀재
#
# 핵심내용:
# 팰린드롬은 앞에서 읽으나 뒤에서 읽으나 같은 문자열이다.
#
# 핵심 사고:
# 문자열 전체를 한꺼번에 비교하지 않고
# 양 끝 문자를 비교한다.
#
# 왼쪽 인덱스 l은 +1,
# 오른쪽 인덱스 r은 -1 하면서
# 가운데 방향으로 좁혀 간다.
#
# 핵심 플로우:
# 1. l >= r → 비교가 끝났으므로 1
# 2. s[l] != s[r] → 바로 0
# 3. 같으면 → recursion(s, l+1, r-1)
#
# 또한 문제에서 recursion 함수의 호출 횟수도 요구하므로
# 함수가 호출될 때마다 count를 1 증가시킨다.
#
# 예:
# ABBA
# A == A
# B == B
# 가운데 도착
# → 1
#
# ABC
# A != C
# → 0

import sys

input = sys.stdin.readline


def recursion(s, l, r):
    global count
    count += 1

    if l >= r:
        return 1
    elif s[l] != s[r]:
        return 0
    else:
        return recursion(s, l + 1, r - 1)


def isPalindrome(s):
    return recursion(s, 0, len(s) - 1)


T = int(input())

for _ in range(T):
    s = input().strip()

    count = 0
    result = isPalindrome(s)

    print(result, count)

# 시간복잡도: O(n)
# 공간복잡도: O(n) - 재귀 호출 스택
