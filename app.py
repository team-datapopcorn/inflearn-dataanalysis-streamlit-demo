# 클로드코드로 데이터분석 자동화하기 — Streamlit 예제 (홈)
# 이 파일은 Claude Code에게 "이 데이터로 대시보드 만들어줘"라고 요청해서 만든 예제입니다.
# 실행: 이 폴더에서  streamlit run app.py

import streamlit as st

st.set_page_config(
    page_title="데이터분석 자동화 — Streamlit 예제",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Streamlit 예제 — 분석을 만지는 화면으로")
st.markdown(
    """
이 앱은 강의 **CH07 · 인터랙티브 앱**에서 다룬, *분석 결과를 한 장 리포트가 아니라
직접 만지는 화면으로 전달하는* 예제입니다. 코드는 **Claude Code**가 썼고,
우리는 "이 데이터로 이런 화면을 보여줘"라고 말만 했습니다.

왼쪽 사이드바에서 페이지를 골라 보세요.
"""
)

c1, c2 = st.columns(2)
with c1:
    st.subheader("📈 캠페인 성과 대시보드")
    st.markdown(
        "채널별 광고 성과(광고비·전환·매출·ROAS)를 기간과 채널로 필터링합니다. "
        "모듈 4의 *캠페인 정산* 예시와 같은 데이터예요."
    )
    st.page_link("pages/1_캠페인_성과.py", label="캠페인 대시보드 열기 →")
with c2:
    st.subheader("🌊 묵호 관광 트렌드")
    st.markdown(
        "한국관광 데이터랩의 동해시 방문자·검색 데이터로 만든 트렌드 탐색기입니다. "
        "샘플 리포트 *'묵호가 떴다'* 와 같은 데이터예요."
    )
    st.page_link("pages/2_묵호_관광트렌드.py", label="묵호 대시보드 열기 →")

st.divider()
st.caption(
    "데이터팝콘 · 클로드코드로 데이터분석 자동화하기 (인프런) · "
    "한 장 리포트(HTML)와 이 앱(Streamlit)은 같은 분석에서 나온 두 가지 전달 방법입니다."
)
