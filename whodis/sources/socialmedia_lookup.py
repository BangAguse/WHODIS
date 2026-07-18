"""Social media lookup using practical OSINT methods."""

import re
import requests
from urllib.parse import quote, urlparse
from ..utils import Scraper


def search_by_phone_number(number: str, platform: str, timeout: int = 10) -> list:
    """
    Search for social media profiles by phone number using practical methods.
    
    Args:
        number: Phone number to search
        platform: Platform name (instagram, facebook, linkedin, twitter)
        timeout: Timeout in seconds
        
    Returns:
        List of found profiles with names and links
    """
    number_clean = number.replace('+', '').replace(' ', '').replace('-', '')
    profiles = []
    
    try:
        # Use multiple search strategies
        search_terms = [
            number_clean,
            f"+{number_clean}",
            f"62{number_clean[-9:]}" if number_clean.startswith('8') else number_clean,
        ]
        
        for search_term in search_terms:
            if platform == 'instagram':
                results = _search_instagram_direct(search_term, timeout)
            elif platform == 'facebook':
                results = _search_facebook_direct(search_term, timeout)
            elif platform == 'linkedin':
                results = _search_linkedin_direct(search_term, timeout)
            elif platform == 'twitter':
                results = _search_twitter_direct(search_term, timeout)
            else:
                results = []
            
            profiles.extend(results)
            
            # Stop if we found something good
            if profiles:
                break
        
        return list(set(profiles))  # Remove duplicates
        
    except Exception:
        return []


def _search_instagram_direct(query: str, timeout: int) -> list:
    """Search Instagram by direct username/phone lookup with actual profile extraction."""
    profiles = []
    try:
        # Method 1: Try direct profile lookup if query is a valid username
        if query.isalnum() or '_' in query:
            url = f"https://www.instagram.com/api/v1/users/search/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            params = {'q': query}
            
            response = requests.get(url, params=params, headers=headers, timeout=timeout)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    for user in data.get('users', [])[:5]:
                        username = user.get('username')
                        full_name = user.get('full_name')
                        
                        if username and username.lower() != 'none':
                            profiles.append({
                                'username': username,
                                'name': full_name or username,
                                'url': f'https://instagram.com/{username}',
                                'follower_count': user.get('follower_count', 0),
                                'is_verified': user.get('is_verified', False),
                                'type': 'Instagram',
                                'relevance_score': 95 if full_name and query.lower() in full_name.lower() else 70
                            })
                except:
                    pass
        
        # Method 2: Try public username page
        if query.replace('+', '').isalnum():
            url = f"https://www.instagram.com/{query}/"
            response = Scraper.fetch(url, timeout=timeout, retries=1)
            
            if response and response.status_code == 200:
                # Extract name from page title
                title_match = re.search(r'<title>([^<]+)</title>', response.text)
                if title_match:
                    title = title_match.group(1)
                    # Parse Instagram title format: "Name (@username) • Instagram"
                    if '(@' in title and ')' in title:
                        name = title.split(' (')[0].strip()
                        username = re.search(r'\(@([^)]+)\)', title)
                        if username:
                            username_text = username.group(1)
                            if name and name.lower() != 'instagram':
                                profiles.append({
                                    'username': username_text,
                                    'name': name,
                                    'url': f'https://instagram.com/{username_text}/',
                                    'type': 'Instagram',
                                    'relevance_score': 90
                                })
    
    except Exception:
        pass
    
    return profiles


