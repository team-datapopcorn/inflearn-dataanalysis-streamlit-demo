# 캠페인 성과 대시보드 — Claude Code가 작성한 Streamlit 예제
import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="캠페인 성과 대시보드", page_icon="📈", layout="wide")

DATA = Path(__file__).resolve().parent.parent / "data" / "캠페인_성과_2025-2026.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA, encoding="utf-8-sig")
    df["월"] = df["월"].astype(str)
    return df


df = load_data()

st.title("📈 캠페인 성과 대시보드")
st.caption("채널별 광고 성과를 기간·채널로 직접 필터링해 봅니다. (모듈 4 · 캠페인 정산과 같은 데이터)")

months = sorted(df["월"].unique())
channels = sorted(df["채널"].unique())

with st.sidebar:
    st.header("필터")
    start, end = st.select_slider("기간(월)", options=months, value=(months[0], months[-1]))
    picked = st.multiselect("채널", channels, default=channels)

mask = (df["월"] >= start) & (df["월"] <= end) & (df["채널"].isin(picked))
f = df[mask]

if f.empty:
    st.warning("선택한 조건에 데이터가 없습니다. 사이드바에서 필터를 바꿔 보세요.")
    st.stop()

total_rev = int(f["매출"].sum())
total_cost = int(f["광고비"].sum())
total_conv = int(f["전환수"].sum())
roas = total_rev / total_cost if total_cost else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("총 매출", f"{total_rev / 1e8:.1f}억 원")
c2.metric("총 광고비", f"{total_cost / 1e4:,.0f}만 원")
c3.metric("ROAS", f"{roas:.1f}배")
c4.metric("총 전환수", f"{total_conv:,}건")

st.subheader("월별 매출 추이 — 채널별")
pivot = f.pivot_table(index="월", columns="채널", values="매출", aggfunc="sum")
st.line_chart(pivot)

col_l, col_r = st.columns(2)
with col_l:
    st.subheader("채널별 매출")
    by_ch = f.groupby("채널")["매출"].sum().sort_values(ascending=False)
    st.bar_chart(by_ch)
with col_r:
    st.subheader("채널별 ROAS")
    ch = f.groupby("채널").agg(매출=("매출", "sum"), 광고비=("광고비", "sum"))
    ch["ROAS"] = (ch["매출"] / ch["광고비"]).round(2)
    st.bar_chart(ch["ROAS"])

st.subheader("상세 데이터")
st.dataframe(f, width="stretch", hide_index=True)
st.download_button(
    "필터된 데이터 CSV 내려받기",
    f.to_csv(index=False).encode("utf-8-sig"),
    "campaign_filtered.csv",
    "text/csv",
)
