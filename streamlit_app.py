import streamlit as st
import random

# 初期資金
if "money" not in st.session_state:
    st.session_state.money = 1000

# カードのリスト
CARD_LIST = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

# カードの点数変換
def card_value(card):
    if card == "A":
        return 1
    elif card in ["10", "J", "Q", "K"]:
        return 0
    else:
        return int(card)

# 合計スコア計算
def total_score(cards):
    return sum(card_value(card) for card in cards) % 10

# 勝者判定
def judge(player_score, banker_score):
    if player_score > banker_score:
        return "Player"
    elif player_score < banker_score:
        return "Banker"
    else:
        return "Tie"

# ゲーム処理
def play_baccarat(bet_side, bet_amount):
    player_cards = [random.choice(CARD_LIST) for _ in range(2)]
    banker_cards = [random.choice(CARD_LIST) for _ in range(2)]

    p_score = total_score(player_cards)
    b_score = total_score(banker_cards)

    result = judge(p_score, b_score)
    payout = 0

    if result == bet_side:
        if result == "Player":
            payout = bet_amount * 2
        elif result == "Banker":
            payout = int(bet_amount * 1.95)  # 通常バンカー勝ちは5%控除
        elif result == "Tie":
            payout = bet_amount * 8
    else:
        payout = 0

    st.session_state.money += (payout - bet_amount)

    return {
        "player_cards": player_cards,
        "banker_cards": banker_cards,
        "player_score": p_score,
        "banker_score": b_score,
        "result": result,
        "payout": payout
    }

# Streamlit UI
st.markdown(
    """
    <a href="//af.moshimo.com/af/c/click?a_id=5158720&p_id=3026&pc_id=6979&pl_id=38504" rel="nofollow" referrerpolicy="no-referrer-when-downgrade" attributionsrc><img src="//image.moshimo.com/af-img/2440/000000038504.jpg" width="700" height="160" style="border:none;"></a><img src="//i.moshimo.com/af/i/impression?a_id=5158720&p_id=3026&pc_id=6979&pl_id=38504" width="1" height="1" style="border:none;" loading="lazy">
    """,
    unsafe_allow_html=True
)
st.markdown("### 🎲 バカラゲームアプリ")
st.markdown("このアプリはPythonとStreamlitで作成したバカラ体験ゲームです。")



st.write(f"💰 現在の所持金: {st.session_state.money} チップ")

if st.session_state.money <= 0:
    st.error("所持金がゼロです。リロードして再スタートしてください。")
    st.stop()

bet_amount = st.number_input("🎲 賭けチップ数", min_value=1, max_value=st.session_state.money, value=100, step=10)
bet_side = st.radio("🧠 賭け先を選んでください", ["Player", "Banker", "Tie"])

if st.button("💥 ゲームスタート！"):
    result = play_baccarat(bet_side, bet_amount)

    st.subheader("🎴 勝負結果")
    st.write(f"**プレイヤー**: {result['player_cards']} → {result['player_score']}点")
    st.write(f"**バンカー**: {result['banker_cards']} → {result['banker_score']}点")
    st.write(f"**勝者**: {result['result']}")
    st.success(f"💵 配当: {result['payout']} チップ")
    st.write(f"💰 新しい所持金: {st.session_state.money} チップ")




st.markdown(
    """
    <a href="//af.moshimo.com/af/c/click?a_id=5158607&p_id=7066&pc_id=20221&pl_id=89317" rel="nofollow" referrerpolicy="no-referrer-when-downgrade" attributionsrc><img src="//image.moshimo.com/af-img/6831/000000089317.jpg" width="468" height="60" style="border:none;"></a><img src="//i.moshimo.com/af/i/impression?a_id=5158607&p_id=7066&pc_id=20221&pl_id=89317" width="1" height="1" style="border:none;" loading="lazy">
    """,
    unsafe_allow_html=True
)