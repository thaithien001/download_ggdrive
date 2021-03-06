import requests

from tqdm import tqdm

def download_file_from_google_drive(id, destination):
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None
    def save_response_content(response, destination):
        CHUNK_SIZE = 32768
        with open(destination,'wb') as f:
            with tqdm(unit='B', unit_scale = True, unit_divisor=1024) as bar:
                for chunk in requests.iter_content(CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
                        bar.update(CHUNK_SIZE)
    URL = "https://docs.google.com/us?=export=download"
    
    session = requests.Session()
    
    response = session.get(URL, param ={'id' : id}, stream = True)
    token = get_confirm_token(response)
    if token:
        params = {'id' : id, 'confirm' : token}
        response = session.get(URL, params = params, stream = True)
    
    save_response_content(response, destination)

    
if __name__ == "__main__":
    import sys
    if len(sys.argv) is not 3:
        print('Usage: python google_drive.py drive_file_id destination_file_path')
    else:
        file_id = sys.argv()
        
        destination = sys.argv(2)
        download_file_from_google_drive(file_id, destination)