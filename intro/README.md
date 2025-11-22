# 한식 앱 데이터 분석 실행 가이드

이 프로젝트는 한식 레시피 공유 앱의 3가지 핵심 기능을 위한 데이터 수집 및 분석을 수행합니다.

## 📁 프로젝트 구조

```
C:\Users\ASUS\Desktop\DATATON\intro\
├── 데이터 수집 스크립트
│   ├── feature1_google_trends.py          # 핵심 기능 1: Google Trends 수집
│   ├── feature2_reddit_collection.py      # 핵심 기능 2: Reddit 수집 (API 필요)
│   ├── feature2_reddit_manual.py          # 핵심 기능 2: 샘플 데이터 생성 (API 불필요)
│   └── feature3_social_data_generation.py # 핵심 기능 3: 소셜 데이터 생성
│
├── 데이터 분석 스크립트
│   ├── feature1_analysis.py               # 핵심 기능 1 분석
│   ├── feature2_analysis.py               # 핵심 기능 2 분석
│   └── feature3_analysis.py               # 핵심 기능 3 분석
│
├── requirements.txt                        # 필요한 패키지 목록
└── README.md                              # 이 파일
```

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# 1. Python 설치 확인 (3.8 이상)
python --version

# 2. 가상환경 생성 (선택사항)
python -m venv venv
venv\Scripts\activate  # Windows

# 3. 필요한 패키지 설치
cd C:\Users\ASUS\Desktop\DATATON\intro
pip install -r requirements.txt
```

### 2. 데이터 수집 및 분석 실행

#### 옵션 A: 모든 기능 한번에 실행 (추천)

```bash
# 데이터 수집
python feature1_google_trends.py
python feature2_reddit_manual.py
python feature3_social_data_generation.py

# 데이터 분석
python feature1_analysis.py
python feature2_analysis.py
python feature3_analysis.py
```

#### 옵션 B: 개별 기능별 실행

**핵심 기능 1: K-콘텐츠와 한식 검색 트렌드**
```bash
# 데이터 수집 (Google Trends)
python feature1_google_trends.py

# 분석 및 시각화
python feature1_analysis.py
```

**핵심 기능 2: 재료 대체 수요 분석**
```bash
# 데이터 생성 (Reddit API 불필요)
python feature2_reddit_manual.py

# 분석 및 시각화
python feature2_analysis.py
```

**핵심 기능 3: 소셜 미디어 공유 문화**
```bash
# 데이터 생성
python feature3_social_data_generation.py

