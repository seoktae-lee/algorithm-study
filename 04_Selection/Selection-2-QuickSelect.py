# 8/20 훕코마 - Selection Problem 2편
# Quick Select
#
# 핵심내용:
# Quick Select는 Pivot을 기준으로 데이터를 나누고,
# k번째 원소가 존재하는 한쪽 부분만 재귀적으로 탐색한다.
#
# 분할:
# A = Pivot보다 작은 원소
# M = Pivot과 같은 원소
# B = Pivot보다 큰 원소
#
# 핵심 사고:
# 정렬 전체가 목적이 아니다.
# k번째 원소가 어느 그룹에 있는지만 알면
# 그 그룹만 계속 탐색할 수 있다.
#
# 핵심 플로우:
# 1. Pivot 선택
# 2. A / M / B로 Partition
# 3. |A| >= k
#    -> A에서 k번째 원소를 다시 탐색
# 4. |A| + |M| < k
#    -> B에서 (k - |A| - |M|)번째 원소를 탐색
# 5. 그 사이면 Pivot이 정답
#
# 시간복잡도:
# Best Case    -> O(n)
# Average Case -> O(n)
# Worst Case   -> O(n^2)
#
# 최악의 경우:
# Pivot이 계속 최댓값 또는 최솟값으로 선택되어
# 한쪽에 거의 모든 원소가 남으면
# n + (n-1) + (n-2) + ...
# -> O(n^2)
#
# 핵심 키워드:
# Pivot / Partition / Quick Select / Average O(n) / Worst O(n^2)
