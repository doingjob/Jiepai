import requests
from urllib.parse import urlencode
import json
import os
from hashlib import md5

def get_page(offset):
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1',
        'from': 'search_tab',
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(params)
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.json()
    except requests.ConnectionError:
        return None

def get_image(json):
    data=json.get('data')
    if data:
        for item in data:
            image_list=item.get('image_list')
            title=item.get('title')
            if image_list:
                for image in image_list:
                    yield{
                         'image':image.get('url'), 
                         'title':title
                     }

def save_image(item):
    if not os.path.exists(item.get('title')):
            os.mkdir(item.get('title'))
    try:
        local_image_url=item.get('image')
        new_image_url=local_image_url.replace('list','large')
        response=requests.get('https:'+new_image_url)
        if response.status_code==200:
            file_path='{0}/{1}.{2}'.format(item.get('title'),md5(response.content).hexdigest(),'jpg')
            if not os.path.exists(file_path):
                with open(file_path,'wb')as f:
                    f.write(response.content)
            else:
                print("Already Downloaded",file_path)
    except requests.ConnectionError:
        print("Failed to save image")


def main(offset):
    json=get_page(offset)
    for item in get_image(json):
        print(item)
        save_image(item)


if __name__=='__main__':
    for i in range(0,2):
        main(i*20)
