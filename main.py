import requests
from pprint import pprint
import json
from progress.bar import IncrementalBar
import configparser



def get_id(screen_name, key):
        url_id= 'https://api.vk.com/method/utils.resolveScreenName'
        params= {
            'screen_name': screen_name,
            'access_token': key, #токен сервисный
            'v': '5.131'
            }
        response= requests.get(url_id, params=params)
        r_j= response.json()
        name_user= r_j['response']['object_id']
        return name_user


def get_photos_at_vk(id: str, key): #получение названий и размеров для json
        photos_url='https://api.vk.com/method/photos.get'
        params= {
            'album_id': 'profile',
            'extended': 1,
            'owner_id': id,
            'access_token': key, #токен сервисный
            'v': '5.131'
        }
        response= requests.get(photos_url, params=params)
        r= response.json()
        lists =  r['response']['items']

        list_likes= []
        for dict_like_sizes in lists:
            dict_like= {}
            likes = dict_like_sizes['likes']['count']
            dict_like['file_name']= f'{likes}.jpg'
            list_likes.append(dict_like)

        list_sizes= []
        for dict_size in lists:
            dict_size_2= {}
            size_list= dict_size['sizes']
            end_dict_size= size_list[-1]
            h= end_dict_size['height']
            w= end_dict_size['width']
            dict_size_2['size']= f'{h} * {w}'
            list_sizes.append(dict_size_2)

        all_on_json_list__= []
        for k in zip(list_likes, list_sizes):
            all_on_json_list__.append({**k[0], **k[1]})
        return all_on_json_list__ 


def size_url(id: str, key):
        photos_url= 'https://api.vk.com/method/photos.get'
        params= {
            'album_id': 'profile',
            'extended': 1,
            'owner_id': id,
            'access_token': key, #токен сервисный
            'v': '5.131'
        }
        response= requests.get(photos_url, params=params)
        r= response.json()
        lists =  r['response']['items']

        list_likes= []
        for dict_like_sizes in lists:
            likes = f"{dict_like_sizes['likes']['count']}"
            format_= '.jpg'
            unics= dict_like_sizes.get('date', '')
            if likes+format_ in list_likes:
                likes_2= likes+'_'.join(unics) +format_ 
                list_likes.append(likes_2)

            else:
                list_likes.append(likes+format_)

        list_sizes_url= []
        for dict_size in lists:
            size_list= dict_size['sizes']
            end_dict_size= size_list[-1]
            list_sizes_url.append(end_dict_size['url'])

        _ziped_size= list(zip(list_likes, list_sizes_url))
        return(_ziped_size)



def create_json_file(vk_id ,range_, key):
    with open('1.json', 'w', encoding='utf-8') as f:
        list_for_json= get_photos_at_vk(vk_id, key=key)
        r_list_for_json= list_for_json[:int(range_)]
        json.dump(r_list_for_json, f)

def create_folder(folder_name,vk_id ,range_, ya_token, key):
    url= 'https://cloud-api.yandex.net/v1/disk/resources'
    headers= {
        "Content-type": "application/json",
        'Authorization': ya_token,
        'Accept': 'application/json'
        }
    response= requests.put(url, headers=headers, params= f'path={folder_name}')
    list_in_def= size_url(vk_id, key=key)
    renged_list= list_in_def [:int(range_)]

    for name,size in renged_list:
        response_up= requests.post(
        url,
         headers=headers,
         params={'url':{size}, 'path':f'{folder_name}/{name}' } )
    return

def get_photos():
    bar = IncrementalBar('Countdown', max = 2)
    
    token_ya= input('Введите токен яндекс полигона: ')
    vk_id_input= input('Введите id пользователя вк: ')
    vk_name_input= input('Введите короткое имя пользователя вк: ')
    range_ph= input('Введите колличество загружаемых фотографий:')
    folder= input('Введите желаемое название папки на диске: ')

    config = configparser.ConfigParser()
    config.read('file.ini')
    key= config['settings']['key']
    if range_ph== '':
        range_ph= 5
                                      
    if vk_name_input and vk_id_input or vk_id_input != '':
        create_folder(folder,vk_id=vk_id_input, range_=range_ph, ya_token=token_ya, key=key)
        bar.next()
        pprint('Данные успешно отправлены в облако')
        create_json_file(vk_id=vk_id_input, range_=range_ph, key=key)
        bar.next()
        pprint('Запись в json прошла успешно')
        bar.finish()
    elif vk_name_input != '':
        id_vk= int(get_id(vk_name_input, key=key))
        create_folder(folder,vk_id=id_vk, range_=range_ph, ya_token=token_ya, key=key)
        bar.next()
        pprint('Данные успешно отправлены в облако')
        create_json_file(vk_id=id_vk, range_=range_ph, key= key)
        bar.next()
        pprint('Запись в json прошла успешно')
        bar.finish()
    else:
        pprint('вы не ввели пользователя вк')


if __name__== '__main__':
    get_photos()
