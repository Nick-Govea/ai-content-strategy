import streamlit as st

# Import our backend modules
from utils.reddit_collector import RedditCollector
from utils.ai_analyzer import AIAnalyzer
from utils.data_processor import DataProcessor
from utils.config import validate_config, is_streamlit_cloud

# Initialize backend services
@st.cache_resource
def init_services():
    """Initialize backend services (cached to avoid re-initialization)"""
    try:
        reddit_collector = RedditCollector()
        ai_analyzer = AIAnalyzer()
        data_processor = DataProcessor()
        return reddit_collector, ai_analyzer, data_processor
    except Exception as e:
        st.error(f"Error initializing services: {e}")
        return None, None, None

# Main app
def main():
    st.title("AI Content Strategy Assistant")
    st.markdown("Analyze Reddit trends and generate content strategies with AI")
    
    # Show environment info
    if is_streamlit_cloud():
        st.sidebar.success("🌐 Running on Streamlit Cloud")
    else:
        st.sidebar.info("💻 Running locally")
    
    # Initialize services
    reddit_collector, ai_analyzer, data_processor = init_services()
    
    if not all([reddit_collector, ai_analyzer, data_processor]):
        st.error("Failed to initialize services. Please check your API keys.")
        if not validate_config():
            st.error("Configuration validation failed. Check your .env file or Streamlit secrets.")
        return
    
    # Sidebar for configuration
    st.sidebar.header("Configuration")
    
    # Subreddit selection
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
    
    # Number of posts to fetch
    post_limit = st.sidebar.slider("Posts per subreddit:", 1, 20, 5)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📊 Data Collection")
        
        if st.button("Fetch Reddit Data"):
            with st.spinner("Fetching Reddit data..."):
                try:
                    # Fetch data from Reddit
                    reddit_data = reddit_collector.get_trending_posts(subreddits, post_limit)
                    
                    # Clean and process data
                    cleaned_data = data_processor.clean_reddit_data(reddit_data)
                    filtered_data = data_processor.filter_top_posts(cleaned_data)
                    
                    # Save to session state
                    st.session_state.reddit_data = filtered_data
                    st.session_state.formatted_data = data_processor.format_for_display(filtered_data)
                    
                    st.success(f"✅ Fetched {sum(len(posts) for posts in filtered_data.values())} posts from {len(filtered_data)} subreddits")
                    
                except Exception as e:
                    st.error(f"Error fetching data: {e}")
    
    with col2:
        st.header("🤖 AI Analysis")
        
        if 'reddit_data' in st.session_state and st.session_state.reddit_data:
            if st.button("Generate AI Analysis"):
                with st.spinner("Analyzing with AI..."):
                    try:
                        if analysis_type == "content_ideas":
                            analysis = ai_analyzer.generate_content_ideas(st.session_state.reddit_data)
                        else:
                            analysis = ai_analyzer.analyze_reddit_trends(st.session_state.reddit_data, analysis_type)
                        
                        st.session_state.analysis = analysis
                        st.success("✅ Analysis complete!")
                        
                    except Exception as e:
                        st.error(f"Error generating analysis: {e}")
    
    # Display results
    if 'formatted_data' in st.session_state and st.session_state.formatted_data:
        st.header("📈 Reddit Data")
        
        for subreddit, posts in st.session_state.formatted_data.items():
            with st.expander(f"r/{subreddit} ({len(posts)} posts)"):
                for post in posts:
                    st.markdown(f"**{post['title']}**")
                    st.markdown(f"Score: {post['score']} | Comments: {post['num_comments']} | Engagement: {post['engagement_rate']}")
                    if post['content']:
                        st.markdown(f"*{post['content'][:100]}...*")
                    st.markdown(f"[View Post]({post['url']})")
                    st.divider()
    
    if 'analysis' in st.session_state:
        st.header("🧠 AI Analysis Results")
        st.markdown(st.session_state.analysis)

if __name__ == "__main__":
    main()