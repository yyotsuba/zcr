import requests

def login():
    params = {'name': 'test1', 'password': '123456', 'email': 'test1'}
    url = 'http://127.0.0.1:8001/login/'
    res = requests.post(url, params=params)
    print(res, res.text)

if __name__ == "__main__":
    login()
