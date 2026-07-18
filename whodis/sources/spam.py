"""Spam database source."""

from ..utils import Scraper


def check_spam(number: str, timeout: int = 10) -> dict:
    """
    Check if number is reported as spam.
    
    Args:
        number: Phone number
        timeout: Timeout in seconds
        
    Returns:
        {
            'found': True/False,
            'data': {'spam_reports': int, 'category': str, ...},
            'error': str or None
        }
    """
    try:
        # Format number for search
        query = number.replace('+', '').replace(' ', '').replace('-', '')
        
        # Search in spam databases
        urls_to_check = [
            f"https://www.truecaller.com/search?q={query}",
            f"https://www.getcontact.com/en/number/{query}",
        ]
        
        spam_reports = 0
        categories = []
        
        for url in urls_to_check:
            try:
                response = Scraper.fetch(url, timeout=timeout, retries=1)
                
                if response:
                    soup = Scraper.parse_html(response.text)
                    
                    if soup:
                        # Look for spam indicators
                        spam_text = soup.get_text()
                        
                        if 'spam' in spam_text.lower():
                            spam_reports += 1
                            categories.append('Spam')
                        if 'fraud' in spam_text.lower():
                            spam_reports += 1
                            categories.append('Fraud')
                        if 'scam' in spam_text.lower():
                            spam_reports += 1
                            categories.append('Scam')
            except:
                pass
        
        if spam_reports > 0:
            return {
                'found': True,
                'data': {
                    'spam_reports': spam_reports,
                    'categories': list(set(categories)),
                    'warning': 'Number reported as spam/fraud',
                    'source': 'Spam Database'
                },
                'error': None
            }
        
        return {
            'found': False,
            'data': {
                'spam_reports': 0,
                'status': 'Not reported as spam'
            },
            'error': None
        }
        
    except Exception as e:
        return {
            'found': False,
            'data': {},
            'error': f'Spam check error: {str(e)}'
        }
