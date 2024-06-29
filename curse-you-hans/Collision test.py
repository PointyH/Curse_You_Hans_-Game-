import matplotlib.pyplot as plt

class Box():

    def __init__(self,x,y,lenx,leny):
        self.x1 = x
        self.y1 = y
        
        self.x2 = x+lenx
        self.y2 = y+leny

    def plot(self, colour):
        x_arr = []
        y_arr = []
        for x,y in zip([self.x1, self.x1, self.x2, self.x2, self.x1], [self.y1, self.y2, self.y2, self.y1, self.y1]):
            x_arr.append(x)
            y_arr.append(y)
        plt.plot(x_arr,y_arr, color=colour)

def collide(o1,o2):
    if ((o2.x1 <= o1.x1 and o1.x1 <= o2.x2) or (o2.x1 <= o1.x2 and o1.x2 <= o2.x2)) and ((o2.y1 <= o1.y1 and o1.y1 <= o2.y2) or (o2.y1 <= o1.y2 and o1.y2 <= o2.y2)):
        return 1
    else:
        return 0
def collision_check(o1,o2):
    if collide(o1,o2) or collide(o2,o1):
        print('collision')
    else:
        print('no collision')
    


    
b1 = Box(1,2,6,5)
b2 = Box(6,3,4,7)
b3 = Box(9,10,3,5)

collision_check(b1,b2)
collision_check(b1,b3)
collision_check(b2,b3)

b1.plot('r')
b2.plot('b')
b3.plot('g')
plt.show()
