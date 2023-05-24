import requests


async def get_card_info(query):
    url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?fname='
    c_url = url + query
    response = requests.get(c_url)
    if response.status_code == 200:
        info = response.json()
        a = 0
        d = 0
        l = 0
        attribute = ''
        try:
            a = info['data'][0]['atk']
            d = info['data'][0]['def']
            l = info['data'][0]['level']
            attribute = info['data'][0]['attribute']
        except Exception as e:
            pass
        
        data = {'name': info['data'][0]['name'],
                'type': info['data'][0]['type'],
                'effect':info['data'][0]['desc'],
                'image_url': info['data'][0]['card_images'][0]['image_url'],
                'race': info['data'][0]['race'],
                'attribute' : attribute,
                'stats': { 'atk' : a, 'def': d, 'level': l}}
        return data
    else:
        data = {'name': '',
                'type': '',
                'effect': '',
                'image_url': '',
                'race': '',
                'attribute' : '',
                'stats': { 'atk' : 0, 'def': 0, 'level': 0}}
        return data
        


    
    