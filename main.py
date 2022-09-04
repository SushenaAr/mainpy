import requests
from pprint import pprint
import json
from progress.bar import IncrementalBar

mylist = [1,2]

bar = IncrementalBar('Countdown', max = len(mylist))


class photos_vk:
    url= 'https://api.vk.com/method/'
    def __init__(self):
        self.params= {
            'access_token': 'd99dde60d99dde60d99dde6022da8da86fdd99dd99dde60ba9a43cff2ab7fc1ec8ac927', #токен сервисный
            'v': '5.131'
        }
        return


    def get_photos_at_vk(self , id: str): #получение названий и размеров для json
        photos_url= photos_vk.url + 'photos.get'
        params= {
            'album_id': 'profile',
            'extended': 1,
            'owner_id': id
        }
        response= requests.get(photos_url, params={**self.params, **params})
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


    def size_url(self, id: str):  #Получаю список для загрузки на диск(формат лайк:юрл)
                                  #я не смог перевести lists в global, написал второй раз получение response,
                                  #впринципе я мог в первой функции сделать return [all_on_json_list_, _ziped_size ],
                                  #а не писать две функции, но уже лень переделывать и читаемость лучше
        photos_url= photos_vk.url + 'photos.get'
        params= {
            'album_id': 'profile',
            'extended': 1,
            'owner_id': id
        }
        response= requests.get(photos_url, params={**self.params, **params})
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



class Yadisk:
    url='https://cloud-api.yandex.net/v1/disk/resources'
    def __init__(self, ya_token):
        self.headers= {
            "Content-type": "application/json",
            'Authorization': ya_token,
            'Accept': 'application/json'
            }


    def create_folder(self, folder_name,vk_id ,range_= 5):
        response= requests.put(Yadisk.url, headers=self.headers, params= f'path={folder_name}')
        list_in_def= photo.size_url(vk_id)
        renged_list= list_in_def [:range_]

        with open('1.json', 'w', encoding='utf-8') as f:
            list_for_json= photo.get_photos_at_vk(vk_id)
            r_list_for_json= list_for_json[:range_]
            json.dump(r_list_for_json, f)
        bar.next()
        pprint('Запись в json прошла успешно')

        for name,size in renged_list:
            response_up= requests.post(Yadisk.url+ '/upload',
             headers=self.headers,
             params={'url':{size}, 'path':f'{folder_name}/{name}' } )
        bar.next()
        pprint('Данные успешно отправлены в облако')
        bar.finish() 
        return


if __name__ == '__main__':
    token_ya= input('Введите токен яндекс полигона: ')
    vk_id_input= input('Введите id пользователя вк: ')
    photo= photos_vk()
    put_photos= Yadisk(ya_token=token_ya)
    put_photos.create_folder('new_reposit',vk_id=vk_id_input)