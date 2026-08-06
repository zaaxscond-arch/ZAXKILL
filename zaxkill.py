#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZAXKILL REAL - TikTok Auto Report Tool v4.0
Created by @zaax__ | FODXA System
REAL WORKING VERSION - Full Structure
"""

import os
import sys
import json
import time
import random
import threading
import queue
import logging
import subprocess
import platform
import shutil
from datetime import datetime
from colorama import init, Fore, Style
import requests

# Initialize
init(autoreset=True)

# Import modules
from modules.reporter import TikTokReporter
from modules.checker import AccountChecker
from modules.scraper import TikTokScraper
from modules.bypass import AntiDetection
from modules.proxy_manager import ProxyManager
from modules.thread_manager import ThreadManager
from modules.browser_manager import BrowserManager
from modules.utils import (
    clear_screen,
    load_banner,
    print_menu,
    validate_username,
    extract_username,
    format_time,
    color_text,
    save_report,
    load_reports,
    generate_id,
    create_dirs,
    check_dependencies
)

VERSION = "REAL 4.0"
AUTHOR = "@zaax__"
STATUS = "UNLOCKED"

class ZAXKILL_REAL:
    def __init__(self):
        self.start_time = datetime.now()
        self.config = self.load_config()
        self.create_directories()
        self.setup_logging()
        
        # Initialize modules
        self.proxy_manager = ProxyManager()
        self.bypass = AntiDetection()
        self.browser = BrowserManager(self.config)
        self.reporter = TikTokReporter(self.config, self.browser, self.proxy_manager)
        self.checker = AccountChecker(self.config)
        self.scraper = TikTokScraper(self.config)
        self.thread_manager = ThreadManager()
        
        self.total_reports = 0
        self.success_reports = 0
        self.failed_reports = 0
        self.running = False
        self.report_queue = queue.Queue()
        
        self.logger.info(f"ZAXKILL REAL v{VERSION} initialized")
        self.logger.info(f"Platform: {platform.system()}")
        
    def load_config(self):
        """Load configuration"""
        default = {
            "version": VERSION,
            "threads": 3,
            "delay_min": 5,
            "delay_max": 10,
            "timeout": 30,
            "max_retries": 3,
            "headless": False,
            "use_proxy": False,
            "use_selenium": True,
            "browser": "chrome",
            "max_reports_per_hour": 150,
            "report_reasons": ["Spam", "Bullying", "Harassment", "Nudity", "Hate Speech", "Scam", "Fake Account"],
            "auto_rotate_user_agent": True,
            "auto_clear_cookies": True,
            "save_cookies": True,
            "session_timeout": 300,
            "log_level": "INFO",
            "mode": "normal",
            "language": "id"
        }
        
        try:
            with open('config/settings.json', 'r') as f:
                config = json.load(f)
                default.update(config)
                return default
        except FileNotFoundError:
            os.makedirs('config', exist_ok=True)
            with open('config/settings.json', 'w') as f:
                json.dump(default, f, indent=4)
            return default
    
    def save_config(self):
        """Save configuration"""
        with open('config/settings.json', 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def create_directories(self):
        """Create all required directories"""
        dirs = ['assets', 'config', 'data', 'logs', 'modules']
        for d in dirs:
            os.makedirs(d, exist_ok=True)
        
        # Create default files
        if not os.path.exists('data/targets.txt'):
            with open('data/targets.txt', 'w') as f:
                f.write("# Add usernames here (one per line)\n")
                f.write("# Example:\n")
                f.write("# username1\n")
                f.write("# username2\n")
        
        if not os.path.exists('data/reports.json'):
            with open('data/reports.json', 'w') as f:
                json.dump([], f)
        
        if not os.path.exists('config/proxy.txt'):
            with open('config/proxy.txt', 'w') as f:
                f.write("# Proxy format: ip:port:username:password\n")
                f.write("# Example:\n")
                f.write("# 192.168.1.1:8080\n")
                f.write("# user:pass@192.168.1.1:8080\n")
    
    def setup_logging(self):
        """Setup logging system"""
        log_level = getattr(logging, self.config.get('log_level', 'INFO'))
        
        logging.basicConfig(
            level=log_level,
            format='[%(asctime)s] %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[
                logging.FileHandler('logs/report.log'),
                logging.FileHandler('logs/error.log'),
                logging.FileHandler('logs/debug.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('ZAXKILL')
    
    def show_banner(self):
        """Display banner"""
        clear_screen()
        banner = load_banner()
        if banner:
            print(Fore.RED + banner + Style.RESET_ALL)
        else:
            print(Fore.RED + "=" * 70)
            print(Fore.CYAN + "         ZAXKILL REAL - TikTok Auto Report Tool")
            print(Fore.GREEN + f"         Author: {AUTHOR} | FODXA System")
            print(Fore.RED + "=" * 70)
        
        print(Fore.YELLOW + "=" * 70)
        print(Fore.CYAN + f"         ZAXKILL REAL v{VERSION}")
        print(Fore.GREEN + f"         Author: {AUTHOR} | FODXA System")
        print(Fore.MAGENTA + f"         Status: {STATUS}")
        print(Fore.YELLOW + "=" * 70)
        print(Fore.CYAN + f"[+] Started: {format_time(self.start_time)}")
        print(Fore.CYAN + f"[+] Reports: {self.total_reports}")
        print(Fore.GREEN + f"[✓] Success: {self.success_reports}")
        print(Fore.RED + f"[✗] Failed: {self.failed_reports}")
        print(Fore.YELLOW + "=" * 70 + "\n")
    
    def menu(self):
        """Main menu"""
        while True:
            self.show_banner()
            print_menu()
            choice = input(Fore.CYAN + "\n[ZAXKILL] >> " + Style.RESET_ALL).strip()
            
            if choice == '1':
                self.single_report()
            elif choice == '2':
                self.mass_report()
            elif choice == '3':
                self.mass_report_file()
            elif choice == '4':
                self.check_account()
            elif choice == '5':
                self.scrape_accounts()
            elif choice == '6':
                self.settings_menu()
            elif choice == '7':
                self.view_stats()
            elif choice == '8':
                self.view_logs()
            elif choice == '9':
                self.clear_data()
            elif choice == '10':
                self.about()
            elif choice == '11':
                self.cleanup()
                sys.exit(0)
            else:
                print(Fore.RED + "[!] Invalid option!")
                time.sleep(1)
    
    def single_report(self):
        """Report single account"""
        clear_screen()
        print(Fore.GREEN + "[+] SINGLE REPORT MODE")
        print(Fore.YELLOW + "-" * 50)
        
        username = input(Fore.CYAN + "[?] Username (tanpa @): " + Style.RESET_ALL).strip().replace('@', '')
        if not username:
            print(Fore.RED + "[!] Username required!")
            input("\nPress Enter...")
            return
        
        print(Fore.CYAN + f"[+] Target: @{username}")
        
        # Check account
        print(Fore.CYAN + "[+] Checking account...")
        info = self.checker.get_info(username)
        if info:
            print(Fore.GREEN + f"    User ID: {info.get('id', 'N/A')}")
            print(Fore.GREEN + f"    Followers: {info.get('followers', 0):,}")
            print(Fore.GREEN + f"    Videos: {info.get('videos', 0)}")
        else:
            print(Fore.RED + "[!] Could not fetch info")
        
        # Select reason
        print(Fore.YELLOW + "\n[+] Report reasons:")
        reasons = self.config['report_reasons']
        for i, r in enumerate(reasons, 1):
            print(f"    {i}. {r}")
        
        choice = input(Fore.CYAN + "[?] Pilih reason (1-{}): ".format(len(reasons)) + Style.RESET_ALL).strip()
        try:
            reason = reasons[int(choice) - 1]
        except:
            reason = reasons[0]
        
        confirm = input(Fore.RED + f"\n[?] Report @{username} for '{reason}'? (y/n): " + Style.RESET_ALL).strip().lower()
        if confirm != 'y':
            print(Fore.YELLOW + "[+] Cancelled")
            input("\nPress Enter...")
            return
        
        # Execute
        print(Fore.CYAN + "\n[+] Sending report...")
        result, method = self.reporter.report_account(username, reason)
        
        self.total_reports += 1
        if result:
            self.success_reports += 1
            print(Fore.GREEN + f"[✓] Report sent! Method: {method}")
            save_report(username, reason, 'success', method)
            self.logger.info(f"SUCCESS: @{username} | {reason} | {method}")
        else:
            self.failed_reports += 1
            print(Fore.RED + "[✗] Failed to send report")
            save_report(username, reason, 'failed', 'none')
            self.logger.error(f"FAILED: @{username}")
        
        input("\nPress Enter to continue...")
    
    def mass_report(self):
        """Mass report from input"""
        clear_screen()
        print(Fore.GREEN + "[+] MASS REPORT MODE")
        print(Fore.YELLOW + "-" * 50)
        
        input_text = input(Fore.CYAN + "[?] Usernames (pisahkan koma): " + Style.RESET_ALL).strip()
        usernames = [u.strip().replace('@', '') for u in input_text.split(',') if u.strip()]
        
        if not usernames:
            print(Fore.RED + "[!] No usernames!")
            input("\nPress Enter...")
            return
        
        self._mass_report_process(usernames)
    
    def mass_report_file(self):
        """Mass report from file"""
        clear_screen()
        print(Fore.GREEN + "[+] MASS REPORT FROM FILE")
        print(Fore.YELLOW + "-" * 50)
        
        file_path = input(Fore.CYAN + "[?] File path (default: data/targets.txt): " + Style.RESET_ALL).strip()
        if not file_path:
            file_path = 'data/targets.txt'
        
        try:
            with open(file_path, 'r') as f:
                usernames = []
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        usernames.append(line.replace('@', '').split('/')[-1])
            
            if not usernames:
                print(Fore.RED + "[!] No usernames in file!")
                input("\nPress Enter...")
                return
            
            self._mass_report_process(usernames)
            
        except FileNotFoundError:
            print(Fore.RED + f"[!] File not found: {file_path}")
            input("\nPress Enter...")
        except Exception as e:
            print(Fore.RED + f"[!] Error: {str(e)}")
            input("\nPress Enter...")
    
    def _mass_report_process(self, usernames):
        """Process mass report"""
        print(Fore.CYAN + f"\n[+] Total targets: {len(usernames)}")
        print(Fore.CYAN + f"[+] Threads: {self.config['threads']}")
        print(Fore.CYAN + f"[+] Delay: {self.config['delay_min']}-{self.config['delay_max']}s")
        
        confirm = input(Fore.RED + "[?] Start mass report? (y/n): " + Style.RESET_ALL).strip().lower()
        if confirm != 'y':
            print(Fore.YELLOW + "[+] Cancelled")
            input("\nPress Enter...")
            return
        
        self.running = True
        self.report_queue = queue.Queue()
        for username in usernames:
            self.report_queue.put(username)
        
        # Start threads
        threads = []
        thread_count = min(self.config['threads'], len(usernames))
        
        for i in range(thread_count):
            t = threading.Thread(target=self._worker_thread)
            t.daemon = True
            t.start()
            threads.append(t)
        
        # Monitor progress
        while self.running:
            remaining = self.report_queue.qsize()
            total = len(usernames)
            completed = total - remaining
            progress = (completed / total) * 100 if total > 0 else 0
            
            print(Fore.CYAN + f"[+] Progress: {progress:.1f}% ({completed}/{total})")
            
            if self.report_queue.empty():
                break
            
            time.sleep(2)
        
        self.running = False
        
        print(Fore.GREEN + "\n[+] Mass report completed!")
        print(Fore.CYAN + f"[✓] Success: {self.success_reports}")
        print(Fore.RED + f"[✗] Failed: {self.failed_reports}")
        input("\nPress Enter to continue...")
    
    def _worker_thread(self):
        """Worker thread for mass report"""
        while self.running and not self.report_queue.empty():
            try:
                username = self.report_queue.get(timeout=2)
                reason = self.config['report_reasons'][0]
                
                result, method = self.reporter.report_account(username, reason)
                
                self.total_reports += 1
                if result:
                    self.success_reports += 1
                    self.logger.info(f"SUCCESS: @{username}")
                    save_report(username, reason, 'success', method)
                else:
                    self.failed_reports += 1
                    self.logger.warning(f"FAILED: @{username}")
                    save_report(username, reason, 'failed', 'none')
                
                delay = random.uniform(self.config['delay_min'], self.config['delay_max'])
                time.sleep(delay)
                
                self.report_queue.task_done()
                
            except queue.Empty:
                break
            except Exception as e:
                self.logger.error(f"Worker error: {str(e)}")
                try:
                    self.report_queue.task_done()
                except:
                    pass
    
    def check_account(self):
        """Check account info"""
        clear_screen()
        print(Fore.GREEN + "[+] CHECK ACCOUNT")
        print(Fore.YELLOW + "-" * 50)
        
        username = input(Fore.CYAN + "[?] Username: " + Style.RESET_ALL).strip().replace('@', '')
        
        info = self.checker.get_full_info(username)
        if info:
            print(Fore.GREEN + info)
        else:
            print(Fore.RED + "[!] Could not fetch info")
        
        input("\nPress Enter to continue...")
    
    def scrape_accounts(self):
        """Scrape accounts by keyword"""
        clear_screen()
        print(Fore.GREEN + "[+] SCRAPE ACCOUNTS")
        print(Fore.YELLOW + "-" * 50)
        
        keyword = input(Fore.CYAN + "[?] Keyword: " + Style.RESET_ALL).strip()
        count = input(Fore.CYAN + "[?] Count (default: 50): " + Style.RESET_ALL).strip()
        count = int(count) if count else 50
        
        print(Fore.CYAN + f"[+] Scraping {count} accounts for '{keyword}'...")
        
        results = self.scraper.search(keyword, count)
        
        if results:
            filename = f"data/scraped_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w') as f:
                for r in results:
                    f.write(r + '\n')
            
            print(Fore.GREEN + f"[✓] Scraped {len(results)} accounts")
            print(Fore.CYAN + f"[+] Saved to: {filename}")
            
            for r in results[:10]:
                print(Fore.CYAN + f"    @{r}")
            if len(results) > 10:
                print(Fore.YELLOW + f"    ... and {len(results) - 10} more")
        else:
            print(Fore.RED + "[!] No results")
        
        input("\nPress Enter to continue...")
    
    def settings_menu(self):
        """Settings menu"""
        clear_screen()
        print(Fore.GREEN + "[+] SETTINGS")
        print(Fore.YELLOW + "-" * 50)
        
        options = [
            ("Threads", "threads", int),
            ("Delay Min (s)", "delay_min", float),
            ("Delay Max (s)", "delay_max", float),
            ("Timeout (s)", "timeout", int),
            ("Max Retries", "max_retries", int),
            ("Headless", "headless", bool),
            ("Use Proxy", "use_proxy", bool),
            ("Use Selenium", "use_selenium", bool),
            ("Max Reports/Hour", "max_reports_per_hour", int),
            ("Auto Rotate UA", "auto_rotate_user_agent", bool)
        ]
        
        for i, (label, key, dtype) in enumerate(options, 1):
            value = self.config.get(key)
            print(f"{i:2}. {label}: {value}")
        
        print(f"\n{Fore.YELLOW}[a] Add proxy")
        print(f"[s] Save and Back")
        print(f"[q] Back without saving")
        
        choice = input(Fore.CYAN + "[?] Pilih: " + Style.RESET_ALL).strip()
        
        if choice.lower() == 'a':
            proxy = input(Fore.CYAN + "[?] Proxy (ip:port): " + Style.RESET_ALL).strip()
            if proxy:
                self.proxy_manager.add(proxy)
                print(Fore.GREEN + "[+] Proxy added")
        
        elif choice.lower() == 's':
            self.save_config()
            print(Fore.GREEN + "[+] Settings saved")
        
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                label, key, dtype = options[idx]
                if dtype == bool:
                    self.config[key] = not self.config[key]
                else:
                    new_val = input(Fore.CYAN + f"[?] New value for {label}: " + Style.RESET_ALL).strip()
                    if new_val:
                        if dtype == int:
                            self.config[key] = int(new_val)
                        elif dtype == float:
                            self.config[key] = float(new_val)
                        else:
                            self.config[key] = new_val
                print(Fore.GREEN + "[+] Updated")
        
        input("\nPress Enter to continue...")
    
    def view_stats(self):
        """View statistics"""
        clear_screen()
        print(Fore.GREEN + "[+] STATISTICS")
        print(Fore.YELLOW + "-" * 50)
        
        reports = load_reports()
        
        print(Fore.CYAN + f"Total Reports: {len(reports)}")
        
        success = len([r for r in reports if r.get('status') == 'success'])
        failed = len([r for r in reports if r.get('status') == 'failed'])
        
        print(Fore.GREEN + f"  ✓ Success: {success}")
        print(Fore.RED + f"  ✗ Failed: {failed}")
        
        # By reason
        if reports:
            reasons = {}
            for r in reports:
                reason = r.get('reason', 'Unknown')
                reasons[reason] = reasons.get(reason, 0) + 1
            
            print(Fore.YELLOW + "\n[+] By Reason:")
            for reason, count in sorted(reasons.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"    {reason}: {count}")
        
        input("\nPress Enter to continue...")
    
    def view_logs(self):
        """View logs"""
        clear_screen()
        print(Fore.GREEN + "[+] LOGS")
        print(Fore.YELLOW + "-" * 50)
        
        try:
            with open('logs/report.log', 'r') as f:
                lines = f.read().splitlines()
                show = lines[-30:] if len(lines) > 30 else lines
                for line in show:
                    print(line)
        except FileNotFoundError:
            print(Fore.YELLOW + "[!] No logs yet")
        
        input("\nPress Enter to continue...")
    
    def clear_data(self):
        """Clear all data"""
        clear_screen()
        print(Fore.RED + "[!] CLEAR ALL DATA")
        print(Fore.YELLOW + "-" * 50)
        
        confirm = input(Fore.RED + "[?] Hapus semua logs dan data? (y/n): " + Style.RESET_ALL).strip().lower()
        if confirm == 'y':
            for f in ['logs/report.log', 'logs/error.log', 'logs/debug.log', 'data/reports.json']:
                if os.path.exists(f):
                    open(f, 'w').close()
            print(Fore.GREEN + "[+] Data cleared")
        else:
            print(Fore.YELLOW + "[+] Cancelled")
        
        input("\nPress Enter to continue...")
    
    def about(self):
        """About info"""
        clear_screen()
        print(Fore.GREEN + "[+] ABOUT ZAXKILL REAL")
        print(Fore.YELLOW + "-" * 50)
        
        about_text = f"""
╔═══════════════════════════════════════════════════════════╗
║                    ZAXKILL REAL                         ║
╠═══════════════════════════════════════════════════════════╣
║ Version        : {VERSION:<45}║
║ Author         : {AUTHOR:<45}║
║ System         : FODXA by @zaax__                       ║
║ Status         : {STATUS:<45}║
║ Platform       : {platform.system():<45}║
║ Python         : {platform.python_version():<45}║
║ Features       : Auto Report, Mass Report, Scraper     ║
║                : Proxy Support, Browser Automation     ║
║ Methods        : API, Selenium, Cloudflare Bypass     ║
╚═══════════════════════════════════════════════════════════╝
"""
        print(about_text)
        input("\nPress Enter to continue...")
    
    def cleanup(self):
        """Cleanup resources"""
        self.logger.info("Cleaning up...")
        if hasattr(self, 'browser'):
            self.browser.cleanup()
        print(Fore.GREEN + "[+] Cleanup done. Goodbye!")

if __name__ == "__main__":
    try:
        create_dirs()
        app = ZAXKILL_REAL()
        app.menu()
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Interrupted")
        sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"[!] Error: {str(e)}")
        sys.exit(1)
