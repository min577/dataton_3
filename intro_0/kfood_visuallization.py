import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.figsize'] = (12, 8)

# 데이터 로드
country_df = pd.read_csv('/mnt/user-data/uploads/kfood_youtube_country_clean.csv')
type_df = pd.read_csv('/mnt/user-data/uploads/kfood_youtube_type_clean.csv')

# 인게이지먼트율 계산
type_df['engagement_rate'] = ((type_df['평균 좋아요 수'] + type_df['평균 댓글 수']) / type_df['평균 조회수'] * 100)

# ==========================================
# 시각화 1: 국가별 조회수 TOP 10
# ==========================================

fig, ax = plt.subplots(figsize=(12, 6))
top10_countries = country_df.groupby('국가')['조회수_건수'].sum().sort_values(ascending=False).head(10)
colors = sns.color_palette("viridis", len(top10_countries))

bars = ax.barh(range(len(top10_countries)), top10_countries.values, color=colors)
ax.set_yticks(range(len(top10_countries)))
ax.set_yticklabels(top10_countries.index)
ax.set_xlabel('Total Views', fontsize=12, fontweight='bold')
ax.set_title('Top 10 Countries by K-Food Content Views\n(YouTube Data Analysis)', 
             fontsize=14, fontweight='bold', pad=20)
ax.invert_yaxis()

# 값 표시
for i, (country, value) in enumerate(top10_countries.items()):
    ax.text(value, i, f' {value:,.0f}', va='center', fontsize=10)

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/1_top10_countries_views.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 1_top10_countries_views.png")
plt.close()

# ==========================================
# 시각화 2: 콘텐츠 유형별 분석 (복합)
# ==========================================

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 2-1: 콘텐츠 유형별 시장 점유율
ax1 = axes[0, 0]
colors_pie = sns.color_palette("Set2", len(type_df))
wedges, texts, autotexts = ax1.pie(type_df['비중(%)'], 
                                     labels=type_df['콘텐츠 유형'],
                                     autopct='%1.1f%%',
                                     startangle=90,
                                     colors=colors_pie,
                                     textprops={'fontsize': 10})
ax1.set_title('Market Share by Content Type', fontsize=12, fontweight='bold', pad=20)

# 2-2: 콘텐츠 유형별 평균 조회수
ax2 = axes[0, 1]
sorted_types = type_df.sort_values('평균 조회수', ascending=True)
bars = ax2.barh(sorted_types['콘텐츠 유형'], sorted_types['평균 조회수'], 
                color=sns.color_palette("coolwarm", len(sorted_types)))
ax2.set_xlabel('Average Views', fontsize=10, fontweight='bold')
ax2.set_title('Average Views by Content Type', fontsize=12, fontweight='bold', pad=20)
for i, v in enumerate(sorted_types['평균 조회수']):
    ax2.text(v, i, f' {v:,.0f}', va='center', fontsize=9)

# 2-3: 인게이지먼트율
ax3 = axes[1, 0]
sorted_engagement = type_df.sort_values('engagement_rate', ascending=True)
bars = ax3.barh(sorted_engagement['콘텐츠 유형'], sorted_engagement['engagement_rate'],
                color=sns.color_palette("summer", len(sorted_engagement)))
ax3.set_xlabel('Engagement Rate (%)', fontsize=10, fontweight='bold')
ax3.set_title('Engagement Rate by Content Type\n(Likes + Comments / Views)', 
              fontsize=12, fontweight='bold', pad=20)
for i, v in enumerate(sorted_engagement['engagement_rate']):
    ax3.text(v, i, f' {v:.2f}%', va='center', fontsize=9)

# 2-4: 시장 점유율 vs 평균 조회수 (상관관계)
ax4 = axes[1, 1]
scatter = ax4.scatter(type_df['비중(%)'], type_df['평균 조회수'], 
                     s=type_df['engagement_rate']*100, 
                     c=type_df['engagement_rate'],
                     cmap='plasma', alpha=0.7, edgecolors='black', linewidth=1.5)

# 각 점에 레이블 추가
for idx, row in type_df.iterrows():
    ax4.annotate(row['콘텐츠 유형'], 
                (row['비중(%)'], row['평균 조회수']),
                xytext=(5, 5), textcoords='offset points',
                fontsize=9, fontweight='bold')

ax4.set_xlabel('Market Share (%)', fontsize=10, fontweight='bold')
ax4.set_ylabel('Average Views', fontsize=10, fontweight='bold')
ax4.set_title('Market Share vs Performance\n(Bubble size = Engagement Rate)', 
              fontsize=12, fontweight='bold', pad=20)

# 컬러바 추가
cbar = plt.colorbar(scatter, ax=ax4)
cbar.set_label('Engagement Rate (%)', fontsize=9)

