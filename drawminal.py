import os
import platform

def clear():
    if platform.system == "Windows":
        os.system("cls")
    else:
        os.system("clear")

class DrawminalBoard:
    def __init__(self):
        size = os.get_terminal_size()

        self.h = size.lines
        self.w = size.columns

        self.map_ = [[" " for _ in range(self.w)] for __ in range(self.h)]
        
    def print_(self):
        clear() 
      
        for row in self.map_:
            print(*row,sep="")
        
    def replace(self,row,col,val):
        if len(val) != 1:
            raise ValueError("len(val) shouldnt be any value other than 1")
        self.map_[row][col] = val

    def clear(self):
        self.map_ = [[" " for _ in range(self.w)] for __ in range(self.h)]
