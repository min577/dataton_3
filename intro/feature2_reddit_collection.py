"""
핵심 기능 2: AI 현지화 (재료 대체 추천)
Reddit r/KoreanFood 커뮤니티에서 재료 대체 관련 질문 수집

PRAW (Python Reddit API Wrapper) 사용
Reddit API 키가 필요합니다: https://www.reddit.com/prefs/apps
"""

import praw
import pandas as pd
import re
from datetime import datetime
import os
import time

# Reddit API 인증 정보 (사용자가 직접 입력해야 합니다)
# https://www.reddit.com/prefs/apps 에서 앱을 생성하고 정보를 입력하세요
REDDIT_CLIENT_ID = 'YOUR_CLIENT_ID'  # 여기에 입력
REDDIT_CLIENT_SECRET = 'YOUR_CLIENT_SECRET'  # 여기에 입력
REDDIT_USER_AGENT = 'korean_food_analysis_v1.0'

# 출력 디렉토리
OUTPUT_DIR = r"C:\Users\ASUS\Desktop\DATATON\intro"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 60)
print("Reddit Korean Food 재료 대체 질문 수집")
print("=" * 60)

# Reddit API 인증 확인
if REDDIT_CLIENT_ID == 'YOUR_CLIENT_ID' or REDDIT_CLIENT_SECRET == 'YOUR_CLIENT_SECRET':
    print("\n⚠️  Reddit API 키를 설정해주세요!")
    print("\n1. https://www.reddit.com/prefs/apps 방문")
    print("2. 'Create App' 또는 'Create Another App' 클릭")
    print("3. 다음 정보 입력:")
    print("   - name: korean_food_analyzer (또는 원하는 이름)")
    print("   - App type: script 선택")
    print("   - redirect uri: http://localhost:8080")
    print("4. 생성된 CLIENT_ID와 SECRET을 스크립트에 입력")
    print("\n대안: 수동으로 수집된 샘플 데이터를 사용하려면 feature2_reddit_manual.py를 실행하세요")
    exit()

try:
    # Reddit 인스턴스 생성
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )
    
    print(f"\n✓ Reddit API 연결 성공")
    print(f"  User: {reddit.user.me() if reddit.user.me() else 'Read-only mode'}")
    
except Exception as e:
    print(f"\n✗ Reddit API 연결 실패: {str(e)}")
    print("\n대안: feature2_reddit_manual.py를 사용하세요")
    exit()

# 재료 대체 관련 키워드
substitute_keywords = [
    'substitute',
    'alternative',
    'replace',
    'replacement',
    'instead of',
    'where to buy',
    'where can i find',
    'can\'t find',
    'hard to find'
]

# 분석할 subreddit
subreddit_name = 'KoreanFood'
subreddit = reddit.subreddit(subreddit_name)

print(f"\n분석 대상: r/{subreddit_name}")
print(f"구독자 수: {subreddit.subscribers:,}")

# 데이터 수집
posts_data = []
comments_data = []

print(f"\n게시물 수집 중...")

# 최근 1000개 게시물 검색
try:
    # 'hot', 'new', 'top' 등 다양한 정렬 방식으로 수집
    for sort_type in ['hot', 'new', 'top']:
        print(f"\n  [{sort_type}] 게시물 수집 중...")
        
        if sort_type == 'hot':
            posts = subreddit.hot(limit=300)
        elif sort_type == 'new':
            posts = subreddit.new(limit=300)
        else:  # top
            posts = subreddit.top(time_filter='year', limit=300)
        
        count = 0
        for post in posts:
            # 제목과 본문에서 재료 대체 키워드 확인
            title_lower = post.title.lower()
            selftext_lower = post.selftext.lower()
            
            is_substitute_related = any(keyword in title_lower or keyword in selftext_lower 
                                       for keyword in substitute_keywords)
            
            posts_data.append({
                'post_id': post.id,
                'title': post.title,
                'selftext': post.selftext,
                'author': str(post.author),
                'created_utc': datetime.fromtimestamp(post.created_utc),
                'score': post.score,
                'num_comments': post.num_comments,
                'url': post.url,
                'is_substitute_related': is_substitute_related,
                'sort_type': sort_type
            })
            
            # 재료 대체 관련 게시물의 댓글도 수집
            if is_substitute_related:
                try:
                    post.comments.replace_more(limit=0)  # "load more comments" 제거
                    for comment in post.comments.list()[:20]:  # 상위 20개 댓글
                        comments_data.append({
                            'post_id': post.id,
                            'comment_id': comment.id,
                            'body': comment.body,
                            'author': str(comment.author),
                            'created_utc': datetime.fromtimestamp(comment.created_utc),
                            'score': comment.score
                        })
                except Exception as e:
                    pass
            
            count += 1
            if count % 50 == 0:
                print(f"    진행: {count}개 게시물 처리...")
            
            time.sleep(0.1)  # API 제한 준수
        
        print(f"  ✓ {count}개 게시물 수집 완료")
        time.sleep(2)

except Exception as e:
    print(f"\n✗ 데이터 수집 오류: {str(e)}")

# 데이터프레임 생성
posts_df = pd.DataFrame(posts_data)
comments_df = pd.DataFrame(comments_data)

# 중복 제거
posts_df = posts_df.drop_duplicates(subset=['post_id'])
comments_df = comments_df.drop_duplicates(subset=['comment_id'])

print(f"\n{'='*60}")
print("수집 결과")
print(f"{'='*60}")
print(f"총 게시물: {len(posts_df)}개")
print(f"재료 대체 관련 게시물: {posts_df['is_substitute_related'].sum()}개")
print(f"수집된 댓글: {len(comments_df)}개")

# CSV 저장
posts_path = os.path.join(OUTPUT_DIR, 'feature2_reddit_posts.csv')
comments_path = os.path.join(OUTPUT_DIR, 'feature2_reddit_comments.csv')

posts_df.to_csv(posts_path, index=False, encoding='utf-8-sig')
comments_df.to_csv(comments_path, index=False, encoding='utf-8-sig')

print(f"\n✓ 데이터 저장 완료:")
print(f"  - {posts_path}")
print(f"  - {comments_path}")

# 재료 대체 관련 게시물 미리보기
if posts_df['is_substitute_related'].sum() > 0:
    print(f"\n[재료 대체 관련 게시물 미리보기]")
    substitute_posts = posts_df[posts_df['is_substitute_related']].head(5)
    for idx, row in substitute_posts.iterrows():
        print(f"\n제목: {row['title']}")
        print(f"작성일: {row['created_utc']}")
        print(f"점수: {row['score']} | 댓글: {row['num_comments']}")

print("\n수집 완료!")
