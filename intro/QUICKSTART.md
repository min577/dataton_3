# 🚀 빠른 실행 가이드

## 단계별 실행 방법

### STEP 1: 파일 다운로드 및 설치
```bash
# 1. 모든 파일을 C:\Users\ASUS\Desktop\DATATON\intro\ 에 저장

# 2. 명령 프롬프트(CMD) 또는 PowerShell 열기

# 3. 디렉토리 이동
cd C:\Users\ASUS\Desktop\DATATON\intro

# 4. 필요한 패키지 설치
pip install -r requirements.txt
```

### STEP 2: 데이터 수집 (한 번에 실행)
```bash
# 핵심 기능 1: K-콘텐츠 검색 트렌드 수집
python feature1_google_trends.py

# 핵심 기능 2: 재료 대체 질문 데이터 생성
python feature2_reddit_manual.py

# 핵심 기능 3: 소셜 미디어 데이터 생성
python feature3_social_data_generation.py
```

### STEP 3: 데이터 분석 (한 번에 실행)
```bash
# 핵심 기능 1 분석
python feature1_analysis.py

# 핵심 기능 2 분석
python feature2_analysis.py

# 핵심 기능 3 분석
python feature3_analysis.py
```

### STEP 4: 결과 확인
```
C:\Users\ASUS\Desktop\DATATON\intro\
├── *.csv (데이터 파일들)
└── visualizations\ (시각화 차트들)
```

## ⏱️ 예상 소요 시간
- 패키지 설치: 2-3분
- 데이터 수집: 5-10분 (Google Trends API 속도에 따라)
- 데이터 분석: 2-3분
- **총 소요 시간: 약 10-15분**

## ✅ 실행 완료 후 확인사항

### 생성되어야 하는 CSV 파일 (12개)
- [x] feature1_google_trends_data.csv
- [x] feature1_analysis_summary.csv
- [x] feature2_ingredient_questions.csv
- [x] feature2_ingredient_info.csv
- [x] feature2_analysis_summary.csv
- [x] feature3_hashtag_trends.csv
- [x] feature3_user_behavior.csv
- [x] feature3_ugc_vs_professional.csv
- [x] feature3_sharing_motivation.csv
- [x] feature3_community_interaction.csv
- [x] feature3_analysis_summary.csv

### 생성되어야 하는 시각화 파일 (14개)
- [x] feature1_Squid_Game_timeline.png
- [x] feature1_Culinary_Class_Wars_timeline.png
- [x] feature1_Itaewon_Class_timeline.png
- [x] feature1_Parasite_timeline.png
- [x] feature1_comparison_analysis.png
- [x] feature2_ingredient_frequency.png
- [x] feature2_category_distribution.png
- [x] feature2_monthly_trend.png
- [x] feature2_ingredient_engagement.png
- [x] feature3_hashtag_growth.png
- [x] feature3_age_behavior.png
- [x] feature3_ugc_vs_professional.png
- [x] feature3_sharing_motivation.png
- [x] feature3_community_effect.png

## 🔍 핵심 분석 결과 미리보기

실행 후 확인할 주요 인사이트:

### 핵심 기능 1
- K-콘텐츠 공개 전후 한식 검색량 증가율
- 통계적 유의성 (p-value)
- 콘텐츠별 비교

### 핵심 기능 2
- 가장 문제되는 재료 TOP 10
- 재료 대체 질문 비율
- 카테고리별 분포

### 핵심 기능 3
- 해시태그 성장률 (2019-2024)
- MZ세대 활동량
- UGC vs 전문가 신뢰도
- 커뮤니티 피드백 효과

## 💡 Tip

모든 스크립트를 한번에 실행하려면:

**Windows (CMD):**
```bash
python feature1_google_trends.py && python feature2_reddit_manual.py && python feature3_social_data_generation.py && python feature1_analysis.py && python feature2_analysis.py && python feature3_analysis.py
```

**Windows (PowerShell):**
```powershell
python feature1_google_trends.py; python feature2_reddit_manual.py; python feature3_social_data_generation.py; python feature1_analysis.py; python feature2_analysis.py; python feature3_analysis.py
```

---

문제 발생 시 README.md의 문제 해결 섹션을 참고하세요!
