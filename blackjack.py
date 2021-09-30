from random import *
import time
import copy

soft17rule=True         #dealer hits on soft 17 (ace and 6)
seed(time.time())
MINBET=10
NDECKS=1
NPLAYERS=1
NPLAYERS=2
STARTINGBANKROLL=100*MINBET
DEALERDELAY=1
BLACKJACKMODIFIER=2 #2 for blackjack paying 2 to 1

class Deck(object):
    def __init__(self):
        self.shuffle()
    def shuffle(self):
        print('*shuffling')
        self.deckCards=sample(range(52*NDECKS),52*NDECKS)
    def dealCard(self):
        if(len(self.deckCards)==0):
            self.shuffle()
        return self.deckCards.pop()

class Hand(object):
    def __init__(self):
        self.cards=[]
        self.wager=MINBET
        self.handval=0
        self.hasDoubled=False
        self.hasSplit=False

class Player(object):
    def __init__(self,pid):
        self.pid=pid
        self.hands=[Hand()]
        self.bankroll=STARTINGBANKROLL

class Stays(Player):
    def makeWager(self):
        self.hands=[Hand()]
        self.hands[0].wager=MINBET

class Human(Player):
    def __init__(self,pid):
        super().__init__(pid)
    def makeWager(self):
        previousWager=self.hands[0].wager
        self.hands=[Hand()]
        self.hands[0].wager=previousWager
        print('change wager? (y/[n]/q)')
        inp=input()
        if(inp=='y'):
            print('wager amount?')
            inp=input()
            if(inp.isdigit()):
                self.hands[0].wager=int(inp)
                return
            else:
                print('wager must be a number')
        elif(inp=='q'):
            exit(1)
        #self.hands[0].wager=MINBET
    def decide(self,decks):
        playerHands=self.hands
        for hand in playerHands:
            h=hand.cards
            recentVal=valHand(h)
            hand.handval=recentVal
            if(recentVal==22):
                print("%s:%s"%(self.pid,strHand(h)))
                print("value:%d"%(valHand(h)))
                if(not hand.hasSplit):
                    print("*blackjack")
                return
            choice='?'
            while(choice!='n'):
                if(len(h)==1):
                    h.append(decks.dealCard())
                    continue
                if(hand.hasDoubled):
                    break
                    
                print("%s:%s"%(self.pid,strHand(h)))
                print("value:%d"%(valHand(h)))
                print("hit? (y/n/d/s/q)")
                choice=input()
                if(choice=='y'):
                    h.append(decks.dealCard())
                    bust=checkBust(h)
                    if(bust):
                        print("*bust")
                        break
                elif(choice=='d'):
                    print("doubling down")
                    newWager=hand.wager*2
                    print("wager: %d -> %d"%(hand.wager,newWager))
                    hand.wager=newWager
                    hand.hasDoubled=True
                    h.append(decks.dealCard())
                    bust=checkBust(h)
                    if(bust):
                        print("*bust")
                    break
                elif(choice=='s'):
                    if(sameFace(h) and (len(h)==2)):
                        print("split")
                        newHand1=Hand()
                        newHand2=Hand()
                        newHand1.hasSplit=True
                        newHand2.hasSplit=True
                        newHand1.cards=[copy.deepcopy(h[0])]
                        newHand2.cards=[copy.deepcopy(h[1])]
                        newHand1.handval=0
                        newHand2.handval=0
                        newHand1.wager=hand.wager
                        newHand2.wager=hand.wager
                        playerHands.remove(hand)
                        playerHands.append(newHand1)
                        playerHands.append(newHand2)
                        return self.decide(decks)
                    else:
                        print('can only split exactly two cards with the same face')

                elif(choice=='q'):
                    exit(1)
                elif(choice!='n'):
                    print('invalid command')

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

def testFunction(t):
    t.decks.deckCards=[0,11,24,13,12,25]
    t.decks.deckCards=[0,11,38,13,12,25]

def checkBust(h):
    if(valHand(h)==0):
        return True
    return False

class Table():
    def __init__(self):
        self.nGames=0
        self.decks=Deck()
        self.cDealer=Hand()
        self.players=[]
        i=0
        pid='player'+str(i)
        self.players.append(Human(pid))
        for p in range(1,NPLAYERS):
            i+=1
            pid='player'+str(i)
            self.players.append(Stays(pid))
    def makeWagers(self):
        for p in self.players:
            p.makeWager()
    def removeCards(self):
        pass
    def shuffle(self):
        self.decks.shuffle()
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
            dealerCards.append(self.decks.dealCard())
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
        self.players[0].decide(self.decks)
    def dealHands(self):
        self.cDealer=Hand()
        dealerCards=self.cDealer.cards
        self.nGames+=1
        #for i in range(NPLAYERS):
        #    self.players[i].hands=[Hand()]
        for j in range(2):
            for i in range(NPLAYERS):
                self.players[i].hands[0].cards.append(self.decks.dealCard())
            dealerCards.append(self.decks.dealCard())
    def valLook(self):
        dealerCards=self.cDealer.cards
        print("game:%d"%(self.nGames))
        print("dealer: %d"%(valHand(dealerCards)))
        for i in range(NPLAYERS):
            for hand in self.players[i]:
                cards=hand.cards
                print("player%d:%d"%(i,valHand(cards)))
    def omniLook(self):
        dealerCards=self.cDealer.cards
        print("game:%d"%(self.nGames))
        print("dealer: %s"%(strHand(dealerCards)))
        for player in self.players:
            print("%s:%s"%(player.pid,strHand(player.hands[0].cards)))
    def look(self):
        dealerCards=self.cDealer.cards
        print("game:%d"%(self.nGames))
        print("dealer: [?? %s]"%(strCard(dealerCards[1])))
    def calculateWinners(self):
        dval=self.dealerDecision()
        for player in reversed(self.players):
            handnum=1
            for hand in player.hands:
                print("%s:%s"%(player.pid,strHand(hand.cards)))
                pval=valHand(hand.cards)
                print('%s wager: %d'%(player.pid,hand.wager))
                print('%s hand %d: %d %d'%(player.pid,handnum,pval,dval))
                handnum+=1
                if(pval==0):
                    print('*bust')
                    print('*%s lost'%player.pid)
                    player.bankroll-=hand.wager
                elif(pval==dval):
                    print('*tie')
                elif(pval>dval):
                    print('*%s won'%player.pid)
                    if(pval==22 and (not hand.hasSplit)):
                        player.bankroll+=BLACKJACKMODIFIER*hand.wager
                    else:
                        player.bankroll+=hand.wager
                else:
                    print('*%s lost'%player.pid)
                    player.bankroll-=hand.wager
                print('*%s bankroll:%d'%(player.pid,player.bankroll))

t=Table()
#testFunction(t)
betsize=MINBET
while True:
    print()
    t.makeWagers()
    t.dealHands()
    t.look()
    #t.omniLook()
    #t.valLook()
    t.playerDecision()
    t.calculateWinners()
