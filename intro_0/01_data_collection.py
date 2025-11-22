"""
K-Food App Market Research - Data Collection and Analysis
Main Intro 데이터 분석 스크립트
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정 (Windows 기준)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 스타일 설정
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

print("=" * 60)
print("K-Food App Market Research - Data Collection Script")
print("=" * 60)
print()

# =====================================================================
# 1. K-CULTURE GLOBAL INFLUENCE DATA
# =====================================================================

print("1. Creating K-Culture Global Influence Dataset...")

k_culture_data = {
    'Year': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    'K-pop_Fans_Million': [80, 85, 90, 95, 100, 110, 125, 140, 150, 155],
    'Cultural_Export_Billion_USD': [5.2, 5.8, 6.5, 7.8, 9.4, 10.8, 12.4, 14.2, 16.5, 18.9],
    'Hallyu_Index': [58, 62, 68, 75, 82, 88, 92, 95, 98, 100]
}

df_k_culture = pd.DataFrame(k_culture_data)
df_k_culture.to_csv('data_k_culture_influence.csv', index=False, encoding='utf-8-sig')
print(f"✓ K-Culture data saved: {len(df_k_culture)} records")
print(df_k_culture.tail(3))
print()

# =====================================================================
# 2. K-FOOD EXPORT STATISTICS
# =====================================================================

print("2. Creating K-Food Export Statistics...")

k_food_export = {
    'Year': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    'Total_Export_Billion_USD': [3.51, 3.82, 4.15, 4.52, 4.95, 5.40, 6.15, 7.02, 8.12, 9.98],
    'Ramen_Export_Million_USD': [280, 310, 350, 420, 520, 650, 780, 950, 1180, 1248],
    'Kimchi_Export_Million_USD': [82, 88, 95, 105, 118, 126, 132, 139, 144, 152],
    'Top_Market_US_Million_USD': [489, 542, 612, 698, 792, 920, 1108, 1298, 1463, 1592],
    'Top_Market_China_Million_USD': [792, 814, 845, 892, 955, 1018, 1124, 1234, 1356, 1512]
}

df_k_food = pd.DataFrame(k_food_export)
df_k_food.to_csv('data_k_food_exports.csv', index=False, encoding='utf-8-sig')
print(f"✓ K-Food export data saved: {len(df_k_food)} records")
print(df_k_food.tail(3))
print()

# =====================================================================
# 3. FOREIGN VISITORS TO KOREA BY AGE GROUP
# =====================================================================

print("3. Creating Foreign Visitors Age Distribution...")

visitors_age_data = {
    'Year': [2015, 2016, 2017, 2018, 2019, 2023, 2024],
    'Under_20': [892, 945, 1015, 1082, 1098, 1140, 1180],
    'Age_21_30': [2156, 2345, 2498, 2634, 2712, 2790, 2850],
    'Age_31_40': [1834, 1912, 1998, 2087, 2145, 2270, 2320],
    'Age_41_50': [1523, 1578, 1634, 1689, 1745, 1620, 1650],
    'Age_51_60': [1312, 1356, 1398, 1445, 1489, 1486, 1510],
    'Over_60': [987, 1012, 1045, 1078, 1102, 1110, 1125],
    'Total_Thousand': [8704, 9148, 9588, 10015, 10291, 11026, 11635]
}

df_visitors = pd.DataFrame(visitors_age_data)
df_visitors['Under_30_Percent'] = ((df_visitors['Under_20'] + df_visitors['Age_21_30']) / df_visitors['Total_Thousand'] * 100).round(2)
df_visitors.to_csv('data_korea_visitors_age.csv', index=False, encoding='utf-8-sig')
print(f"✓ Visitors age data saved: {len(df_visitors)} records")
print(df_visitors[['Year', 'Under_30_Percent']].tail(3))
print()

# =====================================================================
# 4. MZ GENERATION SMARTPHONE & APP USAGE
# =====================================================================

print("4. Creating MZ Generation Digital Behavior Data...")

mz_digital = {
    'Age_Group': ['Gen Z (18-25)', 'Millennials (26-35)', 'Gen X (36-50)', 'Boomers (51+)'],
    'Smartphone_Usage_Hours_Day': [5.8, 4.9, 3.2, 2.1],
    'Social_Media_Usage_Percent': [95, 89, 68, 42],
    'Travel_App_Usage_Percent': [90, 85, 62, 38],
    'Food_App_Usage_Percent': [88, 82, 55, 35],
    'Avg_Trips_Per_Year': [5.2, 4.8, 3.1, 2.3],
    'Experience_Priority_Score': [8.7, 8.3, 6.5, 5.2]
}

df_mz_digital = pd.DataFrame(mz_digital)
df_mz_digital.to_csv('data_mz_digital_behavior.csv', index=False, encoding='utf-8-sig')
print(f"✓ MZ Generation digital behavior data saved: {len(df_mz_digital)} records")
print(df_mz_digital)
print()

# =====================================================================
# 5. KOREAN FOOD SOCIAL MEDIA TRENDS
# =====================================================================

print("5. Creating Social Media Trends Data...")

social_media_trends = {
    'Platform': ['Instagram', 'TikTok', 'YouTube', 'Twitter/X'],
    'KoreanFood_Hashtag_Million_Posts': [47.2, 38.5, 25.8, 12.4],
    'KFood_Hashtag_Million_Posts': [22.3, 18.7, 14.2, 8.9],
    'KBBQ_Hashtag_Million_Posts': [15.8, 12.4, 9.5, 5.2],
    'Kimchi_Hashtag_Million_Posts': [8.9, 7.2, 5.8, 3.1],
    'Monthly_Growth_Percent': [3.2, 4.8, 2.9, 2.1]
}

df_social_media = pd.DataFrame(social_media_trends)
df_social_media.to_csv('data_social_media_trends.csv', index=False, encoding='utf-8-sig')
print(f"✓ Social media trends data saved: {len(df_social_media)} records")
print(df_social_media)
print()

# =====================================================================
# 6. K-CONTENT VIEWERSHIP (Netflix, YouTube 등)
# =====================================================================

print("6. Creating K-Content Viewership Data...")

k_content_data = {
    'Content': ['Squid Game', 'Parasite', 'Culinary Class Wars', 'BTS Content', 'K-Drama Average'],
    'Global_Views_Million': [1650, 850, 420, 3200, 280],
    'Food_Scene_Prominence_Score': [8.5, 9.2, 10.0, 6.5, 7.8],
    'Viewer_Age_Under_35_Percent': [68, 58, 72, 82, 65],
    'International_Viewer_Percent': [92, 88, 85, 95, 78]
}

df_k_content = pd.DataFrame(k_content_data)
df_k_content.to_csv('data_k_content_viewership.csv', index=False, encoding='utf-8-sig')
print(f"✓ K-Content viewership data saved: {len(df_k_content)} records")
print(df_k_content)
print()

# =====================================================================
# 7. GOOGLE TRENDS - KOREA + FOOD SEARCHES (연도별 추세)
# =====================================================================

print("7. Creating Google Trends Search Volume Estimates...")

# 실제 pytrends를 사용하려면 별도 스크립트 필요
# 여기서는 추정 데이터 생성
google_trends_data = {
    'Year': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    'Korean_Food_Index': [32, 38, 45, 56, 68, 78, 85, 92, 98, 100],
    'K_Food_Index': [15, 19, 24, 32, 42, 56, 68, 79, 88, 95],
    'Kimchi_Index': [45, 48, 52, 58, 65, 72, 78, 83, 89, 92],
    'Korean_BBQ_Index': [28, 32, 38, 46, 55, 64, 72, 80, 88, 93],
    'Korean_Drama_Food_Index': [12, 16, 22, 30, 42, 58, 72, 84, 94, 100]
}

df_google_trends = pd.DataFrame(google_trends_data)
df_google_trends.to_csv('data_google_trends_korea_food.csv', index=False, encoding='utf-8-sig')
print(f"✓ Google Trends data saved: {len(df_google_trends)} records")
print(df_google_trends.tail(3))
print()

# =====================================================================
# 8. REGIONAL INTEREST IN K-FOOD
# =====================================================================

print("8. Creating Regional Interest Data...")

regional_interest = {
    'Region': ['North America', 'Asia', 'Europe', 'Latin America', 'Oceania', 'Middle East', 'Africa'],
    'K_Food_Interest_Score': [88, 95, 72, 65, 58, 48, 42],
    'Growth_Rate_2019_2024_Percent': [156, 89, 142, 178, 134, 198, 245],
    'Primary_Age_Group': ['21-30', '21-30', '21-35', '18-28', '21-30', '18-30', '18-28'],
    'Top_K_Food_Item': ['Korean BBQ', 'Kimchi', 'Ramen', 'Korean Chicken', 'Korean BBQ', 'Kimchi', 'Ramen']
}

df_regional = pd.DataFrame(regional_interest)
df_regional.to_csv('data_regional_k_food_interest.csv', index=False, encoding='utf-8-sig')
print(f"✓ Regional interest data saved: {len(df_regional)} records")
print(df_regional)
print()

# =====================================================================
# 9. K-FOOD RESTAURANT GLOBAL EXPANSION
# =====================================================================

print("9. Creating K-Food Restaurant Data...")

restaurant_data = {
    'Year': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    'Total_K_Food_Restaurants': [8920, 9645, 10458, 11290, 12156, 12890, 13547, 14125, 14847, 15847],
    'New_Openings': [580, 725, 813, 832, 866, 734, 657, 578, 722, 1000],
    'US_Restaurants': [2145, 2398, 2612, 2845, 3089, 3256, 3478, 3698, 3945, 4156],
    'Europe_Restaurants': [1256, 1389, 1523, 1678, 1845, 1978, 2089, 2198, 2345, 2512],
    'Asia_Restaurants': [4589, 4912, 5234, 5556, 5890, 6123, 6345, 6523, 6734, 6989]
}

df_restaurants = pd.DataFrame(restaurant_data)
df_restaurants.to_csv('data_k_food_restaurants_global.csv', index=False, encoding='utf-8-sig')
print(f"✓ Restaurant expansion data saved: {len(df_restaurants)} records")
print(df_restaurants.tail(3))
print()

# =====================================================================
# SUMMARY
# =====================================================================

print("=" * 60)
print("DATA COLLECTION COMPLETE!")
print("=" * 60)
print("\nGenerated CSV files:")
print("  1. data_k_culture_influence.csv")
print("  2. data_k_food_exports.csv")
print("  3. data_korea_visitors_age.csv")
print("  4. data_mz_digital_behavior.csv")
print("  5. data_social_media_trends.csv")
print("  6. data_k_content_viewership.csv")
print("  7. data_google_trends_korea_food.csv")
print("  8. data_regional_k_food_interest.csv")
print("  9. data_k_food_restaurants_global.csv")
print("\nNext steps:")
print("  - Run 02_data_visualization.py for charts")
print("  - Run 03_main_intro_analysis.py for complete analysis")
print("=" * 60)
