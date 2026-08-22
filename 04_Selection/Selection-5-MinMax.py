# 8/22 훕코마 - Selection Problem
# 백준 10818번: 최소, 최대
#
# 핵심내용:
# N개의 정수가 주어졌을 때, 최솟값과 최댓값을 구하는 가장 기초적인 선택 문제이다.
# N이 최대 1,000,000으로 크기 때문에 정렬(O(N log N)) 없이
# 단 한 번의 순회(O(N))만으로 최솟값과 최댓값을 찾아야 한다.
#
# 핵심 개념:
# 1. 선형 탐색 (Linear Scan): 배열의 원소를 하나씩 보며 조건 검사
# 2. 기준값 초기화: 첫 번째 원소(arr[0])를 min, max로 설정하여
#    임의의 극단값(infinity)을 주지 않고도 직관적으로 초기화
#
# 접근법:
# 1. N과 N개의 정수 리스트 입력
# 2. min_value와 max_value를 모두 첫 번째 원소(arr[0])로 설정
# 3. 배열 전체를 반복문으로 돌며 min_value보다 작으면 갱신,
#    max_value보다 크면 갱신
# 4. 최종 min_value, max_value 출력
#
# 핵심 사고:
# 전체 정렬(O(N log N))이 필요한 문제인지,
# 단지 최소/최대만 찾으면 되는 문제(O(N))인지를 구분하는 감각을 기른다.
#
# 핵심 플로우:
# 입력 받기 -> arr[0] 기준 설정 -> 배열 1회 순회하며 min/max 갱신 -> 출력
#
# 핵심 키워드:
# Selection Problem / Linear Scan / O(N) / Min-Max / Initialization

N = int(input())
arr = list(map(int, input().split()))

min_value = arr[0]
max_value = arr[0]

for x in arr:
    if x < min_value:
        min_value = x
    if x > max_value:
        max_value = x

print(min_value, max_value)
