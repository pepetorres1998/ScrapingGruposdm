class EraseSpaces:
    def __init__(self, lis):
        self.list = self.erase_it(lis)

    def erase_it(self, lis):
        newlist = []
        for i in range(len(lis)):
            if(lis[i] != ' '):
                if(lis[i] != '\n'):
                    newlist.append(lis[i])
            elif(lis[i] != '\n'):
                if(lis[i-1] != ' ' and lis[i+1] != ' '):
                    newlist.append(lis[i])
        newlist = "".join(newlist)
        return newlist

if(__name__=='__main__'):
    list = [' ', ' ', ' ', ' ', 'n', 'o', ' ', 'n', 'o', ' ', ' ', ' ', ' ']
    print(list)
    erased = EraseSpaces(list)
    print(erased.list)
