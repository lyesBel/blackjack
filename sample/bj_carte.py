CARDS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
#import numpy as np
from copy import copy,deepcopy
class card():
    
    def __init__(self,name : str):
        assert name in  CARDS
        self.name = name
        if name.isnumeric():
            if name =='1':
                self.values = [1,11]
            else: 
                self.values = [int(name)]
        else:
            self.values = [10]
    def __str__(self):
        return self.name +'\n'+str(self.values)
    @staticmethod
    def card_values(name : str):
        a_card = card(name)
        return a_card.values
            
            
class cards():
    def __init__(self):
        self.cards = []
        self.values = {0}
        self.score = 0
        self.nb_cards = 0
    def _add(self,new_card : card):
        self.cards.append(new_card)
        self.nb_cards+=1
        self.values = { s1 + s2 for s1 in self.values for s2 in new_card.values if s1+s2 <=21}
        if self.values:
            self.score = max(self.values)
        else:
            self.score =  0
            
    def add(self,name:str):
        new_card = card(name)
        self._add(new_card)
    def __str__(self):
        return str([str(card) for card in self.cards])+'\n'+str(self.values) + f' score : {self.score}'
    def is_burst(self):
        if not self.values:
            return True
        return min(self.values)>21
    def is_blackjack(self):
        return self.nb_cards == 2 and self.score == 21
    def is_dealer_stop(self):
        return self.score>=17
    
    def is_player_stop(self):
        return self.score in (21,0)

class game():
    def __init__(self):
        self.dealer = cards()
        self.dealer_scores = [0]*22
        self.player = cards()
        self.player_scores_1_card = [0.]*22
        self.player_scores_2_card = [0.]*22
    def __str__(self):
        # return 'Dealer '+str(self.dealer)+'\n player : '+str(self.player)+'\n'\
        # +'probas dealer '+str([f"{i} : {self.dealer_scores[i]*100}" for i in range(22)])\
        # +f'\n Stand win {round(self.proba_stand_win()*100)}%'\
        # +f'\n Hit win 1 card {round(self.get_proba_win_hit_1()*100)}%'\
        # +f'  Burst risque 1 card  {round(self.get_proba_burst_1()*100)}%'\
        # +f'\n Hit win <=2 cards {round(self.get_proba_win_hit_2()*100)}%'\
        # +f'  Burst risque <=2 cards  {round(self.get_proba_burst_2()*100)}%'
        
        return f'\n Stand win {round(self.proba_stand_win()*100)}%'\
        +f'\n Hit win 1 card {round(self.get_proba_win_hit_1()*100)}%'\
        +f'  Burst risque 1 card  {round(self.get_proba_burst_1()*100)}%'\
        +f'\n Hit win <=2 cards {round(self.get_proba_win_hit_2()*100)}%'\
        +f'  Burst risque <=2 cards  {round(self.get_proba_burst_2()*100)}%'
        
    def add_dealer(self,name:str):
        self.dealer.add(name)    
        
    def add_player(self,name:str):
        self.player.add(name)
    
   
    def generate_dealer(self):
        self.add_card_dealer_rec(self.dealer)
        
    def add_card_dealer_rec(self,dealer : cards):
        if dealer.is_dealer_stop() or  dealer.is_burst():
            self.dealer_scores[dealer.score] += ((1/13)**(dealer.nb_cards-1))
        else:
            for _card in CARDS:
                new_dealer = deepcopy(dealer)
                new_dealer.add(_card)
                self.add_card_dealer_rec(new_dealer)
    def generate_player(self):
        self.player_scores_1_card = [0.]*22
        self.player_scores_2_card  = [0.]*22
        l_hands = []
        for _card in CARDS:
            new_player = deepcopy(self.player)
            new_player.add(_card)
            self.player_scores_1_card[new_player.score] += 1/13
            if not new_player.is_player_stop():
                l_hands.append(deepcopy(new_player))
        
        while l_hands:
            current_player =l_hands.pop(0)
            for _card in CARDS:
                new_player = deepcopy(current_player)
                prev_player_values = new_player.values
                new_player.add(_card)
                if new_player.is_burst():
                    real_player_value = current_player.score
                else:
                    real_player_value=0
                    for card_value in card.card_values(_card):
                        for player_value in prev_player_values:
                            if card_value + player_value == new_player.score :
                                real_player_value=player_value
                                break 
                        if real_player_value != 0:
                            break 
                self.player_scores_2_card[new_player.score]+=  (1/13)**2
        #self.player_scores_2_card[0]+=self.player_scores_1_card[0]
        #self.player_scores_2_card[21]+=self.player_scores_1_card[21]
        
              
    def proba_leq_score(self,score,b_with_burst = True):
        return sum(self.dealer_scores[:score+1]) - (self.dealer_scores[0] if not b_with_burst else 0)   
        
    def get_proba_burst_1(self):
        return  self.player_scores_1_card[0]
    
    def get_proba_burst_2(self):
        return  self.player_scores_2_card[0]+self.player_scores_1_card[0]
    
    def get_proba_win_hit_1(self):
        return (1- self.player_scores_1_card[0])  * sum([ self.player_scores_1_card[j]*self.proba_leq_score(j,True)  for j in range(1,22)])
    
    def get_proba_win_hit_2(self):
        return (1- self.player_scores_1_card[0]- self.player_scores_1_card[21]) * (1-self.player_scores_2_card[0])  * sum([ (self.player_scores_2_card[j])*self.proba_leq_score(j,True)  for j in range(1,22)])
    
    def proba_stand_win(self):
        return self.proba_leq_score(self.player.score)
        
    def play_hit(self,card):
        self.add_player(card)
        self.generate_player()
        
        print(my_game)
    
    
if __name__ =='__main__':
    # my_card = card('Q')
    # print(my_card)
    # hand = cards()
    # hand.add('1')
    # print(hand)
    # hand.add('1')
    # print(hand)
    # hand.add('9')
    # print(hand)
    
    
    # hand.add('1')
    # print(hand)
    # play = input("Le jeu ?")
    # l_play = [k if k!='0' else 'J' for k in play.split(' ')]
    # my_game = game()
    
    # my_game.add_player(l_play[0] )
    # my_game.add_player(l_play[1])
    # # my_game.add_player('6')
    
    # my_game.add_dealer(l_play[2])
    # my_game.generate_dealer()
    # my_game.generate_player()
    
    
    # print(my_game)
    #print(my_game.proba_player_win())
    probas = [0]*22
    for card1 in CARDS:
        for card2 in CARDS:
            my_game = game()
            my_game.add_dealer(card1)
            my_game.add_dealer(card2)
            my_game.generate_dealer()
            for i in range(len(my_game.dealer_scores)):
                probas[i]+=my_game.dealer_scores[i]*((1/13))
                
            
    
    