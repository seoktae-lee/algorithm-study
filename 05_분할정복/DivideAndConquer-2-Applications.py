# [2026-08-24] 훕코마 - 분할정복 응용 (이진탐색, 피보나치 수)
# 동영상 2편: 알고리즘 분할정복법 소개 - 피보나치 수 및 이진탐색
#
# 핵심내용:
# 단순 재귀로 구현 시 O(1.618^n)의 지수 시간이 걸리는 피보나치 수열을
# 2x2 행렬의 거듭제곱으로 변환하여 O(log N) 시간에 해결하고,
# 정렬된 배열에서 탐색 범위를 반씩 버리는 이진 탐색(O(log N))을 다룬다.
#
# 핵심 개념:
# 1. 이진 탐색 (Binary Search): 중앙값 비교 후 탐색 범위를 매번 1/2로 버림
# 2. 행렬 피보나치: [[F_n+1, F_n], [F_n, F_n-1]] = [[1, 1], [1, 0]]^n 관계식 활용
# 3. 분할정복 거듭제곱: 2x2 행렬의 n승을 O(log N) 시간에 계산
#
# 접근법 (행렬 피보나치):
# 1. 2x2 행렬 곱셈 함수 matrix_mul 구현
# 2. 행렬 거듭제곱 함수 matrix_pow를 분할정복(O(log N)) 방식으로 구현
# 3. [[1, 1], [1, 0]] 행렬의 n승을 구한 뒤 F_n 위치의 값 반환
#
# 핵심 사고:
# 수열의 점화식을 행렬 곱셈 형태로 재정의하면 분할정복 거듭제곱 기법을
# 그대로 적용하여 지수 시간 알고리즘을 로그 시간 알고리즘으로 대폭 단축할 수 있다.
#
# 핵심 플로우:
# 피보나치 점화식 -> 2x2 행렬식 변환 -> 행렬 분할정복 거듭제곱 -> O(log N) 결과 반환
#
# 핵심 키워드:
# Binary Search / Fibonacci / Matrix Exponentiation / O(log N) / Reusability

def matrix_mul(A, B):
    return [
        [A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
        [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]]
    ]

def matrix_pow(A, n):
    if n == 1:
        return A
    
    matrix = matrix_pow(A, n // 2)
    squared = matrix_mul(matrix, matrix)
    
    if n % 2 == 0:
        return squared
    else:
        return matrix_mul(squared, A)

def fibonacci(n):
    if n == 0:
        return 0
    base_matrix = [[1, 1], [1, 0]]
    result_matrix = matrix_pow(base_matrix, n)
    return result_matrix[0][1]

# 예시 실행
print(fibonacci(10))  # 55
