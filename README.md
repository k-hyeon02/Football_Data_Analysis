# Python을 이용한 축구 데이터 분석 (Football Data Analysis)

경희대학교 물리학과 정보물리학 <Info-Physics> 2024년 가을학기 3조 최종 프로젝트입니다.

## 📌 프로젝트 개요

본 프로젝트는 복잡한 JSON 형태의 축구 경기 데이터(La Liga 2010 - 2021년 경기 위주)를 Python을 사용하여 파싱하고 분석합니다.
경기 승패에 영향을 미치는 통계적으로 유의미한 요소를 식별하고, Matplotlib 및 Seaborn을 활용하여 전술적 인사이트를 시각화하는 것을 목표로 합니다.

## ✨ 주요 기능

* **전술 시각화**:
    * 패스 네트워크 (Pass Networks)
    * 슛 맵 (Shot Maps)
    * 이벤트 체인 (Event Chains)
* **다수 경기 비교 분석**:
    * 승리팀/패배팀 간의 비교 히트맵 (패스, 슛, 턴오버)
    * 주요 지표 분포 그래프
* **통계 검증**:
    * 주요 지표(유효슛, 점유율, 턴오버 등)에 대한 T-test (Independent t-test) 수행

## 📊 주요 결과 (분석 인사이트)

* 공격 진영에서의 점유율, 유효슛, 패스 수를 높이는 것이 승리에 유리함을 통계적으로 확인
* 승리팀은 패배팀보다 패널티 박스 안쪽에서의 슛 빈도가 높게 나타남
* 승리팀은 패배팀에 비해 더 적은 턴오버를 기록했으며, 이는 경기 승패에 유의미한 차이를 보임

## 🚀 실행 방법

### 1. 레포지토리 복제

git clone https://github.com/your-username/Football_Data_Analysis.git
cd Football_Data_Analysis

### 2. 필요 라이브러리 설치

```bash
pip install -r requirements.txt
```

### 3. 데이터

Note: 본 레포지토리에는 용량 문제로 원본 데이터 파일이 포함되어 있지 않습니다.

원본 데이터는 StatsBomb Open Data에서 제공하며, 아래 GitHub 레포지토리에서 확인 및 다운로드할 수 있습니다. https://github.com/statsbomb/open-data

데이터를 다운로드한 후, data/events 및 data/lineups 폴더 구조에 맞게 위치시켜야 합니다.

프로젝트에서 활용한 La Liga 2010 ~ 2021 데이터는 `Laliga_10_21` 폴더에 위치합니다.

### 4. script 실행
* 단일 경기 분석(single_final.py) - (ex. ID: 3773457)
  ```bash
  python single_final.py
  ```
* 다수 경기 분석(multi_final.py)
  ```bash
  python multi_final.py
  
## 📁 프로젝트 구조
```bash
Football-Data-Analysis/
│
├── README.md           # 프로젝트 설명
├── requirements.txt    # 필요 라이브러리
│
├── single_final.py     # 단일 경기 분석 스크립트
├── multi_final.py      # 다수 경기 분석 스크립트
│
├── module/             # 분석용 헬퍼 함수 모듈
│   ├── eventchain_map.py:      # 슛 이벤트와 직전의 키 패스(key pass)를 추적하여 공격 과정을 시각화
│   ├── heatmap.py:             # 패스, 슛 등의 위치 데이터를 12x8 그리드로 비닝(binning)하여 히트맵 생성
│   ├── match_table.py:         # 단일 경기의 'Match Statistics' 및 'Most Player' 통계 테이블 생성
│   ├── pass_networkmap_def.py: # 선수 간의 패스 횟수를 기반으로 '패스 네트워크' 시각화
│   ├── shot_map_def.py:        # 팀의 모든 슛 이벤트를 득점/유효슛/빗나간슛으로 구분하여 '슛 맵' 생성
│   └── turnovermap.py:         # 실패한 패스, 듀얼 패배 등 '턴오버' 발생 위치를 유형별로 시각화
│
├── data/               # 원본 데이터 (JSON) - (직접 구성 필요)
│   ├── events/
│   ├── lineups/
│   └── matches/
│
├── Laliga_10_21       # 스페인 라리가 2010~2021 경기 데이터 - 다수 경기 분석에 활용
│
│
└── presentation/       # 최종 발표 자료
    └── football_analysis.pdf
