"""Twitter/X source with improved lookup."""

from .socialmedia_lookup import search_by_phone_number


def check_twitter(number: str, timeout: int = 10) -> dict:
    """
    Search for Twitter/X accounts associated with phone number (REAL method).
    
    Args:
        number: Phone number
        timeout: Timeout in seconds
        
    Returns:
        {
            'found': True/False,
            'data': {'accounts': list, ...},
            'error': str or None
        }
    """
    try:
        # Search Twitter by phone number using proper API
        profiles = search_by_phone_number(number, 'twitter', timeout)
        
        if profiles:
            # Extract usernames from found profiles
            usernames = [p.get('username', p.get('name', '')) for p in profiles if p.get('username') or p.get('name')]
            
            return {
                'found': True,
                'data': {
                    'accounts': usernames,
                    'profiles': profiles,
                    'count': len(profiles),
                    'source': 'Twitter/X'
                },
                'error': None
            }
        
        return {
            'found': False,
            'data': {},
            'error': 'No Twitter accounts found'
        }
        
    except Exception as e:
        return {
            'found': False,
            'data': {},
            'error': f'Twitter error: {str(e)}'
        }
