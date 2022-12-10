import os
import json
import signal
import autoit
from steampy.guard import generate_one_time_code

class SteamAccount():
    def __init__(self, login, password, shared_secret):
        self.login = login
        self.password = password
        self.shared_secret = shared_secret
        self.win_steam_title = f'[{self.login}] # Steam'
        self.win_csgo_title = f'[{self.login}] # Counter-Strike: Global Offensive - Direct3D 9'
        self.win_csgo_PID = 0
        self.win_csgo_pos = ()
        self.status = 'Off'
        self.posX = 0
        self.posY = 0
    def GuardGen(self):
        return generate_one_time_code(self.shared_secret)
    def SteamLaunch(self):
        autoit.run(f'C:\Program Files (x86)\Steam\steam.exe '
                   f'-noreactlogin '
                   f'-login {self.login} {self.password}')
        autoit.win_wait_active('Steam Guard — Необходима авторизация компьютера')
        autoit.win_activate('Steam Guard — Необходима авторизация компьютера')
        autoit.send(self.GuardGen())
        autoit.send('{Enter}')
        autoit.win_wait_close('Steam Guard — Необходима авторизация компьютера')
        autoit.win_wait('Специальные предложения')
        autoit.win_activate('Специальные предложения')
        autoit.win_close('Специальные предложения')
        try:
            autoit.win_wait('Список друзей', 8)
            autoit.win_activate('Список друзей')
            autoit.win_close('Список друзей')
        except:
            pass
        autoit.win_wait('Steam')
        autoit.win_set_title('Steam', self.win_steam_title)
    def CSGOLaunch(self):
        self.status = 'Starting'
        autoit.run(f'C:\Program Files (x86)\Steam\steam.exe '
                   f'-noreactlogin '
                   f'-login {self.login} {self.password} '
                   f'-applaunch 730 '
                   f'-low '
                   f'-nohltv '
                   f'-no-browser '
                   f'-novid '
                   f'-nosound '
                   f'-window -w 400 -h 300')
        autoit.win_wait('Steam Guard — Необходима авторизация компьютера')
        autoit.win_activate('Steam Guard — Необходима авторизация компьютера')
        autoit.win_wait_active('Steam Guard — Необходима авторизация компьютера', 5)
        autoit.send(self.GuardGen())
        autoit.send('{Enter}')
        autoit.win_wait_close('Steam Guard — Необходима авторизация компьютера')
        autoit.win_wait('Counter-Strike: Global Offensive - Direct3D 9')
        autoit.win_activate('Counter-Strike: Global Offensive - Direct3D 9')
        autoit.win_wait_active('Counter-Strike: Global Offensive - Direct3D 9')

        while autoit.win_exists(self.win_csgo_title) == 0:
            autoit.win_activate('Counter-Strike: Global Offensive - Direct3D 9')
            autoit.win_wait_active('Counter-Strike: Global Offensive - Direct3D 9')
            autoit.win_set_title('Counter-Strike: Global Offensive - Direct3D 9', self.win_csgo_title)
        self.MoveWindow(0, 0)
        self.win_csgo_PID = autoit.win_get_process(self.win_csgo_title)
        self.win_csgo_pos = autoit.win_get_pos(self.win_csgo_title)
        self.status = 'Launched'
        self.UpdateAccountsJSON()
    def MoveWindow(self, posX, posY):
        autoit.win_move(self.win_csgo_title, posX, posY)
        self.posX = posX
        self.posY = posY
        self.UpdateAccountsJSON()
    def UpdateAccountsJSON(self):
        info = readJson('launched_accounts.json')
        if self.status == 'Off':
            info.pop(self.login)
        else:
            info[self.login] = {
                'login': self.login,
                'password': self.password,
                'shared_secret': self.shared_secret,
                'win_csgo_title': self.win_csgo_title,
                'win_csgo_PID': self.win_csgo_PID,
                'status': self.status,
                'posX': self.posX,
                'posY': self.posY
            }
        file = open('launched_accounts.json', 'w', encoding='utf-8')
        file.write(json.dumps(info, indent=4))
        file.close()
    def CloseAccount(self):
        os.kill(self.win_csgo_PID, signal.SIGTERM)
        self.win_csgo_PID = 0
        self.status = 'Off'
        self.UpdateAccountsJSON()
    def GetInfoTest(self):
        print(f'{self.login}\n{self.password}\n{self.shared_secret}\n{self.win_csgo_PID}\n{self.win_csgo_pos}\n{self.status}')

def GetSharedSecret(login):
    dir_name = "./maFiles"
    for item in os.listdir(dir_name):
        try:
            info = readJson(f'{dir_name}/{item}')
            if info['account_name'].lower() == login.lower():
                return info['shared_secret']
        except:
            return None

def ParceLogPass():
    accounts = {}
    file = open('logpass.txt')
    ##! pos menyat
    for account in file:
        if account != '\n':
            account_pair = account.split(':')
            accounts[account_pair[0]] = {'login': account_pair[0].lower(),
                                         'password': account_pair[1].replace('\n', '')}
    file.close()
    return accounts

def CreateAccounts():
    accounts = ParceLogPass()
    for login in accounts:
        accounts[login]['shared_secret'] = GetSharedSecret(login)

    file = open('accounts.json', 'w', encoding='utf-8')
    file.write(json.dumps(accounts, indent=4))
    file.close()

def readJson(path):
    file = open(path, encoding='utf-8')
    info = json.loads(file.read())
    file.close()
    return info

def OnStart():
    info = readJson('launched_accounts.json')
    for account in info.copy():
        if autoit.win_exists(info[account]["win_csgo_title"]) == 1:
            continue
        else:
            info.pop(account)
    file = open('launched_accounts.json', 'w', encoding='utf-8')
    file.write(json.dumps(info, indent=4))
    file.close()