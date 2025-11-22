"""
K-Food App Market Research - Data Visualization
Main Intro 시각화 스크립트
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")

print("=" * 60)
print("K-Food App Market Research - Data Visualization")
print("=" * 60)
print()

# =====================================================================
# 1. K-CULTURE GLOBAL INFLUENCE VISUALIZATION
# =====================================================================

print("1. Visualizing K-Culture Global Influence...")

df_k_culture = pd.read_csv('data_k_culture_influence.csv')

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# K-pop Fans Growth
axes[0].plot(df_k_culture['Year'], df_k_culture['K-pop_Fans_Million'], 
             marker='o', linewidth=2.5, markersize=8, color='#FF1744')
axes[0].fill_between(df_k_culture['Year'], df_k_culture['K-pop_Fans_Million'], 
                      alpha=0.3, color='#FF1744')
axes[0].set_title('Global K-pop Fans Growth', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Year', fontsize=11)
axes[0].set_ylabel('Fans (Million)', fontsize=11)
axes[0].grid(True, alpha=0.3)

# Cultural Export Value
axes[1].bar(df_k_culture['Year'], df_k_culture['Cultural_Export_Billion_USD'], 
            color='#2196F3', alpha=0.8, edgecolor='black')
axes[1].set_title('K-Culture Export Value', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Year', fontsize=11)
axes[1].set_ylabel('Export Value (Billion USD)', fontsize=11)
axes[1].grid(True, alpha=0.3, axis='y')

# Hallyu Index
axes[2].plot(df_k_culture['Year'], df_k_culture['Hallyu_Index'], 
             marker='s', linewidth=2.5, markersize=8, color='#4CAF50')
axes[2].fill_between(df_k_culture['Year'], df_k_culture['Hallyu_Index'], 
                      alpha=0.3, color='#4CAF50')
axes[2].set_title('Hallyu Global Influence Index', fontsize=14, fontweight='bold')
axes[2].set_xlabel('Year', fontsize=11)
axes[2].set_ylabel('Index Score', fontsize=11)
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('viz_01_k_culture_influence.png', dpi=300, bbox_inches='tight')
print("✓ Saved: viz_01_k_culture_influence.png")
plt.close()

# =====================================================================
# 2. K-FOOD EXPORT TRENDS
# =====================================================================

print("2. Visualizing K-Food Export Trends...")

df_k_food = pd.read_csv('data_k_food_exports.csv')

fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

# Total Export Trend
ax1 = fig.add_subplot(gs[0, :])
ax1.plot(df_k_food['Year'], df_k_food['Total_Export_Billion_USD'], 
         marker='o', linewidth=3, markersize=10, color='#FF5722', label='Total Export')
ax1.fill_between(df_k_food['Year'], df_k_food['Total_Export_Billion_USD'], 
                 alpha=0.3, color='#FF5722')
ax1.set_title('K-Food Total Export Value (2015-2024)', fontsize=16, fontweight='bold')
ax1.set_xlabel('Year', fontsize=12)
ax1.set_ylabel('Export Value (Billion USD)', fontsize=12)
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3)

# Ramen Export Growth
ax2 = fig.add_subplot(gs[1, 0])
ax2.bar(df_k_food['Year'], df_k_food['Ramen_Export_Million_USD'], 
        color='#FFC107', alpha=0.8, edgecolor='black')
ax2.set_title('Ramen Export Growth', fontsize=14, fontweight='bold')
ax2.set_xlabel('Year', fontsize=11)
ax2.set_ylabel('Export (Million USD)', fontsize=11)
ax2.grid(True, alpha=0.3, axis='y')

# Top Markets Comparison
ax3 = fig.add_subplot(gs[1, 1])
x = np.arange(len(df_k_food['Year']))
width = 0.35
ax3.bar(x - width/2, df_k_food['Top_Market_US_Million_USD'], 
        width, label='USA', color='#2196F3', alpha=0.8)
ax3.bar(x + width/2, df_k_food['Top_Market_China_Million_USD'], 
        width, label='China', color='#F44336', alpha=0.8)
ax3.set_title('Top Markets: USA vs China', fontsize=14, fontweight='bold')
ax3.set_xlabel('Year', fontsize=11)
ax3.set_ylabel('Export (Million USD)', fontsize=11)
ax3.set_xticks(x)
ax3.set_xticklabels(df_k_food['Year'], rotation=45)
ax3.legend(fontsize=11)
ax3.grid(True, alpha=0.3, axis='y')

plt.savefig('viz_02_k_food_exports.png', dpi=300, bbox_inches='tight')
print("✓ Saved: viz_02_k_food_exports.png")
plt.close()

# =====================================================================
# 3. FOREIGN VISITORS AGE DISTRIBUTION
# =====================================================================

print("3. Visualizing Foreign Visitors Age Distribution...")

df_visitors = pd.read_csv('data_korea_visitors_age.csv')

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Age Distribution Trends
age_columns = ['Under_20', 'Age_21_30', 'Age_31_40', 'Age_41_50', 'Age_51_60', 'Over_60']
for col in age_columns:
    axes[0].plot(df_visitors['Year'], df_visitors[col], 
                marker='o', linewidth=2, markersize=6, label=col.replace('_', ' '))
axes[0].set_title('Foreign Visitors by Age Group', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Year', fontsize=11)
axes[0].set_ylabel('Visitors (Thousand)', fontsize=11)
axes[0].legend(fontsize=9, loc='upper left')
axes[0].grid(True, alpha=0.3)

# Under 30 Percentage Trend
axes[1].plot(df_visitors['Year'], df_visitors['Under_30_Percent'], 
            marker='o', linewidth=3, markersize=10, color='#9C27B0')
axes[1].fill_between(df_visitors['Year'], df_visitors['Under_30_Percent'], 
                     alpha=0.3, color='#9C27B0')
axes[1].set_title('Percentage of Visitors Under 30', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Year', fontsize=11)
axes[1].set_ylabel('Percentage (%)', fontsize=11)
axes[1].grid(True, alpha=0.3)
axes[1].axhline(y=35, color='red', linestyle='--', linewidth=1.5, label='35% Threshold')
axes[1].legend(fontsize=10)

plt.tight_layout()
plt.savefig('viz_03_visitors_age_distribution.png', dpi=300, bbox_inches='tight')
print("✓ Saved: viz_03_visitors_age_distribution.png")
plt.close()

# =====================================================================
# 4. MZ GENERATION DIGITAL BEHAVIOR
# =====================================================================

print("4. Visualizing MZ Generation Digital Behavior...")

df_mz = pd.read_csv('data_mz_digital_behavior.csv')

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Smartphone Usage
axes[0, 0].barh(df_mz['Age_Group'], df_mz['Smartphone_Usage_Hours_Day'], 
                color=['#E91E63', '#9C27B0', '#3F51B5', '#607D8B'])
axes[0, 0].set_title('Daily Smartphone Usage by Generation', fontsize=13, fontweight='bold')
axes[0, 0].set_xlabel('Hours per Day', fontsize=11)
axes[0, 0].grid(True, alpha=0.3, axis='x')

# App Usage Comparison
app_data = df_mz[['Age_Group', 'Social_Media_Usage_Percent', 
                   'Travel_App_Usage_Percent', 'Food_App_Usage_Percent']]
x = np.arange(len(df_mz['Age_Group']))
width = 0.25
axes[0, 1].bar(x - width, df_mz['Social_Media_Usage_Percent'], 
               width, label='Social Media', color='#FF5722')
axes[0, 1].bar(x, df_mz['Travel_App_Usage_Percent'], 
               width, label='Travel Apps', color='#2196F3')
axes[0, 1].bar(x + width, df_mz['Food_App_Usage_Percent'], 
               width, label='Food Apps', color='#4CAF50')
axes[0, 1].set_title('App Usage by Generation', fontsize=13, fontweight='bold')
axes[0, 1].set_ylabel('Usage Percentage (%)', fontsize=11)
axes[0, 1].set_xticks(x)
axes[0, 1].set_xticklabels(df_mz['Age_Group'], rotation=15, ha='right')
axes[0, 1].legend(fontsize=10)
axes[0, 1].grid(True, alpha=0.3, axis='y')

# Travel Frequency
axes[1, 0].bar(df_mz['Age_Group'], df_mz['Avg_Trips_Per_Year'], 
               color=['#FF9800', '#FF5722', '#795548', '#9E9E9E'])
axes[1, 0].set_title('Average Trips Per Year', fontsize=13, fontweight='bold')
axes[1, 0].set_ylabel('Number of Trips', fontsize=11)
axes[1, 0].set_xticklabels(df_mz['Age_Group'], rotation=15, ha='right')
axes[1, 0].grid(True, alpha=0.3, axis='y')

# Experience Priority
axes[1, 1].plot(df_mz['Age_Group'], df_mz['Experience_Priority_Score'], 
                marker='o', linewidth=2.5, markersize=10, color='#00BCD4')
axes[1, 1].fill_between(range(len(df_mz)), df_mz['Experience_Priority_Score'], 
                        alpha=0.3, color='#00BCD4')
axes[1, 1].set_title('Experience Priority Score', fontsize=13, fontweight='bold')
axes[1, 1].set_ylabel('Score (0-10)', fontsize=11)
axes[1, 1].set_xticks(range(len(df_mz)))
axes[1, 1].set_xticklabels(df_mz['Age_Group'], rotation=15, ha='right')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('viz_04_mz_digital_behavior.png', dpi=300, bbox_inches='tight')
print("✓ Saved: viz_04_mz_digital_behavior.png")
plt.close()

# =====================================================================
# 5. SOCIAL MEDIA TRENDS
# =====================================================================

print("5. Visualizing Social Media Trends...")

df_social = pd.read_csv('data_social_media_trends.csv')

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Hashtag Volume by Platform
platforms = df_social['Platform']
x = np.arange(len(platforms))
width = 0.2

axes[0].bar(x - 1.5*width, df_social['KoreanFood_Hashtag_Million_Posts'], 
            width, label='#KoreanFood', color='#F44336')
axes[0].bar(x - 0.5*width, df_social['KFood_Hashtag_Million_Posts'], 
            width, label='#KFood', color='#FF9800')
axes[0].bar(x + 0.5*width, df_social['KBBQ_Hashtag_Million_Posts'], 
            width, label='#KBBQ', color='#4CAF50')
axes[0].bar(x + 1.5*width, df_social['Kimchi_Hashtag_Million_Posts'], 
            width, label='#Kimchi', color='#2196F3')

axes[0].set_title('K-Food Hashtag Volume by Platform', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Posts (Million)', fontsize=11)
axes[0].set_xticks(x)
axes[0].set_xticklabels(platforms)
axes[0].legend(fontsize=10)
axes[0].grid(True, alpha=0.3, axis='y')

# Monthly Growth Rate
axes[1].barh(df_social['Platform'], df_social['Monthly_Growth_Percent'], 
             color=['#E91E63', '#9C27B0', '#FF5722', '#00BCD4'])
axes[1].set_title('Monthly Growth Rate by Platform', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Growth Rate (%)', fontsize=11)
axes[1].grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('viz_05_social_media_trends.png', dpi=300, bbox_inches='tight')
print("✓ Saved: viz_05_social_media_trends.png")
plt.close()

# =====================================================================
# 6. GOOGLE TRENDS ANALYSIS
# =====================================================================

print("6. Visualizing Google Trends Data...")

df_trends = pd.read_csv('data_google_trends_korea_food.csv')

fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# All Search Terms
search_terms = ['Korean_Food_Index', 'K_Food_Index', 'Kimchi_Index', 
                'Korean_BBQ_Index', 'Korean_Drama_Food_Index']
colors = ['#F44336', '#FF9800', '#4CAF50', '#2196F3', '#9C27B0']

for term, color in zip(search_terms, colors):
    axes[0].plot(df_trends['Year'], df_trends[term], 
                marker='o', linewidth=2.5, markersize=7, 
                label=term.replace('_', ' '), color=color)

axes[0].set_title('Google Trends: Korea + Food Search Interest (2015-2024)', 
                 fontsize=15, fontweight='bold')
axes[0].set_xlabel('Year', fontsize=12)
axes[0].set_ylabel('Search Interest Index', fontsize=12)
axes[0].legend(fontsize=10, loc='upper left')
axes[0].grid(True, alpha=0.3)

# Growth Rate Calculation
growth_rates = {}
for term in search_terms:
    initial = df_trends[term].iloc[0]
    final = df_trends[term].iloc[-1]
    growth = ((final - initial) / initial) * 100
    growth_rates[term.replace('_Index', '').replace('_', ' ')] = growth

terms = list(growth_rates.keys())
values = list(growth_rates.values())
bars = axes[1].barh(terms, values, color=colors)
axes[1].set_title('Search Interest Growth Rate (2015-2024)', 
                  fontsize=15, fontweight='bold')
axes[1].set_xlabel('Growth Rate (%)', fontsize=12)
axes[1].grid(True, alpha=0.3, axis='x')

# Add value labels
for bar, value in zip(bars, values):
    axes[1].text(value + 5, bar.get_y() + bar.get_height()/2, 
                f'+{value:.1f}%', va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('viz_06_google_trends_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved: viz_06_google_trends_analysis.png")
plt.close()

# =====================================================================
# 7. REGIONAL INTEREST HEATMAP
# =====================================================================

print("7. Visualizing Regional Interest...")

df_regional = pd.read_csv('data_regional_k_food_interest.csv')

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Regional Interest Score
sorted_df = df_regional.sort_values('K_Food_Interest_Score', ascending=True)
bars = axes[0].barh(sorted_df['Region'], sorted_df['K_Food_Interest_Score'], 
                    color=plt.cm.YlOrRd(sorted_df['K_Food_Interest_Score']/100))
axes[0].set_title('K-Food Interest Score by Region', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Interest Score', fontsize=11)
axes[0].grid(True, alpha=0.3, axis='x')

# Growth Rate
sorted_growth = df_regional.sort_values('Growth_Rate_2019_2024_Percent', ascending=True)
bars2 = axes[1].barh(sorted_growth['Region'], sorted_growth['Growth_Rate_2019_2024_Percent'], 
                     color=plt.cm.Greens(sorted_growth['Growth_Rate_2019_2024_Percent']/max(sorted_growth['Growth_Rate_2019_2024_Percent'])))
axes[1].set_title('Growth Rate (2019-2024)', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Growth Rate (%)', fontsize=11)
axes[1].grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('viz_07_regional_interest.png', dpi=300, bbox_inches='tight')
print("✓ Saved: viz_07_regional_interest.png")
plt.close()

# =====================================================================
# 8. COMPREHENSIVE DASHBOARD
# =====================================================================

print("8. Creating Comprehensive Dashboard...")

fig = plt.figure(figsize=(20, 12))
gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.35)

# 1. K-Culture Export Trend
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(df_k_culture['Year'], df_k_culture['Cultural_Export_Billion_USD'], 
         marker='o', linewidth=2.5, color='#2196F3')
ax1.fill_between(df_k_culture['Year'], df_k_culture['Cultural_Export_Billion_USD'], 
                 alpha=0.3, color='#2196F3')
ax1.set_title('K-Culture Export Value', fontsize=11, fontweight='bold')
ax1.set_ylabel('Billion USD', fontsize=9)
ax1.grid(True, alpha=0.3)

# 2. K-Food Export Trend
ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(df_k_food['Year'], df_k_food['Total_Export_Billion_USD'], 
         marker='o', linewidth=2.5, color='#FF5722')
ax2.fill_between(df_k_food['Year'], df_k_food['Total_Export_Billion_USD'], 
                 alpha=0.3, color='#FF5722')
ax2.set_title('K-Food Export Value', fontsize=11, fontweight='bold')
ax2.set_ylabel('Billion USD', fontsize=9)
ax2.grid(True, alpha=0.3)

# 3. Under 30 Visitors Trend
ax3 = fig.add_subplot(gs[0, 2])
ax3.plot(df_visitors['Year'], df_visitors['Under_30_Percent'], 
         marker='o', linewidth=2.5, color='#9C27B0')
ax3.fill_between(df_visitors['Year'], df_visitors['Under_30_Percent'], 
                 alpha=0.3, color='#9C27B0')
ax3.set_title('Visitors Under 30 (%)', fontsize=11, fontweight='bold')
ax3.set_ylabel('Percentage', fontsize=9)
ax3.grid(True, alpha=0.3)

# 4. MZ Generation App Usage
ax4 = fig.add_subplot(gs[1, 0])
mz_subset = df_mz[df_mz['Age_Group'].str.contains('Gen Z|Millennials')]
x_pos = np.arange(len(mz_subset))
width = 0.25
ax4.bar(x_pos - width, mz_subset['Social_Media_Usage_Percent'], 
        width, label='Social Media', color='#FF5722')
ax4.bar(x_pos, mz_subset['Travel_App_Usage_Percent'], 
        width, label='Travel', color='#2196F3')
ax4.bar(x_pos + width, mz_subset['Food_App_Usage_Percent'], 
        width, label='Food', color='#4CAF50')
ax4.set_title('MZ Generation App Usage', fontsize=11, fontweight='bold')
ax4.set_ylabel('Usage %', fontsize=9)
ax4.set_xticks(x_pos)
ax4.set_xticklabels(['Gen Z', 'Millennials'], fontsize=9)
ax4.legend(fontsize=8)
ax4.grid(True, alpha=0.3, axis='y')

# 5. Social Media Hashtag Volume
ax5 = fig.add_subplot(gs[1, 1])
total_posts = df_social.groupby('Platform')[['KoreanFood_Hashtag_Million_Posts', 
                                              'KFood_Hashtag_Million_Posts']].sum().sum(axis=1)
ax5.bar(df_social['Platform'], total_posts, color=['#E91E63', '#9C27B0', '#FF5722', '#00BCD4'])
ax5.set_title('Total K-Food Hashtags', fontsize=11, fontweight='bold')
ax5.set_ylabel('Million Posts', fontsize=9)
ax5.set_xticklabels(df_social['Platform'], rotation=15, ha='right', fontsize=9)
ax5.grid(True, alpha=0.3, axis='y')

# 6. Google Trends Combined
ax6 = fig.add_subplot(gs[1, 2])
for term, color in zip(search_terms[:3], colors[:3]):
    ax6.plot(df_trends['Year'], df_trends[term], 
            marker='o', linewidth=2, label=term.replace('_Index', '').replace('_', ' '), 
            color=color)
ax6.set_title('Google Search Trends', fontsize=11, fontweight='bold')
ax6.set_ylabel('Interest Index', fontsize=9)
ax6.legend(fontsize=7, loc='upper left')
ax6.grid(True, alpha=0.3)

# 7. Regional Interest
ax7 = fig.add_subplot(gs[2, 0])
top_regions = df_regional.nlargest(5, 'K_Food_Interest_Score')
ax7.barh(top_regions['Region'], top_regions['K_Food_Interest_Score'], 
         color=plt.cm.YlOrRd(top_regions['K_Food_Interest_Score']/100))
ax7.set_title('Top 5 Regions Interest', fontsize=11, fontweight='bold')
ax7.set_xlabel('Interest Score', fontsize=9)
ax7.grid(True, alpha=0.3, axis='x')

# 8. Restaurant Growth
df_restaurants = pd.read_csv('data_k_food_restaurants_global.csv')
ax8 = fig.add_subplot(gs[2, 1])
ax8.plot(df_restaurants['Year'], df_restaurants['Total_K_Food_Restaurants'], 
         marker='o', linewidth=2.5, color='#4CAF50')
ax8.fill_between(df_restaurants['Year'], df_restaurants['Total_K_Food_Restaurants'], 
                 alpha=0.3, color='#4CAF50')
ax8.set_title('Global K-Food Restaurants', fontsize=11, fontweight='bold')
ax8.set_ylabel('Number of Restaurants', fontsize=9)
ax8.grid(True, alpha=0.3)

# 9. Key Statistics Summary
ax9 = fig.add_subplot(gs[2, 2])
ax9.axis('off')
summary_text = f"""
KEY STATISTICS (2024)

