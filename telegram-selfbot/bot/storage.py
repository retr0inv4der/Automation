from pathlib import Path
import json

class storage :
    def __init__(self , pointsfilename , user ):
        self.filename = pointsfilename 
        self.user = user 
        
    def save_points(self, points): 
        
        #store the data in a buffer before saving the new one
        with open(self.filename , ) as file : 
            data = json.load(file)
        
        
        with open(self.filename , "w") as file :
            data[self.user] = {
                "total-points" : points 
            } 
            
            file.write(json.dumps(data, indent=4))
    
    
    def load_points(self) -> int:
        try:
            with open(self.filename , "r") as file : 
                data = json.load(file)[self.user].get("total-points")
                if data != None:
                    return data
                else :
                    raise Exception("user doesnt exist")
        except : 
            print("something went wrong loading the user data")
    