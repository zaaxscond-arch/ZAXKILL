"""
TikTok Reporter Module - REAL Version
Handles account reporting using multiple methods
"""

import time
import random
import json
import requests
from datetime import datetime
from .bypass import AntiDetection
from .utils import extract_username

class TikTokReporter:
    def __init__(self, config, browser, proxy_manager):
        self.config = config
        self.browser = browser
        self.proxy_manager = proxy_manager
        self.bypass = AntiDetection()
        self.session = requests.Session()
        self.base_headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'Origin': 'https://www.tiktok.com',
            'Referer': 'https://www.tiktok.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Connection': 'keep-alive'
        }
        self.session.headers.update(self.base_headers)
        
    def get_user_info(self, username):
        """Get user info via API"""
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
                    'verified': user.get('verified', False),
                    'private': user.get('privateAccount', False),
                    'followers': stats.get('followerCount', 0),
                    'following': stats.get('followingCount', 0),
                    'likes': stats.get('heartCount', 0),
                    'videos': stats.get('videoCount', 0)
                }
            return None
        except Exception as e:
            return None
    
    def report_api(self, username, reason):
        """Report via API"""
        try:
            info = self.get_user_info(username)
            if not info:
                return False, "User not found"
            
            user_id = info.get('id')
            if not user_id:
                return False, "No user ID"
            
            endpoints = [
                'https://www.tiktok.com/api/v1/report/',
                'https://www.tiktok.com/api/v2/report/',
                'https://www.tiktok.com/api/report/'
            ]
            
            data = {
                'user_id': str(user_id),
                'reason': reason,
                'type': 'user',
                'report_type': 'account',
                'description': f"Account violates community guidelines: {reason}"
            }
            
            for endpoint in endpoints:
                try:
                    headers = self.bypass.generate_headers()
                    resp = self.session.post(endpoint, json=data, headers=headers, timeout=20)
                    
                    if resp.status_code in [200, 201, 202, 204]:
                        return True, "API success"
                except:
                    continue
            
            return False, "API failed"
            
        except Exception as e:
            return False, f"API error: {str(e)}"
    
    def report_selenium(self, username, reason):
        """Report via Selenium browser automation"""
        try:
            if not self.browser.driver:
                if not self.browser.start():
                    return False, "Browser failed"
            
            driver = self.browser.driver
            url = f"https://www.tiktok.com/@{username}"
            
            driver.get(url)
            time.sleep(random.uniform(3, 5))
            
            # Find report button
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            try:
                # Click more options (three dots)
                more_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@data-e2e='more-btn']"))
                )
                more_btn.click()
                time.sleep(1)
                
                # Click report option
                report_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Report') or contains(text(), 'Laporkan')]"))
                )
                report_btn.click()
                time.sleep(2)
                
                # Select reason
                reasons = driver.find_elements(By.XPATH, f"//div[contains(text(), '{reason}')]")
                if reasons:
                    reasons[0].click()
                    time.sleep(1)
                    
                    # Submit
                    submit_btn = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Submit') or contains(text(), 'Kirim')]"))
                    )
                    submit_btn.click()
                    time.sleep(2)
                    
                    return True, "Selenium success"
                else:
                    return False, "Reason not found"
                    
            except Exception as e:
                return False, f"Selenium error: {str(e)}"
                
        except Exception as e:
            return False, f"Browser error: {str(e)}"
    
    def report_account(self, username, reason):
        """Main report method - tries multiple approaches"""
        methods = []
        
        # Method 1: API
        if self.config.get('use_selenium', True):
            methods.append(('API', self.report_api))
        
        # Method 2: Selenium
        if self.config.get('use_selenium', True):
            methods.append(('Selenium', self.report_selenium))
        
        for method_name, method_func in methods:
            result, details = method_func(username, reason)
            if result:
                return True, method_name
            time.sleep(random.uniform(1, 3))
        
        return False, "All methods failed"
