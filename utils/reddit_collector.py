import praw
import os
from dotenv import load_dotenv

load_dotenv()

class RedditCollector:
    def __init__(self):
        """Initialize Reddit API connection"""
        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT")
        )
    
    def get_hot_posts(self, subreddit_name, limit=10):
        """Fetch hot posts from a subreddit"""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            posts = []
            
            for post in subreddit.hot(limit=limit):
                posts.append({
                    'title': post.title,
                    'content': post.selftext,
                    'score': post.score,
                    'author': str(post.author),
                    'url': post.url,
                    'created_utc': post.created_utc,
                    'num_comments': post.num_comments
                })
            
            return posts
        except Exception as e:
            print(f"Error fetching posts from r/{subreddit_name}: {e}")
            return []
    
    def get_trending_posts(self, subreddits, limit=5):
        """Fetch trending posts from multiple subreddits"""
        all_posts = {}
        
        for subreddit in subreddits:
            posts = self.get_hot_posts(subreddit, limit)
            all_posts[subreddit] = posts
        
        return all_posts 