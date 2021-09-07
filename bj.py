from random import *
import time
seed(time.time())
MINBET=10
NDECKS=4
NPLAYERS=2
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
        for p in range(NPLAYERS):
            self.cPlayer.append([0]*2)
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
        split=False
        bust=False
        print("player0:%s"%(strHand(self.cPlayer[0])))
        choice='?'
        while(choice!='n'):
#            if(split==True):
#                for h in 
            print("hit? (y/n/d/s/q)")
            choice=input()
            if(choice=='y'):
                self.cPlayer[0].append(self.decks.pop())
                print("player0:%s"%(strHand(self.cPlayer[0])))
                print("value:%d"%(valHand(self.cPlayer[0])))
            elif(choice=='s'):
                print("split")
                if(split==True):
                    pass    #do a buncha crap i have to type out eventually maybe
                split=True
                self.splitHands=[[self.cPlayer[0][0]],[self.cPlayer[0][1]]]
                for h in self.splitHands:
                    h.append(self.decks.pop())
                    print("player0:%s"%(strHand(h)))

            elif(choice=='q'):
                return'q'
                
            bust=checkBust(self.cPlayer[0])
            if(bust):
                print("bust")
                print("player0:%s"%(strHand(self.cPlayer[0])))
                return 0
        print("player0:%s"%(strHand(self.cPlayer[0])))
        handval=valHand(self.cPlayer[0])
        if(handval==-1):
            print("blackjack")
            return 22
        return handval
    def deal(self):
        assert(len(self.decks)>1+NPLAYERS)
        self.nGames+=1
        for j in range(2):
            for i in range(NPLAYERS):
                self.cPlayer[i][j]=self.decks.pop()
            self.cDealer[j]=self.decks.pop()
    def valLook(self):
        print("game:%d"%(self.nGames))
        print("dealer: %d"%(valHand(self.cDealer)))
        for i in range(NPLAYERS):
            print("player%d:%d"%(i,valHand(self.cPlayer[i])))
    def omniLook(self):
        print("game:%d"%(self.nGames))
        #print("dealer: %s"%(strCard(self.cDealer)))
        print("dealer: %s"%(strHand(self.cDealer)))
        for i in range(NPLAYERS):
            print("player%d:%s"%(i,strHand(self.cPlayer[i])))
            #print("player%d: %s"%(i,strCard(self.cPlayer[i])))
    def look(self):
        print("game:%d"%(self.nGames))
        print("dealer: [?? %s]"%(strCard(self.cDealer[1])))
        print("player0:%s"%(strHand(self.cPlayer[0])))
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
    t.omniLook()
    t.valLook()
    pval=t.playerDecision()
    if(pval=='q'):
        break
    dval=t.dealerDecision()
    print('%d %d'%(pval,dval))
    if(pval==dval):
        print('*tie')
    elif(pval>dval):
        print('*player win')
        bankroll+=betsize
    else:
        print('*player loss')
        bankroll-=betsize
    print('*bankroll:%d'%bankroll)
