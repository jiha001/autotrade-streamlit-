import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

st.set_page_config(page_title="Binance AutoTrade Dashboard", layout="wide")

STATE_FILE = "bot_state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    else:
        return {"trades": [], "summary": {}}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

state = load_state()

# 오늘 날짜 기준 요약
today = datetime.now().strftime("%Y-%m-%d")
today_trades = [t for t in state.get("trades", []) if t["date"] == today]
today_pnl = sum(t["pnl"] for t in today_trades)
today_win = sum(1 for t in today_trades if t["pnl"] > 0)
today_total = len(today_trades)
today_winrate = round(today_win / today_total * 100, 2) if today_total > 0 else 0

# 상단 요약
st.title("📊 Binance 자동매매 대시보드")
st.metric("📅 오늘 날짜", today)
st.metric("💰 오늘 수익률", f"{today_pnl:.2%}")
st.metric("✅ 승률", f"{today_winrate:.2f}%")
st.markdown("---")

# 매매 기록 테이블
if today_total > 0:
    df = pd.DataFrame(today_trades)
    st.dataframe(df[::-1], use_container_width=True)
else:
    st.info("오늘의 매매 기록이 없습니다.")
