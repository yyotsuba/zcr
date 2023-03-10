import requests

def login():
    params = {'name': 'test1', 'password': '123456'}
    url = 'http://127.0.0.1:8001/login/' 
    res = requests.post(url, params=params)
    cookie = requests.utils.dict_from_cookiejar(res.cookies)
    return cookie

def reserve(cookie):
    params = {'start_time': '2023-03-09 10:03:00', \
              'end_time': '2023-03-09 10:20:10'}
    url = 'http://127.0.0.1:8001/conference/reserve/'
    res = requests.post(url, params=params, cookies=cookie)
    print(res, res.text)

def delete(cookie):
    params = {'conference_id': '719290'}
    url = 'http://127.0.0.1:8001/conference/reserve/'
    res = requests.delete(url, params=params, cookies=cookie)
    print(res, res.text)

if __name__ == "__main__":
    cookie = login()
    delete(cookie)

