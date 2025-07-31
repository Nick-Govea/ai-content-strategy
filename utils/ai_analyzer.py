import google.generativeai as genai
from utils.config import GEMINI_API_KEY, validate_config

class AIAnalyzer:
    def __init__(self):
        """Initialize Gemini API connection"""
        # Validate configuration
        if not validate_config():
            raise ValueError("Missing required Gemini API configuration")
        
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables or secrets")
        
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    def analyze_reddit_trends(self, reddit_data, analysis_type="trends"):
        """Analyze Reddit data and provide insights"""
        try:
            # Format Reddit data for analysis
            formatted_data = self._format_reddit_data(reddit_data)
            
            # Create prompt based on analysis type
            if analysis_type == "trends":
                prompt = f"""
                Analyze these Reddit posts and identify key trends:
                
                {formatted_data}
                
                Provide:
                1. Top 3 trending topics
                2. Common themes
                3. Content strategy recommendations
                
                Keep your response professional and actionable.
                """
            elif analysis_type == "sentiment":
                prompt = f"""
                Analyze the sentiment and tone of these Reddit posts:
                
                {formatted_data}
                
                Provide:
                1. Overall sentiment (positive/negative/neutral)
                2. Key emotional themes
                3. Community mood insights
                """
            else:
                prompt = f"Analyze this Reddit data: {formatted_data}"
            
            # Generate response
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Error analyzing data: {e}"
    
    def generate_content_ideas(self, reddit_data, topic=None):
        """Generate content ideas based on Reddit trends"""
        try:
            formatted_data = self._format_reddit_data(reddit_data)
            
            prompt = f"""
            Based on these Reddit posts, generate 5 content ideas:
            
            {formatted_data}
            
            {f'Focus on: {topic}' if topic else ''}
            
            For each idea, provide:
            - Title
            - Key points to cover
            - Target audience
            - Content format suggestion
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Error generating content ideas: {e}"
    
    def _format_reddit_data(self, reddit_data):
        """Format Reddit data for AI analysis"""
        formatted = ""
        
        for subreddit, posts in reddit_data.items():
            formatted += f"\n--- r/{subreddit} ---\n"
            for post in posts:
                formatted += f"Title: {post['title']}\n"
                if post['content']:
                    formatted += f"Content: {post['content'][:200]}...\n"
                formatted += f"Score: {post['score']}, Comments: {post['num_comments']}\n\n"
        
        return formatted
