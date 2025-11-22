"""
핵심 기능 2: 재료 대체 수요 분석
재료 접근성 문제 정량화 및 시각화
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import Counter
import re
import os

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 디렉토리 설정
DATA_DIR = r"C:\Users\ASUS\Desktop\DATATON\intro"
OUTPUT_DIR = os.path.join(DATA_DIR, 'visualizations')
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 60)
print("재료 대체 수요 분석")
print("=" * 60)

# 데이터 로드
df = pd.read_csv(os.path.join(DATA_DIR, 'feature2_ingredient_questions.csv'))
ingredient_info = pd.read_csv(os.path.join(DATA_DIR, 'feature2_ingredient_info.csv'))

print(f"\n총 {len(df)}개 게시물 로드")
print(f"재료 대체 관련: {df['is_substitute_related'].sum()}개 ({df['is_substitute_related'].sum()/len(df)*100:.1f}%)")

# 1. 재료별 질문 빈도 분석
print(f"\n{'='*60}")
print("1. 가장 많이 질문되는 재료 TOP 10")
print(f"{'='*60}")

substitute_df = df[df['is_substitute_related']].copy()
ingredient_counts = substitute_df['ingredient'].value_counts().head(10)

print(ingredient_counts)

# 시각화 1: 재료별 질문 빈도
fig, ax = plt.subplots(figsize=(12, 6))

bars = ax.barh(range(len(ingredient_counts)), ingredient_counts.values, color='coral', edgecolor='darkred')
ax.set_yticks(range(len(ingredient_counts)))
ax.set_yticklabels(ingredient_counts.index)
ax.set_xlabel('Number of Questions', fontsize=12)
ax.set_title('Top 10 Korean Ingredients with Substitution Questions', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)

# 값 표시
for i, (bar, value) in enumerate(zip(bars, ingredient_counts.values)):
    ax.text(value + 0.1, i, f'{value}', va='center', fontsize=10)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'feature2_ingredient_frequency.png'), dpi=300)
plt.close()

print(f"\n✓ 시각화 저장: feature2_ingredient_frequency.png")

# 2. 카테고리별 분석
print(f"\n{'='*60}")
print("2. 카테고리별 질문 분포")
print(f"{'='*60}")

category_counts = substitute_df['category'].value_counts()
print(category_counts)

# 시각화 2: 카테고리별 파이차트
fig, ax = plt.subplots(figsize=(10, 8))

colors = sns.color_palette('Set2', n_colors=len(category_counts))
wedges, texts, autotexts = ax.pie(
    category_counts.values, 
    labels=category_counts.index,
    autopct='%1.1f%%',
    colors=colors,
    startangle=90
)

# 텍스트 스타일
for text in texts:
    text.set_fontsize(11)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(10)

ax.set_title('Korean Ingredient Categories with Substitution Issues', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'feature2_category_distribution.png'), dpi=300)
plt.close()

print(f"\n✓ 시각화 저장: feature2_category_distribution.png")

# 3. 시간대별 트렌드 분석
print(f"\n{'='*60}")
print("3. 시간대별 재료 대체 질문 트렌드")
print(f"{'='*60}")

substitute_df['year_month'] = pd.to_datetime(substitute_df['created_utc']).dt.to_period('M')
monthly_counts = substitute_df.groupby('year_month').size()

print(f"분석 기간: {monthly_counts.index.min()} ~ {monthly_counts.index.max()}")
print(f"월평균 질문 수: {monthly_counts.mean():.1f}개")

# 시각화 3: 월별 트렌드
fig, ax = plt.subplots(figsize=(14, 6))

x_values = [str(period) for period in monthly_counts.index]
ax.plot(x_values, monthly_counts.values, marker='o', linewidth=2, markersize=6, color='steelblue')
ax.fill_between(range(len(monthly_counts)), monthly_counts.values, alpha=0.3, color='steelblue')

ax.set_xlabel('Year-Month', fontsize=12)
ax.set_ylabel('Number of Questions', fontsize=12)
ax.set_title('Monthly Trend of Ingredient Substitution Questions', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

# x축 라벨 회전
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'feature2_monthly_trend.png'), dpi=300)
plt.close()

print(f"\n✓ 시각화 저장: feature2_monthly_trend.png")

# 4. 인기도 분석 (점수 및 댓글 수)
print(f"\n{'='*60}")
print("4. 재료별 평균 참여도 (점수 + 댓글)")
print(f"{'='*60}")

ingredient_engagement = substitute_df.groupby('ingredient').agg({
    'score': 'mean',
    'num_comments': 'mean'
}).round(1)

ingredient_engagement['total_engagement'] = ingredient_engagement['score'] + ingredient_engagement['num_comments']
ingredient_engagement = ingredient_engagement.sort_values('total_engagement', ascending=False).head(10)

print(ingredient_engagement)

# 시각화 4: 재료별 참여도
fig, ax = plt.subplots(figsize=(12, 6))

x = np.arange(len(ingredient_engagement))
width = 0.35

bars1 = ax.bar(x - width/2, ingredient_engagement['score'], width, label='Avg Score', alpha=0.8, color='skyblue')
bars2 = ax.bar(x + width/2, ingredient_engagement['num_comments'], width, label='Avg Comments', alpha=0.8, color='lightcoral')

ax.set_xlabel('Ingredient', fontsize=12)
ax.set_ylabel('Count', fontsize=12)
ax.set_title('User Engagement by Ingredient (Score + Comments)', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(ingredient_engagement.index, rotation=45, ha='right')
ax.legend()
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'feature2_ingredient_engagement.png'), dpi=300)
plt.close()

print(f"\n✓ 시각화 저장: feature2_ingredient_engagement.png")

# 5. 핵심 인사이트 정리
print(f"\n{'='*60}")
print("핵심 인사이트")
print(f"{'='*60}")

total_questions = len(substitute_df)
total_posts = len(df)
substitute_ratio = (total_questions / total_posts * 100)

print(f"\n1. 재료 접근성 문제의 심각성")
print(f"   - 전체 게시물 중 {substitute_ratio:.1f}%가 재료 대체/구매 관련 질문")
print(f"   - 이는 한식을 만들고 싶어하는 외국인들에게 재료 접근성이")
print(f"     가장 큰 장벽임을 시사")

top_3_ingredients = ingredient_counts.head(3)
print(f"\n2. 가장 문제되는 재료 TOP 3")
for idx, (ingredient, count) in enumerate(top_3_ingredients.items(), 1):
    print(f"   {idx}. {ingredient}: {count}개 질문 ({count/total_questions*100:.1f}%)")

top_category = category_counts.iloc[0]
print(f"\n3. 가장 문제되는 카테고리")
print(f"   - {category_counts.index[0]}: {top_category}개 질문 ({top_category/total_questions*100:.1f}%)")

avg_engagement = substitute_df[['score', 'num_comments']].mean()
print(f"\n4. 커뮤니티 참여도")
print(f"   - 평균 점수: {avg_engagement['score']:.1f}")
print(f"   - 평균 댓글 수: {avg_engagement['num_comments']:.1f}")
print(f"   → 재료 대체 질문은 높은 관심과 참여를 받음")

# 결과 요약 저장
summary_data = {
    'metric': [
        'Total Posts',
        'Substitution Questions',
        'Substitution Question Ratio (%)',
        'Average Score',
        'Average Comments',
        'Top Ingredient',
        'Top Category'
    ],
    'value': [
        total_posts,
        total_questions,
        f'{substitute_ratio:.1f}',
        f'{avg_engagement["score"]:.1f}',
        f'{avg_engagement["num_comments"]:.1f}',
        ingredient_counts.index[0],
        category_counts.index[0]
    ]
}

summary_df = pd.DataFrame(summary_data)
summary_path = os.path.join(DATA_DIR, 'feature2_analysis_summary.csv')
summary_df.to_csv(summary_path, index=False, encoding='utf-8-sig')

print(f"\n✓ 분석 요약 저장: feature2_analysis_summary.csv")

print("\n\n분석 완료! 모든 결과는 다음 경로에 저장되었습니다:")
print(f"  - 데이터: {DATA_DIR}")
print(f"  - 시각화: {OUTPUT_DIR}")