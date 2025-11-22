# K-Food App Market Research - Data Analysis Project

## 프로젝트 개요
외국인 20-30대를 타겟으로 하는 K-Food 앱의 시장 조사 및 데이터 분석 프로젝트

## 타겟
**한류 컨텐츠와 한식을 좋아하며 온라인으로 한국을 경험해보고 싶은 20-30대 외국인 (MZ세대)**

## 프로젝트 구조

```
C:\Users\ASUS\Desktop\DATATON\intro\
├── 00_setup_environment.bat       # 가상환경 및 라이브러리 설치 스크립트
├── 01_data_collection.py          # 데이터 수집 및 CSV 생성
├── 02_data_visualization.py       # 데이터 시각화 (차트 생성)
├── 03_main_intro_analysis.py      # Main Intro 종합 분석
├── data_*.csv                     # 생성된 데이터 파일들
├── viz_*.png                      # 생성된 시각화 파일들
└── MARKET_RESEARCH_SUMMARY.txt    # 분석 요약 보고서
```

## 설치 및 실행 방법

### 1단계: 환경 설정
```bash
# 프로젝트 폴더로 이동
cd C:\Users\ASUS\Desktop\DATATON\intro

# 가상환경 설정 스크립트 실행
00_setup_environment.bat
```

이 스크립트는 다음을 자동으로 수행합니다:
- Python 가상환경 생성 (venv)
- 필요한 라이브러리 설치:
  - pandas, numpy (데이터 처리)
  - matplotlib, seaborn, plotly (시각화)
  - pytrends, requests, beautifulsoup4 (데이터 수집)
  - scikit-learn, jupyter (분석 도구)

### 2단계: 데이터 수집
```bash
# 가상환경 활성화
venv\Scripts\activate

# 데이터 수집 스크립트 실행
python 01_data_collection.py
```

**생성되는 CSV 파일:**
1. `data_k_culture_influence.csv` - K-Culture 글로벌 영향력
2. `data_k_food_exports.csv` - K-Food 수출 통계
3. `data_korea_visitors_age.csv` - 한국 방문 외국인 연령대별 통계
4. `data_mz_digital_behavior.csv` - MZ세대 디지털 행동 패턴
5. `data_social_media_trends.csv` - 소셜미디어 한식 트렌드
6. `data_k_content_viewership.csv` - K-Content 시청률
7. `data_google_trends_korea_food.csv` - Google Trends 검색 데이터
8. `data_regional_k_food_interest.csv` - 지역별 한식 관심도
9. `data_k_food_restaurants_global.csv` - 글로벌 한식당 확장

### 3단계: 데이터 시각화
```bash
python 02_data_visualization.py
```

**생성되는 시각화 파일:**
1. `viz_01_k_culture_influence.png` - K-Culture 영향력 차트
2. `viz_02_k_food_exports.png` - K-Food 수출 트렌드
3. `viz_03_visitors_age_distribution.png` - 방문객 연령 분포
4. `viz_04_mz_digital_behavior.png` - MZ세대 디지털 행동
5. `viz_05_social_media_trends.png` - 소셜미디어 트렌드
6. `viz_06_google_trends_analysis.png` - Google 검색 트렌드
7. `viz_07_regional_interest.png` - 지역별 관심도
8. `viz_08_comprehensive_dashboard.png` - 종합 대시보드

### 4단계: Main Intro 분석
```bash
python 03_main_intro_analysis.py
```

이 스크립트는 프레젠테이션용 Main Intro를 위한 종합 분석을 수행하며,
`MARKET_RESEARCH_SUMMARY.txt` 파일로 결과를 저장합니다.

## 분석 구조

### 1. 왜 외국인인가? (K-Culture의 글로벌 영향력)
- K-pop 팬 규모 및 성장률
- 한류 문화 수출액
- 주요 콘텐츠 성과 (오징어 게임, 기생충, 흑백요리사)
- 경제적 파급효과

### 2. 왜 '식' 문화여야 하는가? (K-Food 글로벌 열풍)
- K-Food 수출 통계 및 시장 규모
- 해외 한식당 수 증가 추이
- 소셜미디어 지표 (Instagram, TikTok 해시태그)
- Google Trends 검색량 분석

### 3. 왜 MZ 세대인가?
- 압도적인 시장 규모 (외국인 방문객의 35.6%)
- 연령대별 방문객 통계
- 앱 기반 솔루션의 최적 타겟
- 스마트폰/앱 사용률
- 경험 소비 주도층

### 4. 디지털 매체를 통한 MZ 세대의 한국 관심도
- 한류 연관 검색어 분석
- Korea + Food 조합 검색량
- MZ세대 SNS 행동 패턴
- 먹방/쿡방 예능 인기

## 주요 데이터 출처

- Korea Tourism Organization (KTO)
- Ministry of Agriculture, Food and Rural Affairs (MAFRA)
- Korea Foundation for International Cultural Exchange (KOFICE)
- Statista
- Google Trends
- Instagram/TikTok/YouTube 소셜미디어 데이터
- Bloomberg, UN Trade and Development

## 분석 결과 활용

생성된 CSV 파일과 시각화 이미지는 다음과 같이 활용할 수 있습니다:

1. **프레젠테이션**: PNG 이미지를 PPT에 삽입
2. **보고서**: CSV 데이터를 Excel로 추가 분석
3. **대시보드**: Plotly/Tableau로 인터랙티브 대시보드 구축
4. **추가 분석**: Jupyter Notebook으로 심화 분석

## 향후 작업

실제 Google Trends API를 사용한 실시간 데이터 수집을 원하신다면:

```python
# pytrends를 사용한 실제 데이터 수집 예시
from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360)
keywords = ['Korean food', 'K-food', 'Kimchi', 'Korean BBQ']
pytrends.build_payload(keywords, timeframe='2015-01-01 2024-12-31')
data = pytrends.interest_over_time()
```

## 문의사항

프로젝트 관련 문의사항이나 추가 분석이 필요한 경우 연락 주세요.

---
**Created**: 2025-01-14
**Target**: Foreign 20-30s MZ Generation K-content & K-food lovers
**Purpose**: Market Research for K-Food Recipe Sharing App
