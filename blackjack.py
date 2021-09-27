from random import *
import time
import copy

class Hand(object):
    __slots__=['cards','handval']
    def __init__(self):
        self.cards=[]
        self.handval=0

class Player(object):
    def __init__(self):
        self.hands=[]

class Human(Player):
    def __init__(self):
        super().__init__()
    def decide(self,decks):
        playerHands=self.hands
        split=False
        for hand in playerHands:
            h=hand.cards
            choice='?'
            while(choice!='n'):
                if(len(h)==1):
                    h.append(decks.pop())
                    continue
                    
                print("player0:%s"%(strHand(h)))
                print("value:%d"%(valHand(h)))
                print("hit? (y/n/d/s/q)")
                choice=input()
                if(choice=='y'):
                    h.append(decks.pop())
#                    print("player0:%s"%(strHand(h)))
#                    print("value:%d"%(valHand(h)))
                    bust=checkBust(h)
                    if(bust):
                        print("*bust")
                        break
                elif(choice=='s'):
                    if(sameFace(h) and (len(h)==2)):
                        print("split")
                        newHand1=Hand()
                        newHand2=Hand()
                        newHand1.cards=[copy.deepcopy(h[0])]
                        newHand2.cards=[copy.deepcopy(h[1])]
                        newHand1.handval=0
                        newHand2.handval=0
                        playerHands.remove(hand)
                        playerHands.append(newHand1)
                        playerHands.append(newHand2)
                        return self.decide()
                    else:
                        print('can only split exactly two cards with the same face')

                elif(choice=='q'):
                    return'q'
                elif(choice!='n'):
                    print('invalid command')
            print("player0:%s"%(strHand(h)))
            recentVal=valHand(h)
            if(recentVal==22):
                print("*blackjack")
            hand.handval=recentVal

soft17rule=True         #dealer hits on soft 17 (ace and 6)
seed(time.time())
MINBET=10
NDECKS=4
NPLAYERS=2
#NPLAYERS=1
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
        if(val>21):
            return 0    #busted hand is worth 0.
        elif(val==21 and nCards==2):
            return 22   #blackjack beats 21.  should also win immediately unless dealer also has blackjack.
        else:
            return 21
    while((aces>0)and(val+10<=21)):
        aces-=1
        val+=10
    if(val>21):
        return 0    #busted hand is worth 0.
    elif(val==21 and nCards==2):
        return 22   #blackjack beats 21.  should also win immediately unless dealer also has blackjack.
    return val
def hasAce(h):
    for c in h:
        if(strFace(c)=='A'):
            return True
    return False
def isSoft17(hand):
    hval=valHand(hand)
    if(hval!=17):
        return False
    if(not hasAce(hand)):
        return False
    if(len(hand)>2):
        return False
    return True
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
def strCard(c):
    return "%s%s"%(strFace(c),strSuit(c))
def sameFace(h):
    if strFace(h[0])==strFace(h[1]):
        return True
    return False
def strHand(h):
    ret="["
    for c in h:
        ret+=strCard(c)+" "
    ret=ret[:-1]
    ret+="]"
    return ret
    #return "[%s %s]"%(strCard(h[0]),strCard(h[1]))

def testFunction():
    for i in range(52*NDECKS):
        x=i
        #print(x)
        #print(strSuit(x))
        #print(strFace(x))
        #print("%s%s"%(strFace(x),strSuit(x)))
        print(strCard(x))

def getShuffledDeck():
    return sample(range(52*NDECKS),52*NDECKS)

def checkBust(h):
    if(valHand(h)==0):
        return True
    return False

class Table():
    def __init__(self):
        self.nGames=0
        self.decks=getShuffledDeck()
        self.cDealer=Hand()
        self.players=[]
        for p in range(NPLAYERS):
            self.players.append(Human())
    def removeCards(self):
        pass
    def shuffle(self):
        self.decks=getShuffledDeck()
    def dealerDecision(self):
        dealerCards=self.cDealer.cards
        bust=False
        dval=valHand(dealerCards)
        self.cDealer.handval=dval
        print("dealer: %s"%(strHand(dealerCards)))
#        print("dealer: %d"%(valHand(dealerCards)))
        if(dval==22):
            print("dealer: %s"%(strHand(dealerCards)))
            print("blackjack")
            return 22
        while((dval<17) or (soft17rule and isSoft17(dealerCards))):
            time.sleep(DEALERDELAY)
            dealerCards.append(self.decks.pop())
            dval=valHand(dealerCards)
            print("*dealer hits")
            print("dealer: %s"%(strHand(dealerCards)))
#            print("dealer: %d"%(valHand(dealerCards)))
            bust=checkBust(dealerCards)
            if(bust):
                print("*dealer busts")
                return 0
        time.sleep(DEALERDELAY)
        print("*dealer stands")
        return valHand(dealerCards)
    def playerDecision(self):
        return self.players[0].decide(self.decks)
    def deal(self):
        dealerCards=self.cDealer.cards
        self.nGames+=1
        for i in range(NPLAYERS):
            self.players[i].hands=[Hand()]
        for j in range(2):
            for i in range(NPLAYERS):
                self.players[i].hands[0].cards.append(self.decks.pop())
            dealerCards.append(self.decks.pop())
    def valLook(self):
        dealerCards=self.cDealer.cards
        print("game:%d"%(self.nGames))
        print("dealer: %d"%(valHand(dealerCards)))
        for i in range(NPLAYERS):
            for hand in self.players[i]:
                cards=hand.cards
                print("player%d:%d"%(i,valHand(cards)))
    def omniLook(self):
        playerCards=self.players[0][0].cards
        dealerCards=self.cDealer.cards
        print("game:%d"%(self.nGames))
        print("dealer: %s"%(strHand(dealerCards)))
        print("player0:%s"%(strHand(playerCards)))
        for i in range(1,NPLAYERS):
            print("player%d:%s"%(i,strHand(self.players[i][0].cards)))
    def look(self):
        playerCards=self.players[0].hands[0].cards
        dealerCards=self.cDealer.cards
        print("game:%d"%(self.nGames))
        print("dealer: [?? %s]"%(strCard(dealerCards[1])))
#        print("player0:%s"%(strHand(playerCards)))
#        for i in range(1,NPLAYERS):
#            print("player%d:[?? ??]"%(i))

#testFunction()
t=Table()
bankroll=STARTINGBANKROLL
betsize=MINBET
while True:
    print()
    t.deal()
    t.look()
    #t.omniLook()
    #t.valLook()
    result=t.playerDecision()
    if(result=='q'):      #quit
        break
    dval=t.dealerDecision()
    i=1
    for hand in t.players[0].hands:
        pval=hand.handval
        print('hand %d: %d %d'%(i,pval,dval))
        i+=1
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
