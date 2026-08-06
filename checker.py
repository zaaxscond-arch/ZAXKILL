"""
Account Checker Module
Fetches TikTok account information
"""

import json
import requests
from .bypass import AntiDetection
from .utils import format_number

class AccountChecker:
    def __init__(self, config):
        self.config = config
        self.bypass = AntiDetection()
        self.session = requests.Session()
        
    def get_info(self, username):
        """Get account info as dict"""
        try:
            url = f"https://www.tiktok.com/api/v1/user/detail/?username={username}"
            headers = self.bypass.generate_headers()
            resp = self.session.get(url, headers=headers, timeout=15)
            
            if resp.status_code == 200:
                data = resp.json()
                user = data.get('userInfo', {}).get('user', {})
                stats = data.get('userInfo', {}).get('stats', {})
                
                return {
                    'id': user.get('id'),
                    'username': user.get('uniqueId'),
                    'nickname': user.get('nickname'),
                    'bio': user.get('bioDescription', ''),
                    'verified': user.get('verified', False),
                    'private': user.get('privateAccount', False),
                    'followers': stats.get('followerCount', 0),
                    'following': stats.get('followingCount', 0),
                    'likes': stats.get('heartCount', 0),
                    'videos': stats.get('videoCount', 0),
                    'created': user.get('createTime', 0)
                }
            return None
        except Exception:
            return None
    
    def get_full_info(self, username):
        """Get formatted account info"""
        info = self.get_info(username)
        if not info:
            return "❌ Account not found or private"
        
        verified = "✅" if info.get('verified') else "❌"
        private = "🔒" if info.get('private') else "🌐"
        
        return f"""
╔══════════════════════════════════════════════════════════════╗
║                    ACCOUNT INFORMATION                      ║
╠══════════════════════════════════════════════════════════════╣
║ Username    : @{info.get('username', 'N/A'):<45}║
║ Nickname    : {info.get('nickname', 'N/A')[:45]:<45}║
║ User ID     : {info.get('id', 'N/A'):<45}║
║ Bio         : {info.get('bio', '')[:45]:<45}║
║ Verified    : {verified:<45}║
║ Private     : {private:<45}║
║ Followers   : {format_number(info.get('followers', 0)):<45}║
║ Following   : {format_number(info.get('following', 0)):<45}║
║ Likes       : {format_number(info.get('likes', 0)):<45}║
║ Videos      : {info.get('videos', 0):<45}║
╚══════════════════════════════════════════════════════════════╝
"""
