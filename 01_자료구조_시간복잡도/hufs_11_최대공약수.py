
# 문제: 최대공약수
#
# 유클리드 호제법을 이용하여 최대공약수를 구한다.
#
# 주어진 코드:
#
# def gcd(a, b):
#     if b == 0:
#         return a
#     return __________
#
# 정답:
# gcd(b, a % b)
#
# 핵심:
# gcd(a, b) = gcd(b, a % b)
#
# 예:
# gcd(48, 18)
# → gcd(18, 12)
# → gcd(12, 6)
# → gcd(6, 0)
# → 6
#
# 시간복잡도:
# O(log n)

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

