"""Truecaller source with improved API."""

import requests
import json
from ..utils import Scraper


def check_truecaller(number: str, timeout: int = 10) -> dict:
    """
    Check Truecaller for phone number information using improved methods.
    
    Args:
        number: Phone number
        timeout: Timeout in seconds
        
    Returns:
        {
            'found': True/False,
            'data': {'name': str, 'spam_score': int, ...},
            'error': str or None
        }
    """
    try:
        # Format number
        number_clean = number.replace('+', '').replace(' ', '').replace('-', '')
        
        # Method 1: Try Truecaller unofficial API (most reliable)
        result = _truecaller_api_lookup(number_clean, timeout)
        if result['found']:
            return result
        
        # Method 2: Try Truecaller web scrape with proper parsing
        result = _truecaller_web_lookup(number, timeout)
        if result['found']:
            return result
        
        # Method 3: Try phone number reverse lookup database
        result = _reverse_phone_lookup(number_clean, timeout)
        if result['found']:
            return result
        
        return {
            'found': False,
            'data': {},
            'error': 'No data found in Truecaller sources'
        }
        
    except Exception as e:
        return {
            'found': False,
            'data': {},
            'error': f'Truecaller error: {str(e)}'
        }


def _truecaller_api_lookup(number: str, timeout: int) -> dict:
    """Try Truecaller API lookup."""
    try:
        # Use Truecaller unofficial API endpoint
        url = "https://www.truecaller.com/api/v1/search"
        
        params = {
            'q': number,
            'countryCode': 'ID'
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Android 13) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Authorization': 'Bearer UNOFFICIAL_TOKEN'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('data') and len(data['data']) > 0:
                person = data['data'][0]
                
                return {
                    'found': True,
                    'data': {
                        'name': person.get('name', 'Unknown'),
                        'phone_type': person.get('type', 'Unknown'),
                        'spam_score': person.get('spamScore', 0),
                        'spam_reports': person.get('spamCount', 0),
                        'location': person.get('location', 'Unknown'),
                    },
                    'error': None
                }
    
    except Exception:
        pass
    
    return {'found': False, 'data': {}, 'error': 'API call failed'}


def _truecaller_web_lookup(number: str, timeout: int) -> dict:
    """Try web scraping Truecaller."""
    try:
        # Format for URL
        query = number.replace('+', '').replace(' ', '').replace('-', '')
        
        url = f"https://www.truecaller.com/search?q={query}"
        
        response = Scraper.fetch(url, timeout=timeout, retries=2)
        
        if response:
            soup = Scraper.parse_html(response.text)
            
            if soup:
                # Look for name and spam info in page content
                # Extract from script tags (data often in JSON)
                scripts = soup.find_all('script')
                
                for script in scripts:
                    if script.string and 'name' in script.string.lower():
                        try:
                            # Try to parse JSON
                            data_str = script.string
                            # Look for JSON pattern
                            import re
                            json_match = re.search(r'\{[^{}]*"name"[^{}]*\}', data_str)
                            if json_match:
                                data = json.loads(json_match.group())
                                
                                return {
                                    'found': True,
                                    'data': {
                                        'name': data.get('name', 'Unknown'),
                                        'spam_score': data.get('spamScore', 0),
                                        'location': data.get('location', 'Unknown'),
                                    },
                                    'error': None
                                }
                        except:
                            pass
    
    except Exception:
        pass
    
    return {'found': False, 'data': {}, 'error': 'Web scrape failed'}


def _reverse_phone_lookup(number: str, timeout: int) -> dict:
    """Try reverse phone lookup from external database."""
    try:
        # Try free reverse lookup APIs
        urls_to_try = [
            f"https://phonedatabase.api/reverse?phone={number}",
            f"https://api.opendata.io/phonelookup?phone={number}",
        ]
        
        for url in urls_to_try:
            try:
                response = requests.get(url, timeout=timeout)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get('found'):
                        return {
                            'found': True,
                            'data': {
                                'name': data.get('name', 'Unknown'),
                                'location': data.get('location', 'Unknown'),
                                'carrier': data.get('carrier', 'Unknown'),
                            },
                            'error': None
                        }
            except:
                continue
    
    except Exception:
        pass
    
    return {'found': False, 'data': {}, 'error': 'Lookup failed'}

