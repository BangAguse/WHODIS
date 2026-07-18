"""Telegram source with Selenium support."""

import os
import json
from ..utils import Scraper

# Try to import Selenium for JavaScript rendering
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


def check_telegram(number: str, timeout: int = 10) -> dict:
    """
    Check if number is registered on Telegram using multiple methods.
    
    Args:
        number: Phone number
        timeout: Timeout in seconds
        
    Returns:
        {
            'found': True/False,
            'data': {'username': str, 'account_found': bool, ...},
            'error': str or None
        }
    """
    try:
        # Format number for Telegram
        tg_number = number.replace('+', '').replace(' ', '').replace('-', '')
        
        # Method 1: Try direct t.me/{number} link (check if exists)
        result = _check_direct_link(tg_number, timeout)
        if result['found']:
            return result
        
        # Method 2: Try Telegram Bot API (if API key available)
        result = _check_telegram_api(tg_number, timeout)
        if result['found']:
            return result
        
        # Method 3: Try web.telegram.org with Selenium (requires browser)
        if SELENIUM_AVAILABLE:
            result = _check_telegram_selenium(tg_number, timeout)
            if result['found']:
                return result
        
        # Method 4: Search public channels/users
        result = _search_telegram_public(tg_number, timeout)
        if result['found']:
            return result
        
        return {
            'found': False,
            'data': {},
            'error': 'Could not find Telegram account'
        }
        
    except Exception as e:
        return {
            'found': False,
            'data': {},
            'error': f'Telegram error: {str(e)}'
        }


def _check_direct_link(number: str, timeout: int) -> dict:
    """Check if direct t.me link exists."""
    try:
        # Try direct link
        url = f"https://t.me/{number}"
        
        response = Scraper.fetch(url, timeout=timeout, retries=1)
        
        if response and response.status_code == 200:
            # Check if page contains valid profile data
            if 'tgme_page' in response.text or 'Telegram' in response.text:
                return {
                    'found': True,
                    'data': {
                        'username': number,
                        'profile_url': url,
                        'account_found': True,
                        'type': 'direct_link'
                    },
                    'error': None
                }
        elif response and response.status_code == 404:
            # 404 means no account with this username
            pass
    
    except Exception:
        pass
    
    return {'found': False, 'data': {}, 'error': 'Direct link failed'}


def _check_telegram_api(number: str, timeout: int) -> dict:
    """Check using Telegram Bot API."""
    try:
        # This requires a bot token - would be from config
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        
        if not bot_token:
            return {'found': False, 'data': {}, 'error': 'No bot token'}
        
        import requests
        
        # Try to resolve username using Telegram API
        url = f"https://api.telegram.org/bot{bot_token}/getChat"
        
        # Try different formats
        for chat_identifier in [number, f"@{number}", f"+{number}"]:
            try:
                params = {'chat_id': chat_identifier}
                response = requests.get(url, params=params, timeout=timeout)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('ok'):
                        chat = data.get('result', {})
                        return {
                            'found': True,
                            'data': {
                                'username': chat.get('username', number),
                                'first_name': chat.get('first_name', ''),
                                'type': chat.get('type', 'unknown'),
                                'account_found': True,
                            },
                            'error': None
                        }
            except:
                continue
    
    except Exception:
        pass
    
    return {'found': False, 'data': {}, 'error': 'API check failed'}


def _check_telegram_selenium(number: str, timeout: int) -> dict:
    """Check using Selenium browser automation."""
    if not SELENIUM_AVAILABLE:
        return {'found': False, 'data': {}, 'error': 'Selenium not available'}
    
    driver = None
    try:
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        
        # Create driver
        driver = webdriver.Chrome(
            service=webdriver.ChromeService(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        # Set timeout
        driver.set_page_load_timeout(timeout)
        driver.implicitly_wait(5)
        
        # Try to access t.me profile
        url = f"https://t.me/{number}"
        driver.get(url)
        
        # Wait for page to load
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tgme_page"))
        )
        
        # Check if profile exists
        page_title = driver.title
        
        if 'Telegram' in page_title and number not in page_title.lower():
            return {
                'found': True,
                'data': {
                    'username': number,
                    'page_title': page_title,
                    'account_found': True,
                    'type': 'selenium',
                    'profile_url': url
                },
                'error': None
            }
    
    except Exception:
        pass
    
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
    
    return {'found': False, 'data': {}, 'error': 'Selenium check failed'}


def _search_telegram_public(number: str, timeout: int) -> dict:
    """Search public Telegram channels and users."""
    try:
        # Try telegram client API search
        # This would require MTProto client
        # For now, use simple HTTP check
        
        search_urls = [
            f"https://telegram.me/{number}",
            f"https://t.me/{number}",
            f"https://www.t.me/{number}",
        ]
        
        for url in search_urls:
            try:
                response = Scraper.fetch(url, timeout=timeout, retries=1)
                
                if response and response.status_code == 200:
                    return {
                        'found': True,
                        'data': {
                            'username': number,
                            'url': url,
                            'account_found': True,
                            'type': 'public_search'
                        },
                        'error': None
                    }
            except:
                continue
    
    except Exception:
        pass
    
    return {'found': False, 'data': {}, 'error': 'Public search failed'}
