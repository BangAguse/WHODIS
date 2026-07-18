"""Forum & web mentions source."""

from ..utils import Scraper


def check_forum(number: str, timeout: int = 10) -> dict:
    """
    Search for phone number mentions in forums and public places.
    
    Args:
        number: Phone number
        timeout: Timeout in seconds
        
    Returns:
        {
            'found': True/False,
            'data': {'mentions': list, 'forums': list, ...},
            'error': str or None
        }
    """
    try:
        # Format number for search
        query = number.replace('+', '').replace(' ', '').replace('-', '')
        
        # Search in various forums
        search_sites = [
            'reddit.com',
            'quora.com',
            'stackoverflow.com',
            'forum.',
            'boards.',
        ]
        
        mentions = []
        forums = []
        
        for site in search_sites:
            url = f"https://www.google.com/search"
            params = {
                'q': f'"{query}" site:{site}'
            }
            
            try:
                response = Scraper.fetch(url, timeout=timeout, retries=1, params=params)
                
                if response:
                    soup = Scraper.parse_html(response.text)
                    
                    if soup:
                        # Extract results
                        results = soup.select('div.VwiC3b')  # Google search snippets
                        
                        for result in results:
                            text = result.get_text(strip=True)
                            link = result.find('a')
                            
                            if text:
                                mentions.append(text[:80])
                                if link:
                                    url_found = link.get('href', '')
                                    if site in url_found:
                                        forums.append(site.split('.')[0].title())
            except:
                pass
        
        if mentions:
            return {
                'found': True,
                'data': {
                    'mentions': list(set(mentions)),
                    'forums': list(set(forums)),
                    'source': 'Forum Search'
                },
                'error': None
            }
        
        return {
            'found': False,
            'data': {},
            'error': 'No forum mentions found'
        }
        
    except Exception as e:
        return {
            'found': False,
            'data': {},
            'error': f'Forum search error: {str(e)}'
        }
