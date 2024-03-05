import json
from info import host
local = "127.0.0.1"
def newjs(server,id):#ENDED
    new_data =  {"name":server,"id":id}
    if(takejs(server) == 0):
        old_data = takejs()
        old_data["Squads"].append(new_data)
        print("NEW SERVER WAS ADDED. HIS NAME: " + server)
        if(host==local):
            with open('./data/data.json', 'w') as file:
                json.dump(old_data, file, ensure_ascii=False, indent=2)
        else:
            with open('/data/data.json', 'w') as file:
                json.dump(old_data, file, ensure_ascii=False, indent=2)
        return 0
    else:
        return -1
        
def takejs(server_name:str = None):#Ended
    try:
        if (host==local):
            with open('./data/data.json','r') as data:
                data_json = json.load(data)
        else:
            with open('/data/data.json','r') as data:
                data_json = json.load(data)
        if(server_name == None):
            return data_json
        else:
            data_json_squads = data_json["Squads"]
            for squad in data_json_squads:
                if(squad["name"]==server_name):
                    return squad["id"]
            return 0
    except:
        return -1
    
def takejsN():#Not ENDED
    try:
        if (host==local): 
            with open('./data/data.json') as data:
                data_json = json.load(data)
                return data_json["Squads"]
        else:
            with open('/data/data.json') as data:
                data_json = json.load(data)
                return data_json["Squads"]
    except FileNotFoundError:
        return FileNotFoundError
    except:
        return "NoSquads"
