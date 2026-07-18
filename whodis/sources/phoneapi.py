"""Reverse phone lookup using multiple APIs."""

import requests
import json


def check_phone_api(number: str, timeout: int = 10) -> dict:
    """
    Check phone number using online reverse lookup APIs.
    
    Args:
        number: Phone number
        timeout: Timeout in seconds
        
    Returns:
        {
            'found': True/False,
            'data': {
                'owner_name': str,
                'last_activity': str,
                'linked_accounts': list,
                ...
            },
            'error': str or None
        }
    """
    try:
        # Format number
        number_clean = number.replace('+', '').replace(' ', '').replace('-', '')
        
        # Try multiple phone lookup APIs
        results = {
            'owner_name': None,
            'location': None,
            'carrier': None,
            'accounts': [],
            'social_profiles': [],
        }
        
        # Try NumVerify API (free tier)
        try:
            numverify_url = f"https://apilayer.net/api/validate"
            params = {'number': number_clean, 'countryCode': 'ID'}
            
            response = requests.get(numverify_url, params=params, timeout=timeout)
            if response.status_code == 200:
                data = response.json()
                if data.get('valid'):
                    results['location'] = data.get('location', 'Unknown')
                    results['carrier'] = data.get('carrier', 'Unknown')
        except:
            pass
        
        # Try OpenPhoneData
        try:
            api_url = f"https://phonedatatoolsapi.p.rapidapi.com/search"
            headers = {
                'X-RapidAPI-Key': 'YOUR_KEY_HERE',
                'X-RapidAPI-Host': 'phonedatatoolsapi.p.rapidapi.com'
            }
            params = {'phone': number_clean, 'country': 'ID'}
            
            response = requests.get(api_url, headers=headers, params=params, timeout=timeout)
            if response.status_code == 200:
                data = response.json()
                if data.get('found'):
                    results['owner_name'] = data.get('name')
                    results['social_profiles'] = data.get('profiles', [])
        except:
            pass
        
        # Check if found any data
        if results['owner_name'] or results['social_profiles']:
            return {
                'found': True,
                'data': results,
                'error': None
            }
        
        return {
            'found': False,
            'data': {},
            'error': 'No phone API matches'
        }
        
    except Exception as e:
        return {
            'found': False,
            'data': {},
            'error': f'Phone API error: {str(e)}'
        }


def check_truecaller_api(number: str, timeout: int = 10) -> dict:
    """
    Check Truecaller using unofficial API.
    
    Args:
        number: Phone number
        timeout: Timeout in seconds
        
    Returns:
        {
            'found': True/False,
            'data': {'name': str, 'spam_score': int, ...},
            'error': str or None
        }
    """
    try:
        # Format number
        number_clean = number.replace('+', '').replace(' ', '').replace('-', '')
        
        # Use Truecaller unofficial API
        url = "https://api4.truecaller.com/v1/search"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36',
            'Authorization': 'Bearer YOUR_TOKEN_HERE'
        }
        
        params = {
            'q': number_clean,
            'countryCode': 'ID',
            'type': '4',
            'limit': '1'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('data'):
                person = data['data'][0] if data['data'] else None
                if person:
                    return {
                        'found': True,
                        'data': {
                            'name': person.get('name', 'Unknown'),
                            'spam_score': person.get('spamScore', 0),
                            'phone_type': person.get('phoneType', 'Unknown'),
                            'carrier': person.get('carrier', 'Unknown'),
                            'location': person.get('location', 'Unknown'),
                        },
                        'error': None
                    }
        
        return {
            'found': False,
            'data': {},
            'error': 'Truecaller API no match'
        }
        
    except Exception as e:
        return {
            'found': False,
            'data': {},
            'error': f'Truecaller error: {str(e)}'
        }


def check_getcontact_api(number: str, timeout: int = 10) -> dict:
    """
    Check GetContact using API.
    
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
        # Format number
        number_clean = number.replace('+', '').replace(' ', '').replace('-', '')
        
        # GetContact API endpoint
        url = "https://getcontactapi.com/api/contacts/check"
        
        headers = {
            'User-Agent': 'GetContact/1.0',
            'Authorization': 'Bearer YOUR_TOKEN_HERE'
        }
        
        data = {
            'phone': number_clean,
            'country': 'ID'
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=timeout)
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('found'):
                contact = result.get('contact', {})
                tags = result.get('tags', [])
                
                return {
                    'found': True,
                    'data': {
                        'name': contact.get('name', 'Unknown'),
                        'tags': tags,
                        'reports': contact.get('reports', 0),
                    },
                    'error': None
                }
        
        return {
            'found': False,
            'data': {},
            'error': 'GetContact no match'
        }
        
    except Exception as e:
        return {
            'found': False,
            'data': {},
            'error': f'GetContact error: {str(e)}'
        }
