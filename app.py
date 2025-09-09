from flask import Flask,render_template,request,session,redirect,url_for
import random
from flask_sqlalchemy import SQLAlchemy

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


#データベース設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baccarat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False,default="guest")
    chips=db.Column(db.Integer,default=1000)

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bet_choice=db.Column(db.String(50), nullable=False)
    bet_amount=db.Column(db.Integer, nullable=False)
    winner=db.Column(db.String(50), nullable=False)
    chips_after=db.Column(db.Integer, nullable=False)
    player_hand=db.Column(db.String(50), nullable=False)
    banker_hand=db.Column(db.String(50), nullable=False)
    player_score=db.Column(db.Integer, nullable=False)
    banker_score=db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()


app.secret_key="バカラアプリ"


@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        name=request.form.get("username")
        user=User.query.filter_by(name=name).first()
        if not user:
            user = User(name=name, chips=1000)
            db.session.add(user)
            db.session.commit()
        session["user_id"]=user.id
        return redirect("/")
    return render_template("login.html")
    


@app.route("/",methods=["GET","POST"])
def index():
    user_id=session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))
    
    user=User.query.get(user_id)
    if not user:
        return redirect(url_for("login"))

    if user.chips==0:
        return render_template("gameover.html")


    if request.method=="POST":
        bet=int(request.form.get("bet"))
        bet_choice=request.form.get("bet_choice")
        if bet<=user.chips:

            player_hand=draw_card()
            banker_hand=draw_card()

            player_score=total_score(player_hand)
            banker_score=total_score(banker_hand)

            winner=judge_winner(player_score,banker_score)

            user.chips=update_chips(user.chips,choice_env(bet_choice),winner,bet)
            db.session.commit()

            history = History(
                user_id=user.id,
                bet_choice=bet_choice,
                bet_amount=bet,
                winner=winner,
                chips_after=user.chips,
                player_hand=", ".join(player_hand),
                banker_hand=", ".join(banker_hand),
                player_score=player_score,
                banker_score=banker_score
            )
            db.session.add(history)
            db.session.commit()



  
            return render_template("result.html",
                                player_hand=player_hand,
                                banker_hand=banker_hand,
                                player_score=player_score,
                                banker_score=banker_score,
                                winner=winner,
                                bet=bet
                                )
        

    return render_template("index.html",user=user,chips=user.chips)

@app.route("/reset")
def reset():
    user_id=session.get("user_id")
    user=User.query.get(user_id)
    user.chips=1000
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/history/<int:user_id>")
def history(user_id):
    user=User.query.get(user_id)
    histories=History.query.filter_by(user_id=user_id).all()
    return render_template("history.html",user=user,histories=histories)

if __name__=="__main__":
    app.run(debug=True)