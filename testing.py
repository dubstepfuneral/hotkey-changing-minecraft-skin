import webbrowser
import requests

with open("SECRET.txt") as file:
    lines = file.readlines()
    id = lines[0][:-1]
    secret = lines[1]
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

skinResponse = requests.post(url="https://api.minecraftservices.com/minecraft/profile/skins", headers={"Authorization": "Bearer " + JWTToken, 
"Content-Type" : "application/json"}, json={
    #https://i.n-mc.co/a5ff7ac2861f6767.png - jamesj skin
    "variant": "classic",
    "url": "https://i.n-mc.co/a5ff7ac2861f6767.png"
})

print(skinResponse.status_code)