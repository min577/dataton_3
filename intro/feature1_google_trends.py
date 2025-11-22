"""
핵심 기능 1: K-콘텐츠 영상 숏폼 + 자동 음식 태깅
Google Trends 데이터
"""

from pytrends.request import TrendReq
import pandas as pd
import time
from datetime import datetime, timedelta
import os

# 출력 디렉토리 설정
OUTPUT_DIR = r"C:\Users\ASUS\Desktop\DATATON\intro"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# pytrends 초기화
pytrends = TrendReq(hl='en-US', tz=360)

# 분석할 K-콘텐츠와 관련 한식 키워드 쌍
content_food_pairs = [
    {
        'content': 'Squid Game',
        'food': 'dalgona candy',
        'release_date': '2021-09-17',
        'timeframe': '2021-08-01 2022-02-28'
    },
    {
        'content': 'Culinary Class Wars',
        'food': 'Korean cooking',
        'release_date': '2024-09-17',
        'timeframe': '2024-08-01 2024-11-30'
    },
    {
        'content': 'Itaewon Class',
        'food': 'Korean street food',
        'release_date': '2020-01-31',
        'timeframe': '2020-01-01 2020-06-30'
    },
    {
        'content': 'Parasite',
        'food': 'Jjapaguri',
        'release_date': '2019-05-21',
        'timeframe': '2019-05-01 2020-02-28'
    }
]

print("=" * 60)
print("K-콘텐츠와 한식 검색 트렌드 상관관계 분석")
print("=" * 60)

all_results = []

for idx, pair in enumerate(content_food_pairs, 1):
    print(f"\n[{idx}/{len(content_food_pairs)}] 분석 중: {pair['content']} → {pair['food']}")
    
    try:
        # 각 콘텐츠-음식 쌍에 대한 트렌드 데이터 수집
        kw_list = [pair['content'], pair['food']]
        
        pytrends.build_payload(
            kw_list,
            cat=0,
            timeframe=pair['timeframe'],
            geo='',  # Worldwide
            gprop=''
        )
        
        # Interest over time 데이터 가져오기
        interest_over_time = pytrends.interest_over_time()
        
        if not interest_over_time.empty:
            # 데이터프레임에 메타 정보 추가
            interest_over_time['content_name'] = pair['content']
            interest_over_time['food_name'] = pair['food']
            interest_over_time['release_date'] = pair['release_date']
            
            all_results.append(interest_over_time)
            
            print(f"   ✓ 데이터 수집 완료: {len(interest_over_time)} 행")
        else:
            print(f"   ✗ 데이터 없음")
        
        # API 제한 회피를 위한 대기
        time.sleep(5)
        
    except Exception as e:
        print(f"   ✗ 오류 발생: {str(e)}")
        time.sleep(10)
        continue

# 모든 결과 통합
if all_results:
    final_df = pd.concat(all_results, ignore_index=False)
    
    # CSV 저장
    output_path = os.path.join(OUTPUT_DIR, 'feature1_google_trends_data.csv')
    final_df.to_csv(output_path, encoding='utf-8-sig')
    
    print(f"\n{'=' * 60}")
    print(f"✓ 데이터 저장 완료: {output_path}")
    print(f"총 {len(final_df)} 행의 데이터 수집")
    print(f"{'=' * 60}")
    
    # 데이터 미리보기
    print("\n[데이터 미리보기]")
    print(final_df.head(10))
    
    # 기본 통계
    print("\n[기본 통계]")
    print(final_df.describe())
else:
    print("\n✗ 수집된 데이터가 없습니다.")

print("\n분석 완료!")
