import json

def newjs(server,id):
    server_id = {server:id}
    server_id_json = json.dumps(server_id)
    with open('data.json','w') as data:
        data.write(server_id_json)
    return server_id