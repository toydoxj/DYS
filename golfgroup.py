import pandas as pd
from itertools import combinations
import numpy as np

# 데이터를 로드합니다 (예시로 CSV 파일로 로드)
data = pd.read_csv('golf_group_data.csv', index_col=0)

# 참가자 리스트 생성
participants = set()
for date in data.columns:
    for group in data.index:
        members = data.loc[group, date]
        if pd.notna(members):
            participants.update([member.strip() for member in members.split(',')])
participants = sorted(participants)

# 매트릭스 초기화
matrix = pd.DataFrame(np.zeros((len(participants), len(participants))), index=participants, columns=participants)

# 각 날짜별 조편성을 분석하여 같은 조에 있었던 참가자 쌍을 매트릭스에 반영
for date in data.columns:
    for group in data.index:
        members = data.loc[group, date]
        if pd.notna(members):
            members_list = [member.strip() for member in members.split(',') if member.strip() != '']  # 공백 제거 및 빈 값 필터링
            for pair in combinations(members_list, 2):
                matrix.loc[pair[0], pair[1]] += 1
                matrix.loc[pair[1], pair[0]] += 1

# 매트릭스에서 '게스트' 제외
filtered_matrix = matrix.drop(index='게스트', errors='ignore').drop(columns='게스트', errors='ignore')

# 가장 숫자가 큰 조합 찾기
max_value = filtered_matrix.values.max()
max_pairs = [(row, col) for row, col in zip(*np.where(filtered_matrix.values == max_value))]
max_pairs = [(filtered_matrix.index[row], filtered_matrix.columns[col]) for row, col in max_pairs]

print(f"'게스트'를 제외하고 가장 많이 같은 조였던 참가자 쌍: {max_pairs}, 횟수: {max_value}")

# 3번 이상 같은 조였던 참가자 쌍 찾기 (4번, 3번 구분)
pairs_4_times = [(row, col) for row, col in zip(*np.where(filtered_matrix.values == 4))]
pairs_4_times = [(filtered_matrix.index[row], filtered_matrix.columns[col]) for row, col in pairs_4_times]

pairs_3_times = [(row, col) for row, col in zip(*np.where(filtered_matrix.values == 3))]
pairs_3_times = [(filtered_matrix.index[row], filtered_matrix.columns[col]) for row, col in pairs_3_times]

print(f"4번 같은 조였던 참가자 쌍: {pairs_4_times}")
print(f"3번 같은 조였던 참가자 쌍: {pairs_3_times}")

# '게스트'와 같은 조가 많이 되었던 참가자 상위 5명 찾기
guest_counts = matrix.loc['게스트'].drop(index='게스트', errors='ignore').sort_values(ascending=False).head(10)
print(f"'게스트'와 같은 조가 많이 되었던 참가자 상위 10명: {guest_counts}")

# 매트릭스를 CSV 파일로 저장
matrix.to_csv('golf_pair_matrix.csv')

print("각 참가자가 몇 번 같은 조였는지 매트릭스 형태로 저장되었습니다.")