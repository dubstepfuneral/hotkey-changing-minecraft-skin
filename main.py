import webbrowser
import keyboard
import requests
from time import time

skins = dict( # skins dictionary/json
{"maid":{"name": "cat boy uwu maid", "url": "https://i.ibb.co/4S4Y9cb/584701d246e30f14-1.png"},
"jamesj":{"name": "jamesj", "url": "https://i.ibb.co/VCZDQxH/a5ff7ac2861f6767.png"},
"squid":{"name": "squid gamist", "url": "https://i.ibb.co/7Rf3nmn/98066a5520e6cbe2.png"},
"christmastony":{"name": "christmas normal", "url": "https://i.ibb.co/xYzkDSf/2f4004e619a99526-1.png"},
"tony":{"name": "normal tony", "url": "https://i.ibb.co/sbRwxd0/2ab1dd68eba7361a.png"},
"tonymask":{"name": "tony skin with mask", "url": "https://i.ibb.co/YcC9gVM/4c8103a59e1e016e-1.png"},
"dream": {"name": "dream", "url" : "https://i.ibb.co/bNShLCZ/a357245a667cb6e4.png"},
"technoblade": {"name" : "technoblade", "url" : "https://i.ibb.co/DMJHKZv/37529af66bcdd70d.png"},
"prxc": {"name" : "prxc", "url" : "https://i.ibb.co/w6ph4n7/24cf5cdd2c821600.png"},
"amongusmaid": {"name" : "amongus maid", "url" : "https://i.ibb.co/6r9scfm/57593de6ff72fce9.png"},
"amongusdrip": {"name" : "amongus drip", "url" : "https://i.ibb.co/GQrjyqB/0466f8154de6dc26.png"},
"amongussquid": {"name" : "amongus squid", "url" : "https://i.ibb.co/5xQGhYW/75675258b6855ed7.png"},
"dreamamongus": {"name" : "dream amongus", "url" : "https://i.ibb.co/DMWZWGz/ccbe8515e88afb86.png"},
"ada": {"name" : "ada", "url" : "https://i.ibb.co/gSGybkH/1a6cf95d457db1d5.png"}})

#setting the which key which skin
num9 = "maid"
num6 = "jamesj"
num3 = "squid"
num0 = "christmastony"
#setting the which key which skin

def changeSkin(key):
    if(ready != True):
        return "cum not success"
    if(time() - time1 > 86400):
        print("TOKEN RAN OUT")
        exit()
    skinName = skins.get(key).get("name")
    skinURL = skins.get(key).get("url")
    global JWTToken
    skinResponse = requests.post(url="https://api.minecraftservices.com/minecraft/profile/skins", headers={"Authorization": "Bearer " + JWTToken, 
    "Content-Type" : "application/json"}, json={
    "variant": "classic",
    "url": skinURL
    })
    if skinResponse.status_code == 200:
        print('Skin change to "' + skinName + '" is successful.')
    else:
        print(skinResponse.text)

with open("SECRET.txt") as file:
    lines = file.readlines()
    id = lines[0][:-1]
    secret = lines[1]

que = input("ARE YOU LOGGED INTO THE RIGHT ACCOUNT? ANSWER QUICKLY (YES/NO): ")
if que.lower() != "yes":
    print("fuck off then")

# getting the jwl token [start]
ready = False
redirect = "https://google.com/"
url = "https://login.live.com/oauth20_authorize.srf?client_id=" + id + "&response_type=code&redirect_uri=" + redirect + "&scope=XboxLive.signin%20offline_access"
webbrowser.open(url, 1, autoraise=True)
print(url)
token = input("Enter token pls: ")
response = requests.post(url="https://login.live.com/oauth20_token.srf", headers={"Content-Type" : "application/x-www-form-urlencoded"}, data="client_id=" + id + "&client_secret=" + secret + "&code=" + token + "&grant_type=authorization_code&redirect_uri=https://google.com/")
accessToken = dict(response.json()).get('access_token')

response1 = requests.post(url="https://user.auth.xboxlive.com/user/authenticate", headers={"Content-Type": "application/json", "Accept": "application/json"}, json={
    "Properties": {
        "AuthMethod": "RPS",
        "SiteName": "user.auth.xboxlive.com",
        "RpsTicket": "d=" + accessToken        
    },
    "RelyingParty": "http://auth.xboxlive.com",
    "TokenType": "JWT"
 })
XBLToken = dict(response1.json()).get('Token')
userhash = dict(response1.json()).get("DisplayClaims").get("xui")[0].get('uhs')

response2 = requests.post(url="https://xsts.auth.xboxlive.com/xsts/authorize", headers={"Content-Type": "application/json", "Accept": "application/json"}, json={
    "Properties": {
        "SandboxId": "RETAIL",
        "UserTokens": [
            XBLToken
        ]
    },
    "RelyingParty": "rp://api.minecraftservices.com/",
    "TokenType": "JWT"
 })
if response2.status_code == 401:
    print("ZAMN!")
    print(response2.text)
    exit()
else:
    XSTSToken = dict(response2.json()).get("Token")

response3 = requests.post(url="https://api.minecraftservices.com/authentication/login_with_xbox", json={
    "identityToken": "XBL3.0 x=" + userhash + ";" + XSTSToken
 })
JWTToken = dict(response3.json()).get("access_token")
time1 = time()
# getting the jwl token [end]
ready = True

keyboard.add_hotkey("num_9", lambda: changeSkin(num9))
keyboard.add_hotkey("num_6", lambda: changeSkin(num6))
keyboard.add_hotkey("num_3", lambda: changeSkin(num3))
keyboard.add_hotkey("num_0", lambda: changeSkin(num0))

keyboard.wait()