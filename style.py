# -*- coding: utf-8 -*-
"""탐정 누아르 테마 — 커스텀 CSS · 히어로 배너 · 판결 스탬프.
폰트 규칙: 제목/히어로 = 명조(분위기), 본문·캡션·표 = 맑은 고딕(선명)."""

import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@700;800&family=Special+Elite&display=swap');

/* ===== 폰트 ===== */
/* 본문·작은 글씨·위젯·표 = 맑은 고딕 (선명하게) */
html, body, .stApp, .stMarkdown, p, li, span, label,
[data-testid="stCaptionContainer"], [data-testid="stMetricLabel"],
[data-testid="stMetricValue"], [data-testid="stWidgetLabel"],
.stSelectbox, .stSlider, .stRadio, .stMultiSelect, .stCheckbox,
table, th, td, button, input {
    font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', '맑은 고딕', sans-serif !important;
}
/* 제목·히어로만 명조 유지 */
h1, h2, h3, .detective-hero h1 { font-family: 'Nanum Myeongjo', serif !important; letter-spacing:.3px; }
/* 판결 스탬프는 타자기 폰트 */
.stamp { font-family: 'Special Elite', monospace !important; }

/* 작은 글씨 크기/줄간격 보정 (너무 작아 깨져보이지 않게) */
.stMarkdown p, li, label { font-size: 0.95rem; line-height: 1.65; }
[data-testid="stCaptionContainer"] p { font-size: 0.86rem; color:#b9b9c8; line-height:1.55; }

/* ===== 레이아웃 (웹 가독 폭) ===== */
.block-container { max-width: 1180px; padding-top: 1.2rem; padding-bottom: 3rem; }

/* ===== 배경 ===== */
.stApp {
    background:
      radial-gradient(circle at 18% 8%, rgba(212,160,23,.07), transparent 42%),
      radial-gradient(circle at 85% 92%, rgba(212,160,23,.05), transparent 42%),
      #14141f;
}

/* ===== 히어로 배너 ===== */
.detective-hero {
    position: relative; overflow: hidden;
    background: linear-gradient(135deg, #20203c 0%, #2b2b50 55%, #18182a 100%);
    border: 1px solid rgba(212,160,23,.55); border-radius: 16px;
    padding: 24px 28px; margin-bottom: 16px;
    box-shadow: 0 10px 34px rgba(0,0,0,.5), inset 0 0 70px rgba(212,160,23,.05);
}
.detective-hero h1 { margin:0; font-size:2.0rem; color:#f5d77a; text-shadow:0 2px 12px rgba(0,0,0,.6); }
.detective-hero p { margin:.45rem 0 0; color:#cdcde0; font-size:1.0rem; }
.detective-hero .glass { position:absolute; right:22px; top:-12px; font-size:6rem; opacity:.16; transform:rotate(-15deg); }

/* ===== 판결 스탬프 ===== */
.stamp {
    display:inline-block; border:3px solid; border-radius:8px;
    padding:4px 16px; font-weight:800; font-size:1.15rem; transform:rotate(-5deg);
    letter-spacing:2px; text-shadow:0 1px 0 rgba(0,0,0,.3);
}
@keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:.55;} }
.stamp.alarm { animation: pulse 1s infinite; }

/* ===== 펼쳐보기 / 지표 카드 ===== */
div[data-testid="stExpander"] { border:1px solid rgba(212,160,23,.30); border-radius:10px; }
div[data-testid="stMetric"] {
    background: rgba(255,255,255,.03); border:1px solid rgba(212,160,23,.28);
    border-radius:10px; padding:10px 12px;
}

/* ===== 버튼 ===== */
.stButton button, .stFormSubmitButton button {
    background: linear-gradient(135deg,#e0b13a,#b8860b) !important;
    color:#16162a !important; font-weight:800 !important; border:none !important;
    border-radius:9px !important; letter-spacing:1px;
}
.stButton button:hover, .stFormSubmitButton button:hover {
    filter:brightness(1.08); box-shadow:0 4px 14px rgba(212,160,23,.4);
}

/* ===== 마크다운 표 최적화 ===== */
.stMarkdown table {
    width:100%; border-collapse:collapse; margin:.7rem 0;
    background: rgba(255,255,255,.02); border-radius:10px; overflow:hidden;
    border:1px solid rgba(212,160,23,.18);
}
.stMarkdown thead th {
    background: rgba(212,160,23,.18); color:#f5d77a !important; font-weight:700;
    padding:11px 13px; text-align:left; border-bottom:1px solid rgba(212,160,23,.35);
    font-size:0.92rem;
}
.stMarkdown tbody td {
    padding:10px 13px; border-bottom:1px solid rgba(255,255,255,.06);
    color:#e3e3ec; font-size:0.92rem; line-height:1.55;
}
.stMarkdown tbody tr:nth-child(even) td { background: rgba(255,255,255,.025); }
.stMarkdown tbody tr:hover td { background: rgba(212,160,23,.07); }

/* 데이터프레임(인터랙티브 표) 테두리 */
div[data-testid="stDataFrame"] { border:1px solid rgba(212,160,23,.22); border-radius:10px; }
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
