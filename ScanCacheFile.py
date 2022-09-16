#pip install requests
#pip install win10toast

import os, requests,re,time,json
from  win10toast import ToastNotifier


FavKey = "New Text Document.txt" #Make a New File with that name inside of the folder with the avatar file to add it to your favorite
waits = 1 #Second wait before another full scan start
APIkey = "" #Your API auth key
#Open file explorer and go to C:\Users\{Ur pc username}\AppData\LocalLow\VRChat\VRChat\Cache-WindowsPlayer

def ScanFile(Path):
    with open(Path):
        pass
         

def scan(dir):
    #Vers
    Notification = ToastNotifier()
    headers={"User-Agent":"insomnia/2022.5.1"}
    apikeyNAuth = {'apiKey': 'JlE5Jldo5Jibnk5O5hTx6XVqsJu4WJ26', 'auth': APIkey}

    s = os.scandir(dir)
    for i in s:
        if i.is_dir():scan(f"{dir}/{i.name}")
        
        if os.path.exists(f"{dir}/info.json"):
            with open(f"{dir}/info.json") as info:
                inf = json.load(info)
                if inf["VRCJson"] == "Private":
                    with open(f"{dir}/Private","w"):
                        pass

        if i.is_file():

            if FavKey != "" or FavKey != "__data" or FavKey != "_info" or FavKey != "AvatarThumbnail.png" or FavKey != "info.json" or "avtr_" not in FavKey:
                if i.name == FavKey:
                    for n in os.scandir(os.path.dirname(i.path)):
                        if "avtr_" in n.name:
                            r = requests.post(url=f"https://api.vrchat.cloud/api/1/favorites",headers=headers,cookies=apikeyNAuth,json={"type": "avatar","favoriteId":n.name,"tags": ["avatars1"]})
                            print(r.json())
                    os.remove(i.path)

            if "avtr" in i.name or "wrld" in i.name or os.path.exists(f"{dir}/info.json") or os.path.exists(f"{dir}/Error"):
                continue

            if i.name == "__data":
                if not os.path.exists(f"{dir}/info.json"):
                    with open(f"{dir}/{i.name}",errors="ignore") as file:
                        avtrID,wrldID = None,None
                        for line in file:
                            if avtrID == None: avtrID = re.search(r"avtr_[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",line)
                            if wrldID == None: wrldID = re.search(r"(wrld|wld)_[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",line)
                       
                        if wrldID:
                            retry = True
                            if retry:
                                try:
                                    r = requests.get(url=f"https://api.vrchat.cloud/api/1/worlds/{wrldID.group(0)}",cookies= apikeyNAuth ,headers=headers)
                                    print(f"Found: {wrldID.group(0)} | Respond:{r.status_code}")
                                    with open(f"{dir}/info.json","w") as jsons:
                                        vrcj = "Private"
                                        if r.status_code == 200:
                                            vrcj = r.json()
                                            with open(f"{dir}/WorldThumbnail.png","wb") as png:
                                                png.write(requests.get(url=vrcj["imageUrl"],headers=headers).content)
                                        wjson = {
                                            "fileNumber": re.search(r"[0-9a-zA-Z]{16}",dir).group(0),
                                            "AvatarID": wrldID.group(0),
                                            "VRCJson": vrcj
                                        }
                                        jsons.write(json.dumps(wjson,indent=4))
                                    with open(f"{dir}/{wrldID.group(0)}","w"):pass
                                    Notification.show_toast(title=f"VRChat | Ripper",msg=f"Found: {wrldID.group(0)}| Response: {r.status_code}",duration=2,icon_path="VRC.ico")
                                    retry = False
                                except (requests.exceptions.SSLError,json.decoder.JSONDecodeError) as Err:
                                    print(f"Error: {Err}")
                                    print(f"Error: Retrying {wrldID}")

                        elif avtrID:
                            retry = True
                            if retry:
                                try:
                                    r = requests.get(url=f"https://api.vrchat.cloud/api/1/avatars/{avtrID.group(0)}",cookies= apikeyNAuth ,headers=headers)
                                    print(f"Found: {avtrID.group(0)} | Respond:{r.status_code}")
                        
                                    if r.status_code == 200:
                                        with open(f"{dir}/info.json","w") as jsons:
                                            vrcj = r.json()
                                            wjson = {
                                                "fileNumber": re.search(r"[0-9a-zA-Z]{16}",dir).group(0),
                                                "AvatarID": avtrID.group(0),
                                                "VRCJson": vrcj
                                            }
                                            jsons.write(json.dumps(wjson,indent=4))
                                            
                                        with open(f"{dir}/AvatarThumbnail.png","wb") as png:
                                            png.write(requests.get(url=vrcj["imageUrl"],headers=headers).content)

                                        with open(f"{dir}/{avtrID.group(0)}","w"):pass

                                    if r.status_code == 404:
                                        with open(f"{dir}/info.json","w") as jsons:
                                            vrcj = "Private"
                                            wjson = {
                                                "fileNumber": re.search(r"[0-9a-zA-Z]{16}",dir).group(0),
                                                "AvatarID": avtrID.group(0),
                                                "VRCJson": vrcj
                                            }
                                            jsons.write(json.dumps(wjson,indent=4))

                                        with open(f"{dir}/{avtrID.group(0)}","w"):pass
                                        with open(f"{dir}/Private","w"):pass
                                    
                                    if r.status_code == 401:
                                        print("Cookie Expired or Cookie isnt working")
                                    retry = False
                                except (requests.exceptions.SSLError,json.decoder.JSONDecodeError) as Err:
                                    print(f"Error: {Err}")
                                    print(f"Error: Retrying {avtrID}")


                            Notification.show_toast(title=f"VRChat | Ripper",msg=f"Found: {avtrID.group(0)}| Response: {r.status_code}",duration=2,icon_path="VRC.ico")

                        else:
                            print(f"{dir} : Error")
                            with open(f"{dir}/Error","w"):pass

if __name__ == "__main__":
    Scan = 0
    Userpath = os.environ["USERPROFILE"]
    VRC = f"{Userpath}/AppData/LocalLow/VRChat/VRChat"
    while True:
        Scan += 1 
        time.sleep(waits)
        scan(f"{VRC}/Cache-WindowsPlayer")

        