K-pop Fans: 155M globally
K-Culture Export: $18.9B
K-Food Export: $9.98B

Visitors Under 30: 35.6%
MZ Gen Population: 32.5%

Social Media Posts:
• Instagram: 47.2M
• TikTok: 38.5M

K-Food Restaurants: 15,847
Growth Rate: +6.7% YoY
"""
ax9.text(0.1, 0.9, summary_text, fontsize=10, verticalalignment='top', 
         family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

plt.suptitle('K-FOOD APP MARKET RESEARCH - COMPREHENSIVE DASHBOARD', 
             fontsize=18, fontweight='bold', y=0.98)

plt.savefig('viz_08_comprehensive_dashboard.png', dpi=300, bbox_inches='tight')
print("✓ Saved: viz_08_comprehensive_dashboard.png")
plt.close()

# =====================================================================
# SUMMARY
# =====================================================================

print("\n" + "=" * 60)
print("VISUALIZATION COMPLETE!")
print("=" * 60)
print("\nGenerated visualizations:")
print("  1. viz_01_k_culture_influence.png")
print("  2. viz_02_k_food_exports.png")
print("  3. viz_03_visitors_age_distribution.png")
print("  4. viz_04_mz_digital_behavior.png")
print("  5. viz_05_social_media_trends.png")
print("  6. viz_06_google_trends_analysis.png")
print("  7. viz_07_regional_interest.png")
print("  8. viz_08_comprehensive_dashboard.png")
print("=" * 60)
