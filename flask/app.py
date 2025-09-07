from flask import Flask,render_template,request,session,redirect,url_for
import random

app=Flask(__name__)


CARD_LIST = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

#カード配布関数
def draw_card():
    hand=[]
    for _ in range(2):
        hand.append(random.choice(CARD_LIST))
    return hand

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

#勝敗判定関数
def judge_winner(p_score,b_score):
    if p_score>b_score:
        return "プレイヤー"
    elif p_score==b_score:
        return "タイ"
    else:
        return "バンカー"  


<<<<<<< HEAD


@app.route("/",methods=["GET","POST"])
def index():
    if request.method=="GET":
        return render_template("index.html")
=======
#選択の設定
def choice_env(choice):
    if choice=="player":
        return "プレイヤー"
    elif choice=="banker":
        return "バンカー"
    elif choice=="tie":
        return "タイ"

#チップの更新
def update_chips(chips,choice,win,amount):
    #結果が引き分けだった時
    if win=="タイ":
        if choice == "タイ":
            chips+=amount*8
        else:
            pass

    #予想が当たった時
    elif choice == win:
        if choice=="プレイヤー":
            chips+=amount
        else:
            chips+=int(amount*0.95)
    
    #予想が外れた時
    else:
        chips-=amount
    
    return chips




app.secret_key="バカラアプリ"

@app.route("/",methods=["GET","POST"])
def index():
    if "chips" not in session:
        session["chips"]=1000
    
    
    chips=session["chips"]

    if chips==0:
        session["chips"]=1000
        return render_template("gameover.html")
>>>>>>> temp

    if request.method=="POST":
        bet=int(request.form.get("bet"))
        bet_choice=request.form.get("bet_choice")
        if bet<=chips:

            player_hand=draw_card()
            banker_hand=draw_card()

            player_score=total_score(player_hand)
            banker_score=total_score(banker_hand)

            winner=judge_winner(player_score,banker_score)

            session["chips"]=update_chips(chips,choice_env(bet_choice),winner,bet)


<<<<<<< HEAD
        return render_template("result.html",
                               player_hand=player_hand,
                               banker_hand=banker_hand,
                               player_score=player_score,
                               banker_score=banker_score,
                               winner=winner
                               )

=======
            return render_template("result.html",
                                player_hand=player_hand,
                                banker_hand=banker_hand,
                                player_score=player_score,
                                banker_score=banker_score,
                                winner=winner,
                                bet=bet
                                )
        
>>>>>>> temp

    return render_template("index.html",chips=chips)

if __name__=="__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)