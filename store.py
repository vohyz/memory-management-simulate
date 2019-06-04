from random import randint
import queue
from time import time

class Store():
    maxsize = 640
    storespace = [[0],[640]] #第一个存申请作业号，第二个存分区大小

    def __init__(self):
        return

    def firstfit(self,quantity):
        store = self.storespace
        for i in range(len(store[0])):
            if store[0][i] == 0 and store[1][i] >= quantity:
                return i
        return -1

    def bestfit(self,quantity):
        store = self.storespace
        store2 = self.storespace[1].copy()
        best = []
        for i in range(len(store[0])):
            best.append(min(store2))
            store2[store2.index(best[i])] = self.maxsize
        for i in best:
            number = store[1].index(i)
            if store[0][number] == 0 and store[1][number] >= quantity:
                return number
        return -1

    def loadfirst(self):
        self.load(130)
        self.load(60)
        self.load(100)
        self.free(1)
        self.load(200)
        self.free(2)
        self.free(0)
        self.load(140)
        self.load(60)
        self.load(50)
        self.free(1)
        self.show()

    def loadbest(self):
        self.load2(130)
        self.load2(60)
        self.load2(100)
        self.free(1)
        self.load2(200)
        self.free(2)
        self.free(0)
        self.load2(140)
        self.load2(60)
        self.load2(50)
        self.free(0)
        self.show()

    def load(self,quantity):
        store = self.storespace
        site = self.firstfit(quantity)
        if store[1][site] > quantity:
            store[1][site] -= quantity
            store[0].insert(site, 1)
            store[1].insert(site, quantity)
        elif store[1][site] == quantity:
            store[0][site] = 1
        else:
            print("FIT WRONG !")

    def load2(self,quantity):
        store = self.storespace
        site = self.bestfit(quantity)
        if store[1][site] > quantity:
            store[1][site] -= quantity
            store[0].insert(site, 1)
            store[1].insert(site, quantity)
        elif store[1][site] == quantity:
            store[0][site] = 1
        else:
            print("FIT WRONG !")

    def free(self,site):
        store = self.storespace
        if site < len(store[0]):
            store[0][site] = 0
            if site < len(store)-1:
                if store[0][site+1] == 0:
                    store[1][site] += store[1].pop(site+1)
                    store[0].pop(site+1)
            if site >= 1:
                if store[0][site-1] == 0:
                    store[1][site-1] += store[1].pop(site)
                    store[0].pop(site)
        else:
            print('NO SITE')

    def show(self):
        store = self.storespace
        address = 0
        print('分区号|起始地址|分区大小|状态\n')
        for i in range(len(store[0])):
            if i > 0:
                address += store[1][i-1]
            print(str(i),'   |   ',str(address),'    |    ',str(store[1][i]),'   |    ',str(store[0][i]),'\n')


class Page():
    pages = 32
    Q = queue.Queue()
    address = []
    page = [[] for i in range(32)]
    exist = 0
    notin = 0


    def __init__(self):
        self.CreateSequence()
        self.CreatePages()
        return

    def CreateSequence(self):
        start = randint(0, 319)
        self.address.append(start)
        self.address.append(start+1)
        for i in range(79):

            a = randint(0,start-1)
            self.address.append(a)
            self.address.append(a + 1)
            b = randint(a+2,319)
            self.address.append(b)
            self.address.append(b+1)
            start = b;
        a = randint(0, start - 1)
        self.address.append(a)
        self.address.append(a + 1)


    def CreatePages(self):
        for i in range(32):
            for j in range(10):
                self.page[i].append(self.address[i*10+j])
                self.address[i*10+j] = 0


    def FIFO(self):  #先进先出，使用队列
        for i in range(32):
            self.address[i] = 0
        self.exist = 0
        self.notin = 0

        for i in range(4):
            if self.Q.empty() == 0:
                self.Q.get()
        for i in range(32):
            for j in range(10):
                page = int(self.page[i][j]/10)


                if self.address[page] == 1:

                    print("页面刚好在内存中,地址:",self.page[i][j],'\n')
                    self.exist += 1
                else:
                    self.notin += 1
                    count = self.address.count(1)
                    if count < 4:
                        self.address[page] = 1
                        self.Q.put(page)
                    elif count == 4:
                        self.address[self.Q.get()] = 0
                        print("发生置换\n")
                        self.address[page] = 1
                        self.Q.put(page)

    def LRU(self):
        for i in range(32):
            self.address[i] = 0
        self.exist = 0
        self.notin = 0
        lruset = [[], []]
        for i in range(32):
            for j in range(10):
                page = int(self.page[i][j]/10)
                if self.address[page] == 1:
                    print("页面刚好在内存中,地址:",self.page[i][j],'\n')
                    self.exist += 1
                    lruset[1][lruset[0].index(page)] = time()
                    self.LRUsort(lruset)
                else:
                    self.notin += 1
                    count = self.address.count(1)
                    if count < 4:
                        self.address[page] = 1
                        lruset[0].append(page)
                        lruset[1].append(time())
                        self.LRUsort(lruset)
                    elif count == 4:
                        self.address[lruset[0][0]] = 0
                        print("发生置换\n")
                        self.address[page] = 1
                        lruset[0][0] = page
                        lruset[1][0] = time()
                        self.LRUsort(lruset)

    def LRUsort(self,lruset):
        long = min(lruset[1])
        seat = lruset[1].index(long)
        temp = lruset[1][seat]
        lruset[1][seat] = lruset[1][0]
        lruset[1][0] = temp
        temp = lruset[0][seat]
        lruset[0][seat] = lruset[0][0]
        lruset[0][0] = temp

    def show(self):
        print("缺页次数:",self.notin)
        print("缺页率:",float(self.notin/320)*100,'%')

first = Store()
page = Page()
while True:
    operate = int(input('请输入您的操作:'
                    '1:载入初始化操作（最先）'
                    '2:载入初始化操作（最优）'   
                    '3:申请内存(最先）'
                    '4:申请内存（最优）'
                    '5:释放内存'
                    '6:显示内存'
                    '7:调页(FIFO)'
                    '8:调页(LRU)'
                    '0:退出'
                    '\n'))
    if operate == 1:
        first.loadfirst()
    elif operate == 2:
        first.loadbest()
    elif operate == 3:
        quantity = int(input('请输入申请空间大小：'))
        first.load(quantity)
    elif operate == 4:
        quantity = int(input('请输入申请空间大小：'))
        first.load2(quantity)
    elif operate == 5:
        site = int(input('请输入释放分区号：'))
        first.free(site)
    elif operate == 6:
        first.show()
    elif operate == 7:
        page.FIFO()
        page.show()
    elif operate == 8:
        page.LRU()
        page.show()
    elif operate == 0:
        break
