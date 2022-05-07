class Place:
    def __init__(self, name, images_lists = []):
        self.name = name
        self.images_lists = images_lists
    
    def change_name(self, new_name):
        self.name = new_name

p1 = Place("Ho Chi Minh City")
print(p1.name)
p1.change_name("Sai Gon")
print(p1.name)

l2 = ["img/img1", "img/img2", "img/img3"]
p2 = Place("Ha Noi", l2)
print(p2.name)
print(p2.images_lists)