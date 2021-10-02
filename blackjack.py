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

CHECKSTRATEGY=False
CHECKSTRATEGY=True

TRAIN=True

JUSTCOMPUTER=False
#JUSTCOMPUTER=True

DEBUG=False

def dbg(x):
    if(DEBUG):
        print(x)

class Deck(object):
    def __init__(self):
        self.shuffle()
    def shuffle(self):
        print('*shuffling')
        self.deckCards=sample(range(52*NDECKS),52*NDECKS)
        self.hilocount=0
        self.prevhilocount=0    #count from previous hand
    def dealCard(self):
        if(len(self.deckCards)==0):
            self.shuffle()
        card=self.deckCards.pop()
        self.updatehilo(card)
        return card
    def updatehilo(self,c):
        cf=strFace(c)
        if cf in ['A','K','Q','J','T']:
            self.hilocount-=1
        elif valCard(c) <= 6:
            self.hilocount+=1
        #print('true hl count:'+str(self.hilocount))
    def gameFinished(self):
        self.prevhilocount=self.hilocount

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
    def print(self,s):
        print(self.pid+' '+s)
    def updatehilo(self,c):
        cf=strFace(c)
        if cf in ['A','K','Q','J','T']:
            self.hilocount-=1
        elif valCard(c) <= 6:
            self.hilocount+=1
    def updatehilocount(self,h,dc):
        self.hilocount=t.decks.prevhilocount
        self.updatehilo(dc)
        for c in h:
            self.updatehilo(c)
        print('prev hl count:'+str(t.decks.prevhilocount))
        print('hl count:'+str(self.hilocount))
    def decide(self,h,dc):
        print("*dealer*: [?? %s]"%(strCard(dc)))
        print("%s:%s"%(self.pid,strHand(h)))
        #print("value:%d"%(valHand(h)))
        self.updatehilocount(h,dc)

class BasicStrategy(Player):
    def makeWager(self):
        self.hands=[Hand()]
        self.hands[0].wager=MINBET
    def decide(self,h,dc):
        super().decide(h,dc)
        return basicStrategy(h,dc)

class Stays(Player):
    def makeWager(self):
        self.hands=[Hand()]
        self.hands[0].wager=MINBET
    def decide(self,h,dc):
        return 'n'

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
    def decide(self,h,dc):
        super().decide(h,dc)
        print("hit? (y/[n]/d/s/q)")
        decision=input()
        if(decision=='q'):
            exit(1)
        if(CHECKSTRATEGY):
            if decision not in ['y','d','s']:
                decision='n'
            ans=basicStrategy(h,dc)
            if(TRAIN):
                if(decision!=ans):
                    print('**%s** chose %s, basic strategy would have chosen %s'%(self.pid,decision,ans))
                else:
                    print('**%s** played correctly according to basic strategy'%(self.pid))
        return decision

def valCard(c):
    v=int(c%13)
    if(v<8):
        return v+2
    if(v==12):
        return 1
    return 10
def basicValHand(h):
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
    return val
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
def basicStrategy(phand,dupcard):
    dupval=valCard(dupcard)
    handval=valHand(phand)
    basichandval=basicValHand(phand)
    if(hasAce(phand) and (basichandval+10)<=21):
        othercard=phand[0]
        if(strFace(othercard)=='A'):
            othercard=phand[1]
        dbg('has ace and '+strFace(othercard))
        if(dupval==1):  #ace
            dupval=11
        if(handval==19):
            if(dupval==6):
                return 'd'
            else:
                return 'n'
        elif(handval==18):
            if(dupval<=6):
                return 'd'
            elif(dupval<=8):
                return 'n'
            else:
                return 'y'
        elif(handval==17):
            if(dupval==2):
                return 'y'
            elif(dupval<=6):
                return 'd'
            else:
                return 'y'
        elif((handval==16)or(handval==15)):
            if(dupval<=3):
                return 'y'
            elif(dupval<=6):
                return 'd'
            else:
                return 'y'
        elif((handval==14)or(handval==13)):
            if(dupval<=4):
                return 'y'
            elif(dupval<=6):
                return 'd'
            else:
                return 'y'
        else:
            return 'n'
    elif(hasPair(phand)):
        face=strFace(phand[0])
        dbg('pair of '+face+'s')
        if(face=='A'):
            return 's'
        elif(face in ['T','J','Q','K']):
            return 'n'
        elif(face=='9'):
            if(dupval==7):
                return 'n'
            elif(dupval>=10):
                return 'n'
            else:
                return 's'
        elif(face=='8'):
            return 's'
        elif(face=='7'):
            if(dupval<=7):
                return 's'
            else:
                return 'y'
        elif(face=='6'):
            if(dupval<=6):
                return 's'
            else:
                return 'y'
        elif(face=='5'):
            if(dupval<=9):
                return 'd'
            else:
                return 'y'
        elif(face=='4'):
            if(dupval in [5,6]):
                return 's'
            else:
                return 'y'
        elif(face in ['3','2']):
            if(dupval<=7):
                return 's'
            else:
                return 'y'
    else:
        dbg('regular hand without an ace')
        if(handval>=17):
            return 'n'
        elif(handval<=8):
            return 'y'
        elif(handval>=13):
            if(dupval<=6):
                return 'n'
            else:
                return 'y'
        elif(handval==12):
            if(dupval<=3):
                return 'y'
            elif(dupval<=6):
                return 'n'
            else:
                return 'y'
        elif(handval==11):
            return 'd'
        elif(handval==10):
            if(dupval<=9):
                return 'd'
            else:
                return 'y'
        elif(handval==9):
            if(dupval==2):
                return 'y'
            elif(dupval<=6):
                return 'd'
            else:
                return 'y'
        else:
            return 'y'
