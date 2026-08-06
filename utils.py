"""
Utility Functions Module
Common helper functions for the application
"""

import os
import sys
import json
import re
import random
import string
import subprocess
import platform
from datetime import datetime
from colorama import Fore, Style

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_banner():
    """Load ASCII banner from file"""
    try:
        with open('assets/banner.txt', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None

def print_menu():
    """Print main menu"""
    menu = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                    ZAXKILL REAL MENU                        ║
╠══════════════════════════════════════════════════════════════╣
║  {Fore.GREEN}[1]  {Fore.WHITE}Single Report                                   ║
║  {Fore.GREEN}[2]  {Fore.WHITE}Mass Report (Manual Input)                      ║
║  {Fore.GREEN}[3]  {Fore.WHITE}Mass Report (From File)                        ║
║  {Fore.GREEN}[4]  {Fore.WHITE}Check Account Info                             ║
║  {Fore.GREEN}[5]  {Fore.WHITE}Scrape Accounts                                ║
║  {Fore.GREEN}[6]  {Fore.WHITE}Settings                                       ║
║  {Fore.GREEN}[7]  {Fore.WHITE}View Statistics                                ║
║  {Fore.GREEN}[8]  {Fore.WHITE}View Logs                                      ║
║  {Fore.GREEN}[9]  {Fore.WHITE}Clear Data                                     ║
║  {Fore.GREEN}[10] {Fore.WHITE}About                                          ║
║  {Fore.GREEN}[11] {Fore.WHITE}Exit                                           ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    print(menu)

def validate_username(username: str) -> bool:
    """Validate TikTok username"""
    if not username:
        return False
    # Remove @ if present
    username = username.replace('@', '').strip()
    # TikTok username rules: alphanumeric, underscore, dot
    pattern = r'^[a-zA-Z0-9_.]{2,24}$'
    return bool(re.match(pattern, username))

def extract_username(input_str: str) -> str:
    """Extract username from various input formats"""
    # Remove @
    username = input_str.replace('@', '')
    
    # If it's a URL
    if 'tiktok.com' in username:
        parts = username.split('/')
        for part in parts:
            if part and not part.startswith('http') and not part.startswith('www'):
                username = part
                break
    
    # Remove trailing slashes
    username = username.rstrip('/')
    
    # Remove query parameters
    if '?' in username:
        username = username.split('?')[0]
    
    return username.strip()

def format_time(dt: datetime) -> str:
    """Format datetime"""
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def format_number(num: int) -> str:
    """Format large numbers"""
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    return str(num)

def color_text(text: str, color: str) -> str:
    """Colorize text"""
    colors = {
        'red': Fore.RED,
        'green': Fore.GREEN,
        'yellow': Fore.YELLOW,
        'blue': Fore.BLUE,
        'magenta': Fore.MAGENTA,
        'cyan': Fore.CYAN,
        'white': Fore.WHITE
    }
    return colors.get(color, Fore.WHITE) + text + Style.RESET_ALL

def save_report(username: str, reason: str, status: str, method: str):
    """Save report to JSON"""
    os.makedirs('data', exist_ok=True)
    try:
        with open('data/reports.json', 'r') as f:
            reports = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        reports = []
    
    reports.append({
        'id': generate_id(),
        'username': username,
        'reason': reason,
        'status': status,
        'method': method,
        'timestamp': datetime.now().isoformat()
    })
    
    with open('data/reports.json', 'w') as f:
        json.dump(reports, f, indent=4)

def load_reports():
    """Load reports from JSON"""
    try:
        with open('data/reports.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def generate_id():
    """Generate random ID"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def create_dirs():
    """Create required directories"""
    dirs = ['assets', 'config', 'data', 'logs']
    for d in dirs:
        os.makedirs(d, exist_ok=True)

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import requests
        import selenium
        import undetected_chromedriver
        import colorama
        import fake_useragent
        import cloudscraper
        return True
    except ImportError as e:
        print(Fore.RED + f"[!] Missing dependency: {e}")
        print(Fore.YELLOW + "[+] Run: pip install -r requirements.txt")
        return False

def get_file_size(filepath: str) -> str:
    """Get file size in human readable format"""
    try:
        size = os.path.getsize(filepath)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    except:
        return "0 B"
