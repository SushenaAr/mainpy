from pprint import pprint
import requests


def intelegent(list_person):
    base_url="https://akabab.github.io/superhero-api/api/all.json"
    response= requests.get(base_url)
    dict_intellligence= {}
    a= response.json()
    for person_dict in a:
        if person_dict['name'] in list_person:
            dict_intellligence[person_dict['name']]= person_dict['powerstats']['intelligence']

    count= 0
    list_best= {}
    for best_value in dict_intellligence.values():
        if best_value > count:
            count= best_value
    
    for one_person, one_values in dict_intellligence.items():
        if count == one_values:
            list_best[one_person]= [one_values]
    


    print(list_best)
            
                

class YaUploader:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        pprint(response.json())
        return response.json()

    def upload_file_to_disk(self, disk_file_path, patch_to_pc):
        href = self._get_upload_link(disk_file_path=disk_file_path).get("href", "")
        response = requests.put(href, data=open(patch_to_pc, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")



def get_info_stack():
    title_and_link=[]
    #Здесь я предпочел не тратить время и не писать параметр тега питон, не тратить время на дату,
    #а создать в встроенном конструкторе
    response= requests.get('https://api.stackexchange.com/2.3/search?fromdate=1661126400&todate=1661299200&order=desc&sort=activity&tagged=python&site=stackoverflow')
    json_obj= response.json()
    for info in json_obj['items']:
        title_and_link.append({info['title']: info['link']}) 
    pprint(title_and_link)
    return


if __name__ == '__main__':
    ya= YaUploader('') #указать токен
    patch_= ""
    file_name= '1.txt'
 #   ya.upload_file_to_disk(f'new_file/{file_name}', f'{file_name}')
 #   get_info_stack()
