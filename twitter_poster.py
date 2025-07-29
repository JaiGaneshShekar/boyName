"""
Twitter API Integration Module

This module handles posting names to Twitter when successful tweaks are found.
Requires Twitter API v2 credentials.
"""

import requests
import json
import os
from typing import Optional, Dict, Any


class TwitterPoster:
    """
    Class to handle Twitter API interactions for posting names.
    """
    
    def __init__(self, bearer_token: Optional[str] = None, 
                 api_key: Optional[str] = None,
                 api_secret: Optional[str] = None,
                 access_token: Optional[str] = None,
                 access_token_secret: Optional[str] = None):
        """
        Initialize Twitter poster with API credentials.
        
        Args:
            bearer_token: Twitter API Bearer Token
            api_key: Twitter API Key
            api_secret: Twitter API Secret
            access_token: Twitter Access Token
            access_token_secret: Twitter Access Token Secret
        """
        self.bearer_token = bearer_token or os.getenv('TWITTER_BEARER_TOKEN')
        self.api_key = api_key or os.getenv('TWITTER_API_KEY')
        self.api_secret = api_secret or os.getenv('TWITTER_API_SECRET')
        self.access_token = access_token or os.getenv('TWITTER_ACCESS_TOKEN')
        self.access_token_secret = access_token_secret or os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        
        self.base_url = "https://api.twitter.com/2/"
        
    def _get_auth_headers(self) -> Dict[str, str]:
        """
        Get authentication headers for Twitter API.
        
        Returns:
            dict: Headers with authorization
        """
        if not self.bearer_token:
            raise ValueError("Bearer token is required for Twitter API")
            
        return {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json"
        }
    
    def create_tweet(self, text: str) -> Dict[str, Any]:
        """
        Create a tweet with the given text.
        
        Args:
            text: Tweet content
            
        Returns:
            dict: Twitter API response
        """
        url = f"{self.base_url}tweets"
        headers = self._get_auth_headers()
        
        payload = {
            "text": text
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": True,
                "message": f"Failed to post tweet: {str(e)}",
                "status_code": getattr(e.response, 'status_code', None)
            }
    
    def format_name_tweet(self, tweak_result: Dict[str, Any]) -> str:
        """
        Format a name tweak result into a tweet.
        
        Args:
            tweak_result: Result from name_tweaker.find_target_tweaks
            
        Returns:
            str: Formatted tweet text
        """
        original = tweak_result['original']
        tweaked = tweak_result['tweaked']
        chaldean_sum = tweak_result['chaldean_sum']
        num_changes = tweak_result['num_changes']
        
        # Create a concise tweet
        tweet_text = f"✨ Name Optimization ✨\n\n"
        tweet_text += f"Original: {original}\n"
        tweet_text += f"Optimized: {tweaked}\n"
        tweet_text += f"Chaldean Value: {chaldean_sum} (reduces to 5)\n"
        tweet_text += f"Changes: {num_changes}\n\n"
        tweet_text += "#Numerology #NameOptimization #ChaldeanNumerology"
        
        # Ensure tweet is under 280 characters
        if len(tweet_text) > 280:
            # Create shorter version
            tweet_text = f"✨ {original} → {tweaked} ✨\n"
            tweet_text += f"Chaldean: {chaldean_sum} (reduces to 5)\n"
            tweet_text += f"{num_changes} change{'s' if num_changes != 1 else ''}\n"
            tweet_text += "#Numerology #ChaldeanNumerology"
        
        return tweet_text
    
    def post_name_optimization(self, tweak_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Post a name optimization result to Twitter.
        
        Args:
            tweak_result: Result from name_tweaker.find_target_tweaks
            
        Returns:
            dict: Twitter API response
        """
        tweet_text = self.format_name_tweet(tweak_result)
        return self.create_tweet(tweet_text)
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test the Twitter API connection.
        
        Returns:
            dict: Connection test result
        """
        url = f"{self.base_url}users/me"
        headers = self._get_auth_headers()
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return {
                "success": True,
                "data": response.json(),
                "message": "Twitter API connection successful"
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Twitter API connection failed"
            }


def create_sample_env_file():
    """
    Create a sample .env file with Twitter API key placeholders.
    """
    env_content = """# Twitter API Credentials
# Get these from https://developer.twitter.com/

TWITTER_BEARER_TOKEN=your_bearer_token_here
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
"""
    
    with open('.env.sample', 'w') as f:
        f.write(env_content)
    
    print("Created .env.sample file. Copy to .env and add your Twitter API credentials.")


if __name__ == "__main__":
    # Create sample environment file
    create_sample_env_file()
    
    # Test connection if credentials are available
    poster = TwitterPoster()
    test_result = poster.test_connection()
    print(f"Twitter API Test: {test_result['message']}")