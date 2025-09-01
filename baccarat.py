import random

CARD_LIST=["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
        
#引いたカードの数字を決める関数
def card_env(card):
    if card=="A":
        return 1
    elif card in ["10","J","Q","K"]:
        return 0
    else:
        return int(card)

#引いたカードの合計を計算する関数
def total_score(cards):
    total = sum(card_env(card) for card in cards)
    return total % 10


#勝者を決める関数
def judge_winner(p_score,b_score):
    if p_score>b_score:
        return "プレイヤー"
    elif p_score==b_score:
        return "タイ"
    else:
        return "バンカー"
    


class Baccarat:
    def __init__(self):
        self.player_hand=[]
        self.banker_hand=[]
        

    #カードを引く関数
    def draw_card(self):      
        #プレイヤーのハンド  
        for _ in range(2):
            self.player_hand.append(random.choice(CARD_LIST))
        
        #バンカーのハンド
        for _ in range(2):
            self.banker_hand.append(random.choice(CARD_LIST))

    def play(self):
        self.draw_card()
        player_score=total_score(self.player_hand)
        banker_score=total_score(self.banker_hand)
        print(f"プレイヤー : {self.player_hand} → 点数{player_score}")
        print(f"バンカー : {self.banker_hand} → 点数{banker_score}")

        self.winner=judge_winner(player_score,banker_score)
        print(f"勝者: {self.winner}")
    
    def get_winner(self):
        return self.winner
        

class Player:
    def __init__(self):
        self.chips=1000

    def choice_env(self,choice):
        if choice=="player":
            return "プレイヤー"
        elif choice=="banker":
            return "バンカー"
        elif choice=="tie":
            return "タイ"
        
    
    def update_chips(self,choice,win,amount):

        #結果が引き分けだった時
        if win=="タイ":
            if choice == "タイ":
                self.chips+=amount*8
            else:
                pass

        #予想が当たった時
        elif choice == win:
            if choice=="プレイヤー":
                self.chips+=amount
            else:
                self.chips+=int(amount*0.95)
        
        #予想が外れた時
        else:
            self.chips-=amount

    def player_bet(self):
        print(f"現在のチップ : {self.chips}")
        while True:
            self.choice=input("どこに賭けますか( player / banker / tie ) : ")
            if self.choice in ["player","banker","tie"]:
                while True:

                    self.amount=int(input("いくら賭けますか : "))
                    if self.amount>self.chips:
                        print("所持金以内のベットしかできません")
                        
                    else:
                        break
                
                break

            print("もう一度賭ける方を選択してください")

    def start_game(self,winner):
        self.update_chips(self.choice_env(self.choice),winner,self.amount)
        print(f"現在のチップ : {self.chips}")



def main():
    you=Player()

    while True:
        game=Baccarat()
        you.player_bet()
        game.play()
        you.start_game(game.get_winner())

        if you.chips<=0:
            break    

        onemore=input("もう一度プレイしますか [y/n] : ")

        if onemore=="n":
            print(f"所持金 : {you.chips}")
            break


    
    
    
if __name__=="__main__":
    main()