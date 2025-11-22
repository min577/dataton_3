"""
핵심 기능 1: 데이터 분석 및 시각화
K-콘텐츠 공개 전후 한식 검색량 변화 분석
(scipy 없이 작동)
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# 한글 폰트 설정 (Windows)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 디렉토리 설정
DATA_DIR = r"C:\Users\ASUS\Desktop\DATATON\intro"
OUTPUT_DIR = os.path.join(DATA_DIR, 'visualizations')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 데이터 로드
print("데이터 로딩 중...")
df = pd.read_csv(os.path.join(DATA_DIR, 'feature1_google_trends_data.csv'), index_col=0, parse_dates=True)

print(f"총 {len(df)} 행 로드 완료\n")

# 콘텐츠별로 분석
unique_contents = df['content_name'].unique()

for content in unique_contents:
    print(f"\n{'='*60}")
    print(f"분석: {content}")
    print(f"{'='*60}")
    
    content_df = df[df['content_name'] == content].copy()
    food_name = content_df['food_name'].iloc[0]
    release_date = pd.to_datetime(content_df['release_date'].iloc[0])
    
    # 공개 전후 기간 설정
    before_period = content_df[content_df.index < release_date]
    after_period = content_df[content_df.index >= release_date]
    
    if len(before_period) > 0 and len(after_period) > 0:
        # 통계 계산
        before_avg = before_period[food_name].mean()
        after_avg = after_period[food_name].mean()
        increase_rate = ((after_avg - before_avg) / before_avg * 100) if before_avg > 0 else 0
        
        print(f"\n[{food_name} 검색량 변화]")
        print(f"  공개 전 평균: {before_avg:.2f}")
        print(f"  공개 후 평균: {after_avg:.2f}")
        print(f"  증가율: {increase_rate:.2f}%")
        
        # 간단한 통계 분석
        if len(before_period) > 1 and len(after_period) > 1:
            before_std = before_period[food_name].std()
            after_std = after_period[food_name].std()
            print(f"  공개 전 표준편차: {before_std:.2f}")
            print(f"  공개 후 표준편차: {after_std:.2f}")
            
            # 증가율 기반 판단
            if increase_rate > 100:
                print(f"  → 매우 유의미한 증가! (증가율 > 100%)")
            elif increase_rate > 50:
                print(f"  → 유의미한 증가 (증가율 > 50%)")
            elif increase_rate > 20:
                print(f"  → 의미있는 증가 (증가율 > 20%)")
            else:
                print(f"  → 소폭 증가 또는 변화 없음")
    
    # 시각화 1: 시계열 그래프
    fig, ax = plt.subplots(figsize=(14, 6))
    
    ax.plot(content_df.index, content_df[content], label=content, linewidth=2, alpha=0.7)
    ax.plot(content_df.index, content_df[food_name], label=food_name, linewidth=2, alpha=0.7)
    
    # 공개일 표시
    ax.axvline(x=release_date, color='red', linestyle='--', linewidth=2, label='Release Date')
    
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Search Interest (0-100)', fontsize=12)
    ax.set_title(f'{content} and {food_name} Search Trends', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, f'feature1_{content.replace(" ", "_")}_timeline.png'), dpi=300)
    plt.close()
    
    print(f"\n  ✓ 시각화 저장: feature1_{content.replace(' ', '_')}_timeline.png")

# 통합 분석: 모든 콘텐츠의 증가율 비교
print(f"\n{'='*60}")
print("전체 콘텐츠 비교 분석")
print(f"{'='*60}")

comparison_data = []

for content in unique_contents:
    content_df = df[df['content_name'] == content].copy()
    food_name = content_df['food_name'].iloc[0]
    release_date = pd.to_datetime(content_df['release_date'].iloc[0])
    
    before_period = content_df[content_df.index < release_date]
    after_period = content_df[content_df.index >= release_date]
    
    if len(before_period) > 0 and len(after_period) > 0:
        before_avg = before_period[food_name].mean()
        after_avg = after_period[food_name].mean()
        increase_rate = ((after_avg - before_avg) / before_avg * 100) if before_avg > 0 else 0
        
        comparison_data.append({
            'Content': content,
            'Food': food_name,
            'Before_Avg': before_avg,
            'After_Avg': after_avg,
            'Increase_Rate': increase_rate
        })

comparison_df = pd.DataFrame(comparison_data)

# 비교 시각화
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# 증가율 막대 그래프
axes[0].bar(range(len(comparison_df)), comparison_df['Increase_Rate'], color='skyblue', edgecolor='navy')
axes[0].set_xticks(range(len(comparison_df)))
axes[0].set_xticklabels(comparison_df['Content'], rotation=45, ha='right')
axes[0].set_ylabel('Increase Rate (%)', fontsize=12)
axes[0].set_title('Food Search Increase After K-Content Release', fontsize=14, fontweight='bold')
axes[0].grid(axis='y', alpha=0.3)

# 공개 전후 평균 비교
x = np.arange(len(comparison_df))
width = 0.35

axes[1].bar(x - width/2, comparison_df['Before_Avg'], width, label='Before Release', alpha=0.8)
axes[1].bar(x + width/2, comparison_df['After_Avg'], width, label='After Release', alpha=0.8)

axes[1].set_xticks(x)
axes[1].set_xticklabels(comparison_df['Content'], rotation=45, ha='right')
axes[1].set_ylabel('Average Search Interest', fontsize=12)
axes[1].set_title('Search Interest Comparison: Before vs After', fontsize=14, fontweight='bold')
axes[1].legend()
axes[1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'feature1_comparison_analysis.png'), dpi=300)
plt.close()

print("\n✓ 비교 분석 그래프 저장: feature1_comparison_analysis.png")

# 결과 요약 CSV 저장
comparison_df.to_csv(os.path.join(DATA_DIR, 'feature1_analysis_summary.csv'), index=False, encoding='utf-8-sig')
print(f"✓ 분석 요약 저장: feature1_analysis_summary.csv")

print("\n[분석 요약]")
print(comparison_df.to_string(index=False))

print("\n\n분석 완료! 모든 결과는 다음 경로에 저장되었습니다:")
print(f"  - 데이터: {DATA_DIR}")
print(f"  - 시각화: {OUTPUT_DIR}")