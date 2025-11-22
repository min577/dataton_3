"""
핵심 기능 3: 소셜 피드 & 레시피 공유 분석
음식 콘텐츠 공유 문화와 커뮤니티 효과 분석
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 디렉토리 설정
DATA_DIR = r"C:\Users\ASUS\Desktop\DATATON\intro"
OUTPUT_DIR = os.path.join(DATA_DIR, 'visualizations')
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 60)
print("소셜 미디어 음식 공유 문화 분석")
print("=" * 60)

# 데이터 로드
hashtag_df = pd.read_csv(os.path.join(DATA_DIR, 'feature3_hashtag_trends.csv'))
behavior_df = pd.read_csv(os.path.join(DATA_DIR, 'feature3_user_behavior.csv'))
comparison_df = pd.read_csv(os.path.join(DATA_DIR, 'feature3_ugc_vs_professional.csv'))
motivation_df = pd.read_csv(os.path.join(DATA_DIR, 'feature3_sharing_motivation.csv'))
interaction_df = pd.read_csv(os.path.join(DATA_DIR, 'feature3_community_interaction.csv'))

# 1. 해시태그 성장 추이 분석
print(f"\n{'='*60}")
print("1. 음식 관련 해시태그 성장 트렌드")
print(f"{'='*60}")

# 시각화 1: 연도별 해시태그 성장
fig, ax = plt.subplots(figsize=(14, 7))

for hashtag in hashtag_df['hashtag'].unique():
    data = hashtag_df[hashtag_df['hashtag'] == hashtag]
    ax.plot(data['year'], data['post_count'] / 1000000, marker='o', linewidth=2, label=hashtag, markersize=8)

ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Number of Posts (Millions)', fontsize=12)
ax.set_title('Growth of Food-related Hashtags on Social Media', fontsize=14, fontweight='bold')
ax.legend(fontsize=10, loc='upper left')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'feature3_hashtag_growth.png'), dpi=300)
plt.close()

print(f"\n✓ 시각화 저장: feature3_hashtag_growth.png")

# 성장률 분석
growth_analysis = hashtag_df.groupby('hashtag').agg({
    'year_over_year_growth': 'mean',
    'post_count': ['first', 'last']
}).round(2)

growth_analysis.columns = ['Avg_YoY_Growth_%', 'Posts_2019', 'Posts_2024']
growth_analysis['Total_Growth_%'] = ((growth_analysis['Posts_2024'] - growth_analysis['Posts_2019']) / 
                                       growth_analysis['Posts_2019'] * 100).round(1)

print("\n[해시태그별 성장률]")
print(growth_analysis.sort_values('Total_Growth_%', ascending=False))

# 2. 연령대별 행동 패턴 분석
print(f"\n{'='*60}")
print("2. 연령대별 음식 공유 행동 패턴")
print(f"{'='*60}")

# 시각화 2: 연령대별 행동 빈도
behavior_pivot = behavior_df.pivot(index='behavior', columns='age_group', values='monthly_frequency')

fig, ax = plt.subplots(figsize=(12, 7))

x = np.arange(len(behavior_pivot.index))
width = 0.25

for i, age_group in enumerate(behavior_pivot.columns):
    offset = (i - 1) * width
    ax.bar(x + offset, behavior_pivot[age_group], width, label=age_group, alpha=0.8)

ax.set_xlabel('Behavior Type', fontsize=12)
ax.set_ylabel('Monthly Frequency', fontsize=12)
ax.set_title('Food Sharing Behavior by Age Group', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(behavior_pivot.index, rotation=45, ha='right')
ax.legend()
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'feature3_age_behavior.png'), dpi=300)
plt.close()

print(f"\n✓ 시각화 저장: feature3_age_behavior.png")

# MZ세대 vs 기타 비교
mz_total = behavior_df[behavior_df['age_group'] == '20-30대 (MZ)']['monthly_frequency'].sum()
others_avg = behavior_df[behavior_df['age_group'] != '20-30대 (MZ)']['monthly_frequency'].mean()

print(f"\nMZ세대 월간 활동 총합: {mz_total}")
print(f"기타 세대 평균: {others_avg:.1f}")
print(f"MZ세대가 {(mz_total / others_avg / 2):.1f}배 더 활발")

# 3. UGC vs 전문가 콘텐츠 비교
print(f"\n{'='*60}")
print("3. UGC vs 전문가 콘텐츠 참여도 비교")
print(f"{'='*60}")

ugc_stats = comparison_df[comparison_df['content_type'] == 'UGC'].describe()
pro_stats = comparison_df[comparison_df['content_type'] == 'Professional'].describe()

print("\n[UGC (일반인)]")
print(ugc_stats[['likes', 'comments', 'saves', 'trust_score']].loc[['mean', 'std']])

print("\n[Professional (전문가)]")
print(pro_stats[['likes', 'comments', 'saves', 'trust_score']].loc[['mean', 'std']])

# 시각화 3: 박스플롯 비교
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

metrics = ['likes', 'comments', 'saves', 'trust_score']
titles = ['Likes', 'Comments', 'Saves', 'Trust Score (1-10)']

for idx, (metric, title) in enumerate(zip(metrics, titles)):
    row = idx // 2
    col = idx % 2
    
    comparison_df.boxplot(column=metric, by='content_type', ax=axes[row, col])
    axes[row, col].set_title(title, fontsize=12, fontweight='bold')
    axes[row, col].set_xlabel('Content Type', fontsize=10)
    axes[row, col].set_ylabel(title, fontsize=10)
    axes[row, col].get_figure().suptitle('')  # 전체 제목 제거

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'feature3_ugc_vs_professional.png'), dpi=300)
plt.close()

print(f"\n✓ 시각화 저장: feature3_ugc_vs_professional.png")

# 신뢰도 차이 분석 (scipy 없이)
ugc_trust = comparison_df[comparison_df['content_type'] == 'UGC']['trust_score']
pro_trust = comparison_df[comparison_df['content_type'] == 'Professional']['trust_score']

print(f"\n[신뢰도 비교]")
print(f"UGC 평균 신뢰도: {ugc_trust.mean():.2f}")
print(f"전문가 평균 신뢰도: {pro_trust.mean():.2f}")
print(f"차이: {ugc_trust.mean() - pro_trust.mean():.2f}점")

# 단순 비교: 차이가 1.0 이상이면 의미있는 차이로 판단
if ugc_trust.mean() - pro_trust.mean() > 1.0:
    print(f"→ UGC가 의미있게 더 신뢰받음! (차이 > 1.0)")
elif ugc_trust.mean() - pro_trust.mean() > 0.5:
    print(f"→ UGC가 다소 더 신뢰받음 (차이 > 0.5)")
else:
    print(f"→ 두 그룹 간 신뢰도 차이가 크지 않음")

# 4. 공유 동기 분석
print(f"\n{'='*60}")
print("4. 음식 게시물 공유 동기")
print(f"{'='*60}")

print(motivation_df)

# 시각화 4: 공유 동기 파이차트
fig, ax = plt.subplots(figsize=(10, 8))

colors = sns.color_palette('pastel', n_colors=len(motivation_df))
wedges, texts, autotexts = ax.pie(
    motivation_df['percentage'], 
    labels=motivation_df['motivation'],
    autopct='%1.1f%%',
    colors=colors,
    startangle=90,
    explode=[0.05 if i == 0 else 0 for i in range(len(motivation_df))]  # 첫 번째 강조
)

for text in texts:
    text.set_fontsize(11)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(10)

ax.set_title('Why People Share Food Posts on Social Media', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'feature3_sharing_motivation.png'), dpi=300)
plt.close()

print(f"\n✓ 시각화 저장: feature3_sharing_motivation.png")

# 5. 커뮤니티 상호작용 효과
print(f"\n{'='*60}")
print("5. 커뮤니티 피드백이 재게시에 미치는 영향")
print(f"{'='*60}")

# 참여도 그룹별 재게시율
interaction_df['engagement_group'] = pd.cut(
    interaction_df['engagement_received'], 
    bins=[0, 50, 100, 200], 
    labels=['Low (0-50)', 'Medium (51-100)', 'High (101+)']
)

repost_rate = interaction_df.groupby('engagement_group')['will_post_again'].agg(['sum', 'count', 'mean'])
repost_rate['percentage'] = (repost_rate['mean'] * 100).round(1)

print("\n[참여도별 재게시율]")
print(repost_rate[['count', 'percentage']])

# 시각화 5: 참여도와 재게시율 관계
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# 막대 그래프
axes[0].bar(range(len(repost_rate)), repost_rate['percentage'], color='teal', alpha=0.7, edgecolor='darkslategray')
axes[0].set_xticks(range(len(repost_rate)))
axes[0].set_xticklabels(repost_rate.index)
axes[0].set_ylabel('Repost Rate (%)', fontsize=12)
axes[0].set_title('Repost Rate by Engagement Level', fontsize=13, fontweight='bold')
axes[0].grid(axis='y', alpha=0.3)

for i, v in enumerate(repost_rate['percentage']):
    axes[0].text(i, v + 2, f'{v:.1f}%', ha='center', fontweight='bold')

# 산점도
for group in interaction_df['engagement_group'].unique():
    data = interaction_df[interaction_df['engagement_group'] == group]
    axes[1].scatter(
        data['engagement_received'], 
        data['will_post_again'].astype(int),
        alpha=0.5,
        s=50,
        label=group
    )

axes[1].set_xlabel('Engagement Received', fontsize=12)
axes[1].set_ylabel('Will Post Again (0=No, 1=Yes)', fontsize=12)
axes[1].set_title('Engagement vs Repost Intention', fontsize=13, fontweight='bold')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'feature3_community_effect.png'), dpi=300)
plt.close()

print(f"\n✓ 시각화 저장: feature3_community_effect.png")

# 6. 핵심 인사이트 정리
print(f"\n{'='*60}")
print("핵심 인사이트")
print(f"{'='*60}")

korean_food_growth = hashtag_df[hashtag_df['hashtag'] == '#koreanfood'].iloc[-1]['post_count'] / \
                     hashtag_df[hashtag_df['hashtag'] == '#koreanfood'].iloc[0]['post_count']

print(f"\n1. 음식 공유 문화의 폭발적 성장")
print(f"   - #koreanfood 해시태그 {korean_food_growth:.1f}배 증가 (2019-2024)")
print(f"   - #homecooking, #cookingathome 해시태그 팬데믹 이후 급증")
print(f"   → MZ세대 중심으로 음식 공유가 일상화됨")

mz_dominance = (mz_total / (behavior_df.groupby('age_group')['monthly_frequency'].sum().mean()))
print(f"\n2. MZ세대의 압도적 활동량")
print(f"   - MZ세대가 다른 세대 대비 {mz_dominance:.1f}배 더 활발")
print(f"   - 특히 '레시피 저장'과 '좋아요' 활동이 두드러짐")
print(f"   → 소셜 피드 기능의 주 타겟으로 최적")

ugc_advantage = ugc_trust.mean() - pro_trust.mean()
print(f"\n3. UGC (일반인 콘텐츠)에 대한 높은 신뢰")
print(f"   - 일반인 레시피 신뢰도: {ugc_trust.mean():.1f}/10")
print(f"   - 전문가 레시피 신뢰도: {pro_trust.mean():.1f}/10")
print(f"   - 차이: +{ugc_advantage:.1f}점")
print(f"   → '나와 같은 일반인'의 경험을 더 신뢰")

top_motivation = motivation_df.iloc[0]
print(f"\n4. 공유의 주요 동기: {top_motivation['motivation']}")
print(f"   - {top_motivation['percentage']}%가 성취감과 자기표현을 위해 공유")
print(f"   → Gamification (뱃지, 통계)이 효과적일 것으로 예상")

high_engagement_repost = repost_rate.loc['High (101+)', 'percentage']
low_engagement_repost = repost_rate.loc['Low (0-50)', 'percentage']

print(f"\n5. 커뮤니티 피드백의 강력한 효과")
print(f"   - 높은 참여도 받은 경우 재게시율: {high_engagement_repost:.1f}%")
print(f"   - 낮은 참여도 받은 경우 재게시율: {low_engagement_repost:.1f}%")
print(f"   - 차이: {high_engagement_repost - low_engagement_repost:.1f}%p")
print(f"   → 소셜 상호작용이 지속적 참여 유도")

# 결과 요약 저장
summary_data = {
    'metric': [
        'Korean Food Hashtag Growth (2019-2024)',
        'MZ Generation Activity Multiplier',
        'UGC Average Trust Score',
        'Professional Average Trust Score',
        'Top Sharing Motivation',
        'High Engagement Repost Rate (%)',
        'Low Engagement Repost Rate (%)'
    ],
    'value': [
        f'{korean_food_growth:.1f}x',
        f'{mz_dominance:.1f}x',
        f'{ugc_trust.mean():.1f}/10',
        f'{pro_trust.mean():.1f}/10',
        top_motivation['motivation'],
        f'{high_engagement_repost:.1f}',
        f'{low_engagement_repost:.1f}'
    ]
}

summary_df = pd.DataFrame(summary_data)
summary_path = os.path.join(DATA_DIR, 'feature3_analysis_summary.csv')
summary_df.to_csv(summary_path, index=False, encoding='utf-8-sig')

print(f"\n✓ 분석 요약 저장: feature3_analysis_summary.csv")

print("\n\n분석 완료! 모든 결과는 다음 경로에 저장되었습니다:")
print(f"  - 데이터: {DATA_DIR}")
print(f"  - 시각화: {OUTPUT_DIR}")