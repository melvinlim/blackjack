from random import *
import time
import copy

class Hand:
    __slots__=['cards','handval']
    def __init__(self,cards,handval):
        self.cards=cards
        self.handval=handval

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
        self.cDealer=Hand([0]*2,0)
        self.cPlayer=[]
        for p in range(NPLAYERS):
            self.cPlayer.append([Hand([0]*2,0)])
    def shuffle(self):
        self.decks=getShuffled()
    def dealerDecision(self):
        dealerCards=self.cDealer.cards
        bust=False
        dval=valHand(dealerCards)
        self.cDealer.handval=dval
        print("dealer: %s"%(strHand(dealerCards)))
        print("dealer: %d"%(valHand(dealerCards)))
        if(dval==-1):
            print("dealer: %s"%(strHand(dealerCards)))
            print("blackjack")
            return 22
        while(dval<17):
            time.sleep(DEALERDELAY)
            dealerCards.append(self.decks.pop())
            dval=valHand(dealerCards)
            print("*dealer hits")
            print("dealer: %s"%(strHand(dealerCards)))
            print("dealer: %d"%(valHand(dealerCards)))
        if(hasAce(dealerCards)):
            dval=valHand(dealerCards)
            while(dval<17):
                dealerCards.append(self.decks.pop())
        bust=checkBust(dealerCards)
        if(bust):
            print("bust")
            return 0
        time.sleep(DEALERDELAY)
        print("*dealer stands")
        print("dealer: %s"%(strHand(dealerCards)))
        print("dealer: %d"%(valHand(dealerCards)))
        return valHand(dealerCards)
    def playerDecisions(self,player):
        split=False
        bust=False
        choice='?'
        for hand in player:
            h=hand.cards
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
                    hand.handval='b'
            print("player0:%s"%(strHand(h)))
            recentVal=valHand(h)
            if(recentVal==-1):
                print("blackjack")
                recentVal=22
            hand.handval=valHand(h)
    def playerDecision(self):
        return self.playerDecisions(self.cPlayer[0])
    def deal(self):
        assert(len(self.decks)>1+NPLAYERS)
        dealerCards=self.cDealer.cards
        self.nGames+=1
        for j in range(2):
            for i in range(NPLAYERS):
                self.cPlayer[i][0].cards[j]=self.decks.pop()
            dealerCards[j]=self.decks.pop()
    def valLook(self):
        dealerCards=self.cDealer.cards
        print("game:%d"%(self.nGames))
        print("dealer: %d"%(valHand(dealerCards)))
        for i in range(NPLAYERS):
            for hand in self.cPlayer[i]:
                cards=hand.cards
                print("player%d:%d"%(i,valHand(cards)))
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
        playerCards=self.cPlayer[0][0].cards
        dealerCards=self.cDealer.cards
        print("game:%d"%(self.nGames))
        print("dealer: [?? %s]"%(strCard(dealerCards[1])))
        print("player0:%s"%(strHand(playerCards)))
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
    result=t.playerDecision()
    if(result=='q'):      #quit
        break
    pval=t.cPlayer[0][0].handval
    if(pval=='b'):    #bust
        pval=0
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
