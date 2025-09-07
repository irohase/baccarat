from flask import Flask,render_template,request,session
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

app.secret_key="バカラアプリ"

@app.route("/",methods=["GET","POST"])
def index():

    session["chips"]=1000
    current=session["chips"]

    if "chips" not in session:
        session["chips"]=1000
        current=session["chips"]

    if request.method=="POST":

        player_hand=draw_card()
        banker_hand=draw_card()

        player_score=total_score(player_hand)
        banker_score=total_score(banker_hand)

        winner=judge_winner(player_score,banker_score)


        return render_template("result.html",
                               player_hand=player_hand,
                               banker_hand=banker_hand,
                               player_score=player_score,
                               banker_score=banker_score,
                               winner=winner
                               )
    return render_template("index.html",chips=current)


if __name__=="__main__":
    app.run(debug=True)