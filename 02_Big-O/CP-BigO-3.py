# CP-BigO-3

# 핵심내용:
# 바깥쪽 for는 n번 반복한다.
# 그 안쪽 for도 n번 반복한다.
# 가장 안쪽 while에서는 k가 2배씩 증가하므로 log n번 반복한다.
# 중첩된 반복문은 반복 횟수를 곱하므로
# n × n × log n = n² log n 이다.

def do_something(n):
    count = 0

    for i in range(n):
        for j in range(n):
            k = 1

            while k < n:
                count += 1
                k *= 2

    return count

# 시간복잡도: O(n² log n)
