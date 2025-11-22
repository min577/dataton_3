"""
OPTIONAL: Real Google Trends Data Collection using pytrends
실제 Google Trends API를 사용하여 데이터를 수집하는 고급 스크립트
"""

from pytrends.request import TrendReq
import pandas as pd
import time
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("Google Trends Real Data Collection")
print("=" * 60)
print("\n⚠️  NOTE: This script requires internet connection")
print("⚠️  Rate limiting applies - script includes delays\n")

# Initialize pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# =====================================================================
# 1. KOREA + FOOD SEARCH TRENDS
# =====================================================================

print("1. Collecting Korea + Food search trends...")

keywords_food = ['Korean food', 'K-food', 'Kimchi', 'Korean BBQ', 'Korean cuisine']

try:
    pytrends.build_payload(
        keywords_food, 
        timeframe='2015-01-01 2024-12-31',
        geo=''  # Worldwide
    )
    
    df_trends_food = pytrends.interest_over_time()
    
    if not df_trends_food.empty:
        df_trends_food = df_trends_food.drop(columns=['isPartial'], errors='ignore')
        df_trends_food.to_csv('real_data_google_trends_korea_food.csv', encoding='utf-8-sig')
        print(f"✓ Saved: real_data_google_trends_korea_food.csv ({len(df_trends_food)} records)")
        print(f"  Date range: {df_trends_food.index[0]} to {df_trends_food.index[-1]}")
    else:
        print("✗ No data returned")
        
except Exception as e:
    print(f"✗ Error: {e}")

time.sleep(60)  # Rate limiting - wait 1 minute

# =====================================================================
# 2. K-DRAMA + FOOD CORRELATION
# =====================================================================

print("\n2. Collecting K-Drama + Food correlation...")

keywords_drama_food = ['Korean drama', 'K-drama', 'Korean food', 'Korean restaurant']

try:
    pytrends.build_payload(
        keywords_drama_food, 
        timeframe='2015-01-01 2024-12-31',
        geo=''
    )
    
    df_trends_drama = pytrends.interest_over_time()
    
    if not df_trends_drama.empty:
        df_trends_drama = df_trends_drama.drop(columns=['isPartial'], errors='ignore')
        df_trends_drama.to_csv('real_data_google_trends_kdrama_food.csv', encoding='utf-8-sig')
        print(f"✓ Saved: real_data_google_trends_kdrama_food.csv ({len(df_trends_drama)} records)")
    else:
        print("✗ No data returned")
        
except Exception as e:
    print(f"✗ Error: {e}")

time.sleep(60)

# =====================================================================
# 3. REGIONAL INTEREST BY COUNTRY
# =====================================================================

print("\n3. Collecting regional interest data...")

regions = {
    'US': 'United States',
    'JP': 'Japan',
    'CN': 'China',
    'GB': 'United Kingdom',
    'FR': 'France',
    'DE': 'Germany',
    'AU': 'Australia',
    'BR': 'Brazil',
    'MX': 'Mexico',
    'TH': 'Thailand'
}

regional_data = []

for country_code, country_name in regions.items():
    print(f"  Collecting {country_name}...")
    
    try:
        pytrends.build_payload(
            ['Korean food'], 
            timeframe='2019-01-01 2024-12-31',
            geo=country_code
        )
        
        df_region = pytrends.interest_over_time()
        
        if not df_region.empty:
            df_region = df_region.drop(columns=['isPartial'], errors='ignore')
            avg_interest = df_region['Korean food'].mean()
            recent_interest = df_region['Korean food'].iloc[-12:].mean()  # Last 12 months
            growth = ((recent_interest - df_region['Korean food'].iloc[:12].mean()) / 
                     df_region['Korean food'].iloc[:12].mean() * 100)
            
            regional_data.append({
                'Country': country_name,
                'Country_Code': country_code,
                'Average_Interest': avg_interest,
                'Recent_12mo_Interest': recent_interest,
                'Growth_Rate_Percent': growth
            })
            
            print(f"    ✓ Avg Interest: {avg_interest:.1f}, Growth: {growth:.1f}%")
        
        time.sleep(5)  # Small delay between requests
        
    except Exception as e:
        print(f"    ✗ Error for {country_name}: {e}")
        continue

if regional_data:
    df_regional = pd.DataFrame(regional_data)
    df_regional.to_csv('real_data_google_trends_regional.csv', index=False, encoding='utf-8-sig')
    print(f"\n✓ Saved: real_data_google_trends_regional.csv ({len(df_regional)} countries)")

time.sleep(60)

# =====================================================================
# 4. RELATED QUERIES
# =====================================================================

print("\n4. Collecting related queries...")

try:
    pytrends.build_payload(
        ['Korean food'], 
        timeframe='today 12-m',  # Last 12 months
        geo=''
    )
    
    # Get related queries
    related_queries = pytrends.related_queries()
    
    if related_queries['Korean food']:
        # Top queries
        top_queries = related_queries['Korean food']['top']
        if top_queries is not None:
            top_queries.to_csv('real_data_related_queries_top.csv', encoding='utf-8-sig')
            print(f"✓ Saved: real_data_related_queries_top.csv")
        
        # Rising queries
        rising_queries = related_queries['Korean food']['rising']
        if rising_queries is not None:
            rising_queries.to_csv('real_data_related_queries_rising.csv', encoding='utf-8-sig')
            print(f"✓ Saved: real_data_related_queries_rising.csv")
    
except Exception as e:
    print(f"✗ Error: {e}")

time.sleep(60)

# =====================================================================
# 5. TRENDING SEARCHES
# =====================================================================

print("\n5. Collecting trending searches (Korea-related)...")

try:
    # Get trending searches for US
    trending = pytrends.trending_searches(pn='united_states')
    trending.to_csv('real_data_trending_searches_us.csv', encoding='utf-8-sig', header=False)
    print(f"✓ Saved: real_data_trending_searches_us.csv")
    
except Exception as e:
    print(f"✗ Error: {e}")

# =====================================================================
# 6. INTEREST BY REGION MAP DATA
# =====================================================================

print("\n6. Collecting interest by region (map data)...")

try:
    pytrends.build_payload(
        ['Korean food'], 
        timeframe='today 12-m',
        geo=''
    )
    
    df_map = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=True)
    df_map = df_map.sort_values('Korean food', ascending=False)
    df_map.to_csv('real_data_interest_by_country.csv', encoding='utf-8-sig')
    print(f"✓ Saved: real_data_interest_by_country.csv ({len(df_map)} countries)")
    print(f"\nTop 10 countries by interest:")
    print(df_map.head(10))
    
except Exception as e:
    print(f"✗ Error: {e}")

# =====================================================================
# SUMMARY
# =====================================================================

print("\n" + "=" * 60)
print("REAL DATA COLLECTION COMPLETE")
print("=" * 60)
print("\n✓ Successfully collected real Google Trends data")
print("\nGenerated files:")
print("  1. real_data_google_trends_korea_food.csv")
print("  2. real_data_google_trends_kdrama_food.csv")
print("  3. real_data_google_trends_regional.csv")
print("  4. real_data_related_queries_top.csv")
print("  5. real_data_related_queries_rising.csv")
print("  6. real_data_trending_searches_us.csv")
print("  7. real_data_interest_by_country.csv")
print("\nNote: Use these files to replace synthetic data for more accurate analysis")
print("=" * 60)
