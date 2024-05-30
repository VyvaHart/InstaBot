import json
from os import write

path = 'tg_bots/ig_ninja/data.json'

def user_id_str(jsonStr):
    str_id = ''
    for i in range(2, len(jsonStr)):
        str_id += jsonStr[i]
        if(jsonStr[i+2] == ':'):
            return str_id

def Base(id, lang, name, sur, nick):
    with open(path, 'r', encoding= 'utf-8') as file:
       data = json.load(file)

    with open(path, 'w', encoding='utf-8') as file:
        if id_copy(data, id):
            for i in data['People']:
                if i['id'] == id:
                    i['language'] = lang
                    break
        else: 
            data['People'].append({"id": id,"language": lang, "first_name": name, "last_name": sur, "nickname": nick})  
        data = json.dump(data, file, sort_keys= False, indent = 4, ensure_ascii = False)

def Stats(option_name):
    with open(path, 'r', encoding= 'utf-8') as file:
       data = json.load(file)

    with open(path, 'w', encoding='utf-8') as file:
        for i in data['Statistics']:
            if option_name == "story":
                i['story'] += 1
                break
            elif option_name == "profile_pic":
                i['profile_pic'] += 1
                break
            elif option_name == "post":
                i['post'] += 1
                break

        data = json.dump(data, file, sort_keys= False, indent = 4, ensure_ascii = False)



def id_copy(data, id):
    list = []
    for i in data["People"]:
        list.append(i["id"])
    
    if id in list:
        return True
    else: return False

