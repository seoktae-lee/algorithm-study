# CP-BigO-2

# 핵심내용:
# i가 0부터 n/2까지 1씩 증가하므로 약 n/2번 반복한다.
# Big-O에서는 상수 1/2를 무시하므로 O(n)이다.
# n/2, n/3처럼 n의 일정한 비율만큼 반복해도 O(n)이다.

def do_something(A, n):
    for i in range(n // 2):
        c = A[i]
        A[i] = A[n - 1 - i]
        A[n - 1 - i] = c

# 시간복잡도: O(n)
