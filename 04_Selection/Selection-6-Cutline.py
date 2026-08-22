# 8/22 훕코마 - Selection Problem
# 백준 25305번: 커트라인
#
# 핵심내용:
# N명의 점수 중 상위 k번째 점수(커트라인)를 구하는 문제이다.
# N이 최대 1,000 정도로 작기 때문에 내림차순 정렬(O(N log N)) 후
# 특정 위치(k번째)의 원소에 직접 접근하는 방식이 가장 간단하다.
#
# 핵심 개념:
# 1. 내림차순 정렬: 점수가 높은 순서대로 배열 재정렬 (scores.sort(reverse=True))
# 2. 0-based Indexing: Python 리스트 인덱스는 0부터 시작하므로
#    1등은 index 0, 2등은 index 1 ... k등은 index k - 1
#
# 접근법:
# 1. N, k 및 점수 리스트 입력
# 2. 점수 리스트를 reverse=True 파라미터로 내림차순 정렬
# 3. k등에 해당하는 index (k - 1)의 값을 출력
#
# 핵심 사고:
# 1번 문제(최소/최대)와 달리 'k번째' 순위 값을 구하려면
# 순서 기준이 명확해야 하므로 정렬(O(N log N))을 활용한다.
#
# 핵심 플로우:
# N, k 입력 -> 점수 입력 -> 내림차순 정렬 -> index (k-1) 접근 -> 출력
#
# 핵심 키워드:
# Cutline / Reverse Sort / O(N log N) / 0-based Index / k-1 Index

N, k = map(int, input().split())
scores = list(map(int, input().split()))

# 내림차순 정렬
scores.sort(reverse=True)

# k번째 점수(k-1 인덱스) 출력
print(scores[k - 1])
