# [2026-08-24] 훕코마 - 분할정복법과 점화식
# 동영상 4편: 알고리즘 분할정복 - 점화식
#
# 핵심내용:
# 분할정복 알고리즘의 실행 시간을 나타내는 점화식 T(N)을
# 재귀 트리(Recursion Tree) 시각화를 통해 직관적으로 도출하고 분석한다.
#
# 핵심 개념:
# 1. 점화식 (Recurrence Relation): T(n) = a * T(n/b) + f(n)
# 2. 재귀 트리 (Recursion Tree): 각 분할 단계의 트리를 그리고
#    트리의 높이(log_b n)와 층별 작업 합을 구하여 전체 복잡도 계산
# 3. 대표 형태 분석:
#    - T(n) = T(n/2) + c       => 이진 탐색 O(log N)
#    - T(n) = 2T(n/2) + cn     => 병합 정렬 O(N log N)
#    - T(n) = 3T(n/2) + cn     => 카라추바 곱셈 O(N^1.58)
#
# 접근법:
# 1. 트리 높이 구하기: n이 1이 될 때까지 b로 나눈 횟수 k = log_b n
# 2. 층별 작업량 합산: 각 깊이에서의 (노드 수 * 노드당 작업량) 계산
# 3. 기저 상태 연산량: 맨 아래 층(잎 노드)의 총 연산량 합산
#
# 핵심 사고:
# 복잡한 수식 전개 없이도 재귀 트리의 깊이와 층별 일의 양을 시각화하면
# 알고리즘의 최종 빅오(Big-O) 시간 복잡도를 한눈에 직관적으로 도출할 수 있다.
#
# 핵심 플로우:
# 점화식 수식화 -> 재귀 트리 시각화 -> 깊이(log N) 및 층별 작업량 합산 -> 최종 시간 복잡도 도출
#
# 핵심 키워드:
# Recurrence Relation / Recursion Tree / Merge Sort / O(N log N) / Master Theorem

# 병합 정렬(Merge Sort)의 T(n) = 2T(n/2) + cn 구조 시뮬레이션 코드
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])    # T(n/2)
    right = merge_sort(arr[mid:])   # T(n/2)
    
    # 병합 과정 (cn 작업량)
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# 예시 실행
print(merge_sort([5, 2, 9, 1, 7, 6]))  # [1, 2, 5, 6, 7, 9]
