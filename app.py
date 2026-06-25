# -*- coding: utf-8 -*-
"""
🕵️ 흡연 탐정 (Smoking Detective) — 진입점
st.navigation 으로 여러 페이지의 메뉴를 직접 구성합니다.
사이드바 = 페이지 메뉴 전용 (필터는 각 페이지 안에 둠 → 스코프 명확).

실행:  py -m streamlit run app.py
"""

import streamlit as st
from style import inject_css

st.set_page_config(page_title="흡연 탐정 🕵️", page_icon="🕵️", layout="wide")
inject_css()

pg = st.navigation([
    st.Page("home.py", title="수사하기", icon="🕵️", default=True),
    st.Page("explore.py", title="데이터 탐험", icon="📊"),
    st.Page("method.py", title="측정 원리", icon="📖"),
])
pg.run()
