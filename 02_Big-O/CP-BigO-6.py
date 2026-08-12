# 복잡도 코드 - 단답형 4

# 핵심내용:
# 바깥쪽 for는 n번 반복한다.
# 안쪽 while에서는 j >> 1을 사용한다.
# >> 1은 j를 2로 나눈 것과 같은 방식으로 값이 절반씩 감소한다.
# n → n/2 → n/4 → n/8 → ...
# 따라서 while은 log n번 반복한다.
# 중첩된 반복이므로 n × log n = n log n이다.
#
# f(6):
# j = 6 → 3 → 1 → 0
# 안쪽 while은 3번 반복한다.
# 바깥쪽 for가 6번이므로 6 × 3 = 18

def f(n):
    c = 0

    for i in range(n):
        j = n

        while j:
            j = j >> 1
            c += 1

    return c

# f(6) = 18
# 시간복잡도: O(n log n)
