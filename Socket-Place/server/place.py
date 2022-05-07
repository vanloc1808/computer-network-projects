class Coordinate:
    def __init__(self, longitude, latitude):
        if (longitude < -180 or longitude > 180):
            raise ValueError("Longitude must be between -180 and 180")
        
        if (latitude < -90 or latitude > 90):
            raise ValueError("Latitude must be between -90 and 90")
        
        self.longitude = longitude
        self.latitude = latitude

