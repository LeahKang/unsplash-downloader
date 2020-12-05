import urllib.request
import requests
import json
import pandas as pd
import time

api_key = '' # your api key
KEYWORD = ['artwork', 'painting'] 
per_page = 30 # maximum 30

def save_img(metadata):
    for i in range(len(metadata)):
        urllib.request.urlretrieve(metadata.iloc[i]['image'], f"./image/{i}_{metadata.index[i]}.jpg")

def get_metadata():
    df = pd.DataFrame(columns=['color', 'description', 'alt_description', 'image', 'link', 'categories', 'tags'])

    for keyword in KEYWORD:
        print(f'{keyword} Downloading..')
        page = 1
        while True:
            host = 'https://api.unsplash.com/search/photos?'
            parameters = f'client_id={api_key}&query={keyword}&page={page}&per_page={per_page}'

            req = requests.get(host+parameters)
            result = json.loads(req.text)
            
            if page == 1:
                print('total page :', result['total_pages'])
                print('total :', result['total'])
                
            print(page, end = ' ')
            
            for i in range(len(result['results'])):
                i_tmp = []
                i_tmp.append(result['results'][i]['color'])
                i_tmp.append(result['results'][i]['description'])
                i_tmp.append(result['results'][i]['alt_description'])
                i_tmp.append(result['results'][i]['urls']['raw'])
                i_tmp.append(result['results'][i]['links']['html'])
                i_tmp.append(result['results'][i]['categories'])
                i_tmp.append(result['results'][i]['tags'])

                df.loc[result['results'][i]['id']] = i_tmp

            if result['total_pages'] < page:
                print(f'\n {keyword} End..')
                break

            page += 1
            time.sleep(1.5*60)  # a limit of 50 requests per hour

    df.to_csv('./metadata.csv')
    return df

def main():
    metadata = get_metadata()

    save_img(metadata)


if __name__ == '__main__':
    main()