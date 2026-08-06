"""
TikTok Scraper Module
Scrapes accounts by keyword or from trending
"""

import time
import json
import random
import requests
from .bypass import AntiDetection

class TikTokScraper:
    def __init__(self, config):
        self.config = config
        self.bypass = AntiDetection()
        self.session = requests.Session()
        
    def search(self, keyword, limit=50):
        """Search accounts by keyword"""
        results = []
        cursor = 0
        
        try:
            while len(results) < limit:
                url = "https://www.tiktok.com/api/v1/search/user/"
                params = {
                    'keyword': keyword,
                    'cursor': cursor,
                    'count': min(30, limit - len(results))
                }
                
                headers = self.bypass.generate_headers()
                resp = self.session.get(url, params=params, headers=headers, timeout=15)
                
                if resp.status_code == 200:
                    data = resp.json()
                    users = data.get('user_list', [])
                    
                    for user in users:
                        username = user.get('unique_id')
                        if username:
                            results.append(username)
                    
                    if not data.get('has_more'):
                        break
                    
                    cursor = data.get('cursor', cursor + 30)
                    time.sleep(random.uniform(1, 2))
                else:
                    break
                    
        except Exception as e:
            pass
        
        return results[:limit]
    
    def trending(self, limit=100):
        """Get trending accounts"""
        results = []
        try:
            url = "https://www.tiktok.com/api/v1/discover/"
            headers = self.bypass.generate_headers()
            resp = self.session.get(url, headers=headers, timeout=15)
            
            if resp.status_code == 200:
                data = resp.json()
                for item in data.get('user_list', []):
                    username = item.get('unique_id')
                    if username:
                        results.append(username)
        except Exception:
            pass
        
        return results[:limit]
    
    def from_hashtag(self, hashtag, limit=50):
        """Get accounts from hashtag"""
        results = []
        cursor = 0
        
        try:
            while len(results) < limit:
                url = f"https://www.tiktok.com/api/v1/search/hashtag/"
                params = {
                    'keyword': hashtag,
                    'cursor': cursor,
                    'count': min(30, limit - len(results))
                }
                
                headers = self.bypass.generate_headers()
                resp = self.session.get(url, params=params, headers=headers, timeout=15)
                
                if resp.status_code == 200:
                    data = resp.json()
                    # Extract users from posts
                    for post in data.get('post_list', []):
                        username = post.get('author', {}).get('unique_id')
                        if username and username not in results:
                            results.append(username)
                    
                    if not data.get('has_more'):
                        break
                    
                    cursor = data.get('cursor', cursor + 30)
                    time.sleep(random.uniform(1, 2))
                else:
                    break
                    
        except Exception:
            pass
        
        return results[:limit]
