import os
import requests


class YaUploader:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {'Content-Type': 'application/json',
                'Authorization': f'OAuth {self.token}'
                }

    def create_folder(self, folder_name):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        params = {'path': folder_name}
        requests.put(url, headers=headers, params=params)

    def get_upload_link(self, path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()['href']

    def upload_files_to_disk(self, path_to_file):
        self.create_folder(path_to_file)
        for file in os.listdir():
            if not file.endswith('.py'):
                href = self.get_upload_link(f'/{path_to_file}/{file}')
                response = requests.put(href, data=open(file, 'rb'))
                response.raise_for_status()
                if response.status_code == 201:
                    print('Download completed')


if __name__ == '__main__':
    TOKEN = ''
    uploader = YaUploader(TOKEN)
    uploader.upload_files_to_disk(os.path.basename(os.getcwd()))