def hasPair(h):
    return sameFace(h)
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
    t.decks.deckCards=[4,50,51,22,23,0,11,38,13,12,25]
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
        pid='*'+pid+'*'
        if not JUSTCOMPUTER:
            self.players.append(Human(pid))
        for p in range(1,NPLAYERS):
            i+=1
            pid='player'+str(i)
            pid='*'+pid+'*'
            #self.players.append(Stays(pid))
            self.players.append(BasicStrategy(pid))
    def makeWagers(self):
        for p in self.players:
            if(p.bankroll<=0):
                p.print('lost at game %d'%self.nGames)
                self.players.remove(p)
        if len(self.players)==0:
            exit(0)
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
        #print("dealer: %s"%(strHand(dealerCards)))
#        print("dealer: %d"%(valHand(dealerCards)))
        if(dval==22):
            print("dealer: %s"%(strHand(dealerCards)))
            print("blackjack")
            return 22
        while((dval<17) or (soft17rule and isSoft17(dealerCards))):
            time.sleep(DEALERDELAY)
            dealerCards.append(self.decks.dealCard())
            dval=valHand(dealerCards)
            print("*dealer* hits")
            print("dealer: %s"%(strHand(dealerCards)))
#            print("dealer: %d"%(valHand(dealerCards)))
            bust=checkBust(dealerCards)
            if(bust):
                print("*dealer* busts")
                return 0
        time.sleep(DEALERDELAY)
        print("*dealer* stands")
        return valHand(dealerCards)
    def playerDecisions(self):
        for player in self.players:
            self.playerDecision(player)
    def playerDecision(self,player):
        decks=self.decks
        playerHands=player.hands
        for hand in playerHands:
            h=hand.cards
            recentVal=valHand(h)
            hand.handval=recentVal
            if(recentVal==22):
                player.print("%s"%(strHand(h)))
                player.print("value:%d"%(valHand(h)))
                if(hand.hasSplit):
                    hand.handval=21
                else:
                    player.print("blackjack")
                continue
            choice='y'
            while(choice=='y'):
                if(len(h)==1):
                    h.append(decks.dealCard())
                    continue
                if(hand.hasDoubled):
                    print("%s:%s"%(player.pid,strHand(h)))
                    break
                    
                choice=player.decide(h,self.cDealer.cards[1])
                if(choice=='y'):
                    h.append(decks.dealCard())
                    bust=checkBust(h)
                    if(bust):
                        player.print("bust")
                        break
                elif(choice=='d'):
                    if(len(h)==2):
                        player.print("doubling down")
                        newWager=hand.wager*2
                        player.print("wager: %d -> %d"%(hand.wager,newWager))
                        hand.hasDoubled=True
                        h.append(decks.dealCard())
                        print("%s:%s"%(player.pid,strHand(h)))
                        bust=checkBust(h)
                        if(bust):
                            player.print("bust")
                        break
                    else:
                        player.print("cannot double down after hitting or doubling down.  standing instead")
                elif(choice=='s'):
                    if(sameFace(h) and (len(h)==2)):
                        player.print("split")
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
                        newHand1.cards.append(decks.dealCard())
                        newHand2.cards.append(decks.dealCard())
                        playerHands.append(newHand1)
                        playerHands.append(newHand2)
                        return self.playerDecision(player)
                    else:
                        player.print('can only split exactly two cards with the same face')

                elif(choice=='q'):
                    exit(1)
                #elif(choice!='n'):
                #    player.print('invalid command')
            recentVal=valHand(h)
            hand.handval=recentVal
    def dealHands(self):
        self.cDealer=Hand()
        dealerCards=self.cDealer.cards
        self.nGames+=1
        #for i in range(NPLAYERS):
        #    self.players[i].hands=[Hand()]
        for j in range(2):
            for player in self.players:
                player.hands[0].cards.append(self.decks.dealCard())
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
        print("game:%d"%(self.nGames))
    def calculateWinners(self):
        dval=self.dealerDecision()
        print("*dealer*  %s"%(strHand(self.cDealer.cards)))
        for player in reversed(self.players):
            handnum=1
            for hand in player.hands:
                if hand.hasDoubled:
                    wager=2*hand.wager
                else:
                    wager=hand.wager
                player.print("%s"%(strHand(hand.cards)))
                #pval=valHand(hand.cards)
                pval=hand.handval
                player.print('wager: %d'%(wager))
                player.print('hand %d: pval:%d dval:%d'%(handnum,pval,dval))
                handnum+=1
                if(pval==0):
                    player.print('bust')
                    player.print('lost')
                    player.bankroll-=wager
                elif(pval==dval):
                    player.print('tie')
                elif(pval>dval):
                    player.print('won')
                    if(pval==22 and (not hand.hasSplit)):
                        player.bankroll+=BLACKJACKMODIFIER*wager
                    else:
                        player.bankroll+=wager
                else:
                    player.print('lost')
                    player.bankroll-=wager
                player.print('bankroll:%d'%(player.bankroll))

UPDATEFREQ=1000
UPDATEDELAY=5
print('computer only? (y/[n])')
dec=input()
if(dec=='y'):
    JUSTCOMPUTER=True
    DEALERDELAY=0

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
    t.playerDecisions()
    t.calculateWinners()
    t.decks.gameFinished()
    if(JUSTCOMPUTER):
        if((t.nGames%UPDATEFREQ)==0):
            #for player in t.players:
            #    player.print('bankroll:%d'%(player.bankroll))
            time.sleep(UPDATEDELAY)
