import requests

async def get_random_quote():
    response = requests.get('https://animechan.vercel.app/api/random')
    if response.status_code == 200:
        return response.json()
    else:
        return { 'anime':'none', 'character': 'none', 'quote': 'none'}

async def get_horoscope(sign):
    if sign == 'help':
        return 0  
    response = requests.get(f'https://ohmanda.com/api/horoscope/{sign}')   
    if response.status_code != 200:
        return 1        
    
    return response.json()