def _search_facebook_direct(query: str, timeout: int) -> list:
    """Search Facebook with actual profile name extraction."""
    profiles = []
    try:
        # Method: Try Facebook graph search (public)
        url = "https://www.facebook.com/search/people/"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        params = {'q': query}
        
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        
        if response.status_code == 200:
            # Extract real profile names from response using multiple patterns
            # Look for actual person cards/results
            name_patterns = [
                r'<h2[^>]*>([^<]+?(?:' + re.escape(query) + r'[^<]*)?)</h2>',
                r'<div[^>]*class="[^"]*name[^"]*"[^>]*>([^<]+)</div>',
                r'<span[^>]*data-testid="[^"]*name[^"]*"[^>]*>([^<]+)</span>',
            ]
            
            found_names = []
            for pattern in name_patterns:
                matches = re.findall(pattern, response.text, re.IGNORECASE)
                found_names.extend(matches)
            
            # Filter and clean names
            for name in found_names[:5]:
                clean_name = name.strip()
                if clean_name and len(clean_name) > 2 and clean_name.lower() not in ['facebook', 'click here', 'view profile', 'add friend']:
                    # Check if name has actual content (not just links/buttons)
                    if not any(word in clean_name.lower() for word in ['javascript', 'onclick', 'href']):
                        profiles.append({
                            'name': clean_name,
                            'url': f'https://facebook.com/search/people/?q={quote(query)}',
                            'type': 'Facebook',
                            'relevance_score': 75 if query.lower() in clean_name.lower() else 50
                        })
    
    except Exception:
        pass
    
    return profiles


def _search_linkedin_direct(query: str, timeout: int) -> list:
    """Search LinkedIn with real profile extraction."""
    profiles = []
    try:
        # LinkedIn public profile search
        url = "https://www.linkedin.com/search/results/people/"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        params = {'keywords': query}
        
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        
        if response.status_code == 200:
            # Extract profile names from search results
            # LinkedIn search results have specific patterns
            name_patterns = [
                r'<h3[^>]*>([^<]+)</h3>',
                r'<h2[^>]*class="[^"]*search-results__result-title[^"]*"[^>]*>([^<]+)</h2>',
                r'<span[^>]*class="name"[^>]*>([^<]+)</span>',
            ]
            
            found_names = []
            for pattern in name_patterns:
                matches = re.findall(pattern, response.text)
                found_names.extend(matches)
            
            # Clean and deduplicate
            for name in found_names[:5]:
                clean_name = name.strip()
                if clean_name and len(clean_name) > 2:
                    if not any(word in clean_name.lower() for word in ['linkedin', 'button', 'click here']):
                        profiles.append({
                            'name': clean_name,
                            'url': f'https://linkedin.com/search/results/people/?keywords={quote(query)}',
                            'type': 'LinkedIn',
                            'relevance_score': 75 if query.lower() in clean_name.lower() else 50
                        })
    
    except Exception:
        pass
    
    return profiles


def _search_twitter_direct(query: str, timeout: int) -> list:
    """Search Twitter/X with real account extraction."""
    profiles = []
    try:
        # Twitter public search
        url = "https://twitter.com/search"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        params = {'q': query, 'f': 'user'}  # f=user filters for user results
        
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        
        if response.status_code == 200:
            # Extract Twitter handles from search results
            # Look for @username patterns
            handle_patterns = [
                r'@([a-zA-Z0-9_]{1,15})',
                r'href="https?://(?:twitter\.com|x\.com)/([a-zA-Z0-9_]{1,15})"',
            ]
            
            found_handles = []
            for pattern in handle_patterns:
                matches = re.findall(pattern, response.text)
                found_handles.extend(matches)
            
            # Deduplicate and filter
            for handle in list(set(found_handles))[:5]:
                if handle and len(handle) > 1 and handle.lower() not in ['home', 'search', 'explore', 'messages', 'notifications']:
                    profiles.append({
                        'username': handle,
                        'name': f'@{handle}',
                        'url': f'https://twitter.com/{handle}',
                        'type': 'Twitter',
                        'relevance_score': 80 if query.lower() in handle.lower() else 60
                    })
    
    except Exception:
        pass
    
    return profiles


def get_best_match(profiles: list, query: str) -> dict or None:
    """
    Get the best matching profile from list.
    
    Args:
        profiles: List of profiles
        query: Original query
        
    Returns:
        Best matching profile or None
    """
    if not profiles:
        return None
    
    # Return highest scored profile
    best = max(profiles, key=lambda x: x.get('relevance_score', 0))
    return best if best.get('relevance_score', 0) > 40 else None

