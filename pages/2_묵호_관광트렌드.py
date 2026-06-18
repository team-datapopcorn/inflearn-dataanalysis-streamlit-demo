# 묵호 관광 트렌드 탐색기 — Claude Code가 작성한 Streamlit 예제
# 데이터: 한국관광 데이터랩 — 동해시(202411~202604)
import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="묵호 관광 트렌드", page_icon="🌊", layout="wide")

DATA = Path(__file__).resolve().parent.parent / "data"


def ym(series):
    """202411 → '2024-11' 형태로."""
    s = series.astype(int).astype(str)
    return s.str[:4] + "-" + s.str[4:6]


@st.cache_data
def load():
    visit = pd.read_csv(DATA / "묵호_방문자수_추이.csv", encoding="utf-8-sig")
    visit["월"] = ym(visit["기준년월"])
    dist = pd.read_csv(DATA / "묵호_거리별_방문자.csv", encoding="utf-8-sig")
    search = pd.read_csv(DATA / "묵호_목적지유형_검색량.csv", encoding="utf-8-sig")
    search.columns = [c.strip() for c in search.columns]
    search["월"] = ym(search["기준연월"])
    local = pd.read_csv(DATA / "묵호_검색_현지인외지인.csv", encoding="utf-8-sig")
    spots = pd.read_csv(DATA / "묵호_인기관광지.csv", encoding="utf-8-sig")
    return visit, dist, search, local, spots


visit, dist, search, local, spots = load()

st.title("🌊 묵호 관광 트렌드 탐색기")
st.caption("한국관광 데이터랩 · 동해시 방문자·검색 데이터 — 샘플 리포트 '묵호가 떴다'와 같은 데이터입니다.")

# --- KPI: 최근 월 ---
last = visit.sort_values("월").iloc[-1]
c1, c2, c3 = st.columns(3)
c1.metric("최근 월 방문자수", f"{int(last['방문자수']):,}명", f"{last['방문자수증감률']:+.1f}% (전년동월)")
c2.metric("누적 방문자수", f"{int(visit['방문자수'].sum()) / 1e4:,.0f}만 명")
c3.metric("기준 기간", f"{visit['월'].min()} ~ {visit['월'].max()}")

# --- 방문자수 추이 ---
st.subheader("월별 방문자수 추이 — 올해 vs 전년동월")
vchart = visit.set_index("월")[["방문자수", "전년동월방문자수"]]
st.line_chart(vchart)
st.caption("⚠️ '동해시' 전체로 보면 큰 변화가 안 보일 수 있습니다. 아래 검색 데이터로 들여다보면 다르게 보입니다.")

# --- 목적지 유형별 검색량 ---
st.subheader("목적지 유형별 검색량 추이")
types = [t for t in sorted(search["목적지 유형"].unique()) if t != "전체"]
with st.sidebar:
    st.header("필터 — 묵호")
    picked = st.multiselect(
        "목적지 유형", types, default=[t for t in ["자연관광", "음식", "숙박"] if t in types]
    )
if picked:
    s = search[search["목적지 유형"].isin(picked)]
    spivot = s.pivot_table(index="월", columns="목적지 유형", values="목적지 검색량", aggfunc="sum")
    st.line_chart(spivot)
else:
    st.info("사이드바에서 목적지 유형을 하나 이상 골라 보세요.")

# --- 거리별 + 현지인/외지인 ---
col_l, col_r = st.columns(2)
with col_l:
    st.subheader("거리별 방문자 분포")
    d = dist.set_index("거리구분명")["방문자비율"]
    st.bar_chart(d)
with col_r:
    st.subheader("업종별 검색 비율 — 현지인 vs 외지인")
    lo = local.set_index("업종중분류명")[["현지인 검색비율", "외지인 검색비율"]]
    st.bar_chart(lo)

# --- 인기 관광지 ---
st.subheader("인기 관광지 Top 10")
st.dataframe(
    spots[["순위", "관광지명", "분류"]].head(10),
    width="stretch",
    hide_index=True,
)
