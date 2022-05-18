import json

data = None

def query_all_places():
    global data
    result = []

    # read data from json file
    for place in data:
        id = place['id']
        name = place['name']
        this_place = {'ID' : id, 'Name' : name}
        result.append(this_place)
    return json.dumps(result).encode()


def query_one_place(place_id):
    global data
    this_place = {
        'ID' : '', 
        'Name' : '', 
        'Coordinate' : '',
        'Description' : ''
    }

    # read data from json file
    for place in data:
        if place['id'] == place_id:
            id = place['id']
            name = place['name']
            description = place['description']
            coordinate = place['coordinate']
            this_place = {'ID' : id, 
                'Name' : name, 
                'Coordinate' : coordinate ,
                'Description' : description}
            break

    return json.dumps(this_place).encode()

def query_avatar(place_id):
    avt_path = ""
    for place in data:
        if place['id'] == place_id:
            avt_path = place["avatar"]
            break
    if avt_path == "":
        raise Exception("No such ID!")
    img = open(avt_path, "rb")
    img_byte = img.read()
    img.close()
    return img_byte

def query_image(place_id, idx):
    img_list = []
    for place in data:
        if place['id'] == place_id:
            img_list = place["images"]
            break
    if img_list == []:
        raise Exception("No such ID!")
    if idx >= len(img_list):
        raise Exception("Out of bound!")
    img = open(img_list[idx], "rb")
    img_byte = img.read()
    img.close()
    return img_byte

def __init__():
    global data
    database_file = open('db.json', 'r')
    data = json.load(database_file)
    database_file.close()