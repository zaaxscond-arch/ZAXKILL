"""
Proxy Manager Module
Handles proxy loading, rotation, and validation
"""

import os
import random
import time
import requests

class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.current_index = 0
        self.load_proxies()
    
    def load_proxies(self):
        """Load proxies from file"""
        try:
            with open('config/proxy.txt', 'r') as f:
                self.proxies = []
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        self.proxies.append(line)
        except FileNotFoundError:
            self.proxies = []
    
    def save_proxies(self):
        """Save proxies to file"""
        os.makedirs('config', exist_ok=True)
        with open('config/proxy.txt', 'w') as f:
            for proxy in self.proxies:
                f.write(proxy + '\n')
    
    def add(self, proxy):
        """Add proxy to list"""
        if proxy and proxy not in self.proxies:
            self.proxies.append(proxy)
            self.save_proxies()
            return True
        return False
    
    def remove(self, proxy):
        """Remove proxy from list"""
        if proxy in self.proxies:
            self.proxies.remove(proxy)
            self.save_proxies()
            return True
        return False
    
    def get_random(self):
        """Get random proxy"""
        if self.proxies:
            return random.choice(self.proxies)
        return None
    
    def get_next(self):
        """Get next proxy in rotation"""
        if not self.proxies:
            return None
        
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        return proxy
    
    def validate(self, proxy):
        """Validate proxy"""
        try:
            test_url = "http://httpbin.org/ip"
            proxies = {'http': proxy, 'https': proxy}
            resp = requests.get(test_url, proxies=proxies, timeout=10)
            return resp.status_code == 200
        except:
            return False
    
    def count(self):
        return len(self.proxies)
    
    def has_proxies(self):
        return len(self.proxies) > 0
    
    def get_all(self):
        return self.proxies.copy()
