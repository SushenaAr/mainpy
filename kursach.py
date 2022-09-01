from time import sleep
import requests
from pprint import pprint


class photos_vk:
    list_sizes_url= []
    all_on_json_list__= []
    url= 'https://api.vk.com/method/'
    def __init__(self):
        self.params= {
            'access_token': 'd99dde60d99dde60d99dde6022da8da86fdd99dd99dde60ba9a43cff2ab7fc1ec8ac927', #токен здесь
            'v': '5.131'
        }

        return

    
    def get_photos_at_vk(self , id: str):
        photos_url= photos_vk.url + 'photos.get'
        params= {
            'album_id': 'profile',
            'extended': 1,
            'owner_id': id
        }
        response= requests.get(photos_url, params={**self.params, **params})
        #получение названий и размеров для json-чика и соединение
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
            dict_size_2['size']= [f'{h} * {w}', end_dict_size['url']]
            list_sizes.append(dict_size_2)

        
        for k in zip(list_likes, list_sizes):
            photos_vk.all_on_json_list__.append({**k[0], **k[1]})

        return photos_vk.all_on_json_list__ #ебануть размерчики сюда

    def size_url(self, id: str):  #Получаю список для загрузки ядиск(формат лайк:юрлик), я не смог заковать lists в global, написал второй раз
        photos_url= photos_vk.url + 'photos.get'
        params= {
            'album_id': 'profile',
            'extended': 1,
            'owner_id': id
        }
        response= requests.get(photos_url, params={**self.params, **params})
        #получение названий и размеров для json-чика и соединение
        r= response.json()
        lists =  r['response']['items']

        list_likes= []
        for dict_like_sizes in lists:
            likes = f"{dict_like_sizes['likes']['count']}.jpg"
            list_likes.append(likes)

        list_sizes= []
        for dict_size in lists:
            size_list= dict_size['sizes']
            end_dict_size= size_list[-1]
            list_sizes.append(end_dict_size['url'])

        _zipeed_size= list(zip(list_likes, list_sizes))
        

        return(_zipeed_size)
            

            
    


class Yadisk:
    url='https://cloud-api.yandex.net/v1/disk/resources'
    def __init__(self):
        self.headers= {
            "Content-type": "application/json",
            'Authorization': 'OAuth y0_AgAAAAAf2yxeAADLWwAAAADM9GjtVAOq_w5dQquZBqgOH-9l1xuv9nM' 
            }

    def create_folder(self, folder_name,vk_id ,range_= 5):
        headers_= {'Accept': 'application/json'}
        response= requests.put(Yadisk.url, headers= {**self.headers,**headers_}, params= f'path= {folder_name}')
        list_in_def= photo.size_url(vk_id)
        renged_list= list_in_def [:range_]
        for name,size in renged_list:   
            pprint(name)
            pprint(size)
            response_up= requests.post(Yadisk.url+ '/upload', headers={**self.headers, **headers_},params={'url':size, 'path': f'{folder_name}/{name}' } )
            return response_up.json()



   # def status(self):
   #     response= requests.get('https://cloud-api.yandex.net/v1/disk/', headers= self.headers)
    #    return response.json()


photo= photos_vk()
put_photos= Yadisk()
pprint(put_photos.create_folder('new_reposit',vk_id= 411548195))
#pprint(put_photos.status())
#pprint(photo.size_url())








#headers_= {'Accept': 'application/json'
 #           "Content-type": "application/json",
 #           'Authorization': 'OAuth y0_AgAAAAAf2yxeAADLWwAAAADM9GjtVAOq_w5dQquZBqgOH-9l1xuv9nM' 
  #          }





#yandex
 #       sizes_list= []
     #   for dict_size in lists:
      #      size_list= dict_size['sizes']
       #     end_dict_size= size_list[-1]
        #    sizes_list.append(end_dict_size['url'])