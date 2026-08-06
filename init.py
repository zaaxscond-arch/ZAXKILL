"""
ZAXKILL REAL - Modules Package
TikTok Auto Report Tool - FODXA System
"""

from .reporter import TikTokReporter
from .checker import AccountChecker
from .scraper import TikTokScraper
from .bypass import AntiDetection
from .proxy_manager import ProxyManager
from .thread_manager import ThreadManager
from .browser_manager import BrowserManager
from .utils import *

__all__ = [
    'TikTokReporter',
    'AccountChecker',
    'TikTokScraper',
    'AntiDetection',
    'ProxyManager',
    'ThreadManager',
    'BrowserManager'
]

__version__ = '4.0.0'
__author__ = '@zaax__'
