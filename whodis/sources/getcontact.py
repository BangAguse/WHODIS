"""GetContact source."""

from ..utils import Scraper


def check_getcontact(number: str, timeout: int = 10) -> dict:
    """
    Check GetContact for phone number information.
    
    Args:
        number: Phone number
        timeout: Timeout in seconds
        
    Returns:
        {
            'found': True/False,
            'data': {'name': str, 'tags': list, ...},
            'error': str or None
        }
    """
    try:
        # Format number for GetContact
        query = number.replace('+', '').replace(' ', '').replace('-', '')
        
        url = f"https://www.getcontact.com/en/number/{query}"
        
        response = Scraper.fetch(url, timeout=timeout, retries=2)
        
        if not response:
            return {
                'found': False,
                'data': {},
                'error': 'Failed to fetch GetContact'
            }
        
        soup = Scraper.parse_html(response.text)
        
        if not soup:
            return {
                'found': False,
                'data': {},
                'error': 'Failed to parse HTML'
            }
        
        # Try to extract name and tags
        name = None
        tags = []
        
        # Look for name in specific classes
        name_elem = soup.select_one('[data-testid="search-title"]')
        if name_elem:
            name = name_elem.get_text(strip=True)
        
        # Look for tags
        tag_elems = soup.select('[data-testid="tag"]')
        for tag_elem in tag_elems:
            tag_text = tag_elem.get_text(strip=True)
            if tag_text:
                tags.append(tag_text)
        
        if name or tags:
            return {
                'found': True,
                'data': {
                    'name': name or 'Not found',
                    'tags': tags if tags else [],
                    'source': 'GetContact'
                },
                'error': None
            }
        
        return {
            'found': False,
            'data': {},
            'error': 'No data found in GetContact'
        }
        
    except Exception as e:
        return {
            'found': False,
            'data': {},
            'error': f'GetContact error: {str(e)}'
        }