# 상관계수 표시
correlation = type_df['비중(%)'].corr(type_df['평균 조회수'])
ax4.text(0.05, 0.95, f'Correlation: {correlation:.3f}', 
         transform=ax4.transAxes, fontsize=10,
         verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/2_content_type_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 2_content_type_analysis.png")
plt.close()

# ==========================================
# 시각화 3: 지역별 선호 콘텐츠 히트맵
# ==========================================

fig, ax = plt.subplots(figsize=(14, 10))

# 피벗 테이블 생성
country_content_pivot = country_df.pivot_table(
    index='국가', 
    columns='콘텐츠 유형', 
    values='조회수_건수', 
    fill_value=0
)

# 정규화 (각 국가별 비율로)
country_content_normalized = country_content_pivot.div(country_content_pivot.sum(axis=1), axis=0) * 100

# 히트맵 생성
sns.heatmap(country_content_normalized, 
            annot=True, 
            fmt='.1f',
            cmap='YlOrRd',
            cbar_kws={'label': 'Share (%)'},
            linewidths=0.5,
            ax=ax)

ax.set_title('Content Type Preference by Country\n(% of total views per country)', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xlabel('Content Type', fontsize=12, fontweight='bold')
ax.set_ylabel('Country', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/3_country_preference_heatmap.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 3_country_preference_heatmap.png")
plt.close()

# ==========================================
# 시각화 4: MZ 세대 타겟팅 근거
# ==========================================

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# 4-1: 참여형 vs 비참여형 콘텐츠
ax1 = axes[0]
participatory = type_df[type_df['콘텐츠 유형'].isin(['브이로그', '먹방', '음식 챌린지'])]
non_participatory = type_df[~type_df['콘텐츠 유형'].isin(['브이로그', '먹방', '음식 챌린지'])]

categories = ['Participatory\n(Vlog/Mukbang/Challenge)', 'Recipe-focused']
shares = [participatory['비중(%)'].sum(), non_participatory['비중(%)'].sum()]
colors_bar = ['#FF6B6B', '#4ECDC4']

bars = ax1.bar(categories, shares, color=colors_bar, edgecolor='black', linewidth=2)
ax1.set_ylabel('Market Share (%)', fontsize=12, fontweight='bold')
ax1.set_title('MZ Generation Content Preference\n(Participatory vs Recipe-focused)', 
              fontsize=12, fontweight='bold', pad=20)
ax1.set_ylim(0, 100)

# 값 표시
for i, (bar, value) in enumerate(zip(bars, shares)):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
            f'{value:.1f}%',
            ha='center', va='bottom', fontsize=14, fontweight='bold')

# 4-2: 인게이지먼트 지표
ax2 = axes[1]
x = np.arange(len(type_df))
width = 0.25

bars1 = ax2.bar(x - width, type_df['평균 조회수']/1000, width, 
                label='Avg Views (K)', color='skyblue', edgecolor='black')
bars2 = ax2.bar(x, type_df['평균 좋아요 수']/10, width, 
                label='Avg Likes (×10)', color='lightcoral', edgecolor='black')
bars3 = ax2.bar(x + width, type_df['평균 댓글 수']*10, width, 
                label='Avg Comments (×10)', color='lightgreen', edgecolor='black')

ax2.set_xlabel('Content Type', fontsize=12, fontweight='bold')
ax2.set_ylabel('Scaled Metrics', fontsize=12, fontweight='bold')
ax2.set_title('Engagement Metrics by Content Type\n(Active vs Passive Consumption)', 
              fontsize=12, fontweight='bold', pad=20)
ax2.set_xticks(x)
ax2.set_xticklabels(type_df['콘텐츠 유형'], rotation=45, ha='right')
ax2.legend(loc='upper left', fontsize=10)
ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/4_mz_targeting_insights.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 4_mz_targeting_insights.png")
plt.close()

# ==========================================
# 시각화 5: 상관관계 매트릭스
# ==========================================

fig, ax = plt.subplots(figsize=(10, 8))

correlation_matrix = type_df[['비중(%)', '평균 조회수', '평균 좋아요 수', '평균 댓글 수', 'engagement_rate']].corr()

mask = np.triu(np.ones_like(correlation_matrix, dtype=bool), k=1)
sns.heatmap(correlation_matrix, 
            mask=mask,
            annot=True, 
            fmt='.3f',
            cmap='coolwarm',
            center=0,
            square=True,
            linewidths=2,
            cbar_kws={'label': 'Correlation Coefficient'},
            ax=ax,
            vmin=-1, vmax=1)

ax.set_title('Correlation Matrix: Content Metrics\n(Key Finding: Low correlation between market share and performance)', 
             fontsize=13, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/5_correlation_matrix.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 5_correlation_matrix.png")
plt.close()

# ==========================================
# 시각화 6: 종합 인사이트 대시보드
# ==========================================

fig = plt.figure(figsize=(18, 10))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# 6-1: 총 조회수 (큰 숫자 강조)
ax1 = fig.add_subplot(gs[0, 0])
total_views = country_df['조회수_건수'].sum()
ax1.text(0.5, 0.5, f'{total_views/1e6:.0f}M', 
         ha='center', va='center', fontsize=40, fontweight='bold', color='#FF6B6B')
ax1.text(0.5, 0.2, 'Total YouTube Views', 
         ha='center', va='center', fontsize=12, fontweight='bold')
ax1.axis('off')
ax1.set_title('Global K-Food Impact', fontsize=13, fontweight='bold', pad=20)

# 6-2: TOP 3 국가
ax2 = fig.add_subplot(gs[0, 1])
top3 = country_df.groupby('국가')['조회수_건수'].sum().nlargest(3)
ax2.barh(range(len(top3)), top3.values, color=['gold', 'silver', '#CD7F32'])
ax2.set_yticks(range(len(top3)))
ax2.set_yticklabels(top3.index)
ax2.invert_yaxis()
ax2.set_title('Top 3 Countries', fontsize=13, fontweight='bold', pad=20)
for i, v in enumerate(top3.values):
    ax2.text(v, i, f' {v/1e6:.0f}M', va='center', fontsize=10)

# 6-3: MZ 참여형 콘텐츠 비중
ax3 = fig.add_subplot(gs[0, 2])
participatory_share = participatory['비중(%)'].sum()
ax3.text(0.5, 0.5, f'{participatory_share:.1f}%', 
         ha='center', va='center', fontsize=40, fontweight='bold', color='#4ECDC4')
ax3.text(0.5, 0.2, 'Participatory Content', 
         ha='center', va='center', fontsize=12, fontweight='bold')
ax3.text(0.5, 0.05, '(Vlog/Mukbang/Challenge)', 
         ha='center', va='center', fontsize=9, style='italic')
ax3.axis('off')
ax3.set_title('MZ Generation Behavior', fontsize=13, fontweight='bold', pad=20)

# 6-4: 콘텐츠 유형별 성과 (가로 막대)
ax4 = fig.add_subplot(gs[1, :])
content_performance = type_df.sort_values('평균 조회수', ascending=True)
bars = ax4.barh(content_performance['콘텐츠 유형'], 
                content_performance['평균 조회수'],
                color=sns.color_palette("Spectral", len(content_performance)))
ax4.set_xlabel('Average Views', fontsize=11, fontweight='bold')
ax4.set_title('Content Performance: The Gap Between Interest and Supply', 
              fontsize=13, fontweight='bold', pad=20)
for i, v in enumerate(content_performance['평균 조회수']):
    ax4.text(v, i, f' {v:,.0f}', va='center', fontsize=10)

# 6-5: 국가별 선호도 상위 5개국
ax5 = fig.add_subplot(gs[2, :2])
top5_countries = ['미국', '일본', '태국', '인도네시아', '인도']
country_subset = country_df[country_df['국가'].isin(top5_countries)]
pivot_top5 = country_subset.pivot_table(
    index='국가', 
    columns='콘텐츠 유형', 
    values='조회수_건수', 
    fill_value=0
)
pivot_top5_norm = pivot_top5.div(pivot_top5.sum(axis=1), axis=0) * 100

pivot_top5_norm.plot(kind='bar', stacked=True, ax=ax5, 
                     color=sns.color_palette("Set3", len(pivot_top5_norm.columns)))
ax5.set_xlabel('Country', fontsize=11, fontweight='bold')
ax5.set_ylabel('Share (%)', fontsize=11, fontweight='bold')
ax5.set_title('Regional Content Preferences (Top 5 Countries)', 
              fontsize=13, fontweight='bold', pad=20)
ax5.legend(title='Content Type', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
ax5.set_xticklabels(ax5.get_xticklabels(), rotation=45, ha='right')

# 6-6: 핵심 상관관계
ax6 = fig.add_subplot(gs[2, 2])
corr_value = correlation_matrix.loc['비중(%)', '평균 조회수']
ax6.text(0.5, 0.6, f'{corr_value:.3f}', 
         ha='center', va='center', fontsize=40, fontweight='bold', 
         color='#FF6B6B' if corr_value < 0 else '#4ECDC4')
ax6.text(0.5, 0.35, 'Market Share vs\nAvg Views Correlation', 
         ha='center', va='center', fontsize=11, fontweight='bold')
ax6.text(0.5, 0.1, 'Negative = Opportunity Gap', 
         ha='center', va='center', fontsize=9, style='italic', color='gray')
ax6.axis('off')
ax6.set_title('Content-Reality Gap', fontsize=13, fontweight='bold', pad=20)

plt.suptitle('K-Food YouTube Analytics: Main Intro Insights Dashboard', 
             fontsize=16, fontweight='bold', y=0.98)

plt.savefig('/mnt/user-data/outputs/6_comprehensive_dashboard.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 6_comprehensive_dashboard.png")
plt.close()

print("\n" + "="*60)
print("All visualizations completed successfully!")
print("="*60)
print("\nFiles saved:")
print("1. 1_top10_countries_views.png - Top 10 countries by views")
print("2. 2_content_type_analysis.png - Content type comprehensive analysis")
print("3. 3_country_preference_heatmap.png - Regional preference heatmap")
print("4. 4_mz_targeting_insights.png - MZ generation targeting evidence")
print("5. 5_correlation_matrix.png - Correlation analysis")
print("6. 6_comprehensive_dashboard.png - Executive summary dashboard")