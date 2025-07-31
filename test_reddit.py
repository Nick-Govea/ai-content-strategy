import praw
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_reddit_connection():
    """Test Reddit API connection"""
    try:
        # Initialize Reddit instance
        reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT")
        )
        
        print("✅ Reddit API connection successful!")
        
        # Test fetching some posts
        subreddit = reddit.subreddit("python")
        posts = list(subreddit.hot(limit=3))
        
        print(f"✅ Successfully fetched {len(posts)} posts from r/python")
        
        # Show first post details
        if posts:
            first_post = posts[0]
            print(f"\n📝 Sample post:")
            print(f"   Title: {first_post.title}")
            print(f"   Score: {first_post.score}")
            print(f"   Author: {first_post.author}")
            print(f"   URL: {first_post.url}")
        
        return True
        
    except Exception as e:
        print(f"❌ Reddit API connection failed: {e}")
        return False

if __name__ == "__main__":
    test_reddit_connection() 