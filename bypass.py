"""
Anti-Detection and Bypass Module
Generates random headers, user agents, and bypass techniques
"""

import random
import string
import time
from fake_useragent import UserAgent

class AntiDetection:
    def __init__(self):
        self.ua = UserAgent()
        self.devices = [
            'Windows NT 10.0; Win64; x64',
            'Macintosh; Intel Mac OS X 10_15_7',
            'X11; Linux x86_64',
            'Windows NT 6.1; Win64; x64',
            'Windows NT 10.0; WOW64'
        ]
        
        self.browsers = [
            'Chrome/120.0.0.0 Safari/537.36',
            'Chrome/119.0.0.0 Safari/537.36',
            'Firefox/121.0',
            'Firefox/120.0',
            'Safari/605.1.15',
            'Edg/120.0.0.0'
        ]
        
        self.languages = [
            'en-US,en;q=0.9,id;q=0.8',
            'en-US,en;q=0.9',
            'id-ID,id;q=0.9,en;q=0.8',
            'en-GB,en;q=0.9',
            'en-US,en;q=0.9,fr;q=0.8'
        ]
        
        self.referrers = [
            'https://www.google.com/',
            'https://www.youtube.com/',
            'https://www.facebook.com/',
            'https://twitter.com/',
            'https://www.instagram.com/',
            'https://www.tiktok.com/'
        ]
    
    def random_user_agent(self):
        """Generate random user agent"""
        try:
            return self.ua.random
        except:
            device = random.choice(self.devices)
            browser = random.choice(self.browsers)
            return f"Mozilla/5.0 ({device}) AppleWebKit/537.36 (KHTML, like Gecko) {browser}"
    
    def random_device(self):
        return random.choice(self.devices)
    
    def random_language(self):
        return random.choice(self.languages)
    
    def random_referrer(self):
        return random.choice(self.referrers)
    
    def random_ip(self):
        return f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    
    def random_session_id(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    
    def generate_headers(self):
        """Generate complete request headers"""
        return {
            'User-Agent': self.random_user_agent(),
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': self.random_language(),
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': self.random_referrer(),
            'Origin': 'https://www.tiktok.com',
            'Sec-Ch-Ua': '"Google Chrome";v="120", "Not_A Brand";v="8"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Connection': 'keep-alive',
            'X-Forwarded-For': self.random_ip(),
            'X-Real-IP': self.random_ip()
        }
    
    def bypass_cloudflare(self, session, url):
        """Try to bypass Cloudflare"""
        try:
            # Add delay and headers
            time.sleep(random.uniform(2, 4))
            headers = self.generate_headers()
            resp = session.get(url, headers=headers, timeout=20)
            return resp
        except:
            return None
