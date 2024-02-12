import json

def newjs(server,id):
    server_id = {server:id}
    if(takejs(server) == 0):
        with open('data.json','w') as data:
            json.dump(server_id, data)
        return server_id
    else:
        return NameError
        

def takejs(server_name) -> int:
    try:
        with open('data.json','r') as data:
            server_id_json = data.read()
    except:
        with open('data.json','w') as data:
            server_id_json = json.dump({})
    try:
        server_id = json.loads(server_id_json)
        return server_id[server_name]
    except:
        return 0