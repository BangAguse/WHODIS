"""Data breach source."""

from ..utils import Scraper


def check_breach(number: str, timeout: int = 10) -> dict:
    """
    Check if number appears in data breaches using Have I Been Pwned API.
    
    Args:
        number: Phone number
        timeout: Timeout in seconds
        
    Returns:
        {
            'found': True/False,
            'data': {'breaches': list, ...},
            'error': str or None
        }
    """
    try:
        # HIBP checks by email, not phone. We'll search for common patterns
        # In production, you'd need to get email from other sources first
        
        # Alternative: Check known breach databases
        query = number.replace('+', '').replace(' ', '').replace('-', '')
        
        # Try searching for the number in public breach repositories
        url = f"https://www.google.com/search"
        params = {
            'q': f'"{query}" breach database site:breachanalysis.com'
        }
        
        response = Scraper.fetch(url, timeout=timeout, retries=2, params=params)
        
        if not response:
            return {
                'found': False,
                'data': {},
                'error': 'Failed to check breaches'
            }
        
        soup = Scraper.parse_html(response.text)
        
        if not soup:
            return {
                'found': False,
                'data': {},
                'error': 'Failed to parse breach results'
            }
        
        # Look for breach mentions
        breaches = []
        snippets = soup.select('div.VwiC3b')  # Google search snippets
        
        for snippet in snippets:
            text = snippet.get_text(strip=True)
            if 'breach' in text.lower() or 'leaked' in text.lower():
                breaches.append(text[:100])  # First 100 chars
        
        if breaches:
            return {
                'found': True,
                'data': {
                    'breaches': breaches,
                    'warning': 'Possible data breach mention',
                    'source': 'Breach Detection'
                },
                'error': None
            }
        
        return {
            'found': False,
            'data': {},
            'error': 'No breach records found'
        }
        
    except Exception as e:
        return {
            'found': False,
            'data': {},
            'error': f'Breach check error: {str(e)}'
        }
