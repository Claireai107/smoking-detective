# -*- coding: utf-8 -*-
"""🕵️ 수사하기 (홈·메인) — 신체 수치 입력 → 흡연 의심도 판결.
이 페이지는 전체 데이터로 학습한 모델을 쓰며, '데이터 탐험'의 필터와 무관합니다."""

import numpy as np
import pandas as pd
import streamlit as st

from helpers import load_data, train_model, roc_auc
from style import hero, stamp

df = load_data()
model = train_model(df)
_, _, auc = roc_auc(df)

# ── 헤더 ──
hero("🕵️ 흡연 탐정",
     "신체검사 수치만으로 흡연을 간파한다. 용의자 정보를 입력하고 <b>수사 개시</b>를 누르시오.", "🔍")
st.caption(f"🏅 이 탐정의 검거 정확도(AUC) **{auc:.2f}** · 작동 원리는 왼쪽 메뉴 📖 **측정 원리**")

# ── 세션 초기화 (결과를 기억해 두는 공간) ──
if "verdict" not in st.session_state:
    st.session_state.verdict = None

# ── 입력 폼 (st.form: '수사 개시' 누를 때 한 번에 제출) ──
with st.form("suspect_form"):
    st.markdown("#### 📋 용의자 정보 입력")
    c1, c2 = st.columns(2)
    in_sex = c1.radio("성별", ["남성", "여성"], horizontal=True)
    in_hemo = c1.slider("혈색소 (hemoglobin)", 8.0, 20.0, 15.0, 0.1)
    in_gtp = c1.slider("GTP (감마지티피)", 5, 300, 30)
    in_trig = c2.slider("중성지방 (triglyceride)", 30, 500, 120)
    in_hdl = c2.slider("HDL (좋은 콜레스테롤)", 20, 120, 55)
    submitted = st.form_submit_button("🔎 수사 개시", type="primary", width="stretch")

# ── 제출 시: 예측 + 근거 만들기 → 세션에 저장 ──
if submitted:
    gender_code = "M" if in_sex == "남성" else "F"
    suspect = pd.DataFrame([{
        "hemoglobin": in_hemo, "Gtp": in_gtp, "triglyceride": in_trig,
        "HDL": in_hdl, "gender": gender_code,
    }])
    score = float(np.clip(model.predict(suspect)[0], 0, 1))

    smk = df[df["smoking"] == 1]
    cues = []
    if in_sex == "남성":
        cues.append("성별 남성")
    if in_hemo >= smk["hemoglobin"].median():
        cues.append(f"혈색소 {in_hemo}↑")
    if in_gtp >= smk["Gtp"].median():
        cues.append(f"GTP {in_gtp}↑")
    if in_trig >= smk["triglyceride"].median():
        cues.append(f"중성지방 {in_trig}↑")
    st.session_state.verdict = {"score": score, "cues": cues}
    if score < 0.35:
        st.balloons()  # 무혐의 축하 효과

# ── 결과 표시 (폼 밖 · 세션값이라 다른 조작에도 유지) ──
v = st.session_state.verdict
if v is not None:
    pct = v["score"] * 100
    st.divider()
    with st.container(border=True):
        st.markdown("### 🗂️ 수사 결과")
        st.progress(min(max(v["score"], 0.0), 1.0))
        if pct >= 60:
            st.markdown(stamp("검거 · GUILTY", "#ff4b4b", alarm=True), unsafe_allow_html=True)
            st.markdown(f"#### 🚨 흡연 의심도 {pct:.0f}% — 빼박입니다 🚬")
        elif pct >= 35:
            st.markdown(stamp("요주의 · SUSPECT", "#e0b13a"), unsafe_allow_html=True)
            st.markdown(f"#### 🟡 흡연 의심도 {pct:.0f}% — 요주의 인물")
        else:
            st.markdown(stamp("무혐의 · CLEARED", "#2ec27e"), unsafe_allow_html=True)
            st.markdown(f"#### ✅ 흡연 의심도 {pct:.0f}% — 무혐의")
        if v["cues"]:
            st.caption("🔬 결정적 증거(흡연자 패턴과 일치): " + " · ".join(v["cues"]))
        else:
            st.caption("🔬 뚜렷한 흡연자 패턴 신호 없음")
else:
    st.info("👆 정보를 입력하고 '수사 개시'를 누르면 판결이 여기에 표시됩니다.")
