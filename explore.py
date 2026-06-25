# -*- coding: utf-8 -*-
"""📊 데이터 탐험 — 흡연과 신체신호의 관계를 직접 탐험.
필터는 이 페이지 본문 상단에 둠 → 아래 분석이 모두 이 필터 기준임이 분명함."""

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

from helpers import load_data, compute_associations, fmt_p
from style import hero

df = load_data()

hero("📊 사건 자료실", "5.5만 건의 검진 기록을 파헤쳐 흡연의 단서를 찾는다.", "🗂️")

# ── 필터 (본문 상단) ──
with st.expander("🔧 데이터 필터", expanded=True):
    age_min, age_max = int(df["age"].min()), int(df["age"].max())
    f1, f2, f3 = st.columns([2, 2, 1])
    age_range = f1.slider("나이 범위", age_min, age_max, (age_min, age_max))
    sex_opts = sorted(df["성별"].unique())
    sex = f2.multiselect("성별", sex_opts, default=sex_opts)
    only_smoker = f3.checkbox("흡연자만")

data = df[df["age"].between(*age_range) & df["성별"].isin(sex)]
if only_smoker:
    data = data[data["smoking"] == 1]

if len(data) == 0:
    st.warning("조건에 맞는 데이터가 없습니다. 필터를 넓혀주세요.")
    st.stop()

st.caption(f"ℹ️ 아래 모든 분석은 위 필터 기준입니다 · 현재 **{len(data):,}명**")

# ── 지표 4개 ──
m1, m2, m3, m4 = st.columns(4)
m1.metric("인원", f"{len(data):,}명")
m2.metric("흡연율", f"{data['smoking'].mean() * 100:.1f}%")
m3.metric("평균 혈색소", f"{data['hemoglobin'].mean():.1f}")
m4.metric("평균 GTP", f"{data['Gtp'].mean():.0f}")

st.divider()

both_groups = data["smoking"].nunique() == 2  # 흡연/비흡연 둘 다 있는지
num_cols = [c for c in data.select_dtypes("number").columns if c not in ("ID", "smoking")]

tab1, tab2, tab3 = st.tabs(["🔍 증거분석", "⚖️ 대질심문", "🔗 공범관계"])

# --- 탭1: 증거분석 ---
with tab1:
    st.subheader("어떤 신호가 흡연과 연관이 큰가?")
    assoc = compute_associations(df)  # 순위표는 '전체 데이터' 기준
    show = assoc.head(8).copy()
    show["p값"] = show["p값"].apply(lambda x: f"{x:.1e}")
    st.dataframe(show, width="stretch")
    st.caption("※ 위 순위표는 전체 데이터 기준 · 상관계수 절댓값 순 · Cohen's d ≥ 0.8 이면 '큰 차이'")

    st.markdown("---")
    pick = st.selectbox("분포로 확인할 신호 (필터 기준)", num_cols,
                        index=num_cols.index("hemoglobin") if "hemoglobin" in num_cols else 0)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(data=data, x=pick, hue="흡연여부", kde=True, ax=ax)
    ax.set_title(f"{pick} 분포 (흡연 vs 비흡연)")
    st.pyplot(fig)

# --- 탭2: 대질심문 (t검정 + 카이제곱) ---
with tab2:
    st.subheader("차이가 진짜인가? (가설검정)")
    if not both_groups:
        st.info("흡연·비흡연 두 그룹이 모두 있어야 비교할 수 있어요. '흡연자만' 필터를 꺼주세요.")
    else:
        var = st.selectbox("검정할 신체신호 (t검정)", num_cols,
                           index=num_cols.index("hemoglobin") if "hemoglobin" in num_cols else 0)
        g_non = data[data["smoking"] == 0][var]
        g_smk = data[data["smoking"] == 1][var]
        t, p_val = stats.ttest_ind(g_non, g_smk, equal_var=False)  # Welch
        # 효과크기 Cohen's d (차이가 '얼마나 큰지')
        n1, n2 = len(g_non), len(g_smk)
        sp = np.sqrt(((n1 - 1) * g_non.std() ** 2 + (n2 - 1) * g_smk.std() ** 2) / (n1 + n2 - 2))
        d = abs(g_smk.mean() - g_non.mean()) / sp
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("비흡연 평균", f"{g_non.mean():.2f}")
        k2.metric("흡연 평균", f"{g_smk.mean():.2f}")
        k3.metric("p-value", fmt_p(p_val))
        k4.metric("효과크기(d)", f"{d:.2f}")
        if d >= 0.8:
            size = "큼 🔴"
        elif d >= 0.5:
            size = "중간 🟡"
        elif d >= 0.2:
            size = "작음 🟢"
        else:
            size = "거의 없음 ⚪"
        if p_val < 0.05:
            st.success(f"✅ 차이가 통계적으로 유의 (p {fmt_p(p_val)}) · 차이의 크기는 **{size}** (d={d:.2f})")
        else:
            st.info("유의하지 않습니다 — 우연일 수 있어요.")
        st.caption("ℹ️ 데이터가 크면 p값은 거의 항상 작아져요(=유의함). 그래서 '차이가 얼마나 큰지'를 보는 "
                   "효과크기(d)를 함께 봅니다. (0.2 작음 · 0.5 중간 · 0.8 큼)")

        st.markdown("---")
        st.markdown("**카이제곱 — 범주형 신호와 흡연의 관계**")
        cat_candidates = [c for c in ["성별", "dental caries", "tartar", "Urine protein"] if c in data.columns]
        cat = st.selectbox("범주형 변수", cat_candidates)
        ctab = pd.crosstab(data[cat], data["흡연여부"])
        st.dataframe(ctab)
        chi2, p, dof, _ = stats.chi2_contingency(ctab)
        st.metric("p-value", fmt_p(p))
        st.success("연관 있음" if p < 0.05 else "연관 없음")

# --- 탭3: 공범관계 (상관 히트맵) ---
with tab3:
    st.subheader("신체신호 간 상관 (히트맵)")
    default_cols = [c for c in ["age", "hemoglobin", "Gtp", "triglyceride", "HDL", "smoking"] if c in data.columns]
    cols = st.multiselect("히트맵에 넣을 변수", num_cols + ["smoking"], default=default_cols)
    if len(cols) >= 2:
        corr = data[cols].corr()
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr, annot=True, cmap="RdYlGn_r", center=0, fmt=".2f", ax=ax)
        st.pyplot(fig)
    else:
        st.info("변수를 2개 이상 선택하세요.")
