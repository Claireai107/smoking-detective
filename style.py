# -*- coding: utf-8 -*-
"""탐정 누아르 테마 — 커스텀 CSS · 히어로 배너 · 판결 스탬프."""

import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;700;800&family=Special+Elite&display=swap');

/* 배경: 어두운 수사실 + 은은한 조명 */
.stApp {
    background:
      radial-gradient(circle at 18% 8%, rgba(212,160,23,.07), transparent 42%),
      radial-gradient(circle at 85% 92%, rgba(212,160,23,.05), transparent 42%),
      #14141f;
}
h1, h2, h3 { font-family: 'Nanum Myeongjo', serif !important; letter-spacing:.3px; }
.stMarkdown, p, label { font-family: 'Nanum Myeongjo', serif; }

/* 히어로 배너 */
.detective-hero {
    position: relative; overflow: hidden;
    background: linear-gradient(135deg, #20203c 0%, #2b2b50 55%, #18182a 100%);
    border: 1px solid rgba(212,160,23,.55); border-radius: 16px;
    padding: 26px 30px; margin-bottom: 16px;
    box-shadow: 0 10px 34px rgba(0,0,0,.5), inset 0 0 70px rgba(212,160,23,.05);
}
.detective-hero h1 { margin:0; font-size:2.1rem; color:#f5d77a; text-shadow:0 2px 12px rgba(0,0,0,.6); }
.detective-hero p { margin:.45rem 0 0; color:#cdcde0; font-size:1.02rem; }
.detective-hero .glass {
    position:absolute; right:22px; top:-12px; font-size:6.2rem;
    opacity:.16; transform:rotate(-15deg);
}

/* 판결 스탬프 */
.stamp {
    display:inline-block; border:3px solid; border-radius:8px;
    padding:4px 16px; font-weight:800; font-size:1.15rem; transform:rotate(-5deg);
    font-family:'Special Elite', monospace; letter-spacing:2px;
    text-shadow:0 1px 0 rgba(0,0,0,.3);
}
@keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:.55;} }
.stamp.alarm { animation: pulse 1s infinite; }

/* 사건파일 카드 / 펼쳐보기 */
div[data-testid="stExpander"] { border:1px solid rgba(212,160,23,.30); border-radius:10px; }

/* 지표 카드 */
div[data-testid="stMetric"] {
    background: rgba(255,255,255,.03);
    border:1px solid rgba(212,160,23,.28); border-radius:10px; padding:10px 12px;
}

/* 버튼 (수사 개시 등) */
.stButton button, .stFormSubmitButton button {
    background: linear-gradient(135deg,#e0b13a,#b8860b) !important;
    color:#16162a !important; font-weight:800 !important; border:none !important;
    border-radius:9px !important; letter-spacing:1px;
}
.stButton button:hover, .stFormSubmitButton button:hover {
    filter:brightness(1.08); box-shadow:0 4px 14px rgba(212,160,23,.4);
}
</style>
"""


def inject_css():
    st.markdown(_CSS, unsafe_allow_html=True)


def hero(title, subtitle, glass="🔍"):
    st.markdown(
        f'<div class="detective-hero"><span class="glass">{glass}</span>'
        f'<h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )


def stamp(text, color, alarm=False):
    cls = "stamp alarm" if alarm else "stamp"
    return f'<span class="{cls}" style="color:{color};border-color:{color};">{text}</span>'
