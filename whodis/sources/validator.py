"""Phone number validator source."""

import phonenumbers
from phonenumbers import country_code_for_region, region_code_for_number


def check_validator(number: str, timeout: int = 10) -> dict:
    """
    Validate phone number and extract metadata.
    
    Args:
        number: Phone number in international format
        timeout: Timeout (not used for validator)
        
    Returns:
        {
            'found': True/False,
            'data': {
                'valid': bool,
                'country': str,
                'country_code': str,
                'region': str,
                'carrier': str,
                'type': str,
                'formatted': str
            },
            'error': str or None
        }
    """
    try:
        # Parse the number
        parsed = phonenumbers.parse(number, None)
        
        # Validate
        is_valid = phonenumbers.is_valid_number(parsed)
        
        if not is_valid:
            return {
                'found': False,
                'data': {
                    'valid': False,
                    'error': 'Nomor tidak valid'
                },
                'error': 'Invalid phone number'
            }
        
        # Get country info
        country_name = phonenumbers.region_code_for_number(parsed)
        country_code = parsed.country_code  # Use the parsed object's country_code property
        
        # Get number type
        number_type = phonenumbers.number_type(parsed)
        type_map = {
            0: "FIXED_LINE",
            1: "MOBILE",
            2: "FIXED_LINE_OR_MOBILE",
            3: "TOLL_FREE",
            4: "PREMIUM_RATE",
            5: "SHARED_COST",
            6: "VOIP",
            7: "PERSONAL_NUMBER",
            8: "PAGER",
            9: "UAN",
            10: "VOICEMAIL",
            11: "UNKNOWN",
        }
        type_str = type_map.get(number_type, "UNKNOWN")
        
        # Get carrier (dari library phonenumbers, limited support)
        carrier = get_carrier_name(country_name, parsed.national_number)
        
        # Format number
        formatted = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        
        return {
            'found': True,
            'data': {
                'valid': True,
                'country': get_country_name(country_name),
                'country_code': country_name,
                'region': country_name,
                'dial_code': f"+{country_code}",
                'carrier': carrier or 'Unknown',
                'type': type_str,
                'formatted': formatted,
                'national_number': str(parsed.national_number)
            },
            'error': None
        }
        
    except phonenumbers.NumberParseException as e:
        return {
            'found': False,
            'data': {},
            'error': f'Parse error: {str(e)}'
        }
    except Exception as e:
        return {
            'found': False,
            'data': {},
            'error': f'Validator error: {str(e)}'
        }


def get_country_name(country_code: str) -> str:
    """Get full country name from country code."""
    countries = {
        'ID': 'Indonesia',
        'MY': 'Malaysia',
        'SG': 'Singapore',
        'PH': 'Philippines',
        'TH': 'Thailand',
        'VN': 'Vietnam',
        'US': 'United States',
        'GB': 'United Kingdom',
        'AU': 'Australia',
        'IN': 'India',
        'JP': 'Japan',
        'CN': 'China',
        'BR': 'Brazil',
        'FR': 'France',
        'DE': 'Germany',
        'IT': 'Italy',
        'ES': 'Spain',
        'KR': 'South Korea',
        'RU': 'Russia',
        'MX': 'Mexico',
    }
    return countries.get(country_code, country_code)


def get_carrier_name(country_code: str, national_number: int) -> str:
    """Get carrier name based on country and number prefix."""
    carriers = {
        'ID': {
            '812': 'Telkomsel',
            '813': 'Telkomsel',
            '814': 'Telkomsel',
            '815': 'Telkomsel',
            '816': 'Telkomsel',
            '855': 'Telkomsel',
            '856': 'Telkomsel',
            '857': 'Telkomsel',
            '858': 'Telkomsel',
            '821': 'Indosat Ooredoo',
            '822': 'Indosat Ooredoo',
            '823': 'Indosat Ooredoo',
            '827': 'Indosat Ooredoo',
            '828': 'Indosat Ooredoo',
            '831': 'Axis',
            '832': 'Axis',
            '833': 'Axis',
            '838': 'Axis',
            '844': 'Axis',
            '845': 'Axis',
            '851': 'Axis',
            '852': 'Axis',
            '853': 'Axis',
            '859': 'Axis',
            '862': 'Smartfren',
            '863': 'Smartfren',
            '864': 'Smartfren',
            '865': 'Smartfren',
            '866': 'Smartfren',
            '867': 'Smartfren',
            '868': 'Smartfren',
            '869': 'Smartfren',
            '881': 'Smartfren',
            '882': 'Smartfren',
            '883': 'Smartfren',
            '884': 'Smartfren',
            '885': 'Smartfren',
            '886': 'Smartfren',
            '887': 'Smartfren',
            '888': 'Smartfren',
            '889': 'Smartfren',
            '841': 'XL Axiata',
            '842': 'XL Axiata',
            '843': 'XL Axiata',
            '849': 'XL Axiata',
            '871': 'XL Axiata',
            '872': 'XL Axiata',
            '873': 'XL Axiata',
            '874': 'XL Axiata',
            '875': 'XL Axiata',
            '876': 'XL Axiata',
            '877': 'XL Axiata',
            '878': 'XL Axiata',
            '879': 'XL Axiata',
            '811': 'Byru',
            '819': 'Byru',
            '898': 'Byru',
            '899': 'Byru',
        }
    }
    
    national_str = str(national_number)
    if country_code in carriers:
        for prefix, carrier in carriers[country_code].items():
            if national_str.startswith(prefix):
                return carrier
    
    return None
