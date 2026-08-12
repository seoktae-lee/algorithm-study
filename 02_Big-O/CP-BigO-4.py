# CP-BigO-4

# 핵심내용:
# k는 1씩 증가하지만 반복 조건이 k² <= n이다.
# 즉 k <= √n이 되는 범위까지만 반복한다.
# 따라서 반복 횟수는 √n에 비례한다.
# 제곱이 n을 넘는 순간 반복이 종료되므로 O(√n)이다.

def do_something(n):
    count = 0
    k = 1

    while k * k <= n:
        count += 1
        k += 1

    return count

# 시간복잡도: O(√n)
