import streamlit as st
import praw
import google.generativeai as genai
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Simple config function that works both locally and on Streamlit Cloud
def get_api_key(key_name):
    """Get API key from Streamlit secrets or environment variables"""
    try:
        # Try Streamlit secrets first (for cloud deployment)
        return st.secrets[key_name]
    except:
        # Fall back to environment variables (for local development)
        return os.getenv(key_name)

# Initialize APIs
def init_apis():
    """Initialize Reddit and Gemini APIs"""
    # Get API keys
    gemini_key = get_api_key("GEMINI_API_KEY")
    reddit_id = get_api_key("REDDIT_CLIENT_ID")
    reddit_secret = get_api_key("REDDIT_CLIENT_SECRET")
    reddit_agent = get_api_key("REDDIT_USER_AGENT")
    
    # Check if all keys are available
    if not all([gemini_key, reddit_id, reddit_secret, reddit_agent]):
        st.error("❌ Missing API keys. Please check your configuration.")
        st.info("For local development: Add keys to .env file")
        st.info("For Streamlit Cloud: Add keys to Streamlit secrets")
        return None, None
    
    try:
        # Initialize Reddit
        reddit = praw.Reddit(
            client_id=reddit_id,
            client_secret=reddit_secret,
            user_agent=reddit_agent
        )
        
        # Initialize Gemini
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        return reddit, model
    except Exception as e:
        st.error(f"❌ Error initializing APIs: {e}")
        return None, None

# Fetch Reddit posts
def fetch_reddit_posts(reddit, subreddits, limit=5):
    """Fetch posts from multiple subreddits"""
    all_posts = {}
    
    for subreddit_name in subreddits:
        try:
            subreddit = reddit.subreddit(subreddit_name)
            posts = []
            
            for post in subreddit.hot(limit=limit):
                posts.append({
                    'title': post.title,
                    'content': post.selftext[:200] + "..." if len(post.selftext) > 200 else post.selftext,
                    'score': post.score,
                    'comments': post.num_comments,
                    'url': post.url,
                    'author': str(post.author)
                })
            
            all_posts[subreddit_name] = posts
            
        except Exception as e:
            st.warning(f"⚠️ Error fetching from r/{subreddit_name}: {e}")
    
    return all_posts

# Analyze with AI
def analyze_with_ai(model, reddit_data, analysis_type):
    """Analyze Reddit data with Gemini AI"""
    try:
        # Format data for AI
        data_text = ""
        for subreddit, posts in reddit_data.items():
            data_text += f"\n--- r/{subreddit} ---\n"
            for post in posts:
                data_text += f"Title: {post['title']}\n"
                data_text += f"Content: {post['content']}\n"
                data_text += f"Score: {post['score']}, Comments: {post['comments']}\n\n"
        
        # Create prompt based on analysis type
        if analysis_type == "trends":
            prompt = f"Analyze these Reddit posts and identify key trends:\n\n{data_text}\n\nProvide:\n1. Top 3 trending topics\n2. Common themes\n3. Content strategy recommendations"
        elif analysis_type == "sentiment":
            prompt = f"Analyze the sentiment of these Reddit posts:\n\n{data_text}\n\nProvide:\n1. Overall sentiment\n2. Key emotional themes\n3. Community mood insights"
        else:  # content_ideas
            prompt = f"Based on these Reddit posts, generate 5 content ideas:\n\n{data_text}\n\nFor each idea, provide:\n- Title\n- Key points\n- Target audience"
        
        # Generate response
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"❌ Error analyzing data: {e}"

# Main app
def main():
    st.title("🤖 AI Content Strategy Assistant")
    st.markdown("Analyze Reddit trends and generate content strategies with AI")
    
    # Initialize APIs
    reddit, model = init_apis()
    
    if not reddit or not model:
        st.stop()
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")
    
    # Subreddit input
    subreddits_input = st.sidebar.text_area(
        "Enter subreddits (one per line):",
        value="python\nprogramming\nwebdev",
        help="Enter subreddit names without the 'r/' prefix"
    )
    subreddits = [sub.strip() for sub in subreddits_input.split('\n') if sub.strip()]
    
    # Analysis type
    analysis_type = st.sidebar.selectbox(
        "Analysis Type:",
        ["trends", "sentiment", "content_ideas"]
    )
    
    # Post limit
    post_limit = st.sidebar.slider("Posts per subreddit:", 1, 10, 5)
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📊 Data Collection")
        
        if st.button("🔍 Fetch Reddit Data"):
            with st.spinner("Fetching Reddit data..."):
                reddit_data = fetch_reddit_posts(reddit, subreddits, post_limit)
                
                if reddit_data:
                    st.session_state.reddit_data = reddit_data
                    total_posts = sum(len(posts) for posts in reddit_data.values())
                    st.success(f"✅ Fetched {total_posts} posts from {len(reddit_data)} subreddits")
                else:
                    st.error("❌ No data fetched")
    
    with col2:
        st.header("🧠 AI Analysis")
        
        if 'reddit_data' in st.session_state and st.session_state.reddit_data:
            if st.button("🤖 Generate Analysis"):
                with st.spinner("Analyzing with AI..."):
                    analysis = analyze_with_ai(model, st.session_state.reddit_data, analysis_type)
                    st.session_state.analysis = analysis
                    st.success("✅ Analysis complete!")
    
    # Display results
    if 'reddit_data' in st.session_state and st.session_state.reddit_data:
        st.header("📈 Reddit Data")
        
        for subreddit, posts in st.session_state.reddit_data.items():
            with st.expander(f"r/{subreddit} ({len(posts)} posts)"):
                for post in posts:
                    st.markdown(f"**{post['title']}**")
                    st.markdown(f"Score: {post['score']} | Comments: {post['comments']}")
                    if post['content']:
                        st.markdown(f"*{post['content']}*")
                    st.markdown(f"[View Post]({post['url']})")
                    st.divider()
    
    if 'analysis' in st.session_state:
        st.header("🧠 AI Analysis Results")
        st.markdown(st.session_state.analysis)

if __name__ == "__main__":
    main()