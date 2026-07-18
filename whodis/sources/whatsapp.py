"""WhatsApp source."""

import requests


def check_whatsapp(number: str, timeout: int = 10) -> dict:
    """
    Check if number is registered on WhatsApp.
    
    Args:
        number: Phone number
        timeout: Timeout in seconds
        
    Returns:
        {
            'found': True/False,
            'data': {'active': bool, ...},
            'error': str or None
        }
    """
    try:
        # Format number for WhatsApp
        wa_number = number.replace('+', '').replace(' ', '').replace('-', '')
        
        # Method 1: Check wa.me redirect
        wa_url = f"https://wa.me/{wa_number}"
        
        try:
            response = requests.head(
                wa_url,
                timeout=timeout,
                allow_redirects=False,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            
            # If it redirects to a chat page, number is registered
            if response.status_code in [301, 302, 303, 307, 308]:
                if 'chat' in response.headers.get('Location', ''):
                    return {
                        'found': True,
                        'data': {
                            'active': True,
                            'whatsapp': 'Registered',
                            'source': 'WhatsApp'
                        },
                        'error': None
                    }
            elif response.status_code == 200:
                # Direct access to chat page
                return {
                    'found': True,
                    'data': {
                        'active': True,
                        'whatsapp': 'Registered',
                        'source': 'WhatsApp'
                    },
                    'error': None
                }
        except requests.Timeout:
            pass
        except requests.RequestException:
            pass
        
        # If no positive result
        return {
            'found': False,
            'data': {},
            'error': 'WhatsApp check inconclusive'
        }
        
    except Exception as e:
        return {
            'found': False,
            'data': {},
            'error': f'WhatsApp error: {str(e)}'
        }
