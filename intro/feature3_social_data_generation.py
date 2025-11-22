"""
핵심 기능 3: 소셜 피드 & 레시피 공유
음식 공유 문화 및 UGC 선호도 데이터 생성

실제 Instagram API는 제한이 많으므로, 공개된 통계와 트렌드 데이터를 기반으로
샘플 데이터를 생성합니다.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# 출력 디렉토리
OUTPUT_DIR = r"C:\Users\ASUS\Desktop\DATATON\intro"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 60)
print("소셜 미디어 음식 공유 문화 데이터 생성")
print("=" * 60)

# 1. 해시태그 성장 추이 데이터 (2019-2024)
# 실제 Instagram 트렌드를 기반으로 한 추정 데이터

hashtag_data = []

# 분석할 해시태그들
hashtags = {
    '#koreanfood': {
        'base': 5000000,  # 2019년 기준 게시물 수
        'growth_rate': 1.25  # 연평균 25% 성장
    },
    '#homecooking': {
        'base': 8000000,
        'growth_rate': 1.35  # 팬데믹 이후 급증
    },
    '#cookingathome': {
        'base': 3000000,
        'growth_rate': 1.40  # 팬데믹 영향으로 높은 성장
    },
    '#kfood': {
        'base': 1000000,
        'growth_rate': 1.45  # 한류 영향으로 급성장
    },
    '#koreanrecipe': {
        'base': 500000,
        'growth_rate': 1.30
    },
    '#foodstagram': {
        'base': 20000000,
        'growth_rate': 1.15  # 이미 대중화
    }
}

# 연도별 데이터 생성
years = range(2019, 2025)
for year in years:
    for hashtag, info in hashtags.items():
        years_passed = year - 2019
        
        # 성장 공식: base * (growth_rate ^ years_passed)
        post_count = int(info['base'] * (info['growth_rate'] ** years_passed))
        
        # 약간의 노이즈 추가 (±5%)
        noise = np.random.uniform(0.95, 1.05)
        post_count = int(post_count * noise)
        
        hashtag_data.append({
            'year': year,
            'hashtag': hashtag,
            'post_count': post_count,
            'growth_rate': info['growth_rate']
        })

hashtag_df = pd.DataFrame(hashtag_data)

# 연도별 성장률 계산
hashtag_df = hashtag_df.sort_values(['hashtag', 'year'])
hashtag_df['year_over_year_growth'] = hashtag_df.groupby('hashtag')['post_count'].pct_change() * 100

print(f"\n✓ 해시태그 트렌드 데이터 생성: {len(hashtag_df)}개 데이터포인트")

# 2. 사용자 행동 패턴 데이터
print("\n음식 공유 행동 패턴 데이터 생성 중...")

# MZ세대 vs 기타 세대 비교
user_behavior_data = []

age_groups = [
    {'group': '20-30대 (MZ)', 'ratio': 0.68},  # MZ세대가 더 활발
    {'group': '30-40대', 'ratio': 0.52},
    {'group': '40대 이상', 'ratio': 0.35}
]

behavior_types = [
    '음식 사진 업로드 (월간)',
    '요리 과정 공유',
    '레시피 저장',
    '음식 게시물 좋아요',
    '음식 관련 댓글',
    '레시피 공유'
]

for age_group in age_groups:
    for behavior in behavior_types:
        # 기본 빈도에 세대별 비율 적용
        base_frequency = {
            '음식 사진 업로드 (월간)': 8,
            '요리 과정 공유': 3,
            '레시피 저장': 12,
            '음식 게시물 좋아요': 25,
            '음식 관련 댓글': 6,
            '레시피 공유': 4
        }
        
        frequency = int(base_frequency[behavior] * age_group['ratio'])
        
        user_behavior_data.append({
            'age_group': age_group['group'],
            'behavior': behavior,
            'monthly_frequency': frequency
        })

behavior_df = pd.DataFrame(user_behavior_data)

print(f"✓ 사용자 행동 패턴 데이터 생성: {len(behavior_df)}개 데이터포인트")

# 3. UGC vs 전문가 콘텐츠 참여도 비교
print("\nUGC vs 전문가 콘텐츠 참여도 데이터 생성 중...")

content_comparison = []

# 100개 게시물 샘플 (50개씩)
for i in range(100):
    if i < 50:  # UGC (일반인)
        content_type = 'UGC'
        avg_likes = np.random.normal(2500, 800)  # 평균 2500, 표준편차 800
        avg_comments = np.random.normal(45, 15)
        avg_saves = np.random.normal(180, 50)
        trust_score = np.random.uniform(7.5, 9.5)  # 10점 만점
    else:  # 전문가 (셰프, 요리사)
        content_type = 'Professional'
        avg_likes = np.random.normal(3200, 1000)  # 좋아요는 더 많지만
        avg_comments = np.random.normal(35, 12)  # 댓글은 더 적음
        avg_saves = np.random.normal(220, 60)
        trust_score = np.random.uniform(6.0, 8.0)  # 신뢰도는 낮음
    
    content_comparison.append({
        'content_type': content_type,
        'likes': max(0, int(avg_likes)),
        'comments': max(0, int(avg_comments)),
        'saves': max(0, int(avg_saves)),
        'trust_score': round(trust_score, 1),
        'engagement_rate': round((avg_comments / avg_likes * 100), 2)
    })

comparison_df = pd.DataFrame(content_comparison)

print(f"✓ 콘텐츠 비교 데이터 생성: {len(comparison_df)}개 샘플")

# 4. 공유 동기 설문 데이터
print("\n음식 공유 동기 설문 데이터 생성 중...")

motivations = {
    '자기표현 / 성취감': 42,
    '다른 사람과 공유하고 싶어서': 28,
    '피드백을 받고 싶어서': 15,
    '기록 목적': 10,
    '기타': 5
}

motivation_data = []
for motivation, percentage in motivations.items():
    motivation_data.append({
        'motivation': motivation,
        'percentage': percentage,
        'respondents': int(300 * percentage / 100)  # 300명 설문 기준
    })

motivation_df = pd.DataFrame(motivation_data)

print(f"✓ 공유 동기 데이터 생성: {len(motivation_df)}개 카테고리")

# 5. 커뮤니티 상호작용 효과
print("\n커뮤니티 상호작용 효과 데이터 생성 중...")

interaction_data = []

# 100명의 사용자 시뮬레이션
for user_id in range(1, 101):
    # 받은 참여도 (좋아요 + 댓글)
    engagement_received = np.random.randint(10, 200)
    
    # 참여도에 따른 다음 게시물 확률
    # 높은 참여도를 받으면 다음 게시 확률 증가
    if engagement_received > 100:
        next_post_prob = 0.85
        days_to_next = np.random.randint(3, 10)
    elif engagement_received > 50:
        next_post_prob = 0.65
        days_to_next = np.random.randint(7, 20)
    else:
        next_post_prob = 0.35
        days_to_next = np.random.randint(15, 40)
    
    will_post_again = np.random.random() < next_post_prob
    
    interaction_data.append({
        'user_id': user_id,
        'engagement_received': engagement_received,
        'will_post_again': will_post_again,
        'days_to_next_post': days_to_next if will_post_again else None
    })

interaction_df = pd.DataFrame(interaction_data)

print(f"✓ 커뮤니티 효과 데이터 생성: {len(interaction_df)}명 사용자")

# 모든 데이터 저장
print(f"\n{'='*60}")
print("데이터 저장 중...")
print(f"{'='*60}")

hashtag_path = os.path.join(OUTPUT_DIR, 'feature3_hashtag_trends.csv')
behavior_path = os.path.join(OUTPUT_DIR, 'feature3_user_behavior.csv')
comparison_path = os.path.join(OUTPUT_DIR, 'feature3_ugc_vs_professional.csv')
motivation_path = os.path.join(OUTPUT_DIR, 'feature3_sharing_motivation.csv')
interaction_path = os.path.join(OUTPUT_DIR, 'feature3_community_interaction.csv')

hashtag_df.to_csv(hashtag_path, index=False, encoding='utf-8-sig')
behavior_df.to_csv(behavior_path, index=False, encoding='utf-8-sig')
comparison_df.to_csv(comparison_path, index=False, encoding='utf-8-sig')
motivation_df.to_csv(motivation_path, index=False, encoding='utf-8-sig')
interaction_df.to_csv(interaction_path, index=False, encoding='utf-8-sig')

print(f"\n✓ 저장 완료:")
print(f"  1. {hashtag_path}")
print(f"  2. {behavior_path}")
print(f"  3. {comparison_path}")
print(f"  4. {motivation_path}")
print(f"  5. {interaction_path}")

# 데이터 미리보기
print(f"\n{'='*60}")
print("[해시태그 트렌드 미리보기]")
print(f"{'='*60}")
print(hashtag_df.head(10))

print(f"\n{'='*60}")
print("[UGC vs 전문가 콘텐츠 평균 비교]")
print(f"{'='*60}")
print(comparison_df.groupby('content_type').mean())

print("\n데이터 생성 완료!")
