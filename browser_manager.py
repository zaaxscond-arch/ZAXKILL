"""
Browser Manager Module
Handles Chrome automation with anti-detection
"""

import os
import time
import random
import subprocess
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
import undetected_chromedriver as uc
from .bypass import AntiDetection

class BrowserManager:
    def __init__(self, config):
        self.config = config
        self.bypass = AntiDetection()
        self.driver = None
        self.is_ready = False
        
    def start(self, proxy=None):
        """Start browser with anti-detection"""
        try:
            options = uc.ChromeOptions()
            
            # Anti-detection arguments
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-software-rasterizer')
            options.add_argument('--window-size=1366,768')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-plugins-discovery')
            options.add_argument('--disable-default-apps')
            options.add_argument('--disable-background-networking')
            options.add_argument('--disable-sync')
            options.add_argument('--disable-translate')
            options.add_argument('--disable-session-crashed-bubble')
            options.add_argument('--disable-infobars')
            options.add_argument('--disable-notifications')
            options.add_argument('--disable-popup-blocking')
            options.add_argument('--disable-prompt-on-repost')
            options.add_argument('--disable-hang-monitor')
            options.add_argument('--disable-client-side-phishing-detection')
            options.add_argument('--disable-component-update')
            options.add_argument('--disable-features=IsolateOrigins,site-per-process')
            options.add_argument('--disable-site-isolation-trials')
            
            # User agent
            options.add_argument(f'--user-agent={self.bypass.random_user_agent()}')
            
            # Headless
            if self.config.get('headless', False):
                options.add_argument('--headless=new')
            
            # Proxy
            if proxy and self.config.get('use_proxy', False):
                options.add_argument(f'--proxy-server={proxy}')
            
            # Create driver
            self.driver = uc.Chrome(options=options, version_main=None)
            
            # Remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Set user agent via CDP
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                'userAgent': self.bypass.random_user_agent()
            })
            
            self.is_ready = True
            return True
            
        except Exception as e:
            print(f"[!] Browser start error: {e}")
            return False
    
    def stop(self):
        """Stop browser"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
        self.driver = None
        self.is_ready = False
    
    def restart(self, proxy=None):
        """Restart browser"""
        self.stop()
        time.sleep(2)
        return self.start(proxy)
    
    def cleanup(self):
        """Cleanup browser resources"""
        self.stop()
        try:
            # Kill any leftover processes
            if platform.system() == 'Windows':
                subprocess.run(['taskkill', '/F', '/IM', 'chrome.exe'], capture_output=True)
            else:
                subprocess.run(['pkill', '-f', 'chrome'], capture_output=True)
        except:
            pass
    
    def get_cookies(self):
        """Get cookies from browser"""
        if not self.driver:
            return []
        try:
            return self.driver.get_cookies()
        except:
            return []
    
    def set_cookies(self, cookies):
        """Set cookies in browser"""
        if not self.driver:
            return False
        try:
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            return True
        except:
            return False
