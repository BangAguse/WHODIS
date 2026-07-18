"""Facebook source with improved lookup."""

from .socialmedia_lookup import search_by_phone_number


def check_facebook(number: str, timeout: int = 10) -> dict:
    """
    Search for Facebook profiles associated with phone number (REAL method).
    
    Args:
        number: Phone number
        timeout: Timeout in seconds
        
    Returns:
        {
            'found': True/False,
            'data': {'profiles': list, ...},
            'error': str or None
        }
    """
    try:
        # Search Facebook by phone number using proper API
        profiles = search_by_phone_number(number, 'facebook', timeout)
        
        if profiles:
            # Extract profile names
            profile_names = [p.get('name', '') for p in profiles if p.get('name')]
            
            return {
                'found': True,
                'data': {
                    'profiles': profile_names,
                    'profile_list': profiles,
                    'count': len(profiles),
                    'source': 'Facebook'
                },
                'error': None
            }
        
        return {
            'found': False,
            'data': {},
            'error': 'No Facebook profiles found'
        }
        
    except Exception as e:
        return {
            'found': False,
            'data': {},
            'error': f'Facebook error: {str(e)}'
        }
