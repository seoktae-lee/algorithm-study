# 8/20 훕코마 - Selection Problem 3편
# Median of Medians (MoM)
#
# 핵심내용:
# Quick Select는 평균 O(n)이지만
# Pivot이 계속 나쁘게 선택되면 최악의 경우 O(n^2)이 된다.
#
# MoM은 이를 방지하기 위해
# 치우치지 않는 Pivot을 선택하는 방법이다.
#
# 핵심 사고:
# 좋은 Pivot을 직접 찾기 어렵다면
# 작은 그룹으로 나눈 뒤 그 그룹들의 중앙값을 이용해
# 더 좋은 Pivot을 만든다.
#
# 핵심 플로우:
# 1. 원소를 5개씩 그룹화
# 2. 각 그룹의 중앙값을 구한다.
# 3. 중앙값들을 모은 배열에서 다시 중앙값을 구한다.
# 4. 이 중앙값을 MoM Pivot으로 사용한다.
# 5. Pivot 기준으로 Partition
# 6. k번째 원소가 있는 쪽만 재귀 탐색
#
# 핵심 보장:
# MoM Pivot을 사용하면 한쪽으로 지나치게 치우친 분할을 방지한다.
# 최소 약 25% 이상을 제거할 수 있으므로
# 한쪽에 남는 데이터는 최대 3n/4 수준으로 제한된다.
#
# 점화식:
# T(n) <= T(n/5) + T(3n/4) + 11n/5
#
# 따라서 Quick Select의 최악 O(n^2) 문제를 해결하고
# 최악의 경우에도 O(n)을 보장할 수 있다.
#
# 핵심 키워드:
# Group of 5 / Median / Median of Medians / Good Pivot / Worst-case O(n)
