class TreeNode:
    def __init__(self,data):
        self.data = data
        self.children = []
        self.parent = None

    def __repr__(self, level=0):
        ret = "    "*level+repr(self.data)+"\n"
        for child in self.children:
            ret += child.__repr__(level+1)
        return ret

    def addChild(self,child):
        child.parent = self
        self.children.append(child)
    
    def removeChild(self,child):
        child.parent = None
        self.children.remove(child)






    

    

