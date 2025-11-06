import json
import os
import pandas as pd

# json 파일이 위치한 폴더 경로
folder_path = 'C:/CODING/R/R_TeamProject/Laliga_10_21'

# 폴더 내 모든 json 파일 목록 가져오기
json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]

# 빈 데이터프레임 생성
df_all = pd.DataFrame()

# 각 json 파일 처리
for json_file in json_files:
    file_path = os.path.join(folder_path, json_file)

    # json 파일 로드
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # DataFrame 변환
    df = pd.DataFrame(data)

    # 원하는 항목만 추출
    df['home_team_name'] = df['home_team'].apply(lambda x: x['home_team_name'])
    df['away_team_name'] = df['away_team'].apply(lambda x: x['away_team_name'])
    df['competition_name'] = df['competition'].apply(lambda x: x['competition_name'])
    df['season_name'] = df['season'].apply(lambda x: x['season_name'])

    columns_to_display = ['match_id',
                          'match_date',
                          'kick_off',
                          'competition_name',
                          'season_name',
                          'home_team_name',
                          'away_team_name',
                          'home_score',
                          'away_score',
                          'match_status',
                          'stadium'
                          ]
    df_selected = df[columns_to_display]

    # 모든 파일의 데이터를 하나로 합치기
    df_all = pd.concat([df_all, df_selected], ignore_index=True)

# match_id 기준 오름차순 정렬
df_all = df_all.sort_values(by='match_id', ascending=True)

# CSV 파일 저장
output_path = 'C:/CODING/R/R_TeamProject/Laliga_10_21/laliga.csv'
df_all.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"모든 JSON 파일이 처리되어 CSV 파일로 저장되었습니다: {output_path}")