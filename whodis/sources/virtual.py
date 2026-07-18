"""Virtual number detection source."""

import json
from pathlib import Path


# Virtual number prefixes database
VIRTUAL_PREFIXES = {
    # Google Voice (US)
    '+1': ['650', '659'],  # Google Voice area codes
    # TextNow (US)
    '+1': ['209', '503', '510', '586', '650', '702', '720', '775', '801', '828', '856', '903', '916', '949', '951', '972'],
    # Burner numbers
    # Format: '+country_code': ['prefix1', 'prefix2', ...]
    '+1': ['272', '362', '482', '612', '817', '838', '841', '843', '870'],
}

def check_virtual(number: str, timeout: int = 10) -> dict:
    """
    Detect if number is a virtual/VoIP number.
    
    Args:
        number: Phone number
        timeout: Timeout in seconds
        
    Returns:
        {
            'found': True/False,
            'data': {'is_virtual': bool, 'type': str, ...},
            'error': str or None
        }
    """
    try:
        # Parse number
        if not number.startswith('+'):
            return {
                'found': False,
                'data': {},
                'error': 'Number must be in international format'
            }
        
        # Extract country code and national number
        # Remove + sign
        number_only = number[1:]
        
        # Check against virtual prefixes
        is_virtual = False
        virtual_type = None
        
        for country_code, prefixes in VIRTUAL_PREFIXES.items():
            if number_only.startswith(country_code[1:]):
                # Check if any prefix matches
                national_part = number_only[len(country_code) - 1:]
                for prefix in prefixes:
                    if national_part.startswith(prefix):
                        is_virtual = True
                        virtual_type = 'VoIP/Virtual'
                        break
        
        # Check common VoIP indicators
        voip_keywords = ['google voice', 'textfree', 'twilio', 'nexmo', 'burner']
        
        if is_virtual:
            return {
                'found': True,
                'data': {
                    'is_virtual': True,
                    'type': virtual_type or 'VoIP',
                    'warning': 'This is a virtual/VoIP number',
                    'source': 'Virtual Detection'
                },
                'error': None
            }
        
        return {
            'found': False,
            'data': {
                'is_virtual': False,
                'likely': 'Real phone number'
            },
            'error': None
        }
        
    except Exception as e:
        return {
            'found': False,
            'data': {},
            'error': f'Virtual detection error: {str(e)}'
        }
