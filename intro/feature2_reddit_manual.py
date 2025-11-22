"""
핵심 기능 2: AI 현지화 - 수동 데이터 버전
Reddit API 없이 미리 정의된 재료 대체 질문 데이터 생성

실제 r/KoreanFood에서 자주 나오는 질문 패턴을 기반으로 샘플 데이터 생성
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# 출력 디렉토리
OUTPUT_DIR = r"C:\Users\ASUS\Desktop\DATATON\intro"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 60)
print("한식 재료 대체 질문 샘플 데이터 생성")
print("=" * 60)

# 실제 r/KoreanFood에서 자주 나오는 재료 대체 질문들
sample_questions = [
    # 고추장 관련
    {
        'ingredient': 'gochujang',
        'category': '장류',
        'questions': [
            'What can I substitute for gochujang in tteokbokki?',
            'Gochujang alternative for non-spicy version?',
            'Can I use sriracha instead of gochujang?',
            'Where to buy gochujang in small towns?',
            'How to make gochujang at home?'
        ]
    },
    # 고춧가루
    {
        'ingredient': 'gochugaru',
        'category': '양념',
        'questions': [
            'Substitute for gochugaru in kimchi?',
            'Can I use regular chili flakes instead of gochugaru?',
            'Gochugaru vs cayenne pepper - can I substitute?',
            'Where to find Korean red pepper flakes?',
            'Best gochugaru alternative for kimchi jjigae?'
        ]
    },
    # 된장
    {
        'ingredient': 'doenjang',
        'category': '장류',
        'questions': [
            'What is a good substitute for doenjang?',
            'Can I use miso instead of doenjang?',
            'Doenjang replacement in doenjang jjigae?',
            'Where to buy fermented soybean paste?',
            'Difference between doenjang and miso - can I swap?'
        ]
    },
    # 참기름
    {
        'ingredient': 'sesame oil',
        'category': '오일',
        'questions': [
            'Can I substitute toasted sesame oil with regular sesame oil?',
            'Sesame oil alternative for Korean food?',
            'Where to find authentic Korean sesame oil?',
            'Can I skip sesame oil in bibimbap?',
            'Best sesame oil brand for Korean cooking?'
        ]
    },
    # 떡
    {
        'ingredient': 'rice cake',
        'category': '곡물',
        'questions': [
            'Where can I buy Korean rice cakes?',
            'Can I make tteokbokki without rice cakes?',
            'Rice cake substitute for tteokbokki?',
            'How to find frozen rice cakes?',
            'Alternative to garaetteok?'
        ]
    },
    # 김치
    {
        'ingredient': 'kimchi',
        'category': '발효식품',
        'questions': [
            'Can I make kimchi jjigae without kimchi?',
            'Where to buy good quality kimchi?',
            'Kimchi substitute in Korean recipes?',
            'How to find authentic kimchi in US?',
            'Can I use sauerkraut instead of kimchi?'
        ]
    },
    # 다시마
    {
        'ingredient': 'dashima',
        'category': '건어물',
        'questions': [
            'Substitute for dashima in Korean soup?',
            'Can I use kombu instead of dashima?',
            'Where to buy dried kelp for Korean cooking?',
            'Dashima alternative for broth?',
            'Is dashima necessary for doenjang jjigae?'
        ]
    },
    # 멸치
    {
        'ingredient': 'dried anchovies',
        'category': '건어물',
        'questions': [
            'Substitute for dried anchovies in Korean broth?',
            'Can I skip anchovies in tteokbokki?',
            'Where to find myeolchi for stock?',
            'Alternative to anchovy broth?',
            'Can I use fish sauce instead of anchovies?'
        ]
    },
    # 쌈장
    {
        'ingredient': 'ssamjang',
        'category': '장류',
        'questions': [
            'How to make ssamjang without doenjang?',
            'Ssamjang substitute for Korean BBQ?',
            'Can I mix gochujang and miso for ssamjang?',
            'Where to buy ssamjang?',
            'Alternative sauce for ssam?'
        ]
    },
    # 청주
    {
        'ingredient': 'cooking wine',
        'category': '주류',
        'questions': [
            'Substitute for Korean cooking wine?',
            'Can I use sake instead of cheongju?',
            'Where to find mirin for Korean cooking?',
            'Is cooking wine necessary in Korean recipes?',
            'Cheongju alternative in marinades?'
        ]
    }
]

# 데이터 생성
posts_data = []
post_id_counter = 1000

for item in sample_questions:
    ingredient = item['ingredient']
    category = item['category']
    
    for question in item['questions']:
        # 랜덤 날짜 (최근 2년 내)
        days_ago = np.random.randint(1, 730)
        created_date = datetime.now() - timedelta(days=days_ago)
        
        # 랜덤 점수 및 댓글 수
        score = np.random.randint(5, 150)
        num_comments = np.random.randint(3, 50)
        
        posts_data.append({
            'post_id': f't3_{post_id_counter}',
            'title': question,
            'selftext': f'I\'m trying to make Korean food but can\'t find {ingredient} locally. Any suggestions?',
            'author': f'user_{np.random.randint(1, 1000)}',
            'created_utc': created_date,
            'score': score,
            'num_comments': num_comments,
            'ingredient': ingredient,
            'category': category,
            'is_substitute_related': True
        })
        
        post_id_counter += 1

# 추가 일반 게시물 (대조군)
general_posts = [
    'Best Korean restaurant in NYC?',
    'Just made my first bibimbap!',
    'How to improve my kimchi jjigae?',
    'Favorite Korean snack to buy online?',
    'Korean instant noodles recommendations?',
    'Learning to make Korean food - where to start?',
    'Best Korean cookbook for beginners?',
    'Korean food Instagram accounts to follow?',
    'How spicy is authentic Korean food?',
    'Vegetarian Korean food options?'
]

for title in general_posts:
    days_ago = np.random.randint(1, 730)
    created_date = datetime.now() - timedelta(days=days_ago)
    
    posts_data.append({
        'post_id': f't3_{post_id_counter}',
        'title': title,
        'selftext': 'I love Korean food! What do you think?',
        'author': f'user_{np.random.randint(1, 1000)}',
        'created_utc': created_date,
        'score': np.random.randint(10, 200),
        'num_comments': np.random.randint(5, 80),
        'ingredient': None,
        'category': None,
        'is_substitute_related': False
    })
    
    post_id_counter += 1

# 데이터프레임 생성
posts_df = pd.DataFrame(posts_data)

# 정렬
posts_df = posts_df.sort_values('created_utc', ascending=False).reset_index(drop=True)

print(f"\n생성된 데이터:")
print(f"  총 게시물: {len(posts_df)}개")
print(f"  재료 대체 관련: {posts_df['is_substitute_related'].sum()}개")
print(f"  일반 게시물: {(~posts_df['is_substitute_related']).sum()}개")

# CSV 저장
output_path = os.path.join(OUTPUT_DIR, 'feature2_ingredient_questions.csv')
posts_df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"\n✓ 데이터 저장: {output_path}")

# 재료별 질문 빈도 분석
print(f"\n{'='*60}")
print("재료별 질문 빈도")
print(f"{'='*60}")

ingredient_counts = posts_df[posts_df['is_substitute_related']]['ingredient'].value_counts()
print(ingredient_counts)

# 카테고리별 분석
print(f"\n{'='*60}")
print("카테고리별 질문 빈도")
print(f"{'='*60}")

category_counts = posts_df[posts_df['is_substitute_related']]['category'].value_counts()
print(category_counts)

# 카테고리-재료 매핑 저장
ingredient_info = []
for item in sample_questions:
    ingredient_info.append({
        'ingredient': item['ingredient'],
        'category': item['category'],
        'question_count': len(item['questions'])
    })

ingredient_df = pd.DataFrame(ingredient_info)
ingredient_path = os.path.join(OUTPUT_DIR, 'feature2_ingredient_info.csv')
ingredient_df.to_csv(ingredient_path, index=False, encoding='utf-8-sig')

print(f"\n✓ 재료 정보 저장: {ingredient_path}")

print("\n데이터 생성 완료!")
