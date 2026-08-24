# [2026-08-24] 훕코마 - 큰 정수 곱셈 (Karatsuba 알고리즘)
# 동영상 3편: 알고리즘 분할정복 - 큰수 곱셈 (Karatsuba 알고리즘)
#
# 핵심내용:
# 초등학교식 n자리 곱셈 방식(O(N^2))을 수학적 변형을 통해
# 크기가 반으로 줄어든 미니 곱셈 횟수를 4회에서 3회로 줄여 O(N^1.58)로 최적화한다.
#
# 핵심 개념:
# 1. 수의 분할: u = a*10^(n/2) + b, v = c*10^(n/2) + d
# 2. 일반 분할 전개: uv = (ac)*10^n + (ad+bc)*10^(n/2) + bd (곱셈 4회 -> O(N^2))
# 3. 카라추바 변형: (ad+bc) = (a+b)(c+d) - ac - bd 식을 사용하여
#    필요한 곱셈을 ac, bd, (a+b)(c+d) 단 3회로 단축
#
# 접근법:
# 1. 수가 충분히 작을 경우(Base Case) 기본 곱셈 수행
# 2. 숫자를 상위 자릿수(a, c)와 하위 자릿수(b, d)로 분할
# 3. 3번의 재귀 곱셈(z0=bd, z1=(a+b)(c+d), z2=ac) 수행
# 4. z2*10^n + (z1 - z2 - z0)*10^(n/2) + z0 조합 후 반환
#
# 핵심 사고:
# 부분 문제의 개수를 4개에서 3개로 단 1개만 줄여도,
# 재귀 트리의 자식 노드 수가 줄어들어 전체 시간 복잡도가 O(N^2)에서 O(N^1.58)로 혁신적으로 개선된다.
#
# 핵심 플로우:
# 수 분할 -> z0, z1, z2 3회 재귀 곱셈 -> 자릿수 연산 결합 -> O(N^1.58) 결과 반환
#
# 핵심 키워드:
# Karatsuba Algorithm / Big Integer Multiplication / O(N^1.58) / O(N^(log2 3)) / Subproblem Reduction

def karatsuba(u, v):
    # Base Case: 수의 길이가 짧으면 일반 곱셈 수행
    if u < 10 or v < 10:
        return u * v
    
    n = max(len(str(u)), len(str(v)))
    m = n // 2
    
    # 10^m 기준으로 수 분할
    power = 10 ** m
    a, b = divmod(u, power)
    c, d = divmod(v, power)
    
    # 3번의 재귀 곱셈 수행
    z0 = karatsuba(b, d)                 # bd
    z2 = karatsuba(a, c)                 # ac
    z1 = karatsuba(a + b, c + d)         # (a+b)(c+d)
    
    # (ad+bc) = z1 - z2 - z0
    return (z2 * (10 ** (2 * m))) + ((z1 - z2 - z0) * power) + z0

# 예시 실행
print(karatsuba(1234, 5678))  # 7006652
