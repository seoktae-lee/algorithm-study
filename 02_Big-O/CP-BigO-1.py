# CP-BigO-1

# 핵심내용:
# k가 1씩 증가하는 것이 아니라 2배씩 증가한다.
# 1 → 2 → 4 → 8 → 16 → ...
# 따라서 반복 횟수는 log n에 비례한다.
# 배수로 증가하는 반복문은 O(log n)이다.

def do_something(n):
    k = 1
    count = 0

    while k < n:
        k *= 2
        count += 1

    return count

# 시간복잡도: O(log n)
