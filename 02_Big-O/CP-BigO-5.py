# 복잡도 코드 - 단답형 3

# 핵심내용:
# 바깥쪽 for는 n번 반복한다.
# 안쪽 while에서는 j가 1부터 시작해서 2배씩 증가한다.
# 1 → 2 → 4 → 8 → ... → n
# 따라서 while은 log n번 반복한다.
# 중첩된 반복이므로 n × log n = n log n이다.
#
# f(8):
# 바깥쪽 8번 × 안쪽 4번 = 32

def f(n):
    c = 0

    for i in range(n):
        j = 1

        while j <= n:
            j *= 2
            c += 1

    return c

# f(8) = 32
# 시간복잡도: O(n log n)