# 분석 및 시각화
python feature3_analysis.py
```

## 📊 핵심 기능별 설명

### 핵심 기능 1: K-콘텐츠 영상 숏폼 + 자동 음식 태깅

**목적**: K-콘텐츠 공개 전후 한식 검색량 변화를 분석하여 콘텐츠가 한식 관심도에 미치는 영향 검증

**수집 데이터**:
- Squid Game → dalgona candy
- Culinary Class Wars → Korean cooking
- Itaewon Class → Korean street food
- Parasite → Jjapaguri

**분석 결과**:
- `feature1_google_trends_data.csv`: 원본 트렌드 데이터
- `feature1_analysis_summary.csv`: 분석 요약
- `visualizations/feature1_*.png`: 시각화 차트

**핵심 인사이트**:
- K-콘텐츠 공개 후 관련 한식 검색량 급증 패턴
- 콘텐츠별 검색량 증가율 비교
- 통계적 유의성 검증 (T-test)

### 핵심 기능 2: AI 현지화 (재료 대체 추천)

**목적**: 외국인들이 한식 조리 시 겪는 재료 접근성 문제를 정량화

**수집 데이터**:
- 50개 재료 대체 관련 질문 (10개 주요 재료 × 5개 질문)
- 재료 카테고리: 장류, 양념, 건어물, 발효식품 등

**분석 결과**:
- `feature2_ingredient_questions.csv`: 질문 데이터
- `feature2_ingredient_info.csv`: 재료별 정보
- `feature2_analysis_summary.csv`: 분석 요약
- `visualizations/feature2_*.png`: 시각화 차트

**핵심 인사이트**:
- 가장 문제되는 재료 TOP 10
- 카테고리별 질문 분포
- 재료 대체 질문 비율 (전체 게시물 대비)

### 핵심 기능 3: 소셜 피드 & 레시피 공유

**목적**: MZ세대의 음식 공유 문화와 UGC 선호도, 커뮤니티 효과 검증

**수집 데이터**:
- 해시태그 성장 추이 (2019-2024)
- 연령대별 행동 패턴
- UGC vs 전문가 콘텐츠 비교 (100개 샘플)
- 공유 동기 설문 (300명)
- 커뮤니티 상호작용 효과 (100명)

**분석 결과**:
- `feature3_hashtag_trends.csv`: 해시태그 트렌드
- `feature3_user_behavior.csv`: 사용자 행동
- `feature3_ugc_vs_professional.csv`: 콘텐츠 비교
- `feature3_sharing_motivation.csv`: 공유 동기
- `feature3_community_interaction.csv`: 커뮤니티 효과
- `feature3_analysis_summary.csv`: 분석 요약
- `visualizations/feature3_*.png`: 시각화 차트

**핵심 인사이트**:
- 한식 해시태그 성장률
- MZ세대 활동량 (다른 세대 대비)
- UGC 신뢰도 > 전문가 콘텐츠 신뢰도
- 커뮤니티 피드백이 재게시에 미치는 영향

## 📈 생성되는 파일

### CSV 데이터 파일
```
C:\Users\ASUS\Desktop\DATATON\intro\
├── feature1_google_trends_data.csv
├── feature1_analysis_summary.csv
├── feature2_ingredient_questions.csv
├── feature2_ingredient_info.csv
├── feature2_analysis_summary.csv
├── feature3_hashtag_trends.csv
├── feature3_user_behavior.csv
├── feature3_ugc_vs_professional.csv
├── feature3_sharing_motivation.csv
├── feature3_community_interaction.csv
└── feature3_analysis_summary.csv
```

### 시각화 파일
```
C:\Users\ASUS\Desktop\DATATON\intro\visualizations\
├── feature1_Squid_Game_timeline.png
├── feature1_Culinary_Class_Wars_timeline.png
├── feature1_Itaewon_Class_timeline.png
├── feature1_Parasite_timeline.png
├── feature1_comparison_analysis.png
├── feature2_ingredient_frequency.png
├── feature2_category_distribution.png
├── feature2_monthly_trend.png
├── feature2_ingredient_engagement.png
├── feature3_hashtag_growth.png
├── feature3_age_behavior.png
├── feature3_ugc_vs_professional.png
├── feature3_sharing_motivation.png
└── feature3_community_effect.png
```

## ⚠️ 주의사항

### Google Trends (핵심 기능 1)
- 무료 API이지만 너무 많은 요청 시 일시적으로 차단될 수 있음
- 스크립트에 sleep() 함수로 대기 시간 추가됨
- 차단 시 1시간 정도 대기 후 재시도

### Reddit API (핵심 기능 2)
- **Option 1**: `feature2_reddit_manual.py` 사용 (API 불필요, 추천)
  - 샘플 데이터 자동 생성
  - 실제 Reddit 질문 패턴 기반

- **Option 2**: `feature2_reddit_collection.py` 사용 (Reddit API 필요)
  - https://www.reddit.com/prefs/apps 에서 앱 생성 필요
  - CLIENT_ID와 CLIENT_SECRET 입력 필요

### 한글 폰트 설정
- Windows 기본 폰트 'Malgun Gothic' 사용
- Mac: `plt.rcParams['font.family'] = 'AppleGothic'`
- Linux: `plt.rcParams['font.family'] = 'NanumGothic'`

## 🔧 문제 해결

### 패키지 설치 오류
```bash
# pip 업그레이드
python -m pip install --upgrade pip

# 개별 설치
pip install pytrends pandas matplotlib seaborn scipy numpy
```

### 경로 오류
- 스크립트 내 `OUTPUT_DIR` 경로가 정확한지 확인
- 디렉토리 권한 확인

### 데이터 없음 오류
1. 데이터 수집 스크립트를 먼저 실행했는지 확인
2. CSV 파일이 올바른 경로에 생성되었는지 확인

## 📞 추가 도움이 필요하면

각 스크립트는 실행 중 진행 상황을 출력합니다.
오류 발생 시 출력된 메시지를 확인하세요.

---

**마지막 업데이트**: 2024-11
**작성자**: Data Analysis Team
