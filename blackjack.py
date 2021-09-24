from random import *
import time
import copy
seed(time.time())
MINBET=10
NDECKS=4
NPLAYERS=2
NPLAYERS=1
STARTINGBANKROLL=100*MINBET
DEALERDELAY=1
def valCard(c):
    v=int(c%13)
    if(v<8):
        return v+2
    if(v==12):
        return 1
    return 10
def valHand(h):
    aces=0
    val=0
    nCards=len(h)
    for c in h:
        cVal=valCard(c)
        val+=cVal
        if(cVal==1):
            aces+=1
    if(val>=21):
        return val
    while((aces>0)and(val+10<=21)):
        aces-=1
        val+=10
    if(val==21 and nCards==2):
        return -1   #-1 means blackjack
    return val
def strFace(c):
    s=int(c%13)
    if(s<8):
        return str(s+2)
    else:
        if(s==8):
            return 'T'
        elif(s==9):
            return 'J'
        elif(s==10):
            return 'Q'
        elif(s==11):
            return 'K'
        elif(s==12):
            return 'A'
def strSuit(c):
    s=int(c/(13*NDECKS))
    if(s==0):
        return 'c'
    elif(s==1):
        return 'd'
    elif(s==2):
        return 'h'
    elif(s==3):
        return 's'
def hasAce(h):
    for c in h:
        if(strFace(c)=='A'):
            return True
    return False
def strCard(c):
    return "%s%s"%(strFace(c),strSuit(c))
def strHand(h):
    ret="["
    for c in h:
        ret+=strCard(c)+" "
    ret=ret[:-1]
    ret+="]"
    return ret
    #return "[%s %s]"%(strCard(h[0]),strCard(h[1]))
for i in range(52*NDECKS):
    x=i
    #print(x)
    #print(strSuit(x))
    #print(strFace(x))
    #print("%s%s"%(strFace(x),strSuit(x)))
    print(strCard(x))

def getShuffled():
    return sample(range(52*NDECKS),52*NDECKS)

def checkBust(h):
    if(valHand(h)>21):
        return True
    return False

d=getShuffled()
print(d)

for c in d:
    print(strCard(c))

class Table():
    nGames=0
    decks=range(52*NDECKS)
    def removeCards(self):
        self.cDealer=[0]*2
        self.cPlayer=[]
        self.cPlayer.append([[0]*2])
        for p in range(1,NPLAYERS):
            self.cPlayer.append([[0]*2])
    def shuffle(self):
        self.decks=getShuffled()
    def dealerDecision(self):
        bust=False
        dval=valHand(self.cDealer)
        print("dealer: %s"%(strHand(self.cDealer)))
        print("dealer: %d"%(valHand(self.cDealer)))
        if(dval==-1):
            print("dealer: %s"%(strHand(self.cDealer)))
            print("blackjack")
            return 22
        while(dval<17):
            time.sleep(DEALERDELAY)
            self.cDealer.append(self.decks.pop())
            dval=valHand(self.cDealer)
            print("*dealer hits")
            print("dealer: %s"%(strHand(self.cDealer)))
            print("dealer: %d"%(valHand(self.cDealer)))
        if(hasAce(self.cDealer)):
            dval=valHand(self.cDealer)
            while(dval<17):
                self.cDealer.append(self.decks.pop())
        bust=checkBust(self.cDealer)
        if(bust):
            print("bust")
            return 0
        time.sleep(DEALERDELAY)
        print("*dealer stands")
        print("dealer: %s"%(strHand(self.cDealer)))
        print("dealer: %d"%(valHand(self.cDealer)))
        return valHand(self.cDealer)
    def playerDecision(self):
        handvals=[]
        split=False
        bust=False
#        print("player0:%s"%(strHand(self.cPlayer[0][0])))
        choice='?'
        for h in self.cPlayer[0]:
            while(choice!='n'):
                print("player0:%s"%(strHand(h)))
                print("value:%d"%(valHand(h)))
                print("hit? (y/n/d/s/q)")
                choice=input()
                if(choice=='y'):
                    h.append(self.decks.pop())
