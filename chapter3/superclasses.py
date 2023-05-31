class Mama:
    def says(self):
        print("Mama classes says")


class Sister(Mama):
    def says(self):
        Mama.says(self) # 調用母類方法1 
        super(Sister,self).says()# 調用母類方法2 
        super().says()          # 調用母類方法3
        print("Sister classes says")

if __name__ =='__main__':
    Sister().says()
