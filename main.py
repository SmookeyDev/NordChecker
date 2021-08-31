from modules.defs import Main
from tkinter import filedialog, Tk
from os import system, name
import time

defs = Main()

class App:
    def __init__(self):
        self.logo = """
███╗░░██╗░█████╗░██████╗░██████╗░░█████╗░██╗░░██╗███████╗░█████╗░██╗░░██╗███████╗██████╗░
████╗░██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗██║░░██║██╔════╝██╔══██╗██║░██╔╝██╔════╝██╔══██╗
██╔██╗██║██║░░██║██████╔╝██║░░██║██║░░╚═╝███████║█████╗░░██║░░╚═╝█████═╝░█████╗░░██████╔╝
██║╚████║██║░░██║██╔══██╗██║░░██║██║░░██╗██╔══██║██╔══╝░░██║░░██╗██╔═██╗░██╔══╝░░██╔══██╗
██║░╚███║╚█████╔╝██║░░██║██████╔╝╚█████╔╝██║░░██║███████╗╚█████╔╝██║░╚██╗███████╗██║░░██║
╚═╝░░╚══╝░╚════╝░╚═╝░░╚═╝╚═════╝░░╚════╝░╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝                                                                                       
        by SmookeyDev
        """
        
        self.data = defs.getData()
        
        self.main()
        
        
    def main(self):
        if name == 'nt':system('cls')
        else: system('clear')
        print(self.logo)
        time.sleep(2)
        defs.save_live()
        defs.save_dead()
        defs.use_proxy()
        if self.data['use_proxy'] == True:
            proxy_list = filedialog.askopenfilename()
            proxy_read = defs.read(proxy_list)
            proxy_array = []
            for i in proxy_read:
                proxy_array.append(i)
            self.data['proxy_list'] = proxy_array
        print("=>> Choose combo list text file. (email:pass) ")
        combo_list = filedialog.askopenfilename()
        combo_read = defs.read(combo_list)
        
        for i in combo_read:
            splitted = i.split(':', 1)
            resp = defs.checker(splitted[0], splitted[1])
            data = resp['data']
            self.data['checked'] += 1
            if resp.get('process') == True:
                if self.data['use_proxy'] == False:
                    print(f"\033[92mApproved =>> Email: {data['email']} | Password: {data['password']} | Expires At: {data['expires_at']}\033[00m")
                else:
                    print(f"\033[92mApproved =>> Email: {data['email']} | Password: {data['password']} | Expires At: {data['expires_at']} ({resp['message']})\033[00m")
                self.data['live'] += 1
                if self.data['save_live'] == True:
                    with open('./live.txt', 'a') as file:
                        file.write(f"{data['email']}:{data['password']}\n")
            else:
                print(f"\033[91mRepproved =>> Email: {data['email']} | Password: {data['password']} ({resp['message']})\033[00m")
                self.data['dead'] += 1
                if self.data['save_dead'] == True:
                    with open('./dead.txt', 'a') as file:
                        file.write(f"{data['email']}:{data['password']}\n")
                        
        print(f"=>> End. Checked: {self.data['checked']} | Live: {self.data['live']} | Dead: {self.data['dead']}")
        
        
        
        
if __name__ == "__main__":
    App()