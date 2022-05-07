import json

class Coordinate:
    def __init__(self, longi, lati):
        if (longi < -180 or longi > 180):
            raise ValueError("longi must be between -180 and 180")
        
        if (lati < -90 or lati > 90):
            raise ValueError("lati must be between -90 and 90")
        
        self._longitude = longi
        self._latitude = lati

class Image:
    def __init__(self, dir):
        self._directory = dir

class Place:
    """
        ** a constructor for Place class
        * @id (str): the id of the place
        * @name (str): the name of the place
        * @coordinate (Coordinate): the coordinate of the place (longitude, latitude)
        * @avatar (Image): the directory to the avatar of the place
        * @images (list of Image): the list of directories to the images of the place
        * @description (str): the description of the place (optional)) 
    """
    def __init__(self, id, name, coordinate, avatar, images, description = ""):
        self._id = id
        self._name = name
        self._coordinate = coordinate
        self._description = description
        self._avatar = avatar
        self._images = images
    
    """
        ** a method to add image(s) to the place
        * @image (Image or list of Image): the image(s) to be added
    """
    def add_image(self, image):
        if isinstance(image, list):  # if the image is a list (contain a variety of images)
            self._images.extend(image)
        else:  # if the image is a single image
            self._images.append(image)

place_dict = {'this': 'is', 'just': 'for', 'it': 'will', 'not': 'be', 'an': 'empty', 'json': 'file'}
out_file = open('db.json', 'w')
json.dump(place_dict, out_file, indent=4)
out_file.close()