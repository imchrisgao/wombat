class plane: # a layer of the tetrahedron
    def __init__(self, n):
        self.rows = [None]*n #a list of rows within the plane/level
        self.__counter = 0
        for i, val in enumerate(self.rows): #get used to using enumerate
            self.rows[i] = [None]*(n-i) 
            self.__counter+=(n-i) 
    
    def getcounter(self):
        return self.__counter
    #**********************************
    #print methods
    def printlevel(self):
        for row in self.rows:
            print(row)

    def printgen(self): #for fun
        for row in self.rows:
            yield row
#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
import copy
import itertools
class tetrahedronarr:
    def __init__(self, l):
        self.planes = [None]*l #a list of planes
        self.__total = 0
        for i in range(len(self.planes)): #but there will be some situations where you probably don't want to use enumerate
            self.planes[i] = plane(i+1)
            self.__total+=self.planes[i].getcounter()
    
    def insertval(self, inputstr):
        temp = inputstr.split(' ')
        if len(temp) != self.__total:
            print('incorrect number of values')
            return
        temp = list(reversed(temp)) #bc I want to use built-in pop()
        for plane in self.planes:
            for row in plane.rows:
                for i in range(len(row)):
                    #row[i] = node(temp.pop()) #consider making nodes...
                    row[i] = int(temp.pop()) #makes popping easier
    #############################################    
    #Find max of a tetrahedron
    def bruteforce(self): #unfortunately finds max sum of wombats by checking every single combination
        onedls = []
        maxsum = 0
        for p, plane in enumerate(self.planes):
            for r, row in enumerate(plane.rows):
                for i, val in enumerate(row):
                    onedls.append((p,r,i))
        #print(onedls)
        for L in range(0, len(onedls)+1):
            for subset in itertools.combinations(onedls, L):
                temp = self.findmulti(list(subset))
                if temp > maxsum:
                    maxsum = temp
        return maxsum
    
    #############################################
    #methods that supplement finding max and also are cool by themselves
    def findpath(self, plane, row, index): #finds all nodes you'd need to remove given a base node
        addlist = []
        self.__findpath(addlist, plane, row, index)
        return addlist
    
    def __findpath(self, addlist, plane, row, index):
        addlist.append((plane, row, index))
        if plane is not 0: 
            for r, ls in enumerate(self.planes[plane-1].rows): #recounting and which nodes is wrong
                for i, val in enumerate(ls):
                    if row-1<=r<=row and index==i and (plane-1, r, i) not in addlist or \
                    row==r and index-1<=i<=index and (plane-1, r, i) not in addlist:
                        self.__findpath(addlist, plane-1, r, i)          
        return 
    
    def sumval(self, plane, row, index): #finds sum given single coordinate. uses private __findcoor
        tree = copy.deepcopy(self)
        addto = 0
        addlist = [] #to avoid recounting
        addto+=self.__findcoor(tree, addto, addlist, plane, row, index) #why isn't this passing by reference?
        return addto
    
    def __findcoor(self, tree, addto, addlist, plane, row, index): 
        addto=tree.planes[plane].rows[row][index] 
        addlist.append((plane, row, index))
        if plane is not 0: 
            for r, ls in enumerate(tree.planes[plane-1].rows): #recounting and which nodes is wrong
                for i, val in enumerate(ls):
                    #print ('plane : ' + str(plane-1) + ' r : ' + str(r) + " i : " + str(i) + " row : " + str(row)) #for testing purposes
                    if row-1<=r<=row and index==i and (plane-1, r, i) not in addlist or \
                    row==r and index-1<=i<=index and (plane-1, r, i) not in addlist:
                        addto+=self.__findcoor(tree, addto, addlist, plane-1, r, i)             
        return addto
    
    def findmulti(self, coorlist): #finds sum of list of coordinates. uses private __findmulti
        #coorlist should be a list of tuples in format of (plane, row, index)
        addto = 0
        tree = copy.deepcopy(self)
        addlist = [] #for visibility and to avoid repeats
        for tup in coorlist:
            plane, row, index = tup
            addto+=self.__findmulti(tree, addto, addlist, plane, row, index) 
            #print(addto)
        #print(addlist)
        return addto
    
    def __findmulti(self, tree, addto, addlist, plane, row, index): 
        addto=tree.planes[plane].rows[row][index] 
        tree.planes[plane].rows[row][index] = 0
        addlist.append((plane, row, index)) #add tuples to this and iterate through them all later
        
        if plane is not 0: 
            for r, ls in enumerate(tree.planes[plane-1].rows): #recounting and which nodes is wrong
                for i, val in enumerate(ls):
                    if row-1<=r<=row and index==i and (plane-1, r, i) not in addlist or \
                    row==r and index-1<=i<=index and (plane-1, r, i) not in addlist:
                        addto+=self.__findmulti(tree, addto, addlist, plane-1, r, i)        
        return addto
    #**********************************
    #print methods
    def printtetra(self):
        for plane in self.planes:
            plane.printlevel()
            print("")
    
    def printtotal(self):
        print('total : ' + str(self.__total))

#----------------------------------------
def main():
    t0 = tetrahedronarr(3) #parameter is number of wombats in tetrahedron
    
    #various strings to test as parameters
    s0 = '5 -2 -7 -3 1 0 8 0 3 2' #values of wombats
    fail = '5 2' 
    
    t0.insertval(s0)
    t0.printtetra()
    t0.printtotal()

    print('Not an elegant solution : ' + str(t0.bruteforce()))
    print(t0.findnotquitemax())

    
if __name__ == "__main__":
    main()
