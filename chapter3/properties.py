class Rectangle:
    def __init__(self,x1,y1,x2,y2):
        self.x1 ,self.y1 = x1,y1 
        self.x2,self.y2 = x2,y2 
    
    def widthget(self):
        return self.x2 - self.x1 
    
    def widthset(self,value):
        self.x2 = self.x1 + value
    
    def heightget(self):
        return self.y2 - self.y1 
    
    def heightset(self,value):
        self.y2 = self.y1 + value 
    
    width = property(
        widthget,widthset,doc= 'rectangle width measured from left'
    )
    height = property(
        heightget,heightset,
        doc= 'rectangle height measured from top'
    )
    def __repr__(self):
        return "{}({},{},{},{})".format(self.__class__.__name__,self.x1,self.y1,self.x2,self.y2)

'''
這些屬性使編寫描述符變得更容易，但在對類使用繼承時必須小心處理。 
創建的屬性是使用當前類的方法動態創建的，不會使用派生類中重寫的方法。
'''
class MetricRectangle(Rectangle):
    def widthget(self):
        return "{} meters".format(self.x2 - self.x1)
    width = property(widthget,Rectangle.width.fset)

'''
由於上述原因，創建屬性的最佳語法是使用屬性作為裝飾器。
這將減少類內部方法簽名的數量，並使代碼更具可讀性和可維護性：
'''
class Rectangle_besser:
    def __init__(self,x1,y1,x2,y2):
        self.x1 ,self.y1 = x1,y1 
        self.x2,self.y2 = x2,y2 
    @property
    def width(self):
        return self.x2 - self.x1 
    
    @width.setter
    def width(self,value):
        self.x2 = self.x1 + value
    @property
    def height(self):
        return self.y2 - self.y1 
    @height.setter
    def height(self,value):
        self.y2 = self.y1 + value 
  
    def __repr__(self):
        return "{}({},{},{},{})".format(self.__class__.__name__,self.x1,self.y1,self.x2,self.y2)


if __name__=='__main__':
    rectangle = Rectangle(10,10,25,34)
    print(rectangle.width,rectangle.height)
    rectangle.width = 100 
    print(rectangle)
    rectangle.height = 100 
    print(rectangle)
    print('00')
    print(MetricRectangle(0, 0, 100, 100).width)