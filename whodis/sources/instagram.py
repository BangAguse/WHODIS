"""Instagram source with improved lookup."""

from .socialmedia_lookup import search_by_phone_number, get_best_match


def check_instagram(number: str, timeout: int = 10) -> dict:
    """
    Search for Instagram profiles associated with phone number (REAL method).
    
    Args:
        number: Phone number
        timeout: Timeout in seconds
        
    Returns:
        {
            'found': True/False,
            'data': {'usernames': list, 'profiles': list, ...},
            'error': str or None
        }
    """
    try:
        # Search Instagram by phone number
        profiles = search_by_phone_number(number, 'instagram', timeout)
        
        if profiles:
            # Extract usernames from found profiles
            usernames = [p.get('username', p.get('name', '')) for p in profiles if p.get('username') or p.get('name')]
            
            return {
                'found': True,
                'data': {
                    'usernames': usernames,
                    'profiles': profiles,
                    'count': len(profiles),
                    'source': 'Instagram'
                },
                'error': None
            }
        
        return {
            'found': False,
            'data': {},
            'error': 'No Instagram profiles found'
        }
        
    except Exception as e:
        return {
            'found': False,
            'data': {},
            'error': f'Instagram error: {str(e)}'
        }