#                    print("player0:%s"%(strHand(h)))
#                    print("value:%d"%(valHand(h)))
                elif(choice=='s'):
                    print("split")
                    self.cPlayer[0].append([h[1]])
                    #self.cPlayer[0][0]=[copy.deepcopy(h[0])]
                    h=[copy.deepcopy(h[0])]
                    h.append(self.decks.pop())
                    h2=self.cPlayer[0][-1]
                    h2.append(self.decks.pop())
                    print("player0:%s"%(strHand(h)))
                    print("player0:%s"%(strHand(h2)))
#                        for h2 in self.cPlayer[0]:
#                            h2.append(self.decks.pop())
#                            print("player0:%s"%(strHand(h2)))

                elif(choice=='q'):
                    return'q'
                    
                bust=checkBust(h)
                if(bust):
                    print("bust")
                    print("player0:%s"%(strHand(h)))
                    return'b'
            #print("player0:%s"%(strHand(self.cPlayer[0])))
            print("player0:%s"%(strHand(h)))
            recentVal=valHand(h)
            if(recentVal==-1):
                print("blackjack")
                recentVal=22
            handvals.append(valHand(h))
        return handvals
    def deal(self):
        assert(len(self.decks)>1+NPLAYERS)
        self.nGames+=1
        for j in range(2):
            for i in range(NPLAYERS):
                self.cPlayer[i][0][j]=self.decks.pop()
            self.cDealer[j]=self.decks.pop()
    def valLook(self):
        print("game:%d"%(self.nGames))
        print("dealer: %d"%(valHand(self.cDealer)))
        for i in range(NPLAYERS):
            for hand in self.cPlayer[i]:
                print("player%d:%d"%(i,valHand(hand)))
                #print("player%d:%d"%(i,valHand(self.cPlayer[i])))
    def omniLook(self):
        print("game:%d"%(self.nGames))
        #print("dealer: %s"%(strCard(self.cDealer)))
        print("dealer: %s"%(strHand(self.cDealer)))
        playerHand=self.cPlayer[0][0]
        print(playerHand)
        print(self.cDealer)
        print("player0:%s"%(0,strHand(playerHand)))
        #print("player0:%s"%(0,strHand(playerHand[0])))
        #for i in range(1,NPLAYERS):
        #    print("player%d:%s"%(i,strHand(self.cPlayer[i])))
        #    #print("player%d: %s"%(i,strCard(self.cPlayer[i])))
    def look(self):
        playerHand=self.cPlayer[0]
        print("game:%d"%(self.nGames))
        print("dealer: [?? %s]"%(strCard(self.cDealer[1])))
        print("player0:%s"%(strHand(playerHand[0])))
        for i in range(1,NPLAYERS):
            print("player%d:[?? ??]"%(i))
            #print("player%d: %s"%(i,strHand(self.cPlayer[i])))

t=Table()
#print(t.cDealer)
#print(t.cPlayer[0])
t.shuffle()
bankroll=STARTINGBANKROLL
betsize=MINBET
for i in range(52*NPLAYERS):
    t.removeCards()
    print()
    t.deal()
    t.look()
    #t.omniLook()
    t.valLook()
    pval=t.playerDecision()
    if(pval=='q'):      #quit
        break
    elif(pval=='b'):    #bust
        pval=0
    else:
        pval=pval[0]
    dval=t.dealerDecision()
    print('%d %d'%(pval,dval))
    if(pval==0):
        print('*bust')
        print('*player loss')
        bankroll-=betsize
    elif(pval==dval):
        print('*tie')
    elif(pval>dval):
        print('*player win')
        bankroll+=betsize
    else:
        print('*player loss')
        bankroll-=betsize
    print('*bankroll:%d'%bankroll)
