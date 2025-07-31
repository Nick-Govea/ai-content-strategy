import json
from datetime import datetime

class DataProcessor:
    def __init__(self):
        pass
    
    def clean_reddit_data(self, reddit_data):
        """Clean and validate Reddit data"""
        cleaned_data = {}
        
        for subreddit, posts in reddit_data.items():
            cleaned_posts = []
            
            for post in posts:
                # Remove empty or invalid posts
                if not post.get('title') or post.get('title') == '[deleted]':
                    continue
                
                # Clean the data
                cleaned_post = {
                    'title': post.get('title', '').strip(),
                    'content': post.get('content', '').strip(),
                    'score': int(post.get('score', 0)),
                    'author': post.get('author', 'Unknown'),
                    'url': post.get('url', ''),
                    'num_comments': int(post.get('num_comments', 0)),
                    'created_utc': post.get('created_utc', 0)
                }
                
                cleaned_posts.append(cleaned_post)
            
            if cleaned_posts:  # Only add subreddits with valid posts
                cleaned_data[subreddit] = cleaned_posts
        
        return cleaned_data
    
    def filter_top_posts(self, reddit_data, min_score=10, min_comments=5):
        """Filter posts by score and comment count"""
        filtered_data = {}
        
        for subreddit, posts in reddit_data.items():
            filtered_posts = [
                post for post in posts
                if post.get('score', 0) >= min_score and post.get('num_comments', 0) >= min_comments
            ]
            
            if filtered_posts:
                filtered_data[subreddit] = filtered_posts
        
        return filtered_data
    
    def save_to_cache(self, data, filename="reddit_cache.json"):
        """Save data to cache file"""
        try:
            with open(f"data/{filename}", 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving cache: {e}")
            return False
    
    def load_from_cache(self, filename="reddit_cache.json"):
        """Load data from cache file"""
        try:
            with open(f"data/{filename}", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
        except Exception as e:
            print(f"Error loading cache: {e}")
            return None
    
    def format_for_display(self, reddit_data):
        """Format data for Streamlit display"""
        formatted = {}
        
        for subreddit, posts in reddit_data.items():
            formatted_posts = []
            
            for post in posts:
                # Convert timestamp to readable date
                created_date = datetime.fromtimestamp(post.get('created_utc', 0))
                
                formatted_post = {
                    'title': post.get('title', ''),
                    'content': post.get('content', ''),
                    'score': post.get('score', 0),
                    'author': post.get('author', 'Unknown'),
                    'url': post.get('url', ''),
                    'num_comments': post.get('num_comments', 0),
                    'created_date': created_date.strftime('%Y-%m-%d %H:%M'),
                    'engagement_rate': self._calculate_engagement(post)
                }
                
                formatted_posts.append(formatted_post)
            
            formatted[subreddit] = formatted_posts
        
        return formatted
    
    def _calculate_engagement(self, post):
        """Calculate engagement rate (comments + score)"""
        score = post.get('score', 0)
        comments = post.get('num_comments', 0)
        return score + comments 